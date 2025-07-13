from django.db import models
import uuid


# Create your models here.
class Listing(models.Model):
    """Model to represent a listing."""
    listing_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                                  unique=True, verbose_name="Listing ID")
    title = models.CharField(max_length=100, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    currency = models.CharField(max_length=4, default='USD', verbose_name="Currency")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Updated At")
    county = models.CharField(max_length=50, verbose_name="County")
    town = models.CharField(max_length=50, verbose_name="Town")
    street = models.CharField(max_length=50, verbose_name="Street")
    image = models.ImageField(upload_to='listings/', verbose_name="Image")
    host = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='listings',
                             verbose_name="Host")
    amenities = models.TextField(blank=True, null=True, verbose_name="Amenities")
    max_guests = models.PositiveIntegerField(default=1, verbose_name="Max Guests")
    availability = models.BooleanField(default=True, verbose_name="Availability")
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('unavailable', 'Unavailable')
    ], default='available', verbose_name="Status")
    category = models.CharField(max_length=50, choices=[
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('cottage', 'Cottage'),
        ('villa', 'Villa'),
        ('bungalow', 'Bungalow'),
        ('studio', 'Studio')
    ], default='apartment', verbose_name="Category")

    def __str__(self) -> str:
        """String Representation of listings"""
        return f"{self.title} - {self.county}, {self.town}"

    class Meta:
        """Meta class for listing model."""
        verbose_name = "Listing"
        verbose_name_plural = "Listings"
        ordering = ['-created_at']
        unique_together = ('host', 'title', 'county', 'town', 'street')
        indexes = [
            models.Index(fields=['host'], name='listing_host_idx'),
            models.Index(fields=['title'], name='listing_title_idx'),
            models.Index(fields=['county'], name='listing_county_idx'),
            models.Index(fields=['town'], name='listing_town_idx'),
            models.Index(fields=['street'], name='listing_street_idx'),
            models.Index(fields=['status'], name='listing_status_idx'),
            models.Index(fields=['category'], name='listing_category_idx'),
            models.Index(fields=['created_at'], name='listing_created_at_idx'),
            models.Index(fields=['updated_at'], name='listing_updated_at_idx'),
        ]


class Booking(models.Model):
    """Class to represent a booking."""
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                                  unique=True, verbose_name="Booking ID")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings',
                                verbose_name="Listing")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='bookings',
                             verbose_name="User")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    booking_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending', verbose_name="Status")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")
    guest_count = models.PositiveIntegerField(default=1, verbose_name="Guest Count")
    special_requests = models.TextField(blank=True, null=True, verbose_name="Special Requests")
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ], default='pending', verbose_name="Payment Status")
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer')
    ], default='credit_card', verbose_name="Payment Method")
    cancellation_policy = models.CharField(max_length=50, choices=[
        ('flexible', 'Flexible'),
        ('moderate', 'Moderate'),
        ('strict', 'Strict')
    ], default='flexible', verbose_name="Cancellation Policy")

    def __str__(self) -> str:
        """String Representation of Booking."""
        return f"Booking {self.booking_id} for {self.listing.title} by {self.user.username}"

    class Meta:
        """Meta class for Booking"""
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']
        unique_together = ('listing_id', 'user', 'start_date', 'end_date')
        indexes = [
            models.Index(fields=['listing_id'], name='booking_listing_idx'),
            models.Index(fields=['user'], name='booking_user_idx'),
            models.Index(fields=['start_date'], name='booking_start_date_idx'),
            models.Index(fields=['end_date'], name='booking_end_date_idx'),
            models.Index(fields=['booking_status'], name='booking_status_idx'),
            models.Index(fields=['created_at'], name='booking_created_at_idx'),
            models.Index(fields=['updated_at'], name='booking_updated_at_idx'),
        ]


class Review(models.Model):
    """Class to represent a review."""
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                                 unique=True, verbose_name="Review ID")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews',
                                   verbose_name="Listing")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reviews',
                             verbose_name="User")
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='reviews',
                                   verbose_name="Booking")
    rating = models.DecimalField(max_digits=3, choices=[
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars')
    ], default=3, decimal_places=2, verbose_name="Rating")
    comment = models.TextField(verbose_name="Comment", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    approved = models.BooleanField(default=False, verbose_name="Approved")
    response = models.TextField(verbose_name="Response", blank=True, null=True)

    def __str__(self) -> str:
        """String Representation of Review."""
        return f"Review {self.review_id} for {self.listing.title} by {self.user.username}"

    class Meta:
        """Meta class for Review."""
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']
        unique_together = ('listing_id', 'user', 'booking_id')
        indexes = [
            models.Index(fields=['listing_id'], name='review_listing_idx'),
            models.Index(fields=['user'], name='review_user_idx'),
            models.Index(fields=['booking_id'], name='review_booking_idx'),
            models.Index(fields=['rating'], name='review_rating_idx'),
            models.Index(fields=['created_at'], name='review_created_at_idx'),
            models.Index(fields=['updated_at'], name='review_updated_at_idx'),
        ]


class Payment(models.Model):
    """Class to represent a payment."""
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                                  unique=True, verbose_name="Payment ID")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='payments',
                             verbose_name="User")
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments',
                                   verbose_name="Booking")
    chapa_tx_ref = models.CharField(max_length=100, unique=True, verbose_name="Chapa Transaction Reference")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    currency = models.CharField(max_length=4, default='USD', verbose_name="Currency")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Payment Date")
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer')
    ], default='credit_card', verbose_name="Payment Method")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='pending', verbose_name="Status")

    def __str__(self) -> str:
        """String Representation of Payment."""
        return f"Payment {self.payment_id} for Booking {self.booking_id.booking_id}"

    class Meta:
        """Meta class for Payment."""
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-payment_date']
        unique_together = ('booking_id', 'payment_method')
        indexes = [
            models.Index(fields=['booking_id'], name='payment_booking_idx'),
            models.Index(fields=['amount'], name='payment_amount_idx'),
            models.Index(fields=['currency'], name='payment_currency_idx'),
            models.Index(fields=['payment_date'], name='payment_date_idx'),
            models.Index(fields=['status'], name='payment_status_idx'),
        ]
