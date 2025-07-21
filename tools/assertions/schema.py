from typing import Any

import allure  # Импортируем allure
from jsonschema import validate
from jsonschema.validators import Draft202012Validator

from tools.logger import get_logger  # Импортируем функцию для создания логгера

logger = get_logger("SCHEMA_ASSERTIONS")  # Создаем логгер с именем "SCHEMA_ASSERTIONS"


@allure.step("Validate JSON schema")  # Добавили allure шаг
def validate_json_schema(instance: Any, schema: dict) -> None:
    """
    Проверяет, соответствует ли JSON-объект (instance) заданной JSON-схеме (schema).
    :param instance: JSON-данные, которые нужно проверить.
    :param schema: Ожидаемая JSON-schema.
    :raises jsonschema.exceptions.ValidationError: Если instance не соответствует schema.
    """
    logger.info("Validating JSON schema")
    validate(
        schema=schema,
        instance=instance,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )