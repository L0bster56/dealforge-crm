# DealForge CRM — Контекст проекта

## Что это

**DealForge CRM** — внутренняя (single-tenant) CRM-система для малого бизнеса на рынке Узбекистана. Разрабатывается с нуля как учебно-коммерческий проект. Языки интерфейса: русский + ўзбекча (латиница). Валюты: UZS + USD.

Команда клиента: 1–10 человек. Деплой: собственный VPS + Docker + nginx.

---

## Документация проекта

| Файл | Содержание |
|---|---|
| [`docs/PRD.md`](docs/PRD.md) | Полный Product Requirements Document (v1.1, Approved) |
| [`docs/entities/README.md`](docs/entities/README.md) | Обзор всех сущностей, ERD-диаграмма, матрица прав |
| [`docs/entities/user.md`](docs/entities/user.md) | Сущность User |
| [`docs/entities/funnel.md`](docs/entities/funnel.md) | Сущность Funnel |
| [`docs/entities/funnel_stage.md`](docs/entities/funnel_stage.md) | Сущность FunnelStage |
| [`docs/entities/source.md`](docs/entities/source.md) | Сущность Source |
| [`docs/entities/lead.md`](docs/entities/lead.md) | Сущность Lead |
| [`docs/entities/lead_custom_field.md`](docs/entities/lead_custom_field.md) | LeadCustomField + Enum + Value |
| [`docs/entities/task.md`](docs/entities/task.md) | Сущность Task |
| [`docs/entities/lead_comment.md`](docs/entities/lead_comment.md) | Сущность LeadComment |
| [`docs/entities/lead_timeline_event.md`](docs/entities/lead_timeline_event.md) | Сущность LeadTimelineEvent |
| [`docs/entities/notification.md`](docs/entities/notification.md) | Сущность Notification |

---

## Технический стек

### Backend (реализован)
- **Python 3.11+**, **FastAPI** + Uvicorn
- **SQLAlchemy 2.0** (async) + **asyncpg** + **PostgreSQL**
- **Alembic** — миграции
- **Argon2** — хеширование паролей
- **python-jose** — JWT (access 15min + refresh 30d)
- **Pydantic v2** — валидация и настройки
- Архитектура: **Clean Architecture** (Domain / Application / Infrastructure / Presentation)

### Frontend (планируется)
- **Next.js 14+** (App Router) + **TypeScript**
- **shadcn/ui** + **Tailwind CSS**
- **@dnd-kit/core** — drag-and-drop (Kanban)
- **Recharts** — графики аналитики
- **next-intl** — i18n (ru / uz-Latn)
- **PWA** (next-pwa) — мобильная поддержка

---

## Архитектура бэкенда

```
backend/src/backend/
├── domain/           ← Сущности, Value Objects, Политики, Спецификации
├── application/      ← Use Cases, DTOs, Интерфейсы репозиториев
├── infrastracture/   ← SQLAlchemy модели, репозитории, JWT, Argon2
│   └── db/sqlalchemy/
│       ├── core/     ← UoW, session, base model, миксины
│       ├── user/
│       ├── funnel/
│       ├── lead/
│       └── source/
└── presentation/     ← FastAPI роутеры (api/v1/)
    └── api/v1/
        ├── auth/
        ├── user/
        ├── funnel/
        └── source/
```

**Ключевые паттерны:**
- Unit of Work (транзакции через `SqlAlchemyUnitOfWork`)
- Repository Pattern (интерфейс в application, реализация в infrastructure)
- Class-Based Views (`fastapi-utils` CBV)
- Value Objects для всей доменной валидации
- Policy-based авторизация в Use Cases
- Mapper Pattern: `to_entity()` / `to_model()` между доменом и БД

---

## Состояние реализации (бэкенд)

### ✅ Полностью реализовано
| Домен | Use Cases | Router | Миграция |
|---|---|---|---|
| Auth | Login, Refresh, GetMe, UpdateMe, ChangePassword | ✅ | ✅ |
| User | Create, Delete, GetById, Update | ✅ | ✅ |
| Funnel | CRUD + Reorder stages | ✅ | ✅ |
| FunnelStage | CRUD + Move | ✅ | ✅ |
| Source | CRUD + Activate/Deactivate + Regenerate secret | ✅ | ❌ нет миграции |
| LeadCustomField | CRUD + AddEnum + RemoveEnum | ✅ use cases | ❌ нет router, нет миграции |

### 🔨 Частично реализовано
| Домен | Что есть | Что отсутствует |
|---|---|---|
| Lead | Domain entity + Value Objects | Infrastructure (таблица, репозиторий), Router |
| LeadCustomFieldValue | Domain logic (set/remove value) | Таблица в БД, репозиторий |

### ❌ Не начато (нужно создавать с нуля)
- **Tasks** — Use Cases, Domain, Infrastructure, Router
- **LeadComments** — Use Cases, Domain, Infrastructure, Router
- **LeadTimelineEvents** — Use Cases, Domain, Infrastructure, Router
- **Notifications** — Use Cases, Domain, Infrastructure, Router, SSE-поток
- **Analytics** — Use Cases, Router (агрегационные запросы)
- **Export** — CSV, XLSX, PDF
- **Public webhook receiver** — публичный эндпоинт для входящих webhook
- **Public form submission** — публичная форма без авторизации

### ⚠️ Известные проблемы
- Таблицы `sources`, `lead_custom_field`, `lead_custom_field_enum` существуют в коде, но **нет Alembic-миграций**
- `LeadCustomField` router не подключён в `main.py`
- Typo в коде: `self.update_at` должно быть `self.updated_at` (`TimeActionMixin`)
- Смешанные импорты: `from src.backend` и `from backend` — непоследовательно

---

## Сущности и их таблицы

| Сущность | Таблица | Статус |
|---|---|---|
| User | `users` | ✅ |
| Funnel | `funnels` | ✅ |
| FunnelStage | `funnel_stages` | ✅ |
| Source | `sources` | 🔨 модель есть, миграция нет |
| LeadCustomField | `lead_custom_field` | 🔨 модель есть, миграция нет |
| LeadCustomFieldEnum | `lead_custom_field_enum` | 🔨 модель есть, миграция нет |
| LeadCustomFieldValue | `lead_custom_field_value` | ❌ |
| Lead | `leads` | ❌ |
| Task | `tasks` | ❌ |
| LeadComment | `lead_comments` | ❌ |
| LeadTimelineEvent | `lead_timeline_events` | ❌ |
| Notification | `notifications` | ❌ |

---

## Роли пользователей

| Роль | Лиды | Настройки | Аналитика |
|---|---|---|---|
| `consultant` | Только свои | Только чтение | Только свои |
| `sales_manager` | Все лиды команды | CRUD | Только свои |
| `director` | Все + создавать | Только чтение | Вся команда |
| `admin` | Все | Полный доступ | Всё |

**Ключевое правило:** `consultant` видит **только** лиды, где `assigned_to = current_user`.

---

## Ключевые бизнес-решения (зафиксированы в PRD)

1. **Single-tenant** — одна компания, одна БД, нет multi-tenancy
2. **Лид в одной воронке** — лид находится только в одной воронке одновременно
3. **Архивация ≠ Удаление** — `is_archived` (скрыт, восстанавливаем) vs `is_deleted` (удалён)
4. **Auto-assign round-robin** — работает и при ручном создании, и через Public Form/Webhook
5. **Bulk-операции** — не реализуются в v1
6. **Дублирование лида** — не реализуется в v1
7. **Director** — может создавать и редактировать лиды (не только смотреть аналитику)
8. **Страница "Мои задачи"** — отдельный раздел в навигации
9. **Уведомления** — только in-app (без Telegram, Email, SMS в v1)
10. **Мобильная версия** — PWA (не нативное приложение)

---

## Структура лида (ключевые поля)

```
Lead:
  name          VARCHAR(255)        # обязательное
  phone         VARCHAR(20)         # +998XXXXXXXXX
  email         VARCHAR(255)
  funnel_id     UUID → Funnel
  stage_id      UUID → FunnelStage
  source_id     UUID → Source
  assigned_to   UUID → User
  created_by    UUID → User
  priority      ENUM(cold/warm/hot)
  amount_uzs    BIGINT              # сумма в UZS
  amount_usd    DECIMAL(15,2)       # сумма в USD
  comment       TEXT
  is_deleted    BOOLEAN
  is_archived   BOOLEAN
```

---

## Аналитика (требования)

**Фильтры:** период (день/неделя/месяц/произвольный) + воронка + менеджер (Manager+)

**Виджеты дашборда:**
1. Сводные KPI: новые лиды, выигранные, сумма сделок, конверсия
2. Воронка — лиды по стадиям (funnel chart)
3. Динамика лидов по времени (line chart)
4. Эффективность менеджеров (таблица)
5. Источники лидов (pie chart)
6. Среднее время в стадии (bar chart)

**Экспорт:** Excel/CSV (лиды) + PDF (аналитика)

---

## Текущая ветка и git-история

- Основная ветка: `main`
- Рабочая ветка: `lesson3`
- Последние коммиты: `Funnel` → `22` → `all branch` → `lesson3.1` → `added VO Name2`

---

## Следующие шаги разработки

### Приоритет 1 — Завершить бэкенд Lead-домена
1. Создать Alembic-миграции для `sources`, `lead_custom_field`, `lead_custom_field_enum`
2. Реализовать `leads` таблицу + Infrastructure + миграцию
3. Реализовать `lead_custom_field_value` таблицу
4. Подключить LeadCustomField router в `main.py`
5. Реализовать Lead Use Cases (Create, Get, List, Update, Delete, Archive, Move stage, Assign)
6. Реализовать Lead Router

### Приоритет 2 — Новые домены
7. Task (Use Cases + Infrastructure + Router)
8. LeadComment (Use Cases + Infrastructure + Router)
9. LeadTimelineEvent (иммутабельный лог, автоматически из Use Cases)

### Приоритет 3 — Уведомления и аналитика
10. Notification (Use Cases + SSE-поток)
11. Analytics (агрегационные запросы + Router)
12. Export (CSV, XLSX, PDF)

### Приоритет 4 — Публичные эндпоинты
13. Webhook receiver (`POST /api/v1/sources/webhook/{id}`)
14. Public Form (`GET/POST /api/v1/sources/form/{id}`)
