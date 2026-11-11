# Сущность: Source (Источник лидов)

**Домен:** Source  
**Таблица БД:** `sources`  
**Статус реализации:** ✅ Полностью реализована  
**Файлы:**
- Domain: `backend/src/backend/domain/source/entity.py`
- Model: `backend/src/backend/infrastracture/db/sqlalchemy/source/model.py`
- Repository: `backend/src/backend/infrastracture/db/sqlalchemy/source/repository.py`

---

## Назначение

Source — канал, через который в систему поступают лиды. Поддерживаются три типа: ручное создание менеджером, публичная веб-форма (ссылка для клиентов) и webhook (интеграция с внешними системами).

---

## Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `name` | VARCHAR(255) | NOT NULL | — | Название источника |
| `source_type` | ENUM | NOT NULL | — | Тип источника |
| `config` | JSONB | NOT NULL | `{}` | Конфигурация (зависит от типа) |
| `is_active` | BOOLEAN | NOT NULL | `true` | Принимает ли источник лиды |
| `is_deleted` | BOOLEAN | NOT NULL | `false` | Мягкое удаление |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |
| `updated_at` | TIMESTAMP | NOT NULL | now() | Дата последнего изменения |

---

## Типы источников (source_type ENUM)

### `manual` — Ручной ввод

Менеджер создаёт лид самостоятельно. Конфигурация не требуется.

```json
{
  "config": {}
}
```

### `public_form` — Публичная форма

Генерируется публичный URL с формой для клиентов.

```json
{
  "config": {
    "title": "Оставьте заявку",
    "form_url_slug": "main-form-2026",
    "success_message": "Спасибо! Мы свяжемся с вами в течение часа.",
    "redirect_url": null,
    "target_funnel_id": "uuid",
    "target_stage_id": "uuid",
    "assignment_strategy": "round_robin",
    "assignment_pool": ["user_uuid_1", "user_uuid_2"],
    "field_mapping": [
      {"form_field": "name",  "lead_field": "name"},
      {"form_field": "phone", "lead_field": "phone"},
      {"form_field": "email", "lead_field": "email"},
      {"form_field": "comment", "lead_field": "comment"}
    ]
  }
}
```

### `webhook` — Вебхук

Внешняя система отправляет POST-запрос с данными лида.

```json
{
  "config": {
    "secret_token": "sha256-hmac-secret",
    "target_funnel_id": "uuid",
    "target_stage_id": "uuid",
    "assignment_strategy": "round_robin",
    "assignment_pool": ["user_uuid_1"],
    "field_mapping": [
      {"webhook_field": "full_name",  "lead_field": "name"},
      {"webhook_field": "mobile",     "lead_field": "phone"},
      {"webhook_field": "mail",       "lead_field": "email"}
    ]
  }
}
```

---

## Стратегии назначения (assignment_strategy)

| Значение | Описание |
|---|---|
| `manual` | Лид создаётся без назначения (менеджер назначается вручную позже) |
| `fixed` | Лид всегда назначается на одного фиксированного пользователя |
| `round_robin` | Лиды распределяются по очереди между пользователями из `assignment_pool` |

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| `leads` | One-to-Many → Lead | Лиды, пришедшие через этот источник |

---

## Бизнес-правила

1. **Деактивированный источник не создаёт лиды** — при `is_active = false` webhook возвращает `403`, форма показывает сообщение "Форма временно недоступна".
2. **Уникальность названия** — два активных источника не могут иметь одинаковое имя.
3. **Регенерация секрета (webhook)** — при регенерации старый токен немедленно становится недействительным. Операция необратима.
4. **Верификация webhook** — входящий запрос должен содержать заголовок `X-Signature: sha256=<hmac>`, вычисленный по телу запроса и секретному токену. Запросы без валидной подписи отклоняются с `401`.
5. **Маппинг полей** — если маппинг не указан, webhook/форма создают лид только с именем. Все остальные поля заполняются по маппингу.
6. **Round-robin счётчик** — порядок назначения хранится в config (индекс последнего назначенного пользователя), инкрементируется атомарно при каждом новом лиде.

---

## Методы доменной модели

| Метод | Описание |
|---|---|
| `create_webhook(name, config)` | Фабрика для webhook-источника, генерирует secret_token |
| `create_public_form(name, config)` | Фабрика для публичной формы |
| `create_manual(name)` | Фабрика для ручного источника |
| `change_name(name)` | Переименовать источник |
| `change_config(config)` | Обновить конфигурацию |
| `activate()` | Установить `is_active = true` |
| `deactivate()` | Установить `is_active = false` |
| `regenerate_secret()` | Создать новый HMAC-секрет (только webhook) |
| `verify_webhook_token(payload, signature)` | Проверить подпись входящего запроса |
| `delete()` | Мягкое удаление |
| `restore()` | Восстановить |

---

## API-эндпоинты

| Метод | Путь | Роль | Описание |
|---|---|---|---|
| `POST` | `/api/v1/sources/` | Manager+ | Создать источник |
| `GET` | `/api/v1/sources/` | All | Список источников |
| `GET` | `/api/v1/sources/{id}` | All | Получить источник |
| `PATCH` | `/api/v1/sources/{id}` | Manager+ | Обновить |
| `POST` | `/api/v1/sources/{id}/activate` | Manager+ | Активировать |
| `POST` | `/api/v1/sources/{id}/deactivate` | Manager+ | Деактивировать |
| `DELETE` | `/api/v1/sources/{id}` | Manager+ | Удалить |
| `POST` | `/api/v1/sources/{id}/regenerate` | Manager+ | Новый webhook-секрет |
| `POST` | `/api/v1/sources/webhook/{id}` | Public | Принять webhook |
| `GET` | `/api/v1/sources/form/{id}` | Public | Получить форму |
| `POST` | `/api/v1/sources/form/{id}` | Public | Отправить форму |

---

## Пример объекта (JSON)

```json
{
  "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "name": "Сайт (главная страница)",
  "source_type": "public_form",
  "is_active": true,
  "is_deleted": false,
  "config": {
    "title": "Получите консультацию",
    "success_message": "Спасибо! Мы свяжемся с вами.",
    "target_funnel_id": "a1b2c3d4-...",
    "target_stage_id": "b2c3d4e5-...",
    "assignment_strategy": "round_robin",
    "assignment_pool": ["user1-uuid", "user2-uuid"],
    "field_mapping": [
      {"form_field": "name", "lead_field": "name"},
      {"form_field": "phone", "lead_field": "phone"}
    ]
  },
  "created_at": "2026-04-10T12:00:00Z",
  "updated_at": "2026-04-10T12:00:00Z"
}
```

> `secret_token` в API-ответах возвращается **только один раз** — при создании и при регенерации.
