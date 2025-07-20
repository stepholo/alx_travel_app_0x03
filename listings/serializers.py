from rest_framework import serializers
from .models import Listing, Booking, Review, Payment


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model."""

    class Meta:
        """Meta class for Listing Serializer."""
        model = Listing
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'listing_id': {'read_only': True},
            'host': {'read_only': True},
            'title': {'required': True},
            'description': {'required': True},
            'price_per_night': {'required': True, 'max_digits': 10, 'decimal_places': 2},
            'currency': {'required': True},
            'county': {'required': True},
            'town': {'required': True},
            'street': {'required': True},
            'max_guests': {'required': True, 'min_value': 1},
            'availability': {'required': True},
            'status': {'required': True},
            'category': {'required': True},
            'image': {'required': False, 'allow_null': True},
            'amenities': {'required': True}
        }

    def validate(self, data: dict) -> dict:
        """Custom validation for Listing."""
        if data['price_per_night'] <= 0:
            raise serializers.ValidationError("Price per night must be greater than zero.")
        if data['max_guests'] <= 0:
            raise serializers.ValidationError("Max guests must be at least 1.")
        if data['status'] not in ['available', 'booked', 'unavailable']:
            raise serializers.ValidationError("Invalid status. Choose from 'available', 'booked', or 'unavailable'.")
        if data['category'] not in ['apartment', 'house', 'cottage', 'villa', 'bungalow', 'studio']:
            raise serializers.ValidationError("Invalid category. Choose from 'apartment', 'house', 'cottage', 'villa', 'bungalow', or 'studio'.")
        if data['availability'] not in [True, False]:
            raise serializers.ValidationError("Availability must be a boolean value.")
        return data


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model."""

    class Meta:
        """Meta class for Booking Serializer."""
        model = Booking
        fields = '__all__'
        read_only_fields = ('booking_id', 'created_at', 'updated_at', 'listing', 'user')
        extra_kwargs = {
            'listing_id': {'required': True},
            'user': {'required': True},
            'start_date': {'required': True},
            'end_date': {'required': True},
            'guests_count': {'required': True, 'min_value': 1},
            'booking_status': {'required': True},
            'total_price': {'required': True, 'max_digits': 10, 'decimal_places': 2},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'special_requests': {'required': False, 'allow_blank': True},
            'payment_status': {'required': True},
            'payment_method': {'required': True},
            'cancellation_policy': {'required': True},
        }

    def validate(self, data: dict) -> dict:
        """Custom validation for Booking."""
        if data['guest_count'] <= 0:
            raise serializers.ValidationError("Guests count must be at least 1.")
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        if data['booking_status'] not in ['pending', 'confirmed', 'cancelled']:
            raise serializers.ValidationError("Invalid booking status. Choose from 'pending', 'confirmed', or 'cancelled'.")
        if data['payment_status'] not in ['paid', 'unpaid', 'refunded']:
            raise serializers.ValidationError("Invalid payment status. Choose from 'paid', 'unpaid', or 'refunded'.")
        if data['payment_method'] not in ['credit_card', 'paypal', 'bank_transfer', 'mpesa']:
            raise serializers.ValidationError("Invalid payment method. Choose from 'credit_card', 'paypal', 'bank_transfer', or 'mpesa.")
        if data['cancellation_policy'] not in ['flexible', 'moderate', 'strict']:
            raise serializers.ValidationError("Invalid cancellation policy. Choose from 'flexible', 'moderate', or 'strict'.")
        return data


class ReviewSerializer(serializers.ModelSerializer):

    """Serializer for Review"""

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'review_id', 'listing_id', 'booking_id', 'user']
        extra_kwargs = {
            'listing_id': {'required': True},
            'booking_id': {'required': True},
            'user': {'required': True},
            'rating': {'required': True},
            'comment': {'required': False, 'allow_blank': True},
            'approved': {'required': True},
            'response': {'required': False}
        }

    def validate(self, data: dict) -> dict:
        """Custom validation for Review"""
        if data['rating'] not in [1, 2, 3, 4, 5]:
            raise serializers.ValidationError("Ensure your rating is between 1 to 5")
        if data['comment'] and len(data['comment']) > 100:
            raise serializers.ValidationError("Comments cannot be more than 100 characters")
        if data['approved'] not in ['yes', 'no']:
            raise serializers.ValidationError("Chooose between yes or no")
        if data['response'] and len(data['response']) > 100:
            raise serializers.ValidationError("Response cannot be more than 100 characters")
        return data


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""

    class Meta:
        """Meta class for Payment Serializer."""
        model = Payment
        fields = '__all__'
        read_only_fields = ('payment_id', 'created_at', 'updated_at')
        extra_kwargs = {
            'booking_id': {'required': True},
            'amount': {'required': True, 'max_digits': 10, 'decimal_places': 2},
            'currency': {'required': True},
            'payment_method': {'required': True},
            'status': {'required': True},
            'transaction_id': {'required': False, 'allow_blank': True}
        }
