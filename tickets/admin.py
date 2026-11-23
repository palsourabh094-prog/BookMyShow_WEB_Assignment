from django.contrib import admin

from .models import Booking, GiftCard, Inquiry, Listing, NewsletterSubscription, ReservedSeat, Showtime, Venue

admin.site.site_header = "BookMyShow Clone administration"
admin.site.site_title = "BookMyShow Clone"


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ["title", "kind", "genre", "price", "featured"]
    list_filter = ["kind", "featured"]
    prepopulated_fields = {"slug": ["title"]}
    search_fields = ["title"]


@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ["listing", "venue", "time"]
    list_filter = ["venue"]


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ["subject", "topic", "email", "created_at"]
    list_filter = ["topic"]


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ["email", "created_at"]
    search_fields = ["email"]


admin.site.register([Venue, Booking, ReservedSeat, GiftCard])
