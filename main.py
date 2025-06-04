import asyncio
import os
import inspect
from fast_bitrix24 import Bitrix
from dotenv import load_dotenv
load_dotenv()

from orm_bitrix24.entity import _Deal, CustomField, TextCustomField, SelectCustomField, Company


# Расширяем базовый класс _Deal, добавляя пользовательские поля 
class Deal(_Deal):
    utm_source = CustomField("UTM_SOURCE")
    delivery_address = TextCustomField("UF_CRM_DELIVERY_ADDRESS")
    delivery_type223 = SelectCustomField("UF_CRM_DELIVERY_TYPE")


async def main():
    # Инициализация клиента Bitrix24
    webhook = os.environ.get("WEBHOOK")
    if not webhook:
        print("Необходимо установить переменную окружения WEBHOOK")
        return
    
    bitrix = Bitrix(webhook)
    
    # Инициализация менеджеров сущностей
    Deal.get_manager(bitrix)
    # Company.get_manager(bitrix)
    
    # Пример получения всех сделок
    deals = await Deal.objects.get_all()
    print(f"Найдено сделок: {len(deals)}")
    deal = deals[0]
    if deals:
        # Получение первой сделки для демонстрации
        deal = deals[0]

        # загружаем данные связанной компании
        await deal.company
        # загружаем данные связанного контакта
        await deal.contact
        # print()
        
        print(deal.company.title)
        print(deal.contact)
        print(f"Сделка: {deal.title} (ID: {deal.id})")
        print(f"Дата создания: {deal.created_at}")
        
        # IDE должен показывать автодополнение для доступных полей
        # Здесь "deal." должен показывать список доступных атрибутов и методов
        
        # Демонстрация доступных атрибутов и методов (в IDE будет автодополнение)
        print("Доступные атрибуты сделки:")
        print(f"- ID: {deal.id}")
        print(f"- Название: {deal.title}")
        print(f"- Сумма: {deal.opportunity}")
        print(f"- Стадия: {deal.stage_id}")
        
        # Получение связанной компании
        company_result = deal.company
    
        
        # Проверяем, является ли результат корутиной
        if inspect.iscoroutine(company_result):
            company = await company_result
        else:
            company = company_result
            
        if company:
            print(f"- Компания: {company.title}")
            company.title = "Тестовая компания"
            
            # В IDE "company." должен показывать список доступных атрибутов
        else:
            # Создание новой компании, если нет связанной
            new_company = await Company.objects.create(title="Тестовая компания")
            print(f"Создана новая компания: {new_company.title} (ID: {new_company.id})")
            
            # Связывание сделки с компанией
            deal.company_id = new_company.id
            await deal.save()
        1/0
        # Изменение значения поля
        original_title = deal.title
        deal.title = f"{original_title} (изменено)"
        await deal.save()
        print(f"Заголовок сделки изменен на: {deal.title}")
        
        # Работа с пользовательскими полями
        print(f"Адрес доставки: {deal.delivery_address}")
        deal.delivery_address = "ул. Примерная, д. 1"
        await deal.save()
        print(f"Новый адрес доставки: {deal.delivery_address}")
        
        # Работа с другими пользовательскими полями 
        print(f"UTM источник: {deal.utm_source}")
        deal.utm_source = "google"
        await deal.save()
        print(f"Новый UTM источник: {deal.utm_source}")
        
        # Добавление тега
        deal.tags.append("test_tag")
        await deal.save()
        print(f"Добавлен тег: test_tag")
        
        # Добавление примечания
        note = await deal.notes.create(text="Тестовое примечание через ORM")
        print(f"Добавлено примечание: {note}")
        print(f"- Текст примечания: {note.text}")
        print(f"- Дата создания: {note.created_at}")
        
        # Получение товаров сделки
        products = await deal.products.get_all()
        print(f"Количество товаров в сделке: {len(products)}")
        
        if products:
            # В IDE "product." должен показывать список доступных атрибутов
            product = products[0]
            print(f"- Товар ID: {product.id}")
            print(f"- Цена: {product.price}")
            print(f"- Количество: {product.quantity}")
            print(f"- Сумма: {product.price * product.quantity}")
        
        # Возврат названия к исходному
        deal.title = original_title
        await deal.save()
        print(f"Заголовок сделки возвращен к: {deal.title}")
    
    # Пример поиска по фильтру
    filtered_deals = await Deal.objects.filter(type_id="SALE")
    print(f"Найдено сделок с типом SALE: {len(filtered_deals)}")
    
    # Пример создания новой сделки с товаром
    new_deal = await Deal.objects.create(
        title="Тестовая сделка через ORM",
        opportunity=1000,
        currency_id="RUB",
        stage_id="NEW",
        delivery_address="ул. Тестовая, д. 123"  # Пользовательское поле
    )
    print(f"Создана новая сделка: {new_deal.title} (ID: {new_deal.id})")


if __name__ == "__main__":
    asyncio.run(main())

