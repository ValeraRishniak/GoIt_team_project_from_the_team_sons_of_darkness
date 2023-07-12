from .bf.adress_book import main as ab_main
from .bf.sort import main as sort_main
from .bf.note_book import main as nb_main


def main():
    while True:
        print('Оберіть функцію, яку ви хочете запустити:',
              '1. Книга контактів.',
              '2. Нотатник.',
              '3. Сортувальник теки.',
              '0. Завершити роботу.', sep='\n')
        user_command = input('Оберіть меню: ')
        if user_command == '1':
            print('-'*25, 'Книга контактів', '-'*25, sep='')
            run = ab_main()
            

        elif user_command == '2':
            print('-'*25, 'Нотатник', '-'*25, sep='')
            run = nb_main()
            

        elif user_command == '3':
            print('-'*25, 'Сортувальник теки', '-'*25, sep='')
            run = sort_main()
            

        elif user_command == '0':
            print('До нових зустрічей!')
            break


if __name__ == '__main__':
    main()