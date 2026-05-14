# Сущности DealForge CRM — Обзор

## Список сущностей

| Сущность | Таблица БД | Статус | Документация |
|---|---|:---:|---|
| User | `users` | ✅ Реализована | [user.md](user.md) |
| Funnel | `funnels` | ✅ Реализована | [funnel.md](funnel.md) |
| FunnelStage | `funnel_stages` | ✅ Реализована | [funnel_stage.md](funnel_stage.md) |
| Source | `sources` | ✅ Реализована | [source.md](source.md) |
| LeadCustomField | `lead_custom_field` | ✅ Реализована | [lead_custom_field.md](lead_custom_field.md) |
| LeadCustomFieldEnum | `lead_custom_field_enum` | ✅ Реализована | [lead_custom_field.md](lead_custom_field.md) |
| LeadCustomFieldValue | `lead_custom_field_value` | 🔨 Domain-слой есть, БД нет | [lead_custom_field.md](lead_custom_field.md) |
| Lead | `leads` | 🔨 Domain-слой есть, БД нет | [lead.md](lead.md) |
| Task | `tasks` | ❌ Не начата | [task.md](task.md) |
| LeadComment | `lead_comments` | ❌ Не начата | [lead_comment.md](lead_comment.md) |
| LeadTimelineEvent | `lead_timeline_events` | ❌ Не начата | [lead_timeline_event.md](lead_timeline_event.md) |
| Notification | `notifications` | ❌ Не начата | [notification.md](notification.md) |

**Легенда:** ✅ Полностью реализована · 🔨 Частично · ❌ Не начата

---

## Диаграмма связей (ERD)

```
┌─────────────────────────────────────────────────────────────────────┐
│                              USERS                                   │
│  id · first_name · last_name · email · username · role · is_active  │
└──────────────────────────┬──────────────────────────────────────────┘
                           │  created_by / assigned_to
          ┌────────────────┼──────────────────────────────────┐
          │                │                                  │
          ▼                ▼                                  ▼
┌──────────────┐  ┌─────────────────────────────────────┐  ┌──────────────┐
│   FUNNELS    │  │                LEADS                 │  │NOTIFICATIONS │
│  id · name   │  │  id · name · phone · email          │  │  id · user   │
│  is_deleted  │  │  funnel_id · stage_id · source_id   │  │  type · body │
└──────┬───────┘  │  assigned_to · created_by           │  │  is_read     │
       │          │  priority · amount_uzs · amount_usd  │  └──────────────┘
       │ 1:N      │  is_deleted · is_archived            │
       ▼          └──┬──────┬─────────┬────────┬────────┘
┌──────────────┐     │      │         │        │
│ FUNNEL_STAGE │◄────┘      │         │        │
│  id · name   │            │ 1:N     │ 1:N    │ 1:N
│  funnel_id   │            ▼         ▼        ▼
│  probability │  ┌──────────────┐ ┌───────┐ ┌──────────────────┐
│  hex_code    │  │    TASKS     │ │COMMENTS│ │ TIMELINE_EVENTS  │
│  order · kind│  │  id · title  │ │id·text│ │  id · event_type │
│  is_archived │  │  lead_id     │ │lead_id│ │  lead_id · actor  │
└──────────────┘  │  assigned_to │ │author │ │  payload (JSONB) │
                  │  deadline    │ └───────┘ └──────────────────┘
                  │  status      │
                  └──────────────┘

┌─────────────────────────────────────────────────────┐
│                     SOURCES                          │
│  id · name · source_type · config (JSONB)           │
│  is_active · is_deleted                              │
└─────────────────────────────────────────────────────┘
          │ 1:N (source_id на leads)
          ▼

┌────────────────────────────────────────────────────────────┐
│                  LEAD_CUSTOM_FIELD                          │
│  id · name · field_type · is_deleted                       │
└──────────────────────┬─────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
┌─────────────────────┐  ┌─────────────────────────┐
│ LEAD_CUSTOM_FIELD   │  │  LEAD_CUSTOM_FIELD_VALUE │
│       _ENUM         │  │  id · lead_id · field_id │
│  id · field_id      │  │  value (FieldValue VO)   │
│  value              │  └─────────────────────────┘
└─────────────────────┘
```

---

## Группировка по доменам

### Domain: Auth & Users
- **User** — сотрудник компании, работает с системой под определённой ролью

### Domain: Funnel (Воронки)
- **Funnel** — воронка продаж (контейнер для стадий)
- **FunnelStage** — отдельная стадия внутри воронки

### Domain: Lead (Лиды)
- **Lead** — потенциальный клиент, проходящий по воронке
- **LeadCustomField** — определение кастомного поля
- **LeadCustomFieldEnum** — вариант значения для select-полей
- **LeadCustomFieldValue** — конкретное значение кастомного поля у лида
- **Task** — задача, привязанная к лиду
- **LeadComment** — комментарий менеджера к лиду
- **LeadTimelineEvent** — событие в истории лида

### Domain: Source (Источники)
- **Source** — канал поступления лидов (webhook / public form / manual)

### Domain: Notification (Уведомления)
- **Notification** — in-app уведомление для пользователя

---

## Общие соглашения

### Первичные ключи
Все сущности используют `UUID v4` в качестве `id`.

### Временные метки
Все сущности имеют:
- `created_at: TIMESTAMP WITH TIME ZONE` — устанавливается один раз при создании
- `updated_at: TIMESTAMP WITH TIME ZONE` — обновляется при каждом изменении

### Мягкое удаление (Soft Delete)
Большинство сущностей не удаляются физически, а получают флаг:
- `is_deleted: BOOLEAN DEFAULT false` — удалён
- При запросах по умолчанию фильтруется `WHERE is_deleted = false`

### Архивация
Только **Lead** поддерживает архивацию:
- `is_archived: BOOLEAN DEFAULT false` — скрыт из активного списка, но не удалён

### Value Objects (Объекты-значения)
Домен использует VO для инкапсуляции валидации:
- `LeadName` — имя лида (непустая строка, max 255)
- `Contact` — телефон + email (оба опциональны, но хотя бы один рекомендуется)
- `FieldValue` — значение кастомного поля (полиморфный тип)

---

## Ролевая матрица доступа к сущностям

| Сущность | Consultant | Sales Manager | Director | Admin |
|---|:---:|:---:|:---:|:---:|
| User (управление) | — | — | — | ✅ CRUD |
| User (свой профиль) | ✅ R/U | ✅ R/U | ✅ R/U | ✅ R/U |
| Funnel | R | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| FunnelStage | R | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| Lead (свои) | ✅ CRU | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| Lead (чужие) | — | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| LeadCustomField | R | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| Source | R | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| Task (свои) | ✅ CRUD | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| Task (чужие) | R | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| LeadComment (свои) | ✅ CRUD | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| LeadComment (чужие) | R | ✅ RD | ✅ RD | ✅ CRUD |
| LeadTimelineEvent | R (только авто) | R | R | R |
| Notification (свои) | ✅ R/mark-read | ✅ R/mark-read | ✅ R/mark-read | ✅ R/mark-read |
| Аналитика (своя) | ✅ | ✅ | ✅ | ✅ |
| Аналитика (вся команда) | — | — | ✅ | ✅ |
