from collections import UserDict
from datetime import datetime
import pickle
import re


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value
    
    #перевірка на коректний номер телефону
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        new_value = (
            value.removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if len(new_value) <= 12 and new_value.isdigit():
            self.__value = new_value
        else:
            print("Будь-ласка перевірте введений номер телефону. Він повинен містити тільки цифри.")


class Birthday(Field):
    #перевірка на коректну дату дня народження
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        try:
            date_birthday = datetime.strptime(value, '%d.%m.%Y')
            self.__value = date_birthday.date()
        except ValueError:
            print("Будь-ласка, введіть день народження у форматі ДД.MM.РРРР")


class Address(Field):
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value


class Email(Field):
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$", value):
            print(f'E-mail не відповідає формату. Будь-ласка спробуйте ще у форматі my.email@user.ua!')
        self._value = value


class Record:
    def __init__(self, name : Name, phones = [], birthday = None, adress = None, email = None):
        self.name = name
        self.phone_list = phones
        if birthday:
            self.birthday = Birthday(birthday)
        if adress:
            self.adress = Address(adress)
        if email:
            self.email = Email(email)

    # додавання номеру телефона
    def add_phone_num(self, phone): # add_phone
        self.phone_list.append(phone)

    # видалення номеру телефона
    def delete_phone_num(self, phone): # del_phone
        for seq_num, i in enumerate(self.phone_list):
            if i == phone:
                self.phone_list.pop(seq_num)

    # редагування номеру телефона
    def change_phone_num(self, old_phone, new_phone): #edit_phone
        for seq_num, i in enumerate(self.phone_list):
            if i == old_phone:
                self.phone_list[seq_num] = new_phone

    # додавання дня народження
    def add_birthday(self, birthday_data):
        self.birthday = Birthday(birthday_data)

    # днів до дня народження
    def days_to_birthday(self):
        date_now = datetime.now()
        date_birthday = datetime(year=date_now.year, month=self.month, day=self.day)
        if date_birthday.date() == date_now.date():
            return f'{self.name} день народження сьогодні!!!'
        elif date_birthday < date_now:
            days_to_birth_day = (datetime(year=date_now.year + 1, month=self.month, day=self.day) - date_now).days
            return f'{self.name} день народження буде через {days_to_birth_day} днів'
        else:
            days_to_birth_day = (date_birthday - date_now).days
            return f'{self.name} день народження буде через {days_to_birth_day+1} днів'

    # додавання адреси
    def add_address(self, address_data):
        self.address = Address(address_data)
    
    # додавання електронної пошти
    def add_email(self, email_data):
        self.email = Email(email_data)


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.ab = []

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, n=2): # параметр n - по замовчуванню 2
        index = 1
        print_block = '-' * 50 + '\n'  # блоки виводу, пагінація
        for record in self.data.values(): # ітеруємось по словнику АдресБук
            print_block += str(record) + '\n'
            if index < n: #якщо індекс меньше нашої n - то додаюмо запис в нашу строку print_block
                index += 1
            else:
                yield print_block # якщо ж індекс більше чим параметр n - то повертаємо всі записи що зібрали
                index = 1
                print_block = '-' * 50 + '\n'
        yield print_block # повертаємо що залишилось


    filename = "AddressBook.bin"
    def save_ab(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.ab, file)

    def load_ab(self, filename):
        with open(filename, 'rb') as file:
            self.ab = pickle.load(file)

address_book = AddressBook()    

def get_all_record(self):
    return self.data.values


def greeting(*args):
    address_book.load_ab("AddressBook.bin")
    return 'Вітаю! Я Ваш помічник з книгою контактів.'


def add_contact(address_book, *args):
    name = Name(args[0])
    phone = Phone(args[1])
    if name.value in address_book:
        if phone in address_book[name.value].phone_list:
            return f'Користувач {name.value} з таким номером телефону існує.'
        else:
            address_book[name.value].add_phone_num(phone)
            return f'Номер телефону {phone.value} додано до контакту {name.value}'
    else:
        address_book[name.value] = Record(name, [phone])
        return f'Додано контакт {name.value} з номером телефону {phone.value}'


def change_contact(address_book, *args):
    name = args[0]
    old_phone = args[1]
    new_phone = args[2]
    address_book[name].change_phone_num(Phone(old_phone), Phone(new_phone))
    return f'Контакту {name} змінено номер телефону з {old_phone} на {new_phone}'


def show_phone(address_book, *args):
    name = args[0]
    phone = address_book[name]
    return f'У контакту {name} такий номер телефону: {phone}'

def del_phone(address_book, *args):
    name, phone = args[0], args[1]
    address_book[name].delete_phone_num(Phone(phone))
    return f'Контакту {name} видалено номер телефону {phone}.'


def add_email(address_book, *args):
    name, email = args[0], args[1]
    address_book[name].email = Email(email)
    return f'Контакту {name} додано електронну пошту {address_book[name].email.value}.'


def add_address(address_book, *args):
    name, address = args[0], list(args[1:])
    address = " ".join(address)
    address_book[name].address = Address(address)
    return f'Контакту {name} додано адресу {address.title()}'


def add_birthday(address_book, *args):
    name, birthday = args[0], args[1]
    address_book[name].birthday = Birthday(birthday)
    return f'Контакту {name} додано дату народження {address_book[name].birthday.value}.'


def days_to_user_birthday(address_book, *args):
    name = args[0]
    if address_book[name].birthday.value is None:
        return 'User has no birthday'
    return f'{address_book[name].days_to_birthday(address_book[name].birthday)} days to user {name} birthday'


def show_birthday_N_days(address_book, *args):
    def func_days(record):
        return record.birthday.value is not None and record.days_to_birthday(record.birthday) <= days

    days = int(args[0])
    result = f'List of users with birthday in {days} days:\n'
    print_list = address_book.iterator(func_days)
    for item in print_list:
        result += f'{item}'
    return result


def exit(*args):
    address_book.save_ab("AddressBook.bin")
    print(f'Дані успішно збережено.')
    return 'До нових зустрічей!'


def find(address_book, *args):
    def func_sub(record):
        return substring.lower() in record.name.value.lower() or \
               any(substring in phone.value for phone in record.phone_list)

    substring = args[0]
    result = f'List of users with \'{substring.lower()}\' in data:\n'
    print_list = address_book.iterator(func_sub)
    for item in print_list:
        result += f'{item}'
    return result

def del_user(address_book, *args):
    name = args[0]
    yes_no = input(f'Ви впевнені що хочете видалити контакт {name}? (y/n) ')
    if yes_no == 'y':
        del address_book[name]
        return f'Контакт {name} успішно видалено.'
    else:
        return 'Контакт не видалявся.'



def info(*args):
    return """
    "help", "?"                       --> Інформація щодо моїх можливостей
    "close", "exit", ".", "0"         --> Вихід з книги контактів
    "add" name phone                  --> Додати користувача у книгу контактів
    "change" name old_phone new_phone --> Змінити номер телефону контакту
    "birthday" name DD.MM.YYYY        --> Додати або змінити дату народження контакту
    "email" name email                --> Додати або змінити email
    "address" name address            --> Додати або змінити адресу контакту
    "del" name phone                  --> Видалити номер телефону контакту
    "delete" name                     --> Видалити контакт
    "show" name                       --> Відобразити телефон за ім'ям
    "show all"                        --> Відобразити всі контакти
    "find" sub                        --> Відобразити дані контакта
    "days to birthday" name           --> Відобразити кількість днів до дня народження контакту
    "users birthday N"                --> Відобразити контакти у яких день народження черех N днів
    """


def unknown_command(*args):
    return 'Невідома команда! Повторіть Ваш запит!'


COMMANDS = {greeting: ['hello'],
            add_contact: ['add '],
            change_contact: ['change '],
            show_phone: ['show '],
            del_phone: ['del '],
            get_all_record: ['all'],
            # show_all: ['all'],
            add_email: ['email'],
            add_address: ['address'],
            add_birthday: ['birthday'],
            days_to_user_birthday: ['days to birthday'],
            show_birthday_N_days: ['users birthday'],
            exit: ['good', 'bye', 'close', 'exit', '.', '0'],
            find: ['find'],
            del_user: ['delete'],
            info: ['help', '?']
            }


def command_parser(user_command: str):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []

# Основна функція
def main():
    print('Вітаю! Я Ваш помічник з книгою контактів.')
    while True:
        user_command = input('Що мені зробити? ')
        command, data = command_parser(user_command)
        print(command(address_book, *data))
        if command is exit:
            break





# Запуск бота-помічника
if __name__ == "__main__":
    main()