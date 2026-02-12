from django.core.exceptions import ValidationError

def validate_social_tag(value):
    if value and not value.startswith('@'):
        raise ValidationError('Тег должен начинаться с символа @.')


def validate_optional_field(key: str, data):
    if key not in data:
        raise ValidationError(f"Отсутствует обязательное поле: '{key}'.")

    value = data[key]
    if not isinstance(value, list):
        raise ValidationError(f"Поле '{key}' должно быть списком.")

    for i, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValidationError(f"Элемент в списке '{key}[{i}]' должен быть объектом.")

        if "name" not in item or not isinstance(item["name"], str) or not item["name"].strip():
            raise ValidationError(f"Запись в '{key}[{i}]' должна содержать непустое поле 'name'.")

        if "specialty" not in item or not isinstance(item["specialty"], str):
            raise ValidationError(f"Запись в '{key}[{i}]' должна содержать поле 'specialty' (строка).")

        if "start_date" not in item or not isinstance(item["start_date"], str):
            raise ValidationError(f"Запись в '{key}[{i}]' должна содержать поле 'start_date' (строка в формате даты).")

        if "end_date" not in item or not isinstance(item["end_date"], str):
            raise ValidationError(f"Запись в '{key}[{i}]' должна содержать поле 'end_date' (строка в формате даты).")


def validate_required_fields(key: str, data):
    if key not in data:
        raise ValidationError(f"Отсутствует обязательное поле: '{key}'.")

    value = data[key]
    if not isinstance(value, list):
        raise ValidationError(f"Поле '{key}' должно быть списком.")

    for i, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValidationError(f"Элемент в списке '{key}[{i}]' должен быть объектом.")

        if "name" not in item or not isinstance(item["name"], str) or not item["name"].strip():
            raise ValidationError(f"Запись в '{key}[{i}]' должна содержать непустое поле 'name'.")

        if "specialty" not in item or not isinstance(item["specialty"], str) or not item["specialty"].strip():
            raise ValidationError(f"Запись в '{key}[{i}]' должна содержать поле 'specialty' (строка).")

        if "start_date" not in item or not isinstance(item["start_date"], str) or not item["start_date"].strip():
            raise ValidationError(f"Запись в '{key}[{i}]' должна содержать поле 'start_date' (строка в формате даты).")

        if "end_date" not in item or not isinstance(item["end_date"], str) or not item["end_date"].strip():
            raise ValidationError(f"Запись в '{key}[{i}]' должна содержать поле 'end_date' (строка в формате даты).")




