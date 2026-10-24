from django.urls import reverse

from portfolio.tests.helpers import LocalizedTestCase

from .models import Profile


class ProfileSingletonTests(LocalizedTestCase):
    def test_load_creates_the_single_row(self):
        profile = Profile.load()
        self.assertEqual(profile.pk, 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_saving_a_new_instance_updates_the_same_row(self):
        Profile.objects.create(name="First")
        Profile(name="Second").save()
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.load().name, "Second")

    def test_delete_is_a_no_op(self):
        profile = Profile.load()
        profile.delete()
        self.assertTrue(Profile.objects.exists())

    def test_localized_headline(self):
        profile = Profile(name="X", headline="Hola", headline_en="Hello")
        self.assertEqual(profile.get_headline("en"), "Hello")
        self.assertEqual(profile.get_headline("es"), "Hola")


class ContextProcessorTests(LocalizedTestCase):
    def test_profile_is_available_in_every_template(self):
        Profile.objects.create(name="Juliana Test")
        for url in (reverse("portfolio:home"), reverse("contact:contact"), "/does-not-exist/"):
            response = self.client.get(url)
            self.assertEqual(response.context["profile"].name, "Juliana Test", url)
            self.assertContains(response, "Juliana Test", status_code=response.status_code)
