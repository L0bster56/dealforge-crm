# Сущность: Notification (Уведомление)

**Домен:** Notification  
**Таблица БД:** `notifications`  
**Статус реализации:** ❌ Не начата  
**Файлы:** отсутствуют (необходимо создать)

---

## Назначение

Notification — in-app уведомление для пользователя. Система автоматически создаёт уведомления при назначении лидов, создании задач, приближении дедлайнов и других значимых событиях. Уведомления отображаются в колокольчике в header навигации.

---

## Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `user_id` | UUID | FK → users, NOT NULL | — | Получатель уведомления |
| `type` | ENUM | NOT NULL | — | Тип события, вызвавшего уведомление |
| `title` | VARCHAR(255) | NOT NULL | — | Краткий заголовок |
| `body` | TEXT | NOT NULL | — | Полный текст уведомления |
| `entity_type` | ENUM | NOT NULL | — | Тип объекта (lead / task) |
| `entity_id` | UUID | NOT NULL | — | ID объекта (для ссылки в UI) |
| `is_read` | BOOLEAN | NOT NULL | `false` | Прочитано ли |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |

---

## Типы уведомлений (type ENUM)

| Значение | Заголовок | Тело сообщения | Получатель |
|---|---|---|---|
| `lead_assigned` | "Вам назначен лид" | "Лид «{name}» назначен на вас" | assigned_to |
| `lead_reassigned` | "Лид переназначен" | "Лид «{name}» был переназначен. Прежний: {old}" | old assigned_to |
| `lead_moved_to_won` | "Сделка выиграна!" | "Лид «{name}» перешёл в стадию «Выиграно»" | assigned_to + created_by |
| `task_created` | "Новая задача" | "Вам назначена задача: «{title}»" | task.assigned_to |
| `task_deadline_soon` | "Дедлайн через час" | "Задача «{title}» по лиду «{lead}» — дедлайн в {time}" | task.assigned_to |
| `task_overdue` | "Просроченная задача" | "Задача «{title}» просрочена. Лид: «{lead}»" | task.assigned_to + task.created_by |

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| `user` | Many-to-One → User | Получатель уведомления |

---

## Бизнес-правила

1. **Только in-app** — уведомления хранятся в БД и отображаются в браузере. Email / Telegram / SMS не используются в v1.
2. **Хранение** — хранятся последние **100 уведомлений** на пользователя. При превышении удаляются самые старые.
3. **Не дублируются** — если пользователь уже получил уведомление типа `task_deadline_soon` по конкретной задаче — повторно не отправляется.
4. **Пометка прочитано** — пользователь может прочитать по одному или все сразу (`read_all`).
5. **Real-time** — уведомления доставляются в реальном времени через WebSocket (SSE как fallback). При закрытом браузере — при следующем открытии.
6. **Счётчик** — непрочитанные уведомления отображаются числом на иконке (макс. 99+).
7. **Ссылка** — клик по уведомлению ведёт на страницу объекта (`entity_type` + `entity_id`).

---

## Real-time доставка

Рекомендуемый подход для v1 — **Server-Sent Events (SSE)**:

```
GET /api/v1/notifications/stream
Authorization: Bearer {token}
Accept: text/event-stream
```

Каждое новое уведомление отправляется клиенту как SSE-событие:
```
event: notification
data: {"id": "uuid", "type": "task_created", "title": "...", ...}
```

В v2 — WebSocket для двусторонней связи.

---

## Планировщик дедлайнов

Для уведомлений о дедлайнах задач необходим фоновый процесс (Celery Beat или APScheduler):

- Каждые **5 минут** проверяет задачи где: `deadline BETWEEN now() AND now() + 1 hour` AND `status != 'done'` AND уведомление ещё не отправлено
- Каждые **15 минут** проверяет просроченные задачи: `deadline < now()` AND `status != 'done'`

---

## API-эндпоинты

| Метод | Путь | Роль | Описание |
|---|---|---|---|
| `GET` | `/api/v1/notifications/` | Auth | Список уведомлений (пагинация) |
| `GET` | `/api/v1/notifications/stream` | Auth | SSE-поток новых уведомлений |
| `GET` | `/api/v1/notifications/unread-count` | Auth | Счётчик непрочитанных |
| `PATCH` | `/api/v1/notifications/{id}/read` | Auth | Отметить одно как прочитанное |
| `PATCH` | `/api/v1/notifications/read-all` | Auth | Отметить все как прочитанные |

---

## Необходимые миграции

```sql
CREATE TYPE notification_type AS ENUM (
    'lead_assigned', 'lead_reassigned', 'lead_moved_to_won',
    'task_created', 'task_deadline_soon', 'task_overdue'
);

CREATE TYPE notification_entity_type AS ENUM ('lead', 'task');

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type notification_type NOT NULL,
    title VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    entity_type notification_entity_type NOT NULL,
    entity_id UUID NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id, created_at DESC);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read)
    WHERE is_read = false;
```

---

## Пример объекта (JSON)

```json
{
  "id": "d0e1f2a3-b4c5-6789-defa-890123456789",
  "type": "task_deadline_soon",
  "title": "Дедлайн через час",
  "body": "Задача «Перезвонить клиенту» по лиду «Акбар Юсупов» — дедлайн в 14:00",
  "entity_type": "task",
  "entity_id": "f6a7b8c9-...",
  "is_read": false,
  "created_at": "2026-05-16T13:00:00Z"
}
```

```json
// GET /api/v1/notifications/unread-count
{
  "count": 3
}
```
