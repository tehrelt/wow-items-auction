import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv('DB_PATH')

current_date = datetime.now().strftime("%d_%m_%Y")
current_date_seconds = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")


def log(message, level='special'):
    with open(f'logs/{current_date}.log', 'a', encoding='utf-8') as f:
        match level:
            case 'info':
                f.write(f'[ИНФО] {message}')
            case 'error':
                f.write(f'[ОШИБКА] {message}')
            case 'warning':
                f.write(f'[ПРЕД] {message}')
            case 'crash':
                f.write(f'[ВЫЛЕТ] {message}')
            case default:
                f.write(message)
        f.write('\n')

class item(object):
    title: str
    price: str
    recipe: dict

    def __init__(self, title: str, price: int, recipe: dict):
        self.title = title
        self.price = price
        self.recipe = recipe

    def set_price(self, price):
        self.price = price

    def to_dict(self):
        return {
            'title': self.title,
            'price': self.price,
            'recipe': self.recipe
        }


def create_item():
    print('Создание предмета')
    log('Создание предмета', 'info')
    is_item_exists = False
    item_list = []
    log(f'Открытие на чтение файл: {DB_PATH}', 'info')
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as j:
            log(f'Выгрузка списка предметов из файла: {DB_PATH}', 'info')
            item_list = json.load(j)
    except Exception as e:
            log('Ошибка чтения файла: ' + str(e), 'error')
        
    while True:
        title = input('Название: ')
        
        for i, ifl in enumerate(item_list):
            log(f'Предмет #{i}: {ifl}', 'info')
            
            if title == ifl['title']:
                log(f'{title} совпадает с {ifl["title"]}#{i}', 'warning')
                print('Предмет уже существует. Попробуйте другое название!')
                is_item_exists = True
                break
            else:
                log(f'{title} не совпадает {ifl["title"]}#{i}', 'info')                
        
        
        if not is_item_exists:
            is_item_exists = False
            break
        
        is_item_exists = False
        
    price = input('Цена: ')
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as j:
            recipe = create_recipe(json.load(j))
    except Exception as e:
        log(f'Ошибка чтения файла: {DB_PATH}', 'error')
        print(f'Вы не создали ни одного предмета. Предмет создан без рецепта. Вы можете изменить его позже.')
        recipe = None
            
    created_item = item(title, price, recipe)
    item_list.append(created_item.to_dict())
    print(f'Предмет {title} создан')
    log(f'Предмет создан {created_item.to_dict()}', 'info')
    
    try:
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(item_list, f, indent=4, ensure_ascii=False)
        
    except Exception as e:
        log('Ошибка записи в файл: ' + str(e), 'error')
        print(e)

def create_recipe(item_list):
    is_ingridient_not_exists = True
    ingridients_count = int(input('Количество ингридиентов: '))
    if ingridients_count > 0:
        recipe = []
        for i in range(ingridients_count):
            ingridient = {}
            while is_ingridient_not_exists:
                ingridient['title'] = input(f'Ингридиент {i+1}: ')
                for item in item_list:
                    if ingridient['title'] == item['title']:
                        is_ingridient_not_exists = False
                        log(f'{ingridient["title"]} совпадает с {item["title"]}#{i}', 'warning')
                        break
                    else:
                        log(f'{ingridient["title"]} не совпадает с {item["title"]}#{i}', 'warning')
                print("Такого предмета в базе нет. Попробуйте другое название!")
                
            ingridient['count'] = input('Количество: ')
            recipe.append(ingridient)
            
            is_ingridient_not_exists = True
                    
        is_created = True
        
    else:
        recipe = None
        is_created = True 
        
    return recipe

def print_all_items():
    print('\tВывод всех предметов\n')
    log(f'Вывод всех предметов', 'info')
    try:
        log(f'Открытие на чтение файл: {DB_PATH}', 'info')
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            log(f'Выгрузка списка предметов из файла: {DB_PATH}', 'info')
            data = json.load(f)
            for i, item in enumerate(data):
                log(f'Вывод предмета {item}#{i}', 'info')
                print(f"{'-'*10} {item['title']}#{i} {'-'*10}")
                print(f"Цена: {item['price']}")
                if item['recipe']:
                    print('Рецепт:')
                    for ingridient in item['recipe']:
                        print(f"\t{ingridient['title']} - {ingridient['count']} шт.")
                else:
                    print(f'Без рецепта')
                print('\n')
    except Exception as e:
        print('Вы не создали ни одного предмета')
        log('Ошибка открытия файла при выводе всех предметов', 'error')
