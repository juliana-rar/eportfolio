from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_date", "is_read")
    list_filter = ("is_read", "created_date")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "message", "created_date")
    actions = ["mark_as_read"]

    def has_add_permission(self, request):
        return False

    @admin.action(description=_("Mark selected messages as read"))
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
