from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Message


class ContactForm(forms.ModelForm):
    # Honeypot: hidden from people with CSS, but naive bots fill every field.
    website = forms.CharField(
        label=_("Leave this field empty"),
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "off", "tabindex": "-1"}),
    )

    class Meta:
        model = Message
        fields = ["name", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = "form__input form__textarea" if name == "message" else "form__input"
            field.widget.attrs.setdefault("class", css)

    def full_clean(self):
        super().full_clean()
        # Point invalid inputs at their error list for screen readers.
        for name in self.errors:
            if name in self.fields:
                self.fields[name].widget.attrs["aria-describedby"] = f"id_{name}_error"

    def is_spam(self):
        return bool(self.cleaned_data.get("website"))
