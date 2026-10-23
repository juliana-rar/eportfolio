from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Project, ProjectImage, Technology


def thumbnail(image, size=64):
    if not image:
        return "-"
    return format_html(
        '<img src="{}" alt="" width="{}" height="{}">',
        image.url, size, size,
    )


class ProjectImageInline(admin.TabularInline):
    """Screenshots, ordered by the editable `order` column."""

    model = ProjectImage
    extra = 1
    fields = ("preview", "image", "caption", "caption_en", "order")
    readonly_fields = ("preview",)
    ordering = ("order", "pk")

    @admin.display(description=_("preview"))
    def preview(self, obj):
        return thumbnail(obj.image)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "project_count")
    list_filter = ("category",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description=_("projects"))
    def project_count(self, obj):
        return obj.projects.count()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title", "cover_preview", "year", "status", "is_public", "is_featured", "order",
    )
    list_display_links = ("title", "cover_preview")
    list_editable = ("order", "is_featured")
    list_filter = ("technologies", "status", "is_featured", "is_public", "year")
    search_fields = ("title", "title_en", "summary", "summary_en")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    inlines = [ProjectImageInline]
    fieldsets = (
        (_("Content (Spanish)"), {"fields": ("title", "slug", "summary", "description")}),
        (_("Content (English)"), {"fields": ("title_en", "summary_en", "description_en")}),
        (_("Details"), {"fields": ("cover", "technologies", "role", "year", "status")}),
        (_("Links"), {"fields": ("repo_url", "live_url")}),
        (_("Visibility"), {"fields": ("is_public", "is_featured", "order")}),
    )

    @admin.display(description=_("cover"))
    def cover_preview(self, obj):
        return thumbnail(obj.cover, 48)
