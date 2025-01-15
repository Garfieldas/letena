from django.contrib import admin
from .models import Appointment

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('last_seven_id', 'client', 'day', 'time')
    list_filter = ('day', 'is_completed')

    def last_seven_id(self, obj):
        return str(obj.id)[-7:]  # Get the last 7 digits of the id

    last_seven_id.short_description = 'Užsakymo nr.'  # Optional: Set a custom column name

admin.site.register(Appointment, AppointmentAdmin)