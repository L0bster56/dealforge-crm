# Сущность: Task (Задача)

**Домен:** Lead  
**Таблица БД:** `tasks`  
**Статус реализации:** ❌ Не начата  
**Файлы:** отсутствуют (необходимо создать)

---

## Назначение

Task — задача, связанная с конкретным лидом. Менеджер создаёт задачи, чтобы не забыть перезвонить клиенту, отправить документы или провести встречу. Задача имеет дедлайн, ответственного и статус выполнения. Просроченные задачи подсвечиваются и генерируют уведомления.

---

## Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `lead_id` | UUID | FK → leads, NOT NULL | — | Лид, к которому привязана задача |
| `title` | VARCHAR(255) | NOT NULL | — | Название задачи |
| `description` | TEXT | nullable | null | Описание / детали задачи |
| `deadline` | TIMESTAMP | NOT NULL | — | Дедлайн (дата + время) |
| `assigned_to` | UUID | FK → users, NOT NULL | — | Ответственный за выполнение |
| `created_by` | UUID | FK → users, NOT NULL | current user | Создатель задачи |
| `status` | ENUM | NOT NULL | `todo` | Статус выполнения |
| `is_deleted` | BOOLEAN | NOT NULL | `false` | Мягкое удаление |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |
| `updated_at` | TIMESTAMP | NOT NULL | now() | Дата последнего изменения |

---

## Статус задачи (status ENUM)

| Значение | Название | Описание |
|---|---|---|
| `todo` | К выполнению | Задача создана, ещё не начата |
| `in_progress` | В работе | Задача взята в работу |
| `done` | Выполнена | Задача завершена |

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| `lead` | Many-to-One → Lead | Лид, которому принадлежит задача |
| `assigned_user` | Many-to-One → User | Ответственный |
| `created_user` | Many-to-One → User | Создатель |

---

## Бизнес-правила

1. **Привязка к лиду обязательна** — задача не может существовать без лида. При удалении лида задачи сохраняются (доступны в архиве).
2. **Статус — только вперёд (не строго)** — статус может меняться в любую сторону (например, задача перешла `done`, но её вернули в `in_progress`).
3. **Выполненные задачи** — задача со статусом `done` отображается в разделе "Выполнено" внутри лида; создаётся событие в timeline.
4. **Уведомления:**
   - При создании задачи → уведомление `assigned_to`
   - За 1 час до дедлайна → уведомление `assigned_to`
   - В момент дедлайна (если не `done`) → уведомление `assigned_to` + `created_by`
5. **Права на редактирование:**
   - Создатель задачи или `assigned_to` может менять статус
   - `Sales Manager+` может редактировать или удалять любую задачу
   - `Consultant` может управлять только задачами в своих лидах
6. **Просроченная задача** — задача считается просроченной если `deadline < now()` и `status != 'done'`. Подсвечивается красным в UI.

---

## События в Timeline (при изменении задачи)

| Событие | Тип в timeline |
|---|---|
| Создание задачи | `task_created` |
| Завершение задачи (status → done) | `task_done` |

---

## Страница "Мои задачи"

Отдельный раздел в навигации, где пользователь видит все свои задачи по всем лидам.

**Фильтры:**
- Статус: todo / in_progress / done
- Период дедлайна: сегодня / эта неделя / просроченные
- Воронка / лид (поиск)

**Сортировка:**
- По дедлайну (по умолчанию — ASC)
- По дате создания

---

## API-эндпоинты

| Метод | Путь | Роль | Описание |
|---|---|---|---|
| `POST` | `/api/v1/leads/{lead_id}/tasks/` | All (в своих лидах) | Создать задачу |
| `GET` | `/api/v1/leads/{lead_id}/tasks/` | All | Задачи по лиду |
| `GET` | `/api/v1/leads/{lead_id}/tasks/{id}` | All | Получить задачу |
| `PATCH` | `/api/v1/leads/{lead_id}/tasks/{id}` | All (свои) / Manager+ | Редактировать |
| `DELETE` | `/api/v1/leads/{lead_id}/tasks/{id}` | All (свои) / Manager+ | Удалить |
| `GET` | `/api/v1/tasks/my` | All | Все мои задачи |

---

## Необходимые миграции

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID NOT NULL REFERENCES leads(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    deadline TIMESTAMP WITH TIME ZONE NOT NULL,
    assigned_to UUID NOT NULL REFERENCES users(id),
    created_by UUID NOT NULL REFERENCES users(id),
    status VARCHAR(20) NOT NULL DEFAULT 'todo'
        CHECK (status IN ('todo', 'in_progress', 'done')),
    is_deleted BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX idx_tasks_lead_id ON tasks(lead_id);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_tasks_deadline ON tasks(deadline) WHERE is_deleted = false;
CREATE INDEX idx_tasks_status ON tasks(status) WHERE is_deleted = false;
```

---

## Пример объекта (JSON)

```json
{
  "id": "f6a7b8c9-d0e1-2345-fabc-456789012345",
  "lead_id": "d4e5f6a7-...",
  "title": "Перезвонить клиенту",
  "description": "Уточнить детали встречи и отправить КП",
  "deadline": "2026-05-16T14:00:00+05:00",
  "assigned_to": {
    "id": "550e8400-...",
    "full_name": "Санжар Анваров"
  },
  "created_by": {
    "id": "550e8400-...",
    "full_name": "Санжар Анваров"
  },
  "status": "todo",
  "is_deleted": false,
  "is_overdue": false,
  "created_at": "2026-05-14T10:00:00Z",
  "updated_at": "2026-05-14T10:00:00Z"
}
```

> `is_overdue` — вычисляемое поле (не хранится в БД): `deadline < now() AND status != 'done'`
