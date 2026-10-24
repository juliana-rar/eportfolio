from io import StringIO

from django.core.management import call_command

from portfolio.management.commands.seed_portfolio import PROJECTS
from portfolio.models import Project, ProjectImage, Technology
from siteprofile.models import Profile

from .helpers import LocalizedTestCase, TempMediaMixin


def seed(*args):
    call_command("seed_portfolio", *args, stdout=StringIO())


class SeedPortfolioTests(TempMediaMixin, LocalizedTestCase):
    def test_creates_projects_technologies_and_images(self):
        seed()
        self.assertEqual(Project.objects.count(), len(PROJECTS))
        self.assertTrue(Technology.objects.filter(name="Django").exists())
        self.assertEqual(ProjectImage.objects.count(), len(PROJECTS) * 3)
        self.assertTrue(all(p.cover for p in Project.objects.all()))

    def test_is_idempotent(self):
        seed("--no-images")
        seed("--no-images")
        self.assertEqual(Project.objects.count(), len(PROJECTS))
        self.assertEqual(ProjectImage.objects.count(), 0)

    def test_projects_with_a_todo_are_not_public(self):
        seed("--no-images")
        for project in Project.objects.all():
            has_todo = "TODO" in project.summary
            self.assertEqual(project.is_public, not has_todo, project.slug)

    def test_does_not_overwrite_profile_edits_without_reset(self):
        Profile.objects.create(name="Someone else", headline="My own headline")
        seed("--no-images")
        profile = Profile.load()
        self.assertEqual(profile.name, "Someone else")
        self.assertEqual(profile.headline, "My own headline")
        self.assertTrue(profile.bio)  # empty fields are filled in

    def test_reset_removes_projects_that_are_not_in_the_seed(self):
        Project.objects.create(title="Leftover", summary="x", year=2020)
        seed("--reset", "--no-images")
        self.assertFalse(Project.objects.filter(title="Leftover").exists())
        self.assertEqual(Project.objects.count(), len(PROJECTS))
