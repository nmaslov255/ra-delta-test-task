import re

from django.core.exceptions import ValidationError


def validate_name(value):
    forbidden_pattern = r"[@#$%^&*()+=\[\]{};:<>\/?!|]"
    matched_chars = re.findall(forbidden_pattern, value)

    if matched_chars:
        raise ValidationError(
            f"Field cannot contain: {', '.join(matched_chars)}"
        )