# UseCase: UpdateUser — Обновить данные пользователя

## Что решает

Позволяет администратору обновить данные любого пользователя: имя, фамилию, email, username. Содержит проверку прав через `CanUpdateUserPolicy` — запрещает понижение или смену роли в обход политики безопасности.

**Файл:** `backend/src/backend/application/user/use_cases/update_user.py`

**Статус:** ✅ Реализовано

---

## Участники

| Поле | Значение |
|------|----------|
| **Actor** | Администратор системы |
| **Роли** | `admin` |

---

## Входные данные

| Параметр | Тип | Описание |
|----------|-----|----------|
| `user_id` | `UUID` | ID пользователя, которого обновляют |
| `cmd.first_name` | `str` | Новое имя |
| `cmd.last_name` | `str` | Новая фамилия |
| `cmd.email` | `str` | Новый email |
| `cmd.username` | `str` | Новый логин |

---

## Порядок действий

```
1. Открыть Unit of Work
2. Загрузить пользователя из БД по user_id
   └─ Если не найден → ошибка UserNotFoundError
3. Проверить права актора через CanUpdateUserPolicy
   │  Правило: нельзя изменять пользователей с ролью выше своей
   └─ Если нет прав → ошибка PermissionError
4. Проверить уникальность нового email
   (исключая текущего пользователя)
   └─ Если занят → ошибка EmailAlreadyExistsError
5. Проверить уникальность нового username
   (исключая текущего пользователя)
   └─ Если занят → ошибка UsernameAlreadyExistsError
6. Обновить данные сущности:
   - user.change_first_name(cmd.first_name)
   - user.change_last_name(cmd.last_name)
   - user.change_email(cmd.email)
   - user.change_username(cmd.username)
7. Сохранить изменения в БД
8. Зафиксировать транзакцию (commit)
```

---

## Возможные ошибки

| Ошибка | Условие |
|--------|---------|
| `UserNotFoundError` | Пользователь не найден |
| `PermissionError` | Актор не имеет прав на обновление (через `CanUpdateUserPolicy`) |
| `EmailAlreadyExistsError` | Новый email уже занят |
| `UsernameAlreadyExistsError` | Новый username уже занят |

---

## Результат

`None` — успешное выполнение без возвращаемого значения.

---

## Бизнес-правила

- `CanUpdateUserPolicy` защищает от **эскалации привилегий**: нельзя дать пользователю роль выше своей
- Роль и статус активности (`is_active`) через этот use case **не меняются** — для смены роли нужен отдельный use case
- Пользователь может обновить `username`, в отличие от `UpdateMe` — разграничение: самостоятельно username не меняется, только через Admin
