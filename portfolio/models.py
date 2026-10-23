from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .i18n import LocalizedMixin


def unique_slugify(instance, value, max_length=60):
    """Return a slug for `value` that is unique for the instance's model."""
    base = slugify(value)[:max_length].strip("-") or "item"
    slug, n = base, 2
    qs = type(instance)._default_manager.exclude(pk=instance.pk)
    while qs.filter(slug=slug).exists():
        suffix = f"-{n}"
        slug = f"{base[: max_length - len(suffix)]}{suffix}"
        n += 1
    return slug


class Technology(models.Model):
    class Category(models.TextChoices):
        FRONTEND = "frontend", _("Frontend")
        BACKEND = "backend", _("Backend")
        DEVOPS = "devops", _("DevOps")
        MOBILE = "mobile", _("Mobile")
        DB = "db", _("Database")

    name = models.CharField(_("name"), max_length=60, unique=True)
    slug = models.SlugField(_("slug"), max_length=60, unique=True, blank=True)
    # FileField (not ImageField) so SVG icons are accepted.
    icon = models.FileField(
        _("icon"),
        upload_to="technologies/",
        blank=True,
        validators=[FileExtensionValidator(["svg", "png", "webp", "jpg", "jpeg"])],
    )
    category = models.CharField(_("category"), max_length=10, choices=Category.choices)

    class Meta:
        ordering = ["category", "name"]
        verbose_name = _("technology")
        verbose_name_plural = _("technologies")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    @classmethod
    def grouped(cls, technologies):
        """Return [(category label, [technologies])] in Category order, skipping empty groups."""
        buckets = {value: [] for value in cls.Category.values}
        for tech in technologies:
            buckets[tech.category].append(tech)
        return [
            (cls.Category(value).label, techs) for value, techs in buckets.items() if techs
        ]


class ProjectQuerySet(models.QuerySet):
    def public(self):
        return self.filter(is_public=True)

    def featured(self):
        return self.public().filter(is_featured=True)


class Project(LocalizedMixin, models.Model):
    class Status(models.TextChoices):
        FINISHED = "finished", _("Finished")
        IN_PROGRESS = "in_progress", _("In progress")

    title = models.CharField(_("title (ES)"), max_length=120)
    title_en = models.CharField(_("title (EN)"), max_length=120, blank=True)
    slug = models.SlugField(_("slug"), max_length=140, unique=True, blank=True)
    summary = models.CharField(_("summary (ES)"), max_length=280)
    summary_en = models.CharField(_("summary (EN)"), max_length=280, blank=True)
    description = models.TextField(_("description (ES, Markdown)"), blank=True)
    description_en = models.TextField(_("description (EN, Markdown)"), blank=True)
    cover = models.ImageField(_("cover image"), upload_to="projects/covers/", blank=True)
    technologies = models.ManyToManyField(
        Technology, related_name="projects", blank=True, verbose_name=_("technologies")
    )
    role = models.CharField(_("role"), max_length=120, blank=True)
    year = models.PositiveSmallIntegerField(
        _("year"), validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )
    status = models.CharField(
        _("status"), max_length=12, choices=Status.choices, default=Status.FINISHED
    )
    repo_url = models.URLField(_("repository URL"), blank=True)
    live_url = models.URLField(_("live URL"), blank=True)
    is_featured = models.BooleanField(_("featured"), default=False)
    is_public = models.BooleanField(_("public"), default=True)
    order = models.PositiveIntegerField(_("order"), default=0)
    created_date = models.DateTimeField(_("created"), auto_now_add=True)

    objects = ProjectQuerySet.as_manager()

    class Meta:
        ordering = ["order", "-created_date"]
        verbose_name = _("project")
        verbose_name_plural = _("projects")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title, max_length=140)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def get_title(self, lang=None):
        return self.localized("title", lang)

    def get_summary(self, lang=None):
        return self.localized("summary", lang)

    def get_description(self, lang=None):
        return self.localized("description", lang)


class ProjectImage(LocalizedMixin, models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images", verbose_name=_("project")
    )
    image = models.ImageField(
        _("image"), upload_to="projects/screens/", width_field="width", height_field="height"
    )
    # Filled automatically by Pillow so templates can emit width/height attributes.
    width = models.PositiveIntegerField(editable=False, null=True)
    height = models.PositiveIntegerField(editable=False, null=True)
    caption = models.CharField(_("caption (ES)"), max_length=200, blank=True)
    caption_en = models.CharField(_("caption (EN)"), max_length=200, blank=True)
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = _("screenshot")
        verbose_name_plural = _("screenshots")

    def __str__(self):
        return self.caption or f"{self.project} #{self.order}"

    def get_caption(self, lang=None):
        return self.localized("caption", lang)
