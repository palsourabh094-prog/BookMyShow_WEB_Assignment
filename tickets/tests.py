from datetime import timedelta
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .booking import BookingError, PROMO_CODE, confirm_booking
from .models import Booking, GiftCard, NewsletterSubscription, Showtime


class BookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="demo@example.test")
        self.other_user = User.objects.create_user(username="second@example.test")
        self.show = Showtime.objects.select_related("listing").first()
        self.day = timezone.localdate() + timedelta(days=1)

    def reserve(self, user, draft_id, *, gift_code=None, promo=PROMO_CODE):
        return confirm_booking(
            user=user, listing=self.show.listing, showtime=self.show, day=self.day,
            labels=["A1"], draft_id=draft_id, promo=promo, gift_code=gift_code,
        )

    def test_retry_does_not_redeem_credit_twice(self):
        card = GiftCard.objects.create(purchaser=self.user, recipient="Demo", amount=500, balance=500)
        draft_id = str(uuid4())
        order = self.reserve(self.user, draft_id, gift_code=card.code)
        self.assertEqual(self.reserve(self.user, draft_id, gift_code=card.code), order)
        card.refresh_from_db()
        self.assertEqual(card.balance, 500 - order.gift_credit)
        self.assertEqual(order.gift_credit, self.show.listing.price - order.discount)
        self.assertEqual(order.total, 0)
        self.assertEqual(Booking.objects.count(), 1)

    def test_second_customer_cannot_reserve_the_same_seat(self):
        self.reserve(self.user, str(uuid4()))
        with self.assertRaisesMessage(BookingError, "One of those seats is now unavailable."):
            self.reserve(self.other_user, str(uuid4()))
        self.assertEqual(Booking.objects.count(), 1)

    def test_confirmation_is_private(self):
        order = self.reserve(self.user, str(uuid4()))
        self.client.force_login(self.other_user)
        for name in ("confirmation", "download_receipt"):
            with self.subTest(name=name):
                response = self.client.get(reverse(f"tickets:{name}", args=[order.pk]))
                self.assertEqual(response.status_code, 404)

    def test_receipt_download_contains_booking_details(self):
        order = self.reserve(self.user, str(uuid4()), promo="CURTAIN10")
        self.assertGreater(order.discount, 0)
        self.client.force_login(self.user)
        response = self.client.get(reverse("tickets:download_receipt", args=[order.pk]))
        self.assertEqual(response.headers["Content-Disposition"], f'attachment; filename="booking-{order.pk}.txt"')
        self.assertContains(response, str(order.pk))
        self.assertContains(response, "Seats: A1")

    def test_post_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("tickets:region"), {"region": "noida"})
        self.assertEqual(response.status_code, 403)


class NewsletterTests(TestCase):
    def test_rejects_invalid_addresses_and_deduplicates_case(self):
        url = reverse("tickets:newsletter")
        response = self.client.post(url, {"email": "not an email"})
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(NewsletterSubscription.objects.count(), 0)

        for email in ("Viewer@example.test", "viewer@example.test"):
            self.assertRedirects(self.client.post(url, {"email": email}), url)

        self.assertEqual(NewsletterSubscription.objects.get().email, "viewer@example.test")
