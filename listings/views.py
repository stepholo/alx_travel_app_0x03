from .models import Listing, Booking, Review, Payment
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer, PaymentSerializer
from rest_framework import viewsets, permissions, filters
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .tasks import send_booking_confirmation_email


CHAPA_API_URL = "https://api.chapa.co/v1/transaction/initialize"
CHAPA_VERIFY_URL = "https://api.chapa.co/v1/transaction/verify/"
CHAPA_SECRET_KEY = settings.CHAPA_SECRET_KEY


class ListingViewSet(viewsets.ModelViewSet):
    """ViewSet for Listing model"""
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'created_at']


class BookingViewSet(viewsets.ModelViewSet):
    """ViewSet for Booking model"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'listing_title']
    ordering_fields = ['created_at', 'total_price']

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        # Trigger email confirmation task
        send_booking_confirmation_email.delay(booking.user.email, booking.id)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review model"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'comment']
    ordering_fields = ['created_at', 'rating']


class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        booking_id = request.data.get('booking_id')
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=404)

        tx_ref = f"booking_{booking.id}_{request.user.id}"
        data = {
            "amount": str(booking.total_price),
            "currency": "ETB",
            "email": request.user.email,
            "tx_ref": tx_ref,
            "callback_url": "https://yourdomain.com/api/payments/verify/",
        }
        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        chapa_resp = requests.post(CHAPA_API_URL, json=data, headers=headers)
        if chapa_resp.status_code == 200:
            resp_data = chapa_resp.json()
            Payment.objects.create(
                booking=booking,
                user=request.user,
                chapa_tx_ref=tx_ref,
                status="Pending"
            )
            return Response({
                "checkout_url": resp_data['data']['checkout_url'],
                "tx_ref": tx_ref
            })
        return Response({'error': 'Payment initiation failed.'}, status=400)


class VerifyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tx_ref = request.query_params.get('tx_ref')
        try:
            payment = Payment.objects.get(chapa_tx_ref=tx_ref, user=request.user)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found.'}, status=404)

        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        chapa_resp = requests.get(f"{CHAPA_VERIFY_URL}{tx_ref}/", headers=headers)
        if chapa_resp.status_code == 200:
            resp_data = chapa_resp.json()
            status_str = resp_data['data']['status']
            if status_str == "success":
                payment.status = "Completed"
                from .tasks import send_payment_confirmation_email
                send_payment_confirmation_email.delay(request.user.email, payment.booking.id)
            else:
                payment.status = "Failed"
            payment.save()
            return Response({'status': payment.status})
        return Response({'error': 'Verification failed.'}, status=400)
