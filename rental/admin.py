from django.contrib import admin
from .models import Bicycle, Rental
from .patterns import AdminManager


class BicycleAdmin(admin.ModelAdmin):
    list_display = ("bicycle_id", "type", "status")  # Columns to show
    list_filter = ("status", "type")  # Filters on the side
    search_fields = ("bicycle_id",)  # Search by ID

    def save_model(self, request, obj, form, change):
        # Use Singleton AdminManager for approval on save
        admin_manager = AdminManager()
        super().save_model(request, obj, form, change)
        if not change:  # New bicycle added
            admin_manager.approve_rental(obj)  # Misnamed, but reusing for consistency

    def delete_model(self, request, obj):
        # Notify admin on deletion
        admin_manager = AdminManager()
        print(f"Admin deleted bicycle {obj}")
        super().delete_model(request, obj)


class RentalAdmin(admin.ModelAdmin):
    list_display = ("user", "bicycle", "start_time", "end_time", "cost")
    list_filter = ("start_time", "end_time")
    search_fields = ("user__username", "bicycle__bicycle_id")


admin.site.register(Bicycle, BicycleAdmin)
admin.site.register(Rental, RentalAdmin)


def save_model(self, request, obj, form, change):
    admin_manager = AdminManager()
    super().save_model(request, obj, form, change)
    if not change:
        admin_manager.manage_bicycle("added", obj)
