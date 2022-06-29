import os

import functional
from dotenv import load_dotenv

def main():
    while True:
        print('0. Выйти')
        print('1. Создать предмет')
        print('2. Вывести данные')
        print('3. Вывести дерево рецептов')
        key = input("Ваш выбор: ")
        match key:
            case '0':
                print('Выход')
                functional.log(f'\n\n{"-"*20} Выход из программы {functional.current_date_seconds} {"-"*20} \n\n')
                break
            case '1':
                functional.create_item()
            case '2':
                functional.print_all_items()
            case default:
                print('Неизвестная команда')
                

if __name__ == '__main__':
    
    functional.log(f'\n\n{"-"*20} Программа запущена {functional.current_date_seconds} {"-"*20} \n\n')
    try:
        main()
    except Exception as e:
        functional.log(f'Вылет: {e}', 'crash')
        functional.log(f'\n\n{"-"*20} Выход из программы {functional.current_date_seconds} {"-"*20} \n\n')