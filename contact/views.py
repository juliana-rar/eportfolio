from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .forms import ContactForm


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Spam gets the same success message so bots learn nothing.
            if not form.is_spam():
                form.save()
            messages.success(request, _("Thank you! Your message has been sent."))
            return redirect("contact:contact")
        messages.error(request, _("Please fix the errors below."))
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})
