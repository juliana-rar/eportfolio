from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from portfolio.i18n import LocalizedMixin


class Profile(LocalizedMixin, models.Model):
    """Singleton with the site owner's data. Always stored with pk=1."""

    name = models.CharField(_("name"), max_length=120)
    headline = models.CharField(_("headline (ES)"), max_length=200, blank=True)
    headline_en = models.CharField(_("headline (EN)"), max_length=200, blank=True)
    bio = models.TextField(_("bio (ES, Markdown)"), blank=True)
    bio_en = models.TextField(_("bio (EN, Markdown)"), blank=True)
    avatar = models.ImageField(
        _("avatar"), upload_to="profile/", blank=True,
        width_field="avatar_width", height_field="avatar_height",
    )
    avatar_width = models.PositiveIntegerField(editable=False, null=True)
    avatar_height = models.PositiveIntegerField(editable=False, null=True)
    cv = models.FileField(
        _("CV (PDF)"), upload_to="profile/", blank=True,
        validators=[FileExtensionValidator(["pdf"])],
    )
    email = models.EmailField(_("email"), blank=True)
    github_url = models.URLField(_("GitHub URL"), blank=True)
    linkedin_url = models.URLField(_("LinkedIn URL"), blank=True)
    location = models.CharField(_("location"), max_length=120, blank=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profile")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # The singleton cannot be deleted; edit it instead.
        pass

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1, defaults={"name": "Portfolio"})
        return obj

    def get_headline(self, lang=None):
        return self.localized("headline", lang)

    def get_bio(self, lang=None):
        return self.localized("bio", lang)
