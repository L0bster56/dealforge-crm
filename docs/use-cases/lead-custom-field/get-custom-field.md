# UseCase: GetCustomField — Получить кастомное поле

## Что решает

Возвращает данные кастомного поля лида по UUID. Поддерживает режим включения удалённых полей (для административных целей).

**Файл:** `backend/src/backend/application/lead/use_cases/custom_fields/get_custom_field.py`

**Статус:** ✅ Реализовано

---

## Участники

| Поле | Значение |
|------|----------|
| **Actor** | Любой авторизованный пользователь |
| **Роли** | Все роли |

---

## Входные данные (`GetCustomFieldCommand`)

| Поле | Тип | Описание |
|------|-----|----------|
| `field_id` | `UUID` | ID поля |
| `include_deleted` | `bool` | Включать ли удалённые поля (по умолчанию `False`) |

---

## Порядок действий

```
1. Открыть Unit of Work
2. Загрузить поле из БД по field_id
   └─ Если не найдено → ошибка CustomFieldNotFoundError
3. Если поле удалено (is_deleted = True) И include_deleted = False:
   └─ ошибка CustomFieldNotFoundError
4. Конвертировать в view-DTO через to_view(result)
5. Вернуть CustomFieldViewDTO
```

---

## Возможные ошибки

| Ошибка | Условие |
|--------|---------|
| `CustomFieldNotFoundError` | Поле не найдено или удалено (при `include_deleted = False`) |

---

## Результат (`CustomFieldViewDTO`)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `UUID` | ID поля |
| `name` | `str` | Название |
| `field_type` | `FieldType` | Тип поля |
| `enums` | `list[EnumViewDTO]` | Варианты выбора (для select-типов) |
| `is_deleted` | `bool` | Статус удаления |
