from django.contrib import admin

from .models import Room, Booking

class RoomAdmin(admin.ModelAdmin):
    list_display = ['type_text', 'available_date', 'price_number', 'description_text']


admin.site.register(Room, RoomAdmin)
admin.site.register(Booking)
