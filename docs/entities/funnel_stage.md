# Сущность: FunnelStage (Стадия воронки)

**Домен:** Funnel  
**Таблица БД:** `funnel_stages`  
**Статус реализации:** ✅ Полностью реализована  
**Файлы:**
- Domain: `backend/src/backend/domain/funnel/entity.py` (класс `FunnelStage`)
- Model: `backend/src/backend/infrastracture/db/sqlalchemy/funnel/models.py`
- Repository: `backend/src/backend/infrastracture/db/sqlalchemy/funnel/repository/funnel_stage.py`

---

## Назначение

FunnelStage — это отдельный шаг внутри воронки продаж. Стадии определяют весь жизненный цикл лида: от первого контакта до финального результата. Менеджер перемещает лиды между стадиями (drag-and-drop на Kanban-доске).

---

## Поля

| Поле | Тип | Ограничения | По умолчанию | Описание |
|---|---|---|---|---|
| `id` | UUID | PK | auto | Уникальный идентификатор |
| `funnel_id` | UUID | FK → funnels, NOT NULL | — | Воронка, которой принадлежит стадия |
| `name` | VARCHAR(255) | NOT NULL | — | Название стадии |
| `win_probability` | SMALLINT | NOT NULL, 0–100 | — | Вероятность выигрыша в % |
| `hex_code` | CHAR(7) | NOT NULL | — | Цвет стадии в формате `#RRGGBB` |
| `order` | SMALLINT | NOT NULL | — | Порядковый номер для сортировки |
| `kind` | ENUM | NOT NULL | `initial` | Тип стадии |
| `is_archived` | BOOLEAN | NOT NULL | `false` | Архивирована ли стадия |
| `created_at` | TIMESTAMP | NOT NULL | now() | Дата создания |
| `updated_at` | TIMESTAMP | NOT NULL | now() | Дата последнего изменения |

---

## Тип стадии (kind ENUM)

| Значение | Описание | Цвет (рекомендация) |
|---|---|---|
| `initial` | Начальная стадия — лид только поступил | Синий / серый |
| `intermediate` | Промежуточные переговоры | Жёлтый / оранжевый |
| `won` | Сделка выиграна | Зелёный |
| `lost` | Сделка проиграна | Красный |

---

## Связи

| Связь | Тип | Описание |
|---|---|---|
| `funnel` | Many-to-One → Funnel | Родительская воронка |
| `leads` | One-to-Many → Lead | Лиды, находящиеся на этой стадии |

---

## Бизнес-правила

1. **Порядок стадий** — стадии упорядочены по полю `order`. Изменение порядка происходит через операцию `reorder`, которая атомарно пересчитывает `order` для всех стадий воронки.
2. **Уникальность названия** — в рамках одной воронки не может быть двух стадий с одинаковым именем.
3. **Ограничение kind** — в одной воронке может быть несколько стадий типа `won` и `lost`, но должна быть хотя бы одна `initial`.
4. **Архивация** — архивированная стадия (`is_archived = true`) скрывается с Kanban-доски. Лиды в ней не отображаются в основном списке, но не теряются.
5. **Цвет** — `hex_code` обязателен, используется для цветовой маркировки колонок на Kanban и карточек в аналитике.
6. **Вероятность выигрыша** — `win_probability` применяется в аналитике для расчёта прогнозируемой суммы сделок (pipeline forecast).
7. **Нельзя удалить стадию с лидами** — стадия может быть удалена или заархивирована только если в ней нет активных лидов (или после их переноса).

---

## Методы доменной модели

| Метод | Описание |
|---|---|
| `create(funnel_id, name, probability, hex, order, kind)` | Фабричный метод |
| `change_order(new_order)` | Обновляет порядковый номер |
| `change(name, probability, hex, kind)` | Обновляет поля стадии |
| `archive()` | Устанавливает `is_archived = true` |
| `unarchive()` | Снимает архивацию |

---

## Value Objects

- **StageName (Name)** — непустая строка, max 255 символов
- **WinProbability** — целое число от 0 до 100 включительно
- **HexCode** — строка в формате `#RRGGBB` (7 символов)

---

## Сервисы

- **StageOrderingService** — управляет пересчётом `order` при drag-and-drop; обеспечивает целостность порядка при добавлении, удалении и перемещении стадий.

---

## API-эндпоинты

| Метод | Путь | Роль | Описание |
|---|---|---|---|
| `POST` | `/api/v1/funnel/{id}/stages` | Manager+ | Создать стадию |
| `GET` | `/api/v1/funnel/{id}/stages` | All | Список стадий воронки |
| `GET` | `/api/v1/funnel/{id}/stages/{stage_id}` | All | Получить стадию |
| `PATCH` | `/api/v1/funnel/{id}/stages/{stage_id}` | Manager+ | Обновить стадию |
| `DELETE` | `/api/v1/funnel/{id}/stages/{stage_id}` | Manager+ | Удалить стадию |
| `POST` | `/api/v1/funnel/{id}/stages/reorder` | Manager+ | Изменить порядок стадий |

---

## Пример объекта (JSON)

```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "funnel_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Первичный контакт",
  "win_probability": 15,
  "hex_code": "#4A90D9",
  "order": 1,
  "kind": "initial",
  "is_archived": false,
  "created_at": "2026-04-01T10:05:00Z",
  "updated_at": "2026-04-01T10:05:00Z"
}
```
