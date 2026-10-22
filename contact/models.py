from django.db import models
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    name = models.CharField(_("name"), max_length=120)
    email = models.EmailField(_("email"))
    message = models.TextField(_("message"), max_length=5000)
    created_date = models.DateTimeField(_("received"), auto_now_add=True)
    is_read = models.BooleanField(_("read"), default=False)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self):
        return f"{self.name} <{self.email}>"
