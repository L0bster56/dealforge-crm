# UseCase: GetFunnelStage — Получить этап воронки

## Что решает

Загружает конкретный этап воронки по его UUID и проверяет, что он принадлежит указанной воронке. Защищает от обращения к чужим этапам через подбор ID.

**Файл:** `backend/src/backend/application/funnel/use_cases/get_funnel_stage.py`

**Статус:** ✅ Реализовано

---

## Участники

| Поле | Значение |
|------|----------|
| **Actor** | Любой авторизованный пользователь |
| **Роли** | Все роли |

---

## Входные данные (`GetFunnelStageCommand`)

| Поле | Тип | Описание |
|------|-----|----------|
| `stage_id` | `UUID` | ID этапа |
| `funnel_id` | `UUID` | ID воронки (для проверки принадлежности) |

Воронка также передаётся как атрибут use case (`self.funnel`).

---

## Порядок действий

```
1. Открыть Unit of Work
2. Загрузить этап из БД по stage_id
   └─ Если не найден → ошибка StageNotFoundError
3. Проверить, что stage.funnel_id == self.funnel.id
   └─ Если не совпадает → ошибка StageNotFunnelError
4. Вернуть доменную сущность FunnelStage
```

---

## Возможные ошибки

| Ошибка | Условие |
|--------|---------|
| `StageNotFoundError` | Этап с указанным ID не существует |
| `StageNotFunnelError` | Этап существует, но принадлежит другой воронке |

---

## Результат

Доменная сущность `FunnelStage`:

| Поле | Тип |
|------|-----|
| `id` | `UUID` |
| `funnel_id` | `UUID` |
| `name` | `Name` |
| `win_probability` | `Probability` |
| `hex_code` | `HexCode` |
| `order` | `int` |
| `kind` | `StageKind` |
| `is_archived` | `bool` |

---

## Бизнес-правила

- Проверка принадлежности (`funnel_id == self.funnel.id`) защищает от IDOR-атаки: нельзя получить этап чужой воронки, зная только его UUID
