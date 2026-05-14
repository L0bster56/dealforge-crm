# Сущность: User (Пользователь)

**Домен:** Auth & Users  
**Таблица БД:** `users`  
**Статус реализации:** ✅ Полностью реализована  
**Файлы:**
- Domain: `backend/src/backend/domain/user/entity.py`
- Model: `backend/src/backend/infrastracture/db/sqlalchemy/user/models.py`
- Repository: `backend/src/backend/infrastracture/db/sqlalchemy/user/repository.py`

---

## Назначение

User — сотрудник компании, который работает в системе. Каждый пользователь имеет роль, определяющую его права доступа. Система не является публичной — все учётные записи создаются администратором вручную.

---

## Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `first_name` | VARCHAR(100) | NOT NULL | — | Имя |
| `last_name` | VARCHAR(100) | NOT NULL | — | Фамилия |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | — | Логин (уникальный) |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE | — | Email (уникальный) |
| `password_hash` | TEXT | NOT NULL | — | Хеш пароля (Argon2) |
| `role` | ENUM | NOT NULL | — | Роль пользователя |
| `is_active` | BOOLEAN | NOT NULL | `true` | Активен ли аккаунт |
| `last_interaction` | TIMESTAMP | nullable | `null` | Дата последнего действия |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |
| `updated_at` | TIMESTAMP | NOT NULL | now() | Дата последнего изменения |

---

## Роли (ENUM)

| Значение | Название | Описание |
|---|---|---|
| `consultant` | Консультант | Видит и управляет только своими лидами |
| `sales_manager` | Менеджер по продажам | Видит все лиды, управляет настройками |
| `director` | Директор | Полный доступ к данным + аналитика |
| `admin` | Администратор | Системные настройки, управление пользователями |

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| `leads` (assigned_to) | One-to-Many | Лиды, назначенные на этого пользователя |
| `leads` (created_by) | One-to-Many | Лиды, созданные этим пользователем |
| `tasks` (assigned_to) | One-to-Many | Задачи, назначенные на пользователя |
| `tasks` (created_by) | One-to-Many | Задачи, созданные пользователем |
| `lead_comments` | One-to-Many | Комментарии пользователя |
| `lead_timeline_events` | One-to-Many | События, совершённые пользователем |
| `notifications` | One-to-Many | Уведомления пользователя |

---

## Бизнес-правила

1. **Email и username уникальны** — система не позволит создать двух пользователей с одинаковым email или username.
2. **Деактивация вместо удаления** — пользователь не удаляется физически; устанавливается `is_active = false`. Все его данные (лиды, задачи) сохраняются.
3. **Создание только Admin** — только пользователь с ролью `admin` может создавать новых пользователей.
4. **Смена пароля** — пользователь меняет пароль сам, указывая старый пароль для подтверждения.
5. **Смена роли** — только Admin может изменить роль пользователя.
6. **Нельзя деактивировать себя** — Admin не может деактивировать свой собственный аккаунт.

---

## Value Objects

- **Email** — валидирует формат email (`email-validator`)
- **Name** — непустая строка, max 100 символов, trim пробелов
- **Username** — латиница + цифры + `_`, min 3, max 50 символов

---

## Методы доменной модели

| Метод | Описание |
|---|---|
| `interact()` | Обновляет `last_interaction` на текущее время |
| `change_password(new_hash)` | Устанавливает новый хеш пароля |
| `change_first_name(name)` | Меняет имя через VO |
| `change_last_name(name)` | Меняет фамилию через VO |
| `change_email(email)` | Меняет email через VO |
| `change_username(username)` | Меняет username через VO |

---

## API-эндпоинты

| Метод | Путь | Роль | Описание |
|---|---|---|---|
| `POST` | `/api/v1/auth/login` | Public | Вход в систему |
| `POST` | `/api/v1/auth/refresh` | Auth | Обновить access token |
| `GET` | `/api/v1/auth/me` | Auth | Получить свой профиль |
| `PATCH` | `/api/v1/auth/me` | Auth | Обновить свой профиль |
| `POST` | `/api/v1/auth/change-password` | Auth | Сменить пароль |
| `POST` | `/api/v1/users/` | Admin | Создать пользователя |
| `GET` | `/api/v1/users/{id}` | Admin | Получить пользователя |
| `PATCH` | `/api/v1/users/{id}` | Admin | Обновить пользователя |
| `DELETE` | `/api/v1/users/{id}` | Admin | Деактивировать пользователя |

---

## Пример объекта (JSON)

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "first_name": "Санжар",
  "last_name": "Анваров",
  "username": "sanjar_a",
  "email": "sanjar@dealforge.uz",
  "role": "sales_manager",
  "is_active": true,
  "last_interaction": "2026-05-14T10:30:00Z",
  "created_at": "2026-04-01T09:00:00Z",
  "updated_at": "2026-05-14T10:30:00Z"
}
```

> `password_hash` никогда не возвращается в API-ответах.
