# UseCase: GetLead — Получить лид

## Что решает

Загружает полные данные лида по UUID, включая кастомные значения полей. Применяет фильтрацию по роли: `consultant` видит только свои лиды.

**Статус:** ❌ Не реализовано (планируется — Приоритет 1)

---

## Участники

| Поле | Значение |
|------|----------|
| **Actor** | Любой авторизованный пользователь |
| **Роли** | Все роли (с ограничениями по видимости) |

---

## Входные данные

| Поле | Тип | Описание |
|------|-----|----------|
| `lead_id` | `UUID` | ID лида |

---

## Порядок действий

```
1. Открыть Unit of Work

2. Загрузить лид из БД по lead_id (вместе с кастомными значениями)
   └─ Если не найден или is_deleted = True → LeadNotFoundError

3. Проверить доступ по роли:
   - Если actor.role == consultant И lead.assigned_to ≠ actor.id
     → LeadAccessDeniedError (или LeadNotFoundError — не раскрывать существование)

4. Вернуть LeadViewDTO со всеми полями, включая custom_values
```

---

## Возможные ошибки

| Ошибка | Условие |
|--------|---------|
| `LeadNotFoundError` | Лид не найден, удалён, или недоступен по роли |

---

## Результат (`LeadViewDTO`)

Все поля лида: `id`, `name`, `phone`, `email`, `funnel_id`, `stage_id`, `source_id`, `assigned_to`, `created_by`, `priority`, `amount_uzs`, `amount_usd`, `comment`, `is_archived`, `is_deleted`, `created_at`, `updated_at`, `custom_values[]`.

---

## Бизнес-правила

- **Consultant** видит только лиды, где `assigned_to = self.id`
- **Sales Manager, Director, Admin** видят все лиды
- Удалённые лиды (`is_deleted = True`) недоступны всем (только через специальный архив-запрос с флагом)
