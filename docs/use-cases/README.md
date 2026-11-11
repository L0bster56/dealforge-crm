# Use Cases — DealForge CRM

Полная документация всех use cases системы. Каждый файл описывает одну бизнес-операцию: её назначение, порядок выполнения, проверки и возможные ошибки.

---

## Статус реализации

| Символ | Значение |
|--------|----------|
| ✅ | Реализовано (код существует) |
| ❌ | Не реализовано (планируется) |

---

## Auth — Аутентификация

| Use Case | Файл | Статус |
|----------|------|--------|
| Вход в систему | [auth/login.md](auth/login.md) | ✅ |
| Обновление токенов | [auth/refresh-token.md](auth/refresh-token.md) | ✅ |
| Получить текущего пользователя | [auth/get-me.md](auth/get-me.md) | ✅ |
| Обновить профиль | [auth/update-me.md](auth/update-me.md) | ✅ |
| Изменить пароль | [auth/change-password.md](auth/change-password.md) | ✅ |

---

## User — Управление пользователями

| Use Case | Файл | Статус |
|----------|------|--------|
| Создать пользователя | [user/create-user.md](user/create-user.md) | ✅ |
| Получить пользователя по ID | [user/get-user.md](user/get-user.md) | ✅ |
| Обновить пользователя | [user/update-user.md](user/update-user.md) | ✅ |
| Деактивировать пользователя | [user/delete-user.md](user/delete-user.md) | ✅ |

---

## Funnel — Воронки продаж

| Use Case | Файл | Статус |
|----------|------|--------|
| Создать воронку | [funnel/create-funnel.md](funnel/create-funnel.md) | ✅ |
| Получить воронку | [funnel/get-funnel.md](funnel/get-funnel.md) | ✅ |
| Список воронок | [funnel/list-funnel.md](funnel/list-funnel.md) | ✅ |
| Переименовать воронку | [funnel/update-funnel.md](funnel/update-funnel.md) | ✅ |
| Удалить воронку | [funnel/delete-funnel.md](funnel/delete-funnel.md) | ✅ |

---

## FunnelStage — Этапы воронки

| Use Case | Файл | Статус |
|----------|------|--------|
| Создать этап | [funnel-stage/create-funnel-stage.md](funnel-stage/create-funnel-stage.md) | ✅ |
| Получить этап | [funnel-stage/get-funnel-stage.md](funnel-stage/get-funnel-stage.md) | ✅ |
| Список этапов | [funnel-stage/list-funnel-stage.md](funnel-stage/list-funnel-stage.md) | ✅ |
| Обновить этап | [funnel-stage/update-funnel-stage.md](funnel-stage/update-funnel-stage.md) | ✅ |
| Удалить этап | [funnel-stage/delete-funnel-stage.md](funnel-stage/delete-funnel-stage.md) | ✅ |
| Переместить этап (drag-drop) | [funnel-stage/move-funnel-stage.md](funnel-stage/move-funnel-stage.md) | ✅ |

---

## Source — Источники лидов

| Use Case | Файл | Статус |
|----------|------|--------|
| Создать источник | [source/create-source.md](source/create-source.md) | ✅ |
| Получить источник | [source/get-source.md](source/get-source.md) | ✅ |
| Список источников | [source/list-source.md](source/list-source.md) | ✅ |
| Обновить источник | [source/update-source.md](source/update-source.md) | ✅ |
| Удалить источник | [source/delete-source.md](source/delete-source.md) | ✅ |
| Активировать источник | [source/activate-source.md](source/activate-source.md) | ✅ |
| Деактивировать источник | [source/deactivate-source.md](source/deactivate-source.md) | ✅ |
| Перегенерировать webhook-токен | [source/regenerate-webhook-secret.md](source/regenerate-webhook-secret.md) | ✅ |

---

## LeadCustomField — Кастомные поля лида

| Use Case | Файл | Статус |
|----------|------|--------|
| Создать поле | [lead-custom-field/create-custom-field.md](lead-custom-field/create-custom-field.md) | ✅ |
| Получить поле | [lead-custom-field/get-custom-field.md](lead-custom-field/get-custom-field.md) | ✅ |
| Список полей | [lead-custom-field/list-custom-field.md](lead-custom-field/list-custom-field.md) | ✅ |
| Переименовать поле | [lead-custom-field/update-custom-field.md](lead-custom-field/update-custom-field.md) | ✅ |
| Удалить поле (soft) | [lead-custom-field/delete-custom-field.md](lead-custom-field/delete-custom-field.md) | ✅ |
| Восстановить поле | [lead-custom-field/restore-custom-field.md](lead-custom-field/restore-custom-field.md) | ✅ |
| Добавить вариант (enum) | [lead-custom-field/add-enum-value.md](lead-custom-field/add-enum-value.md) | ✅ |
| Удалить вариант (enum) | [lead-custom-field/remove-enum-value.md](lead-custom-field/remove-enum-value.md) | ✅ |

---

## Lead — Лиды

| Use Case | Файл | Статус |
|----------|------|--------|
| Создать лид | [lead/create-lead.md](lead/create-lead.md) | ❌ |
| Получить лид | [lead/get-lead.md](lead/get-lead.md) | ❌ |
| Список лидов | [lead/list-lead.md](lead/list-lead.md) | ❌ |
| Обновить лид | [lead/update-lead.md](lead/update-lead.md) | ❌ |
| Удалить лид (soft) | [lead/delete-lead.md](lead/delete-lead.md) | ❌ |
| Архивировать лид | [lead/archive-lead.md](lead/archive-lead.md) | ❌ |
| Переместить лид в этап | [lead/move-lead-stage.md](lead/move-lead-stage.md) | ❌ |
| Назначить лид менеджеру | [lead/assign-lead.md](lead/assign-lead.md) | ❌ |
| Задать кастомное значение | [lead/set-custom-value.md](lead/set-custom-value.md) | ❌ |

---

## Task — Задачи

| Use Case | Файл | Статус |
|----------|------|--------|
| Создать задачу | [task/create-task.md](task/create-task.md) | ❌ |
| Получить задачу | [task/get-task.md](task/get-task.md) | ❌ |
| Список задач | [task/list-task.md](task/list-task.md) | ❌ |
| Обновить задачу | [task/update-task.md](task/update-task.md) | ❌ |
| Удалить задачу | [task/delete-task.md](task/delete-task.md) | ❌ |
| Завершить задачу | [task/complete-task.md](task/complete-task.md) | ❌ |

---

## LeadComment — Комментарии к лиду

| Use Case | Файл | Статус |
|----------|------|--------|
| Добавить комментарий | [lead-comment/create-comment.md](lead-comment/create-comment.md) | ❌ |
| Список комментариев | [lead-comment/list-comments.md](lead-comment/list-comments.md) | ❌ |
| Редактировать комментарий | [lead-comment/update-comment.md](lead-comment/update-comment.md) | ❌ |
| Удалить комментарий | [lead-comment/delete-comment.md](lead-comment/delete-comment.md) | ❌ |

---

## LeadTimelineEvent — Лента событий

| Use Case | Файл | Статус |
|----------|------|--------|
| Список событий лида | [lead-timeline-event/list-events.md](lead-timeline-event/list-events.md) | ❌ |
| Добавить заметку вручную | [lead-timeline-event/add-manual-note.md](lead-timeline-event/add-manual-note.md) | ❌ |

---

## Notification — Уведомления

| Use Case | Файл | Статус |
|----------|------|--------|
| Список уведомлений | [notification/list-notifications.md](notification/list-notifications.md) | ❌ |
| Прочитать уведомление | [notification/mark-read.md](notification/mark-read.md) | ❌ |
| Прочитать все уведомления | [notification/mark-all-read.md](notification/mark-all-read.md) | ❌ |
