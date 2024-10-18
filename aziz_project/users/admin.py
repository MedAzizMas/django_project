from django.contrib import admin
from .models import Participant, Reservation

# Inline admin interface for Reservation model inside Participant admin.
class ReservationInline(admin.TabularInline):
    # The model this inline is related to
    model = Reservation
    
    # The number of extra empty forms shown in the inline section
    extra = 1  
    
    # Fields to display as read-only in the inline
    readonly_fields = ("reservation_date",)  
    
    # Fields that should provide an autocomplete search when creating or editing
    autocomplete_fields = ('participant',)  

# Admin interface customization for the Participant model.
class ParticipantAdmin(admin.ModelAdmin):
    # Fields to display in the list view of participants
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "cin",  # Assumed to be a unique identification field (e.g., ID number)
        "Participant_Category",  # Custom field related to participant categories
        "created_at",  # Timestamp for when the participant was created
        "updated_at",  # Timestamp for the last update
    )
    
    # Fields available for the search bar in the participant admin interface
    search_fields = ("username", "first_name", "last_name", "email", "cin")
    
    # Number of participants to display per page in the list view
    list_per_page = 10
    
    # Default sorting of participant list based on the 'created_at' field
    ordering = ("created_at",)
    
    # Fields that are not editable and should be shown as read-only
    readonly_fields = ("created_at", "updated_at")  

    # Organizing fields into sections for the detail view of a participant
    fieldsets = (
        ('Informations personnelles', {  # Personal information section
            'fields': ('username', 'first_name', 'last_name', 'email', 'cin', 'Participant_Category')
        }),
        ('Données de suivi', {  # Tracking information section (timestamps)
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    # Adding the inline interface to manage reservations directly from the participant admin
    inlines = [ReservationInline]  

    # Filter options available on the right-hand side of the participant list view
    list_filter = (
        'Participant_Category',  # Allows filtering participants by category
        'created_at',  # Allows filtering based on creation date
    )
    
    # Fields that are editable directly from the participant list view
    list_editable = ('first_name', 'last_name')


class reservationadmin(admin.ModelAdmin):
    list_display = ["conference", "participant","confirmed","reservation_date"]
    actions=['confirmed','unconfirmed']
    def confirmed(self,request,queryset):
        queryset.update(confirmed=True)
        self.message_user(request,"les reservations sont confirmes")
    confirmed.short_description="Reservation à confirmer"
    def unconfirmed(self,request,queryset):
        queryset.update(confirmed=False)
        self.message_user(request,"les reservations ne sont pas confirmes")
    unconfirmed.short_description="Reservation à ne pas confirmer"

    
# Registering the Participant model with the custom admin interface
admin.site.register(Participant, ParticipantAdmin)
# Registering the Reservation model to be manageable in the Django admin
admin.site.register(Reservation,reservationadmin)
