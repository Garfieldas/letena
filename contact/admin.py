from django.contrib import admin
from .models import Review, Message

class MessageAdmin(admin.ModelAdmin):
    list_display=('name', 'created')
    # readonly_fields = [field.name for field in Message._meta.fields]  # Make all fields read-only
    fields = ('name', 'phone', 'message')
    readonly_fields = ('name', 'phone', 'message')
    list_filter = ('created',)

    def has_change_permission(self, request, obj=None):
        return False  # Disable editing

    def has_delete_permission(self, request, obj=None):
        return True  # Allow deletion
    
    def has_add_permission(self, request):
        return False  # Disable the "Add" button
    

class ReviewAdmin(admin.ModelAdmin):
    list_display=('name', 'service', 'created')
    list_filter = ('created',)

admin.site.register(Review, ReviewAdmin)
admin.site.register(Message, MessageAdmin)
