from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from faker import Faker
import random
from datetime import timedelta

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with sample data for Users, Listings, Bookings, and Reviews"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        users = self.create_users(10)
        listings = self.create_listings(users, 20)
        bookings = self.create_bookings(users, listings, 30)
        self.create_reviews(users, listings, bookings, 10)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))

    def create_users(self, num_users):
        users = []
        for _ in range(num_users):
            username = fake.user_name()
            email = fake.email()
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                }
            )
            if created:
                user.set_password(fake.password())
                user.save()
            users.append(user)
        return users

    def create_listings(self, users, num_listings):
        categories = ['apartment', 'house', 'villa', 'cottage', 'studio']
        statuses = ['available', 'booked', 'unavailable']

        listings = []
        for _ in range(num_listings):
            host = random.choice(users)
            title = fake.catch_phrase()
            county = fake.city()
            town = fake.city()
            street = fake.street_name()

            if Listing.objects.filter(host=host, title=title, county=county, town=town, street=street).exists():
                continue

            listing = Listing.objects.create(
                title=title,
                description=fake.text(max_nb_chars=100),
                price_per_night=round(random.uniform(50, 500), 2),
                currency='USD',
                county=county,
                town=town,
                street=street,
                host=host,
                image=None,
                amenities=', '.join(fake.words(nb=5)),
                max_guests=random.randint(1, 10),
                availability=random.choice([True, False]),
                status=random.choice(statuses),
                category=random.choice(categories),
                created_at=timezone.now() - timedelta(days=random.randint(1, 365)),
                updated_at=timezone.now()
            )
            listings.append(listing)
        return listings

    def create_bookings(self, users, listings, num_bookings):
        booking_statuses = ['confirmed', 'pending', 'cancelled']
        payment_statuses = ['paid', 'unpaid', 'failed']
        payment_methods = ['credit_card', 'paypal', 'bank_transfer', 'mpesa']
        cancellation_policies = ['flexible', 'moderate', 'strict']

        bookings = []
        for _ in range(num_bookings):
            listing = random.choice(listings)
            user = random.choice(users)
            start_date = fake.date_between(start_date='-30d', end_date='+30d')
            end_date = start_date + timedelta(days=random.randint(1, 7))
            guests_count = random.randint(1, listing.max_guests)

            if Booking.objects.filter(listing_id=listing, user=user, start_date=start_date, end_date=end_date).exists():
                continue

            duration = (end_date - start_date).days
            total_price = listing.price_per_night * duration

            booking = Booking.objects.create(
                listing_id=listing,
                user=user,
                start_date=start_date,
                end_date=end_date,
                guest_count=guests_count,
                total_price=total_price,
                payment_status=random.choice(payment_statuses),
                payment_method=random.choice(payment_methods),
                booking_status=random.choice(booking_statuses),
                cancellation_policy=random.choice(cancellation_policies),
                special_requests=fake.sentence() if random.choice([True, False]) else '',
                created_at=timezone.now() - timedelta(days=random.randint(1, 30)),
                updated_at=timezone.now()
            )
            bookings.append(booking)
        return bookings

    def create_reviews(self, users, listings, bookings, num_reviews):
        ratings = [1, 2, 3, 4, 5]

        for _ in range(num_reviews):
            booking = random.choice(bookings)
            listing = booking.listing_id
            user = booking.user

            if Review.objects.filter(listing_id=listing, user=user, booking_id=booking).exists():
                continue

            Review.objects.create(
                listing_id=listing,
                user=user,
                booking_id=booking,
                rating=random.choice(ratings),
                comment=fake.paragraph(nb_sentences=2) if random.choice([True, False]) else '',
                approved=random.choice([True, False]),
                response=fake.sentence() if random.choice([True, False]) else '',
                created_at=timezone.now() - timedelta(days=random.randint(1, 30)),
                updated_at=timezone.now()
            )
