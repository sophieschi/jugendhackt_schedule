from re import match

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_acronym(acronym):
    regex = r"^[a-z0-9_]{4,}$"
    if not match(regex, acronym):
        raise ValidationError(_("acronym must match " + regex))


def validate_slug(slug):
    regex = r"^[a-z0-9\-_]{4,}$"
    if not match(regex, slug):
        raise ValidationError(_("slug must match " + regex))
