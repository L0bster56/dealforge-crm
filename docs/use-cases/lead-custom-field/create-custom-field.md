# UseCase: CreateCustomField — Создать кастомное поле лида

## Что решает

Создаёт новое кастомное поле для лидов. Кастомные поля позволяют адаптировать форму лида под специфику бизнеса — добавлять дополнительные атрибуты (бюджет, регион, тип продукта и т.д.). Поддерживает несколько типов: текст, число, дата, булево, выбор одного варианта, выбор нескольких.

**Файл:** `backend/src/backend/application/lead/use_cases/custom_fields/create_custom_field.py`

**Статус:** ✅ Реализовано

---

## Участники

| Поле | Значение |
|------|----------|
| **Actor** | Менеджер или выше |
| **Роли** | `sales_manager`, `director`, `admin` |

---

## Входные данные (`CreateCustomFieldCommand`)

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название поля (уникальное) |
| `type` | `FieldType` | Тип: `text / number / date / boolean / select_one / select_all` |
| `values` | `list[str]` | Варианты выбора (только для `select_one` и `select_all`) |

---

## Порядок действий

```
1. Проверить права актора через CanMangeCustomField
   └─ Если нет прав → ошибка PermissionError

2. Валидация: проверить соответствие типа и enum-значений:
   - Если тип select_one/select_all и values пустой → SelectFieldWithoutEnumsError
   - Если тип не select и values переданы → SelectFieldWithoutEnumsError
   (выполняется до открытия UoW)

3. Открыть Unit of Work

4. Проверить уникальность имени:
   uow.custom_fields.name_exists(cmd.name)
   └─ Если имя уже занято → CustomFieldNameAlreadyExistsError

5. Создать доменную сущность через LeadCustomField.create(name, field_type)
   └─ Генерируется UUID
   └─ is_deleted = False
   └─ enums = []

6. Если тип select_one / select_all:
   Для каждого значения в cmd.values:
   └─ Вызвать field.add_enum(value=value)
      → создаётся LeadCustomFieldEnum с уникальным UUID

7. Сохранить поле через uow.custom_fields.add(field)

8. Зафиксировать транзакцию (commit)

9. Вернуть CreateCustomFieldResult(field_id=field.id)
```

---

## Возможные ошибки

| Ошибка | Условие |
|--------|---------|
| `PermissionError` | Роль актора — `consultant` |
| `SelectFieldWithoutEnumsError` | Несоответствие типа и наличия/отсутствия enum-значений |
| `CustomFieldNameAlreadyExistsError` | Поле с таким именем уже существует |

---

## Результат (`CreateCustomFieldResult`)

| Поле | Тип | Описание |
|------|-----|----------|
| `field_id` | `UUID` | ID созданного поля |

---

## Бизнес-правила

- Уникальность имени обязательна — поле идентифицируется по имени в интерфейсе
- Для `select_one` / `select_all` варианты выбора создаются сразу вместе с полем
- Варианты выбора можно добавлять позже через `AddEnumValue`
- Удалённые поля (`is_deleted = True`) не проверяются на уникальность имени — можно создать поле с именем удалённого
