# UseCase: CreateSource — Создать источник лидов

## Что решает

Создаёт новый источник лидов одного из трёх типов: `webhook`, `public_form` или `manual`. Каждый тип имеет свою конфигурацию и логику валидации. Для webhook возвращается одноразовый секретный токен.

**Файл:** `backend/src/backend/application/source/use_cases/create_source.py`

**Статус:** ✅ Реализовано

---

## Участники

| Поле | Значение |
|------|----------|
| **Actor** | Менеджер или выше |
| **Роли** | `sales_manager`, `director`, `admin` |

---

## Типы источников и их конфигурация

### Тип `manual`
Ручное создание лидов через CRM-интерфейс.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название источника |
| `config.type` | `"manual"` | Тип конфигурации |

### Тип `webhook`
Приём лидов из внешних систем через HTTP-запрос.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название источника |
| `config.default_funnel_id` | `UUID` | Воронка по умолчанию |
| `config.default_stage_id` | `UUID` | Этап по умолчанию |
| `config.assignment_strategy` | `AssignmentStrategyType` | Стратегия назначения |
| `config.assignment_pool` | `list[UUID]` | Список менеджеров для назначения |
| `config.field_mapping` | `dict` | Маппинг полей из webhook-payload |

### Тип `public_form`
Публичная форма на сайте для самостоятельной заявки.

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Название источника |
| `config.slug` | `str` | Уникальный URL-идентификатор |
| `config.fields` | `list[FormFieldDTO]` | Поля формы |
| `config.default_funnel_id` | `UUID` | Воронка по умолчанию |
| `config.default_stage_id` | `UUID` | Этап по умолчанию |
| `config.assignment_strategy` | `AssignmentStrategyType` | Стратегия назначения |
| `config.assignment_pool` | `list[UUID]` | Список менеджеров |
| `config.redirect_url` | `str \| None` | URL редиректа после отправки |
| `config.success_messages` | `str \| None` | Сообщение об успехе |

---

## Порядок действий

```
1. Проверить права актора через CanManageSourcesPolicy
   └─ Если нет прав → ошибка PermissionError

2. Открыть Unit of Work

3. Выбрать ветку по типу конфигурации (match cmd.config):

   ── WEBHOOK ──────────────────────────────────────────────
   3a. Проверить воронку и этап:
       - Загрузить воронку по default_funnel_id
         └─ Если не найдена или удалена → FunnelNotFoundError
       - Загрузить этап по default_stage_id
         └─ Если не найден → StageNotFunnelError
       - Проверить, что этап принадлежит воронке
         └─ Если нет → StageNotFunnelError
   3b. Проверить пул назначения (assignment_pool):
       - Загрузить пользователей по списку UUID
       - Проверить, что все активны (is_active = True)
       - Проверить роли: только consultant и sales_manager
         └─ Если нарушение → AssignmentPoolInvalidRoleError
   3c. Создать сущность через Source.create_webhook(...)
       └─ Генерируется секретный токен + его хеш сохраняется в БД
   3d. Результат включает secret_token (показывается только один раз)

   ── PUBLIC FORM ───────────────────────────────────────────
   3a. Проверить воронку и этап (аналогично webhook)
   3b. Проверить пул назначения (аналогично webhook)
   3c. Проверить уникальность slug:
       └─ Если slug уже существует → SlugAlreadyError
   3d. Проверить кастомные поля формы:
       - Извлечь custom_field_id из полей с kind=custom_field
       - Загрузить поля из БД
       - Проверить, что все не удалены (is_deleted = False)
         └─ Если поле не найдено → CustomFieldNotFoundError
   3e. Конвертировать DTO в доменные объекты FormFieldConfig
   3f. Создать сущность через Source.create_public_form(...)
   3g. Результат включает public_url = base_url + "/" + slug

   ── MANUAL ────────────────────────────────────────────────
   3a. Создать сущность через Source.create_manual(name=cmd.name)

4. Сохранить источник в БД через uow.sources.add(source)

5. Зафиксировать транзакцию (commit)

6. Вернуть CreateSourceResult
```

---

## Возможные ошибки

| Ошибка | Условие |
|--------|---------|
| `PermissionError` | Роль актора — `consultant` или ниже |
| `FunnelNotFoundError` | Воронка не найдена или удалена |
| `StageNotFunnelError` | Этап не найден или не принадлежит воронке |
| `AssignmentPoolInvalidRoleError` | Пользователь неактивен или имеет неподходящую роль |
| `SlugAlreadyError` | Slug уже используется другой формой |
| `CustomFieldNotFoundError` | Кастомное поле не найдено или удалено |

---

## Результат (`CreateSourceResult`)

| Поле | Тип | Условие |
|------|-----|---------|
| `source_id` | `UUID` | Всегда |
| `secret_token` | `str \| None` | Только для webhook |
| `public_url` | `str \| None` | Только для public_form |

---

## Бизнес-правила

- `secret_token` для webhook показывается **только один раз** при создании — затем хранится только хеш. При утере — пересоздать через `RegenerateWebhookSecret`
- В `assignment_pool` допускаются только роли `consultant` и `sales_manager` — director и admin не включаются в пул автоназначения
- Тип источника (`source_type`) **нельзя изменить** после создания — только через удаление и пересоздание
