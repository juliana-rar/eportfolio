from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.utils.translation import override

from portfolio.models import Project, ProjectImage, Technology
from portfolio.templatetags.portfolio_tags import markdown_filter

from .helpers import TINY_GIF, LocalizedTestCase, TempMediaMixin, make_project, make_tech


class SlugTests(LocalizedTestCase):
    def test_slug_is_generated_from_title(self):
        project = make_project("Festes Majors de Catalunya")
        self.assertEqual(project.slug, "festes-majors-de-catalunya")

    def test_duplicate_titles_get_unique_slugs(self):
        first = make_project("Gallery")
        second = make_project("Gallery")
        third = make_project("Gallery")
        self.assertEqual([first.slug, second.slug, third.slug], ["gallery", "gallery-2", "gallery-3"])

    def test_slug_is_kept_when_the_title_changes(self):
        project = make_project("Old name")
        project.title = "New name"
        project.save()
        project.refresh_from_db()
        self.assertEqual(project.slug, "old-name")

    def test_explicit_slug_is_respected(self):
        project = make_project("Anything", slug="custom-slug")
        self.assertEqual(project.slug, "custom-slug")

    def test_technology_slug_handles_symbols(self):
        dotnet = make_tech(".NET")
        csharp = make_tech("C#")
        self.assertEqual(dotnet.slug, "net")
        self.assertEqual(csharp.slug, "c")

    def test_absolute_url_uses_slug(self):
        project = make_project("Detail page")
        self.assertEqual(project.get_absolute_url(), "/projects/detail-page/")


class OrderingAndQuerySetTests(LocalizedTestCase):
    def test_ordering_by_order_then_newest_first(self):
        old = make_project("Old", order=1)
        new = make_project("New", order=1)
        first = make_project("First", order=0)
        # created_date is auto_now_add: push "old" into the past explicitly.
        Project.objects.filter(pk=old.pk).update(created_date=timezone.now() - timedelta(days=1))
        self.assertEqual(list(Project.objects.all()), [first, new, old])

    def test_public_excludes_hidden_projects(self):
        visible = make_project("Visible")
        make_project("Hidden", is_public=False)
        self.assertEqual(list(Project.objects.public()), [visible])

    def test_featured_requires_public(self):
        featured = make_project("Featured", is_featured=True)
        make_project("Hidden featured", is_featured=True, is_public=False)
        make_project("Plain")
        self.assertEqual(list(Project.objects.featured()), [featured])

    def test_grouped_follows_category_order_and_skips_empty(self):
        make_tech("Podman", Technology.Category.DEVOPS)
        make_tech("Django", Technology.Category.BACKEND)
        make_tech("Vue", Technology.Category.FRONTEND)
        groups = Technology.grouped(Technology.objects.all())
        self.assertEqual([label for label, _ in groups], ["Frontend", "Backend", "DevOps"])


class LocalizationTests(LocalizedTestCase):
    def test_english_field_is_used_in_english(self):
        project = make_project("Galería", title_en="Gallery")
        self.assertEqual(project.get_title("en"), "Gallery")
        self.assertEqual(project.get_title("es"), "Galería")

    def test_english_falls_back_to_spanish_when_empty(self):
        project = make_project("Solo español")
        self.assertEqual(project.get_title("en"), "Solo español")

    def test_active_language_is_used_by_default(self):
        project = make_project("Galería", title_en="Gallery")
        with override("en"):
            self.assertEqual(project.get_title(), "Gallery")
        with override("es"):
            self.assertEqual(project.get_title(), "Galería")


class ProjectImageTests(TempMediaMixin, LocalizedTestCase):
    def test_dimensions_are_stored_and_images_are_ordered(self):
        project = make_project("With screenshots")
        second = ProjectImage.objects.create(
            project=project, order=2, image=SimpleUploadedFile("b.gif", TINY_GIF, "image/gif"))
        first = ProjectImage.objects.create(
            project=project, order=1, image=SimpleUploadedFile("a.gif", TINY_GIF, "image/gif"))
        self.assertEqual((first.width, first.height), (1, 1))
        self.assertEqual(list(project.images.all()), [first, second])


class MarkdownFilterTests(LocalizedTestCase):
    def test_renders_markdown(self):
        html = markdown_filter("## Title\n\n**bold** and `code`")
        self.assertIn("<h2>Title</h2>", html)
        self.assertIn("<strong>bold</strong>", html)

    def test_strips_dangerous_markup(self):
        html = markdown_filter('<script>alert(1)</script>[x](javascript:alert(1)) <img src=x onerror="alert(1)">')
        self.assertNotIn("<script", html)
        self.assertNotIn("javascript:", html)
        self.assertNotIn("onerror", html)
