import bleach
import markdown as md
from django import template
from django.conf import settings
from django.urls import translate_url
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = {
    "p", "br", "hr", "strong", "em", "a", "ul", "ol", "li", "blockquote",
    "code", "pre", "h2", "h3", "h4", "img",
    "table", "thead", "tbody", "tr", "th", "td",
}
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "title", "width", "height", "loading"],
    "th": ["align"],
    "td": ["align"],
}


@register.filter
def tr(obj, field):
    """`{{ project|tr:"title" }}` -> title_en in English, title otherwise."""
    return obj.localized(field)


@register.filter(name="markdown")
def markdown_filter(text):
    """Render Markdown and sanitize the result, so admin content can't inject markup."""
    if not text:
        return ""
    html = md.markdown(text, extensions=["extra", "sane_lists"])
    clean = bleach.clean(
        html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,
        protocols={"http", "https", "mailto"}, strip=True,
    )
    return mark_safe(clean)


@register.filter
def initials(name):
    return "".join(word[0] for word in str(name).split()[:2]).upper()


@register.filter
def first_word(text):
    """First name for the greeting: "Ana María López" -> "Ana"."""
    words = str(text).split()
    return words[0] if words else ""


@register.filter
def two_digits(number):
    """Index numbers set like a table of contents: 3 -> "03"."""
    return f"{int(number):02d}"


@register.simple_tag(takes_context=True)
def absolute_uri(context, url=None):
    """Absolute URL for `url` (or the current path, without query string)."""
    request = context.get("request")
    url = url if url is not None else (request.path if request else "/")
    if request:
        return request.build_absolute_uri(url)
    return settings.SITE_URL.rstrip("/") + url


@register.simple_tag(takes_context=True)
def alternate_urls(context):
    """[(lang code, absolute URL)] of the current page in every language (hreflang)."""
    request = context.get("request")
    if not request:
        return []
    current = request.build_absolute_uri(request.path)
    return [(code, translate_url(current, code)) for code, _name in settings.LANGUAGES]
