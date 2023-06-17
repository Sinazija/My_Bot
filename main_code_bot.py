import csv
from datetime import datetime, timedelta
from my_classes import AddressBook, Name, Phone, Birthday, Email, Address, NumberPhoneError, BirthdayError, EmailError, AddressError

# список для хранения имеющихся данных у контактов
contacts_data = []

# список  имен комманд для окончания работы бота:
finish = ['good bye', 'close', 'exit', 'help']

# файл csv для сохранение данных адресной книги на диск
file_name = 'contacts_data.csv'

field_names = ['name', 'phones', 'birthday', 'email', 'address']


# функция декоратор для функций обработчиков команд:
def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return f'There is no such name in contacts. Please, add the contact with this name first or enter correct ' \
                   f'name'
        except ValueError:
            return f'You have entered an invalid command, please refine your query'
        except IndexError:
            return f'Give me name and phone please'
        except NumberPhoneError:
            return f'This number phone is not correct, please repeat the command and enter correct number phone, ' \
                   f'or enter next command'
        except FileNotFoundError:
            return f'Please first enter and save the data'
        except BirthdayError:
            return f'Invalid birthday date. Please, put the date in format dd-mm-yyyy'
        except EmailError:
            return f'This email is not correct, please repeat the command and enter correct email, or enter next command'
        except AddressError:
            return f'This address is not format, please repeat the command and enter correct adress, or enter next ' \
                   f'command'

    return inner


# Парсер введеных команд:
def parcer(user_input):
    command, *data = user_input.strip().lower().split(' ', 1)
    if command in command_func:
        if data:
            data = data[0].split(' ', 1)
            return command_func[command], data
        else:
            return command_func[command], data
    else:
        return f'You have entered an invalid command, please refine your query'


# функция добавления контакта и его данных
@input_error
def add_data():
    new_contact = {}

    name = input('Name: ')
    phone = input(
        "Phone (add data in format '+38 number phone' or 'number phone'): ")
    birthday = input('Birthday(enter data in the format dd-mm-year): ')
    email = input('Email: ')
    address = input(
        'Address(enter data in the format "name street" "number building" "name town"): ')

    if name.title() != '':
        new_contact['name'] = Name(name.title())
    if phone != '':
        new_contact['phones'] = [Phone(phone)]
    if birthday != '':
        new_contact['birthday'] = Birthday(birthday)
    if email != '':
        new_contact['email'] = Email(email)
    if address != '':
        new_contact['address'] = Address(address)

    for key, value in new_contact.items():
        if key == 'name':
            for cont in contacts_data:
                if new_contact[key].value == cont['name'].value:
                    return f'This contact has already exist, please, try once again\nHow can I help you?Enter please command: '

            contacts_data.append(new_contact)
            return f'Contact added successfully\nHow can I help you?Enter please command: '

    raise KeyError


@input_error
def show_contacts():  # функция для показа всех контактов
    if contacts_data:
        print(50 * '-')
        for cont in contacts_data:
            for key, value in cont.items():
                print(f'{key}: {value}')
            print(50 * '-')
    else:
        print('There are no records')
    return f'How can I help you?Enter please command:  '


@input_error
def exit_program():  # функция  для окончания работы бота
    return f'Have a good mood!'


# функция  для сохранения данных в файл csv
def save_contacts(local_file_name, local_contacts_data):
    with open(local_file_name, 'w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(local_contacts_data)
    return f'Data saved successfully\nHow can I help you?Enter please command: '


# функция  для чтения  данных из  файла csv
@input_error
def read_contacts(local_file_name, data):
    with open(local_file_name, 'r', newline='', encoding='utf-8') as file_obj:
        reader = csv.DictReader(file_obj)
        for row in list(reader):
            row['phones'] = [str(x) for x in eval(row['phones'].replace(
                '[', "['").replace(', ', "','").replace(']', "']"))] if row['phones'] else []
            entity = AddressBook(**row)
            new_data = entity.get_contact()
            unique_identifier = new_data['name'].value

            if not any(contact['name'].value == unique_identifier for contact in data):
                data.append(new_data)

    print(50 * '-')
    for cont in data:
        for key, value in cont.items():
            print(f'{key}: {value}')
        print(50 * '-')
    return f'How can I help you?Enter please command: '


@input_error
# функция  для редактирования контакта
def edit_data(name):
    name = Name(name.title())

    for cont in contacts_data:
        if cont['name'].value == name.value:
            item = {}
            for key, data in cont.items():
                item[key] = map(lambda x: str(x.value), data) if type(
                    data) == list else data.value

            entity = AddressBook(**item)

            for field_name in field_names:
                if 'phones' == field_name:
                    if 'phones' in cont.keys() and len(cont['phones']):
                        print('At the moment you have several phones.\n')
                        for phone in cont['phones']:
                            print(f'{phone}\n')
                        print('Choose which one you want to change.\n')
                        print(
                            'To change, specify the data in the format "[OldPhone] [NewPhone]".\n')
                        print(
                            'if you add a new phone the data in the format "[NewPhone]".\n')
                        print(
                            'If you do not want to change the phone then just press ENTER".\n')

                        user_input_new_value = input(f'{field_name}: ')

                        if user_input_new_value:
                            data_phone = user_input_new_value.strip().lower().split(' ', 1)

                            if len(data_phone) == 2:
                                cont[field_name] = entity.edit_phone(
                                    **{'old_phone': data_phone[0], 'new_phone': data_phone[1]})
                            else:
                                cont[field_name] = entity.add_phone(
                                    data_phone[0])
                    else:
                        user_input_new_value = input(f'{field_name}: ')
                        if user_input_new_value:
                            cont[field_name] = entity.edit(
                                **{field_name: [user_input_new_value]})
                else:
                    user_input_new_value = input(f'{field_name}: ')
                    if user_input_new_value:
                        cont[field_name] = entity.edit(
                            **{field_name: user_input_new_value})

            return f'Contact {cont["name"]} edited successfully\nHow can I help you?Enter please command: '
    raise KeyError


@input_error
# функция  для удаления контакта
def remove_contact(name):
    name = Name(name.title())

    for cont in contacts_data:
        if cont['name'].value == name.value:
            contacts_data.remove(cont)

            return f'Remove contact successfully\nHow can I help you?Enter please command: '
    raise KeyError


# функция  для поиска  данных в адресной книге
def search(value_search):
    found_contacts = list(filter(lambda item: value_search.lower(
    ).strip() in item['name'].value.lower().strip(), contacts_data))

    if not found_contacts:
        return f'No data in contacts\nHow can I help you?Enter please command: '
    else:
        print(50 * '-')
        for cont in found_contacts:
            for key, value in cont.items():
                print(f'{key}: {value}')
            print(50 * '-')

        return f'How can I help you?Enter please command: '

# Конвертация дат в datetime объекты


def convert_dates(contacts_data):
    new_contacts_data = []
    for contact in contacts_data:
        birthday = str(contact['birthday'])
        day, month, year = map(int, birthday.split('-'))
        date_object = datetime(year, month, day)
        new_contact = {'name': contact['name'], 'birthday': date_object}
        new_contacts_data.append(new_contact)
    return new_contacts_data

# Функция вывода списка дней рождений через заданное число дней


def upcoming_birthdays(days):
    new_contacts_data = convert_dates(contacts_data)

    today = datetime.now().date()
    target_date = today + timedelta(days=int(days))
    upcoming_birthdays_list = [
        str(contact['name'])
        for contact in new_contacts_data
        if (contact['birthday'].month, contact['birthday'].day) == (target_date.month, target_date.day)
    ]
    if len(upcoming_birthdays_list) == 0:
        return f'There are no birthdays that day\nHow can I help you?Enter please command: '
    else:
        return f'List of birthdays: {", ".join(upcoming_birthdays_list)}\nHow can I help you?Enter please command: '


# словарь для хранения  имен функций обработчиков команд:
command_func = {'add': add_data, 'show all': show_contacts, 'exit': exit_program,
                'save': save_contacts, 'search': search,
                'read': read_contacts, 'edit': edit_data, 'remove-contact': remove_contact, 'birthday-list': upcoming_birthdays}


# функция работы бота адресной книги:
def main(user_input):
    while True:
        try:
            if user_input.lower().strip() in finish:
                user_input_parser = parcer('exit')
                command, arg = user_input_parser
                print(command(*arg))
                break
            elif user_input.lower().strip() == 'show all':
                print(show_contacts())
                user_input = input()
            else:
                user_input_parser = parcer(user_input)
                command, arg = user_input_parser
                if command == save_contacts or command == read_contacts:
                    print(command(file_name, contacts_data))
                    user_input = input()
                else:
                    print(command(*arg))
                    user_input = input()

        except (ValueError, TypeError):
            user_input = input(
                f'You have entered an invalid command, please refine your query\nHow can I help you?Enter please command: ')
