"""Тест для проверки работы аннотаций типов для Deal.objects.get_all()"""
import os
import asyncio
from dotenv import load_dotenv
from fast_bitrix24 import Bitrix

from entity.deal import Deal
from entity.company import Company
from entity.contact import Contact

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем webhook из переменных окружения
webhook = os.getenv("BITRIX24_WEBHOOK")

async def test_annotations():
    """
    Тест для проверки работы аннотаций типов.
    
    В этом тесте мы демонстрируем, что:
    1. IDE правильно распознает тип deal в списке deals
    2. Автодополнение для deal.title и других полей работает
    """
    # Инициализация Bitrix и менеджеров объектов
    bitrix = Bitrix(webhook)
    Deal.get_manager(bitrix)
    Company.get_manager(bitrix)
    Contact.get_manager(bitrix)
    
    # Получаем все сделки
    deals = await Deal.objects.get_all()
    print(f"Найдено сделок: {len(deals)}")
    
    if deals:
        # Должны работать подсказки IDE при обращении к deal
        deal = deals[0]
        # Проверяем доступ к различным полям и свойствам
        print(deal.company.title)
        print(f"ID: {deal.id}")
        print(f"Название: {deal.title}")
        print(f"Сумма: {deal.opportunity}")
        
        # Проверяем работу связанных объектов
        company = deal.company
        if company and not isinstance(company, tuple):  # Проверка, что это не корутина
            if hasattr(company, '__await__'):  # Если это корутина, ожидаем результат
                company = await company
            if company:
                print(f"Компания: {company.title}")
        
        # Проверяем получение примечаний
        notes = await deal.notes.filter()
        print(f"Количество примечаний: {len(notes)}")
        
        # Проверяем работу с продуктами
        products = await deal.products.get_all()
        print(f"Количество продуктов: {len(products)}")

if __name__ == "__main__":
    asyncio.run(test_annotations()) 