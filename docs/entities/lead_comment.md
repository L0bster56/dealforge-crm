# Сущность: LeadComment (Комментарий к лиду)

**Домен:** Lead  
**Таблица БД:** `lead_comments`  
**Статус реализации:** ❌ Не начата  
**Файлы:** отсутствуют (необходимо создать)

---

## Назначение

LeadComment — текстовый комментарий, который менеджер оставляет к лиду. Используется для фиксации результатов звонков, встреч, договорённостей и внутренних заметок. Отображается в хронологическом порядке в детальной карточке лида.

---

## Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `lead_id` | UUID | FK → leads, NOT NULL | — | Лид, к которому относится комментарий |
| `author_id` | UUID | FK → users, NOT NULL | current user | Автор комментария |
| `text` | TEXT | NOT NULL, min 1 char | — | Текст комментария |
| `is_deleted` | BOOLEAN | NOT NULL | `false` | Мягкое удаление |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |
| `updated_at` | TIMESTAMP | NOT NULL | now() | Дата редактирования |

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| `lead` | Many-to-One → Lead | Лид, которому принадлежит комментарий |
| `author` | Many-to-One → User | Автор комментария |

---

## Бизнес-правила

1. **Редактирование только автором** — изменить текст комментария может только его автор (или Admin).
2. **Окно редактирования — 24 часа** — после создания автор может отредактировать комментарий в течение 24 часов. Позже — только удаление.
3. **Удаление:**
   - Автор может удалить свой комментарий в любое время (мягкое удаление)
   - `Sales Manager` может удалять любые комментарии в лидах своей команды
4. **Видимость** — комментарии видят все пользователи, у которых есть доступ к этому лиду.
5. **Нет редактирования чужих** — `Sales Manager` не может редактировать комментарии других; только удалять.
6. **Каскад** — при удалении лида комментарии сохраняются (доступны при восстановлении).
7. **Событие в timeline** — добавление комментария создаёт запись `comment_added` в `lead_timeline_events`.

---

## Отображение в UI

Комментарии отображаются в детальной карточке лида в разделе "Комментарии":
- Аватар и имя автора
- Дата и время (относительная: "5 минут назад", "вчера в 14:30")
- Текст комментария
- Кнопки "Редактировать" / "Удалить" (если есть права)
- Пометка "(изменено)" если `updated_at > created_at`

---

## API-эндпоинты

| Метод | Путь | Роль | Описание |
|---|---|---|---|
| `POST` | `/api/v1/leads/{lead_id}/comments/` | All (в доступных лидах) | Добавить комментарий |
| `GET` | `/api/v1/leads/{lead_id}/comments/` | All | Список комментариев (хронология) |
| `PATCH` | `/api/v1/leads/{lead_id}/comments/{id}` | Автор (24ч) / Admin | Редактировать |
| `DELETE` | `/api/v1/leads/{lead_id}/comments/{id}` | Автор / Manager+ | Удалить |

---

## Необходимые миграции

```sql
CREATE TABLE lead_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID NOT NULL REFERENCES leads(id),
    author_id UUID NOT NULL REFERENCES users(id),
    text TEXT NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_lead_comments_lead_id ON lead_comments(lead_id)
    WHERE is_deleted = false;
```

---

## Пример объекта (JSON)

```json
{
  "id": "a7b8c9d0-e1f2-3456-abcd-567890123456",
  "lead_id": "d4e5f6a7-...",
  "author": {
    "id": "550e8400-...",
    "full_name": "Санжар Анваров",
    "avatar": null
  },
  "text": "Клиент подтвердил встречу на пятницу. Нужно подготовить презентацию.",
  "is_edited": true,
  "created_at": "2026-05-14T11:00:00Z",
  "updated_at": "2026-05-14T11:15:00Z"
}
```

> `is_edited` — вычисляемое поле: `updated_at > created_at + 5 seconds`
