import shutil
import tempfile

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import translation

from portfolio.models import Project, Technology


class LocalizedTestCase(TestCase):
    """Start every test in the default language.

    A request to an /en/ URL leaves English active in the test thread, so a
    later reverse() would build /en/ URLs. Real servers re-activate the
    language on every request; tests need it reset explicitly.
    """

    def setUp(self):
        super().setUp()
        translation.activate(settings.LANGUAGE_CODE)
        self.addCleanup(translation.activate, settings.LANGUAGE_CODE)

# Smallest valid GIF: lets ImageField fill width/height without real files.
TINY_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x00\x00\x00\x00\x00"
    b",\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


class TempMediaMixin:
    """Point MEDIA_ROOT at a throwaway directory for the whole test class."""

    @classmethod
    def setUpClass(cls):
        cls._media_dir = tempfile.mkdtemp(prefix="eportfolio-test-media-")
        cls._media_override = override_settings(MEDIA_ROOT=cls._media_dir)
        cls._media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls._media_override.disable()
        shutil.rmtree(cls._media_dir, ignore_errors=True)


def make_project(title="Project", **kwargs):
    defaults = {"summary": f"{title} summary", "year": 2026}
    defaults.update(kwargs)
    technologies = defaults.pop("technologies", [])
    project = Project.objects.create(title=title, **defaults)
    if technologies:
        project.technologies.set(technologies)
    return project


def make_tech(name="Django", category=Technology.Category.BACKEND):
    return Technology.objects.create(name=name, category=category)
