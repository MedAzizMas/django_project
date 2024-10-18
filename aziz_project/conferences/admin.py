from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Conference
from users.models import Reservation
from django.db.models import Count
from django.utils import timezone
from datetime import date

# Inline admin interface for Reservation model within the Conference admin.
class ReservationInline(admin.StackedInline):
    model = Reservation  # The model related to this inline
    extra = 1  # Number of empty forms to show by default in the inline
    readonly_fields = ('reservation_date',)  # Making 'reservation_date' a read-only field
    can_delete = True  # Allow deletion of reservation instances from the inline

# Custom filter to filter conferences based on the number of participants.
class ParticipationFilter(admin.SimpleListFilter):
    title = "participant filter"  # Title that appears in the admin filter section
    parameter_name = "participants"  # The URL query parameter for this filter

    def lookups(self, request, model_admin):
        """Define the filtering options."""
        return (
            ('0', 'No Participants'),  # Conferences with no participants
            ('more', 'With Participants'),  # Conferences with at least one participant
        )

    """def queryset(self, request, queryset):
        #Filter the queryset based on the selected filter option.
        if self.value() == '0':
            # Annotate each conference with the count of associated reservations and filter where count is 0
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count=0)
        elif self.value() == 'more':
            # Filter conferences where the count of associated reservations is greater than 0
            return queryset.annotate(participant_count=Count('reservations')).filter(participant_count__gt=0)
        return queryset  # Return unfiltered queryset if no option is selected
    """
    def queryset(self, request, queryset):
        #Filter the queryset based on the selected filter option.
        if self.value() == '0':
            # Annotate each conference with the count of associated reservations and filter where count is 0
            return queryset.filter(reservations__isnull=True)
        elif self.value() == 'more':
            # Filter conferences where the count of associated reservations is greater than 0
            return queryset.filter(reservations__isnull=False)
        return queryset  # Return unfiltered queryset if no option is selected


# Custom filter to filter conferences based on their dates (past, today, upcoming).
class ConferenceDateFilter(admin.SimpleListFilter):
    title = 'Conference Date'  # Title for the filter in the admin interface
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
            # Filter conferences that ended before today
            return queryset.filter(end_date__lt=today)
        elif self.value() == 'today':
            # Filter conferences that are happening today
            return queryset.filter(start_date__lte=today, end_date__gte=today)
        elif self.value() == 'upcoming':
            # Filter conferences that are scheduled to start after today
            return queryset.filter(start_date__gt=today)
        return queryset  # Return unfiltered queryset if no option is selected

# Custom admin interface for the Conference model.
class ConferenceAdmin(admin.ModelAdmin):
    # Fields to display in the list view of conferences
    list_display = ("titre", "location", "start_date", "end_date", "price")
    
    # Fields that can be searched via the search bar
    search_fields = ('titre',)
    
    # Number of conferences to display per page
    list_per_page = 2
    
    # Default sorting of the conference list (first by 'start_date', then by 'titre')
    ordering = ('start_date', 'titre')

    # Organizing fields into sections for the detail view of a conference
    fieldsets = (
        ('Description', {
            'fields': ('titre', 'decription', 'category', 'location', 'price', 'capacity')
        }),
        ('Horaire', {  # "Schedule" section
            'fields': ('start_date', 'end_date', 'created_at', 'updated_at')
        }),
        ('Documents', {  # Section for attached files, like the conference program
            'fields': ('program',)
        }),
    )
    
    # Fields that are read-only
    readonly_fields = ('created_at', 'updated_at')
    
    # Adding inline form to manage reservations within the conference admin
    inlines = [ReservationInline]
    
    # Autocomplete for 'category' field to help search and select categories
    autocomplete_fields = ('category',)
    
    # Adding filters in the right sidebar of the conference list view
    list_filter = ('titre', ParticipationFilter, ConferenceDateFilter,)

# Register the Conference model with the custom ConferenceAdmin interface
admin.site.register(Conference, ConferenceAdmin)
