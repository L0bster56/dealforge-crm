# Сущность: Lead (Лид)

**Домен:** Lead  
**Таблица БД:** `leads`  
**Статус реализации:** 🔨 Domain-слой реализован, таблица БД и миграция отсутствуют  
**Файлы:**
- Domain: `backend/src/backend/domain/lead/entity.py`
- Application: `backend/src/backend/application/lead/`
- Infrastructure: ❌ отсутствует (`leads` таблица не создана)

---

## Назначение

Lead (лид) — потенциальный клиент, который находится в процессе продажи. Это центральная сущность всей CRM: лид привязывается к воронке, проходит по стадиям, имеет контактные данные, кастомные поля, задачи и историю действий.

---

## Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `name` | VARCHAR(255) | NOT NULL | — | Имя лида (клиента) |
| `phone` | VARCHAR(20) | nullable | null | Телефон (+998XXXXXXXXX) |
| `email` | VARCHAR(255) | nullable | null | Email контакта |
| `funnel_id` | UUID | FK → funnels, NOT NULL | — | Воронка, в которой находится лид |
| `stage_id` | UUID | FK → funnel_stages, NOT NULL | — | Текущая стадия в воронке |
| `source_id` | UUID | FK → sources, nullable | null | Источник лида |
| `assigned_to` | UUID | FK → users, nullable | null | Назначенный менеджер |
| `created_by` | UUID | FK → users, NOT NULL | current user | Кто создал лид |
| `priority` | ENUM | nullable | null | Приоритет: cold / warm / hot |
| `amount_uzs` | BIGINT | nullable | null | Сумма сделки в UZS |
| `amount_usd` | DECIMAL(15,2) | nullable | null | Сумма сделки в USD |
| `comment` | TEXT | nullable | null | Внутренняя заметка (основная) |
| `is_deleted` | BOOLEAN | NOT NULL | `false` | Мягкое удаление |
| `is_archived` | BOOLEAN | NOT NULL | `false` | Архивация |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |
| `updated_at` | TIMESTAMP | NOT NULL | now() | Дата последнего изменения |

---

## Приоритет (priority ENUM)

| Значение | Название | Цвет на Kanban |
|---|---|---|
| `cold` | Холодный | Синий |
| `warm` | Тёплый | Жёлтый |
| `hot` | Горячий | Красный |

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| `funnel` | Many-to-One → Funnel | Воронка лида |
| `stage` | Many-to-One → FunnelStage | Текущая стадия |
| `source` | Many-to-One → Source | Источник (nullable) |
| `assigned_user` | Many-to-One → User | Назначенный менеджер |
| `created_user` | Many-to-One → User | Создатель лида |
| `custom_values` | One-to-Many → LeadCustomFieldValue | Значения кастомных полей |
| `tasks` | One-to-Many → Task | Задачи по лиду |
| `comments` | One-to-Many → LeadComment | Комментарии |
| `timeline` | One-to-Many → LeadTimelineEvent | История действий |

---

## Бизнес-правила

1. **Лид в одной воронке** — лид находится только в одной воронке одновременно. Смена воронки означает обновление `funnel_id` + `stage_id` (первая `initial` стадия новой воронки).
2. **Видимость по роли:**
   - `Consultant` — видит только лиды, где `assigned_to = current_user`
   - `Sales Manager`, `Director`, `Admin` — видят все лиды
3. **Автоназначение (round-robin)** — при создании лида через Public Form или вручную с выбором стратегии `round_robin`, система автоматически назначает менеджера из пула.
4. **Архивация vs Удаление:**
   - `is_archived = true` — лид скрыт из активного списка Kanban, но доступен в разделе "Архив"
   - `is_deleted = true` — лид полностью скрыт; восстанавливается только администратором
5. **Сумма сделки** — поля `amount_uzs` и `amount_usd` независимы. Менеджер может указать одно или оба значения.
6. **Stage принадлежит Funnel** — при смене стадии система проверяет, что новая `stage_id` принадлежит текущему `funnel_id` лида.
7. **Событие в timeline** — любое значимое изменение лида автоматически создаёт `LeadTimelineEvent`.

---

## Автоматические события в Timeline

При следующих операциях над лидом создаётся запись в `lead_timeline_events`:

| Операция | Тип события |
|---|---|
| Создание лида | `created` |
| Смена стадии | `stage_changed` |
| Смена назначенного менеджера | `assigned` |
| Смена приоритета | `priority_changed` |
| Перенос в другую воронку | `funnel_changed` |
| Архивация | `archived` |
| Восстановление из архива | `restored` |

---

## Методы доменной модели

| Метод | Описание |
|---|---|
| `set_custom_value(field_id, value)` | Установить значение кастомного поля |
| `remove_custom_value(field_id)` | Удалить значение кастомного поля |
| `delete()` | Мягкое удаление |
| `archive()` | Архивировать |
| `restore()` | Восстановить из архива или удаления |

---

## Value Objects

- **LeadName** — непустая строка, max 255 символов
- **Contact** — содержит `phone` и `email`; оба поля опциональны, но хотя бы одно рекомендуется
- **Phone** — формат `+998XXXXXXXXX` (узбекский номер)

---

## Фильтры списка лидов

| Параметр | Тип | Описание |
|---|---|---|
| `funnel_id` | UUID | Фильтр по воронке |
| `stage_id` | UUID | Фильтр по стадии |
| `source_id` | UUID | Фильтр по источнику |
| `assigned_to` | UUID | Фильтр по менеджеру (Manager+) |
| `priority` | ENUM | Фильтр по приоритету |
| `is_archived` | boolean | Показать архивированные |
| `created_from` | date | Дата создания от |
| `created_to` | date | Дата создания до |
| `search` | string | Поиск по имени / телефону / email |
| `page` | int | Пагинация |
| `page_size` | int | Размер страницы (макс. 100) |

---

## API-эндпоинты

| Метод | Путь | Роль | Описание |
|---|---|---|---|
| `POST` | `/api/v1/leads/` | All | Создать лид |
| `GET` | `/api/v1/leads/` | All | Список лидов (Kanban-данные) |
| `GET` | `/api/v1/leads/{id}` | All | Детальная карточка |
| `PATCH` | `/api/v1/leads/{id}` | All (свои) / Manager+ | Редактировать лид |
| `PATCH` | `/api/v1/leads/{id}/stage` | All (свои) / Manager+ | Сменить стадию |
| `PATCH` | `/api/v1/leads/{id}/assign` | Manager+ | Переназначить менеджера |
| `POST` | `/api/v1/leads/{id}/archive` | Manager+ | Архивировать |
| `POST` | `/api/v1/leads/{id}/restore` | Manager+ | Восстановить |
| `DELETE` | `/api/v1/leads/{id}` | Manager+ | Удалить |
| `GET` | `/api/v1/leads/export/csv` | All | Экспорт в CSV |
| `GET` | `/api/v1/leads/export/excel` | All | Экспорт в XLSX |

---

## Пример объекта (JSON)

```json
{
  "id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "name": "Акбар Юсупов",
  "phone": "+998901234567",
  "email": "akbar@example.com",
  "funnel_id": "a1b2c3d4-...",
  "stage_id": "b2c3d4e5-...",
  "source_id": "c3d4e5f6-...",
  "assigned_to": "550e8400-...",
  "created_by": "550e8400-...",
  "priority": "hot",
  "amount_uzs": 15000000,
  "amount_usd": 1200.00,
  "comment": "Клиент готов к встрече, перезвонить в пятницу",
  "is_deleted": false,
  "is_archived": false,
  "custom_values": [
    {
      "field_id": "field-uuid",
      "field_name": "Город",
      "field_type": "text",
      "value": "Ташкент"
    }
  ],
  "created_at": "2026-05-01T09:00:00Z",
  "updated_at": "2026-05-14T15:30:00Z"
}
```
