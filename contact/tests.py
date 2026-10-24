from django.contrib.messages import get_messages
from django.urls import reverse

from portfolio.tests.helpers import LocalizedTestCase

from .forms import ContactForm
from .models import Message

VALID = {"name": "Ada", "email": "ada@example.com", "message": "Hello, I have a project."}


class ContactViewTests(LocalizedTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("contact:contact")

    def test_page_renders_the_form_with_a_hidden_honeypot(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], ContactForm)
        self.assertContains(response, 'class="form__hp" aria-hidden="true"')
        self.assertContains(response, 'name="website"')

    def test_valid_submit_saves_the_message_and_redirects(self):
        response = self.client.post(self.url, VALID)
        self.assertRedirects(response, self.url)
        message = Message.objects.get()
        self.assertEqual((message.name, message.email), ("Ada", "ada@example.com"))
        self.assertFalse(message.is_read)
        feedback = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertEqual(len(feedback), 1)

    def test_success_message_is_shown_after_redirect(self):
        response = self.client.post(self.url, VALID, follow=True)
        self.assertContains(response, 'class="flash flash--success"')

    def test_honeypot_submission_is_discarded_silently(self):
        response = self.client.post(self.url, {**VALID, "website": "http://spam.example"})
        # Same response as a real submit, so bots learn nothing...
        self.assertRedirects(response, self.url)
        self.assertEqual(len(list(get_messages(response.wsgi_request))), 1)
        # ...but nothing is stored.
        self.assertFalse(Message.objects.exists())

    def test_invalid_submit_shows_errors_and_saves_nothing(self):
        response = self.client.post(self.url, {"name": "Ada", "email": "not-an-email", "message": ""})
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertIn("email", form.errors)
        self.assertIn("message", form.errors)
        self.assertFalse(Message.objects.exists())
        # Errors are wired to their inputs for screen readers.
        self.assertContains(response, 'aria-describedby="id_email_error"')
        self.assertContains(response, 'id="id_email_error"')

    def test_works_in_english(self):
        response = self.client.post("/en/contact/", VALID, follow=True)
        self.assertContains(response, "Thank you! Your message has been sent.")
        self.assertEqual(Message.objects.count(), 1)


class ContactFormTests(LocalizedTestCase):
    def test_honeypot_is_optional_and_detected(self):
        clean = ContactForm(VALID)
        spam = ContactForm({**VALID, "website": "x"})
        self.assertTrue(clean.is_valid())
        self.assertTrue(spam.is_valid())
        self.assertFalse(clean.is_spam())
        self.assertTrue(spam.is_spam())
