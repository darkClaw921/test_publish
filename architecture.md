# Архитектура ORM для Bitrix24

## Описание

ORM-система для работы с сущностями Bitrix24 через API. Обеспечивает удобный объектно-ориентированный интерфейс для работы с сущностями CRM.

## Структура проекта

### Структура директорий и файлов

```
orm_bitrix24/
  ├── entity/                  # Модуль с ORM-классами
  │   ├── __init__.py          # Инициализация модуля
  │   ├── base.py              # Базовые классы для ORM
  │   ├── company.py           # Класс для работы с компаниями
  │   ├── contact.py           # Класс для работы с контактами 
  │   ├── deal.py              # Базовый класс для работы со сделками
  │   ├── deal.pyi             # Stub-файл для автодополнения в IDE
  │   └── note.py              # Класс для работы с примечаниями
  ├── tests/                   # Модуль с тестами
  │   ├── conftest.py          # Конфигурация pytest
  │   └── test_deal.py         # Тесты для сделок
  ├── main.py                  # Пример использования ORM
  └── pyproject.toml           # Конфигурация проекта
```

## Описание модулей

### entity/base.py
Базовые классы для ORM-системы:
- `Field` - Базовый класс для описания полей сущностей
- Специализированные поля (`IntegerField`, `StringField`, и др.)
- `CustomField` - Базовый класс для пользовательских полей
- `EntityManager` - Менеджер для выполнения операций над сущностями
- `RelatedManager` - Менеджер для работы со связанными сущностями
- `BaseEntity` - Базовый класс для всех сущностей

### entity/company.py
Определяет класс `Company` для работы с компаниями в Bitrix24.

### entity/contact.py
Определяет класс `Contact` для работы с контактами в Bitrix24.

### entity/deal.py
Определяет классы для работы со сделками:
- `Deal` - Основной класс для работы со сделками (экспортируется как `_Deal`)
- `DealNote` - Класс для работы с примечаниями к сделкам
- `Product` - Класс для работы с товарами сделки
- `ProductsManager` - Менеджер для работы с товарными позициями сделки

### entity/note.py
Определяет класс `Note` для работы с примечаниями.

### entity/deal.pyi
Stub-файл для IDE с аннотациями типов для автодополнения, включая:
- Типы всех полей, включая пользовательские
- Типы для связанных объектов (company, contact)
- Возвращаемые типы для методов

### tests/conftest.py
Конфигурация для pytest:
- Загрузка переменных окружения
- Проверка наличия необходимых переменных перед запуском тестов

### tests/test_deal.py
Тесты для проверки работы с сущностью "Сделка":
- Создание сделки (test_deal_create)
- Получение сделки по ID (test_deal_get)
- Обновление полей сделки (test_deal_update)
- Фильтрация сделок (test_deal_filter)
- Удаление сделки (test_deal_delete)
- Работа с пользовательскими полями (test_custom_fields)

## Принцип работы

1. Данные из API Bitrix24 преобразуются в объекты соответствующих классов
2. Доступ к полям и изменение полей осуществляется через соответствующие свойства объектов
3. Связанные объекты загружаются при обращении к ним (lazy loading)
4. Для сохранения изменений используется метод `save()`
5. Для выборки по фильтру используется метод `filter(**kwargs)`
6. Для получения всех сущностей используется метод `get_all()`
7. Для получения сущности по ID используется метод `get_by_id(id)`
8. Для удаления сущности используется метод `delete()`
9. Пользовательские поля добавляются через наследование от базового класса `_Deal`
10. Товары сделки управляются через объект `deal.products`

## Пользовательские поля

Пользовательские поля в Bitrix24 (с префиксом UF_) поддерживаются через:

1. Базовый класс `CustomField` и его специализации:
   - `TextCustomField` - для текстовых полей
   - `SelectCustomField` - для полей выбора
   - `UrlCustomField` - для URL полей

2. Добавление полей через наследование:
   ```python
   from entity import _Deal, CustomField, TextCustomField
   
   # Расширяем базовый класс _Deal, добавляя пользовательские поля
   class Deal(_Deal):
       utm_source = CustomField("UTM_SOURCE")
       delivery_address = TextCustomField("UF_CRM_DELIVERY_ADDRESS")
   ```

3. Особенности именования:
   - Если передаётся точное имя поля в Bitrix24 (начинающееся с UF_), оно используется как есть
   - В противном случае система автоматически добавляет префикс UF_ и переводит имя в верхний регистр

4. Поддержка автодополнения в IDE через stub-файлы (.pyi)

## Тестирование

### Запуск тестов

Для запуска тестов используется pytest:

```bash
pytest -xvs tests/
```

### Требования для тестов

1. Установить зависимости для тестов:
   ```bash
   pip install pytest pytest-asyncio
   ```

2. Настроить переменные окружения:
   - `WEBHOOK` - URL вебхука для доступа к API Bitrix24

### Структура тестов

Тесты построены с использованием pytest и pytest-asyncio для асинхронного тестирования.
Используются фикстуры для:
- Инициализации клиента Bitrix24
- Создания тестовых сущностей перед тестами
- Очистки тестовых данных после тестов

## Примеры использования

```python
# Определение пользовательских полей через наследование
from entity import _Deal, CustomField, TextCustomField 

class Deal(_Deal):
    utm_source = CustomField("UTM_SOURCE")
    delivery_address = TextCustomField("UF_CRM_DELIVERY_ADDRESS")

# Инициализация
bitrix = Bitrix(webhook_url)
Deal.get_manager(bitrix)
Company.get_manager(bitrix)  # Инициализация для связанных сущностей

# Получение всех сделок
deals = await Deal.objects.get_all()

# Доступ к полям
print(deal.title)

# Доступ к связанному объекту (проверка если корутина)
company_result = deal.company
if inspect.iscoroutine(company_result):
    company = await company_result
else:
    company = company_result
    
# Изменение полей
deal.title = "Новое название"
await deal.save()

# Работа с пользовательскими полями
deal.utm_source = "google"
deal.delivery_address = "ул. Примерная, д.1"
await deal.save()

# Добавление примечания
await deal.notes.create(text="Примечание")

# Работа с товарами сделки
product = deal.products.add(product_id=123, price=1000)
await deal.save()

# Получение сделки по ID
deal = await Deal.objects.get_by_id(123)

# Удаление сделки
success = await deal.delete()
if success:
    print("Сделка успешно удалена")

# Фильтрация
deals = await Deal.objects.filter(stage_id="NEW")
``` 