# Сущность: LeadTimelineEvent (Событие в истории лида)

**Домен:** Lead  
**Таблица БД:** `lead_timeline_events`  
**Статус реализации:** ❌ Не начата  
**Файлы:** отсутствуют (необходимо создать)

---

## Назначение

LeadTimelineEvent — запись в хронологической истории лида. Каждое значимое действие над лидом автоматически фиксируется как событие. Timeline даёт полную картину жизненного цикла лида: кто, что и когда с ним делал. Также сюда попадают ручные записи менеджера (звонок, встреча).

---

## Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `lead_id` | UUID | FK → leads, NOT NULL | — | Лид, к которому относится событие |
| `actor_id` | UUID | FK → users, nullable | null | Кто совершил действие (null = система) |
| `event_type` | ENUM | NOT NULL | — | Тип события |
| `payload` | JSONB | NOT NULL | `{}` | Детали события |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата и время события |

> Events — **иммутабельны**. Никаких UPDATE или DELETE не предусмотрено.

---

## Типы событий (event_type ENUM)

### Автоматические (система генерирует при изменении лида)

| Значение | Когда создаётся | Пример payload |
|---|---|---|
| `lead_created` | Лид создан | `{"source": "manual"}` |
| `stage_changed` | Смена стадии | `{"from": "Новый", "to": "Переговоры", "from_id": "uuid", "to_id": "uuid"}` |
| `funnel_changed` | Смена воронки | `{"from": "Основные", "to": "VIP", "new_stage": "Новый"}` |
| `assigned` | Смена назначенного | `{"from": "Имя", "to": "Другое имя", "from_id": "uuid", "to_id": "uuid"}` |
| `priority_changed` | Смена приоритета | `{"from": "cold", "to": "hot"}` |
| `archived` | Лид архивирован | `{}` |
| `restored` | Восстановлен из архива | `{}` |
| `task_created` | Создана задача | `{"task_id": "uuid", "task_title": "Перезвонить", "assigned_to": "Имя"}` |
| `task_done` | Задача выполнена | `{"task_id": "uuid", "task_title": "Перезвонить"}` |
| `comment_added` | Добавлен комментарий | `{"comment_id": "uuid", "preview": "Клиент подтвердил..."}` |

### Ручные (менеджер добавляет вручную)

| Значение | Описание | Payload |
|---|---|---|
| `call_logged` | Зафиксирован факт звонка | `{"direction": "outbound", "duration": null, "note": "текст"}` |
| `meeting_logged` | Зафиксирована встреча | `{"note": "текст встречи"}` |
| `message_logged` | Зафиксировано сообщение | `{"channel": "whatsapp", "note": "текст"}` |

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| `lead` | Many-to-One → Lead | Лид, к которому относится событие |
| `actor` | Many-to-One → User | Пользователь, совершивший действие |

---

## Бизнес-правила

1. **Иммутабельность** — события нельзя редактировать или удалять. История должна быть полной и честной.
2. **Автоматические события** — создаются системой внутри Use Case-ов (например, в `MoveFunnelStageUseCase` при смене стадии автоматически вызывается `CreateTimelineEventUseCase`).
3. **Ручные события** — создаются через отдельный API-эндпоинт менеджером. Это лог "что было сделано": "Позвонил клиенту", "Провёл встречу".
4. **actor_id = null** — зарезервировано для событий, созданных системой без участия пользователя (например, лид создан через webhook).
5. **Сортировка** — всегда по `created_at DESC` (новейшие сверху).
6. **Ограничение** — отображаются последние 200 событий; пагинация для глубокой истории.

---

## Отображение в UI (Timeline)

Каждое событие в UI отображается как строка:

```
[иконка типа] [Имя актора] [текст события] · [дата/время]

Пример:
⬆️  Санжар Анваров  переместил лид: "Новый" → "Переговоры"  ·  14 мая, 15:30
📞  Санжар Анваров  позвонил клиенту: "Клиент перезвонит завтра"  ·  14 мая, 12:00
✅  Санжар Анваров  выполнил задачу: "Отправить КП"  ·  13 мая, 16:45
🎯  Лид создан через Публичную форму (сайт)  ·  12 мая, 09:00
```

---

## API-эндпоинты

| Метод | Путь | Роль | Описание |
|---|---|---|---|
| `GET` | `/api/v1/leads/{lead_id}/timeline/` | All (в доступных лидах) | История событий лида |
| `POST` | `/api/v1/leads/{lead_id}/timeline/` | All | Добавить ручное событие (звонок, встреча) |

---

## Необходимые миграции

```sql
CREATE TYPE timeline_event_type AS ENUM (
    'lead_created', 'stage_changed', 'funnel_changed',
    'assigned', 'priority_changed', 'archived', 'restored',
    'task_created', 'task_done', 'comment_added',
    'call_logged', 'meeting_logged', 'message_logged'
);

CREATE TABLE lead_timeline_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID NOT NULL REFERENCES leads(id),
    actor_id UUID REFERENCES users(id),
    event_type timeline_event_type NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_timeline_lead_id ON lead_timeline_events(lead_id, created_at DESC);
```

---

## Пример объектов (JSON)

```json
// Автоматическое событие — смена стадии
{
  "id": "b8c9d0e1-f2a3-4567-bcde-678901234567",
  "lead_id": "d4e5f6a7-...",
  "actor": {
    "id": "550e8400-...",
    "full_name": "Санжар Анваров"
  },
  "event_type": "stage_changed",
  "payload": {
    "from": "Первичный контакт",
    "to": "Переговоры",
    "from_id": "stage-uuid-1",
    "to_id": "stage-uuid-2"
  },
  "created_at": "2026-05-14T15:30:00Z"
}

// Ручное событие — звонок
{
  "id": "c9d0e1f2-a3b4-5678-cdef-789012345678",
  "lead_id": "d4e5f6a7-...",
  "actor": {
    "id": "550e8400-...",
    "full_name": "Санжар Анваров"
  },
  "event_type": "call_logged",
  "payload": {
    "direction": "outbound",
    "note": "Клиент перезвонит завтра после 15:00"
  },
  "created_at": "2026-05-14T12:00:00Z"
}
```
