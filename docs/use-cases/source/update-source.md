# UseCase: UpdateSource — Обновить источник лидов

## Что решает

Обновляет название и/или конфигурацию существующего источника лидов. Применяет патч-подход: обновляются только переданные поля (`model_dump(exclude_unset=True)`). Тип источника (`source_type`) изменить нельзя.

**Файл:** `backend/src/backend/application/source/use_cases/update_source.py`

**Статус:** ✅ Реализовано

---

## Участники

| Поле | Значение |
|------|----------|
| **Actor** | Менеджер или выше |
| **Роли** | `sales_manager`, `director`, `admin` |

---

## Входные данные

| Поле | Тип | Описание |
|------|-----|----------|
| `cmd.name` | `str \| None` | Новое название (опционально) |
| `cmd.config` | `UpdateConfigDTO \| None` | Новая конфигурация (опционально) |

Источник передаётся как атрибут use case (`self.source`).

---

## Порядок действий

```
1. Проверить права актора через CanManageSourcesPolicy
   └─ Если нет прав → ошибка PermissionError

2. Открыть Unit of Work

3. Если cmd.name передано:
   └─ Вызвать source.change_name(cmd.name)

4. Если cmd.config передано:
   4a. Проверить, что config.type == source.source_type
       └─ Если типы различаются → CanNotSourceTypeError

   4b. Построить новую конфигурацию по типу:

       ── WEBHOOK ──────────────────────────────────────────
       - Извлечь изменённые поля (exclude_unset=True)
       - Если изменились funnel_id или stage_id → проверить валидность
         (воронка существует, этап принадлежит воронке)
       - Если изменился assignment_pool → проверить пул
         (активные, роли consultant/sales_manager)
       - Создать новый WebhookConfig через dataclasses.replace(current, **changes)

       ── PUBLIC FORM ───────────────────────────────────────
       - Извлечь изменённые поля (exclude_unset=True)
       - Если изменился slug (и он отличается от текущего) → проверить уникальность
       - Если изменились funnel_id или stage_id → проверить валидность
       - Если изменился assignment_pool → проверить пул
       - Если изменились fields → проверить кастомные поля
       - Создать новый PublicFormConfig через dataclasses.replace(current, **changes)

       ── MANUAL ────────────────────────────────────────────
       - Нет конфигурируемых полей → вернуть None (нечего менять)

   4c. Если новая конфигурация не None → source.change_config(new_config)

5. Сохранить источник через uow.sources.update(self.source)

6. Зафиксировать транзакцию (commit)
```

---

## Возможные ошибки

| Ошибка | Условие |
|--------|---------|
| `PermissionError` | Нет прав |
| `CanNotSourceTypeError` | Попытка изменить тип источника |
| `FunnelNotFoundError` | Воронка не найдена или удалена |
| `StageNotFunnelError` | Этап не принадлежит воронке |
| `AssignmentPoolInvalidRoleError` | Пул содержит неактивных или неподходящих пользователей |
| `SlugAlreadyError` | Новый slug уже занят |
| `CustomFieldNotFoundError` | Кастомное поле не найдено или удалено |

---

## Результат

`None` — успешное выполнение без возвращаемого значения.

---

## Бизнес-правила

- **Patch-семантика**: поля, не переданные в запросе (`exclude_unset=True`), остаются без изменений
- Тип источника **нельзя изменить** — это принципиальное ограничение
- `secret_token` для webhook не обновляется через этот use case — только через `RegenerateWebhookSecret`
