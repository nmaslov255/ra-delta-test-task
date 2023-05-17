import re
from typing import NoReturn

import jsonschema
from django.core.exceptions import ValidationError


def raise_for_invalide_name(value: str) -> NoReturn:
    """Validate name for forbidden characters

    Args:
        value (str): Name string

    Raises:
        ValidationError: Invalide model field
    """
    forbidden_pattern = r"[@#$%^&*()+=\[\]{};:<>\/?!|]"
    matched_chars = re.findall(forbidden_pattern, value)

    if matched_chars:
        raise ValidationError(
            f"Field cannot contain: {', '.join(matched_chars)}"
        )


def raise_for_invalide_cbr_json(json: dict) -> NoReturn:
    """Validate json schema for www.cbr-xml-daily.ru/daily_json.js

    Args:
        json (dict): JSON responce from cbr-xml-daily.ru

    Raises:
        ValidationError: Invalide json schema
    """
    schema = {
        "type": "object",
        "properties": {
            "Date": {"type": "string", "format": "date-time"},
            "PreviousDate": {"type": "string", "format": "date-time"},
            "PreviousURL": {"type": "string", "format": "uri"},
            "Timestamp": {"type": "string", "format": "date-time"},
            "Valute": {
                "type": "object",
                "patternProperties": {
                    "^[A-Z]{3}$": {
                        "type": "object",
                        "properties": {
                            "ID": {"type": "string"},
                            "NumCode": {"type": "string"},
                            "CharCode": {"type": "string"},
                            "Nominal": {"type": "integer"},
                            "Name": {"type": "string"},
                            "Value": {"type": "number"},
                            "Previous": {"type": "number"}
                        },
                        "required": ["ID", "NumCode", "CharCode", "Nominal",
                                     "Name", "Value", "Previous"],
                        "additionalProperties": False
                    }
                },
                "additionalProperties": False
            }
        },
        "required": ["Date", "PreviousDate", "PreviousURL",
                     "Timestamp", "Valute"],
        "additionalProperties": False
    }

    jsonschema.validate(json, schema)
