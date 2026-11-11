# UseCase: UpdateLead — Обновить лид

## Что решает

Обновляет данные лида: контактную информацию, приоритет, суммы сделки, комментарий. Смена воронки/этапа и назначение менеджера выполняются через отдельные use cases (`MoveLead`, `AssignLead`) для явного аудит-трейла.

**Статус:** ❌ Не реализовано (планируется — Приоритет 1)

---

## Участники

| Поле | Значение |
|------|----------|
| **Actor** | Пользователь с доступом к лиду |
| **Роли** | `consultant` (только свои), `sales_manager`, `director`, `admin` |

---

## Входные данные

| Поле | Тип | Описание |
|------|-----|----------|
| `lead_id` | `UUID` | ID лида |
| `name` | `str \| None` | Новое имя |
| `phone` | `str \| None` | Новый телефон |
| `email` | `str \| None` | Новый email |
| `priority` | `Priority \| None` | Новый приоритет |
| `amount_uzs` | `int \| None` | Новая сумма в UZS |
| `amount_usd` | `Decimal \| None` | Новая сумма в USD |
| `comment` | `str \| None` | Новый комментарий |

---

## Порядок действий

```
1. Открыть Unit of Work

2. Загрузить лид из БД
   └─ Если не найден → LeadNotFoundError

3. Проверить доступ по роли:
   - Consultant → только свои лиды
   → Если нет доступа → LeadAccessDeniedError

4. Применить изменения через доменные методы (patch-семантика):
   - lead.change_name(name) — если передано
   - lead.change_contact(phone, email) — если передано
   - lead.change_priority(priority) — если передано
   - lead.set_amounts(amount_uzs, amount_usd) — если передано
   - lead.change_comment(comment) — если передано

5. Сохранить лид в БД

6. Создать LeadTimelineEvent "lead_updated" (автоматически)

7. Зафиксировать транзакцию (commit)
```

---

## Возможные ошибки

| Ошибка | Условие |
|--------|---------|
| `LeadNotFoundError` | Лид не найден |
| `LeadAccessDeniedError` | Consultant пытается обновить чужой лид |
| `ValueError` (VO) | Некорректный формат полей |

---

## Результат

`None` — успешное выполнение.

---

## Бизнес-правила

- Смена воронки/этапа через этот use case **запрещена** — только через `MoveLead`
- Смена назначенного менеджера через этот use case **запрещена** — только через `AssignLead`
- Каждое обновление фиксируется в `LeadTimelineEvent`
