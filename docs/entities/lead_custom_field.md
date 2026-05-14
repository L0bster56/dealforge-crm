# Сущности: LeadCustomField, LeadCustomFieldEnum, LeadCustomFieldValue

**Домен:** Lead  
**Таблицы БД:** `lead_custom_field`, `lead_custom_field_enum`, `lead_custom_field_value`  
**Статус реализации:**
- `LeadCustomField` — ✅ Domain + Infrastructure реализованы
- `LeadCustomFieldEnum` — ✅ Domain + Infrastructure реализованы
- `LeadCustomFieldValue` — 🔨 Domain-слой есть, таблица в БД отсутствует

**Файлы:**
- Domain: `backend/src/backend/domain/lead/entity.py`
- Models: `backend/src/backend/infrastracture/db/sqlalchemy/lead/custom_field/models.py`
- Repository: `backend/src/backend/infrastracture/db/sqlalchemy/lead/custom_field/repository.py`

---

## Назначение

Система кастомных полей позволяет Sales Manager-у создавать дополнительные поля для лидов без участия разработчиков. Например: "Город", "Источник рекламы", "Количество сотрудников" и т.д.

Архитектура состоит из трёх сущностей:
- **LeadCustomField** — определение (схема) поля: имя, тип, список вариантов
- **LeadCustomFieldEnum** — вариант значения для полей типа `select_one` / `select_all`
- **LeadCustomFieldValue** — фактическое значение поля у конкретного лида

---

## LeadCustomField — Определение кастомного поля

### Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `name` | VARCHAR(255) | NOT NULL, UNIQUE | — | Название поля (уникальное) |
| `field_type` | ENUM | NOT NULL | — | Тип данных поля |
| `is_deleted` | BOOLEAN | NOT NULL | `false` | Мягкое удаление |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |
| `updated_at` | TIMESTAMP | NOT NULL | now() | Дата последнего изменения |

### Типы полей (field_type ENUM)

| Значение | UI-компонент | Хранение | Пример |
|---|---|---|---|
| `text` | Однострочный input | `TEXT` | "Ташкент" |
| `number` | Числовой input | `NUMERIC` | 42, 3.14 |
| `date` | Date picker | `DATE` | "2026-06-01" |
| `boolean` | Чекбокс | `BOOLEAN` | true / false |
| `select_one` | Dropdown (один выбор) | `UUID` (enum_id) | "VIP-клиент" |
| `select_all` | Multi-select | `UUID[]` (enum_ids) | ["VIP", "Повторный"] |

### Связи

| Связь | Тип | Описание |
|---|---|---|
| `enums` | One-to-Many → LeadCustomFieldEnum | Варианты для select-полей |
| `values` | One-to-Many → LeadCustomFieldValue | Значения у конкретных лидов |

### Бизнес-правила

1. **Уникальность названия** — система не позволяет создать два поля с одинаковым именем (даже если одно удалено).
2. **Неизменяемость типа** — тип поля нельзя изменить после создания (это нарушило бы существующие значения).
3. **Мягкое удаление** — при `is_deleted = true` поле скрывается из UI. Значения лидов сохраняются в БД.
4. **Восстановление** — удалённое поле можно восстановить; его старые значения станут снова доступны.
5. **Только Manager+** — создавать, редактировать, удалять кастомные поля может только Sales Manager, Director или Admin.

### Методы доменной модели

| Метод | Описание |
|---|---|
| `create(name, field_type, enums)` | Фабричный метод |
| `rename(new_name)` | Переименовать поле |
| `delete()` | Мягкое удаление |
| `restore()` | Восстановить |
| `add_enum(value)` | Добавить вариант для select-поля |
| `remove_enum(enum_id)` | Удалить вариант |

---

## LeadCustomFieldEnum — Вариант значения (для select-полей)

### Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `custom_field_id` | UUID | FK → lead_custom_field, NOT NULL | — | Поле-родитель |
| `value` | VARCHAR(255) | NOT NULL | — | Текст варианта |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |

### Бизнес-правила

1. **Уникальность внутри поля** — два варианта в одном поле не могут иметь одинаковое `value`.
2. **Нельзя удалить вариант, если он используется** — если у хотя бы одного лида есть значение этого enum, удаление запрещается (или требует явного подтверждения с очисткой значений).
3. **Порядок** — варианты отображаются в порядке создания. Сортировка drag-and-drop — v2.

---

## LeadCustomFieldValue — Значение поля у лида

### Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `lead_id` | UUID | FK → leads, NOT NULL | — | Лид, которому принадлежит значение |
| `custom_field_id` | UUID | FK → lead_custom_field, NOT NULL | — | Определение поля |
| `value_text` | TEXT | nullable | null | Значение для `text` |
| `value_number` | NUMERIC | nullable | null | Значение для `number` |
| `value_date` | DATE | nullable | null | Значение для `date` |
| `value_boolean` | BOOLEAN | nullable | null | Значение для `boolean` |
| `value_enum_ids` | UUID[] | nullable | null | Значения для `select_one` / `select_all` |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |
| `updated_at` | TIMESTAMP | NOT NULL | now() | Дата обновления |

> Хранение в разных колонках (вместо JSONB) гарантирует типобезопасность и возможность индексирования.

### Бизнес-правила

1. **Один набор значений на лид** — для каждой пары `(lead_id, custom_field_id)` существует максимум одна запись.
2. **Тип соответствует полю** — при записи значения система проверяет, что заполнена колонка, соответствующая `field_type` родительского `LeadCustomField`.
3. **select_one** — `value_enum_ids` содержит ровно один `UUID` из вариантов поля.
4. **select_all** — `value_enum_ids` содержит один или несколько `UUID` из вариантов поля.
5. **Каскадное удаление** — при удалении лида (`is_deleted = true`) значения сохраняются в БД.

---

## API-эндпоинты (LeadCustomField)

| Метод | Путь | Роль | Описание |
|---|---|---|---|
| `POST` | `/api/v1/custom-fields/` | Manager+ | Создать поле |
| `GET` | `/api/v1/custom-fields/` | All | Список полей |
| `GET` | `/api/v1/custom-fields/{id}` | All | Получить поле |
| `PATCH` | `/api/v1/custom-fields/{id}` | Manager+ | Переименовать |
| `DELETE` | `/api/v1/custom-fields/{id}` | Manager+ | Удалить |
| `POST` | `/api/v1/custom-fields/{id}/restore` | Manager+ | Восстановить |
| `POST` | `/api/v1/custom-fields/{id}/enums` | Manager+ | Добавить вариант |
| `DELETE` | `/api/v1/custom-fields/{id}/enums/{enum_id}` | Manager+ | Удалить вариант |

Значения кастомных полей лида передаются в теле запроса при создании/редактировании лида:  
`PATCH /api/v1/leads/{id}` → поле `custom_values: [{field_id, value}]`

---

## Пример (JSON)

```json
{
  "id": "e5f6a7b8-c9d0-1234-efab-345678901234",
  "name": "Источник рекламы",
  "field_type": "select_one",
  "is_deleted": false,
  "enums": [
    {"id": "enum-uuid-1", "value": "Instagram"},
    {"id": "enum-uuid-2", "value": "Telegram"},
    {"id": "enum-uuid-3", "value": "Сарафанное радио"}
  ],
  "created_at": "2026-04-15T11:00:00Z",
  "updated_at": "2026-04-15T11:00:00Z"
}
```

```json
// Значение поля у конкретного лида (в ответе /leads/{id})
{
  "field_id": "e5f6a7b8-...",
  "field_name": "Источник рекламы",
  "field_type": "select_one",
  "value": "Instagram"
}
```
