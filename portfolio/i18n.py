"""Helpers to pick the Spanish (`field`) or English (`field_en`) column of a model."""
from django.utils.translation import get_language


class LocalizedMixin:
    """Adds `localized(field, lang)` to models with `<field>` / `<field>_en` pairs.

    Spanish is stored in the plain field and English in the `_en` field. When the
    English value is empty, the Spanish one is used as a fallback.
    """

    def localized(self, field, lang=None):
        lang = (lang or get_language() or "es")[:2]
        if lang == "en":
            value = getattr(self, f"{field}_en", "")
            if value:
                return value
        return getattr(self, field, "")
