# UseCase: UpdateFunnelStage — Обновить этап воронки

## Что решает

Изменяет свойства существующего этапа воронки: название, вероятность выигрыша и цвет. Порядок этапа (`order`) через этот use case не меняется — для перемещения используется `MoveFunnelStage`.

**Файл:** `backend/src/backend/application/funnel/use_cases/update_funnel_stage.py`

**Статус:** ✅ Реализовано

---

## Участники

| Поле | Значение |
|------|----------|
| **Actor** | Менеджер или выше |
| **Роли** | `sales_manager`, `director`, `admin` |

---

## Входные данные (`UpdateFunnelStageCommand`)

| Поле | Тип | Описание |
|------|-----|----------|
| `name` | `str` | Новое название этапа |
| `win_probability` | `int` | Новая вероятность выигрыша 0–100 (%) |
| `hex` | `str` | Новый цвет `#RRGGBB` |

Воронка и этап передаются как атрибуты use case (`self.funnel`, `self.stage`).

---

## Порядок действий

```
1. Проверить права актора через CanCreateFunnelPolicy
   │  (используется та же политика, что и при создании)
   │  Правило: роль должна быть sales_manager и выше
   └─ Если нет прав → ошибка PermissionError (до открытия UoW)

2. Открыть Unit of Work

3. Вызвать stage.change(name=cmd.name, win_probability=cmd.win_probability, hex=cmd.hex)
   └─ Валидация через Value Objects:
      - Name: не пустое, max 255 символов
      - Probability: 0–100
      - HexCode: #RRGGBB

4. Сохранить этап в БД через uow.stages.update_stage(self.stage)

5. Зафиксировать транзакцию (commit)
```

---

## Возможные ошибки

| Ошибка | Условие |
|--------|---------|
| `PermissionError` | Роль актора — `consultant` |
| `ValueError` (VO) | Некорректное название, вероятность или цвет |

---

## Результат

`None` — успешное выполнение без возвращаемого значения.

---

## Бизнес-правила

- `kind` (тип этапа: initial/intermediate/won/lost) через этот use case **не меняется**
- `order` через этот use case **не меняется** — только через `MoveFunnelStage`
