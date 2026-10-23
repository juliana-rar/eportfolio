from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Singleton admin: the changelist jumps straight to the only record."""

    fieldsets = (
        (None, {"fields": ("name", "avatar", "location", "email")}),
        (_("Spanish"), {"fields": ("headline", "bio")}),
        (_("English"), {"fields": ("headline_en", "bio_en")}),
        (_("Links and files"), {"fields": ("cv", "github_url", "linkedin_url")}),
    )

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        profile = Profile.load()
        return redirect(reverse("admin:siteprofile_profile_change", args=[profile.pk]))
