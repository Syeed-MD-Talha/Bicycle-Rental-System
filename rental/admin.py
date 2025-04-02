from django.contrib import admin
from .models import Bicycle, Rental
from .patterns import AdminManager
from django.utils.html import format_html


class BicycleAdmin(admin.ModelAdmin):
    list_display = (
        "bicycle_id",
        "type",
        "status",
        "price_per_hour",
        "image_thumbnail",
    )  # Add price_per_hour
    list_filter = ("status", "type")
    search_fields = ("bicycle_id",)
    fields = (
        "bicycle_id",
        "type",
        "status",
        "price_per_hour",
        "image",
    )  # Include in form

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: auto;" />', obj.image.url
            )
        return "No Image"

    image_thumbnail.short_description = "Image"

    def save_model(self, request, obj, form, change):
        admin_manager = AdminManager()
        super().save_model(request, obj, form, change)
        if not change:
            admin_manager.manage_bicycle("added", obj)

    def delete_model(self, request, obj):
        admin_manager = AdminManager()
        print(f"Admin deleted bicycle {obj}")
        super().delete_model(request, obj)


class RentalAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "bicycle",
        "start_time",
        "end_time",
        "cost",
        "transaction_id",
    )
    list_filter = ("start_time", "end_time")
    search_fields = ("user__username", "bicycle__bicycle_id")


admin.site.register(Bicycle, BicycleAdmin)
admin.site.register(Rental, RentalAdmin)
