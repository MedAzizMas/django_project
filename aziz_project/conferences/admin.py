from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Conference
from users.models import *
from django.db.models import Count
from django.utils import timezone
from datetime import date
# Register your models here.
class ReservationInline(admin.StackedInline):
    model=Reservation
    extra=1
    readonly_fields=('reservation_date',)
    can_delete=True
class ParticipationFilter(admin.SimpleListFilter):
    title="participant filter"
    parameter_name="participants"
    def lookups(self, request, model_admin):
        return (
            ('0', 'No Participants'),
            ('more', 'With Participants'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        elif self.value() == 'more':
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)
        return queryset
class ConferenceDateFilter(admin.SimpleListFilter):
    title = 'Conference Date'  # This is the title that will appear in the admin interface
    parameter_name = 'conference_date'  # URL query parameter used for this filter

    def lookups(self, request, model_admin):
        """Define the options that will appear in the filter."""
        return (
            ('past', 'Past Conferences'),
            ('today', 'Today\'s Conferences'),
            ('upcoming', 'Upcoming Conferences'),
        )

    def queryset(self, request, queryset):
        """Filter the queryset based on the selected value."""
        today = date.today()  # Get today's date
        if self.value() == 'past':
            # Return conferences that ended before today
            return queryset.filter(end_date__lt=today)
        elif self.value() == 'today':
            # Return conferences that are happening today
            return queryset.filter(start_date__lte=today, end_date__gte=today)
        elif self.value() == 'upcoming':
            # Return conferences that are scheduled for the future
            return queryset.filter(start_date__gt=today)
        return queryset
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("titre", "location", "start_date", "end_date", "price")
    search_fields = ('titre',)
    list_per_page = 2
    ordering = ('start_date', 'titre')

    fieldsets = (
        ('Description', {
            'fields': ('titre', 'decription', 'category', 'location','price','capacity')
        }),
        ('Horaire', {
            'fields': ('start_date', 'end_date','created_at','updated_at')
        }),
        ('Documents', {
            'fields': ('program',)
        }),
    )
    readonly_fields=('created_at','updated_at')
    inlines=[ReservationInline]
    autocomplete_fields=('category',)
    list_filter=('titre',ParticipationFilter,ConferenceDateFilter,)

admin.site.register(Conference, ConferenceAdmin)