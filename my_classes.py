from collections import UserDict
from datetime import datetime
import re


class NumberPhoneError(Exception):
    pass


class BirthdayError(Exception):
    pass


class EmailError(Exception):
    pass


class AddressError(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value
        self.__private_value = None


class Name(Field):

    @property
    def value(self):
        return self.__private_value

    @value.setter
    def value(self, new_value):
        if new_value != '':
            self.__private_value = new_value
        else:
            raise KeyError('Enter correct user name')

    def __repr__(self):
        return f'{self.value}'


class Phone(Field):

    @property
    def value(self):
        return self.__private_value

    @value.setter
    def value(self, new_value):
        if new_value == '':
            self.__private_value = (''.join(new_value.split()))
        elif (''.join(new_value.split())).isdigit() or (new_value[0] == '+' and (''.join(new_value.split()))[1:].isdigit()):
            self.__private_value = (''.join(new_value.split()))
        else:
            raise NumberPhoneError('Enter correct number phone')

    def __repr__(self):
        return f'{self.value}'


class Birthday(Field):
    @property
    def value(self):
        return self.__private_value

    @value.setter
    def value(self, new_birthday):
        try:
            if new_birthday == '':
                self.__private_value = new_birthday
            elif datetime.strptime(new_birthday, '%d-%m-%Y'):
                self.__private_value = new_birthday
        except Exception:
            raise BirthdayError

    def __repr__(self):
        return f'{self.value}'

class Email(Field):
    def __init__(self, email=''):
        self.__private_value = None
        self.value = email

    @property
    def value(self):
        return self.__private_value

    @value.setter
    def value(self, new_email):
        try:
            if new_email == '':
                self.__private_value = new_email
            else:
                mail = bool(
                    re.search(r"[a-zA-Z]+[\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}", new_email))
                if mail:
                    self.__private_value = new_email
                else:
                    raise EmailError('Enter correct email')
        except Exception:
            raise EmailError('Enter correct email')

    def __repr__(self):
        return f'{self.value}'


class Address(Field):
    def __init__(self, address=''):
        self.__private_value = None
        self.value = address

    @property
    def address(self):
        return self.__private_value

    @address.setter
    def address(self, new_address):
        try:
            if new_address == '':
                self.__private_value = new_address
            else:
                adr = bool(
                    re.search(r'^[A-Za-z0-9\s.,-]+ \d+[A-Za-z]* [A-Za-z\s]+$', new_address))
                if adr:
                    self.__private_value = new_address
                else:
                    raise AddressError('Enter correct adress')
        except ValueError:
            raise AddressError('Enter correct address')

    def __repr__(self):
        return f'{self.value}'

class AddressBook:
    def __init__(self, **kwargs):
        self.data = {}

        for key, value in kwargs.items():
            if key == 'name':
                self.data['name'] = Name(value)
            elif key == 'phones':
                self.data['phones'] = []
                for phone in value:
                    self.data['phones'].append(Phone(str(phone)))
            elif key == 'birthday':
                self.data['birthday'] = Birthday(value)
            elif key == 'email':
                self.data['email'] = Email(value)
            elif key == 'address':
                self.data['address'] = Address(value)

    def __repr__(self):
        return f'{self.data["name"]}, {self.data["birthday"]}'

    def add_phone(self, phone):
        if phone != '':
            self.data['phones'].append(Phone(str(phone)))
        return self.data['phones']

    def delete_phone(self, phone: Phone):
        for p in self.data['phones']:
            if str(p) == phone:
                self.data['phones'].remove(p)

    def edit_phone(self, **kwargs):
        for p in self.data['phones']:
            if str(p) == kwargs['old_phone']:
                self.data['phones'][self.data['phones'].index(p)] = Phone(kwargs['new_phone'])

        return self.data['phones']

    def add_birthday(self, birthday):
        self.data['birthday'] = Birthday(birthday)
        return self.data['birthday']

    def add_email(self, email):
        self.data['email'] = Email(email)
        return self.data['email']

    def add_address(self, address):
        self.data['address'] = Address(address)
        return self.data['address']

    def days_to_birthday(self):
        if self.data['birthday']:
            current_date = datetime.now()
            data_birthday = datetime.strptime(str(self.data['birthday']), '%d-%m-%Y')
            current_data_birthday = data_birthday.replace(
                year=current_date.year)
            if current_data_birthday < current_date:
                next_birthday = data_birthday.replace(
                    year=(current_date.year + 1))
                result = next_birthday - current_date
            else:
                result = current_data_birthday - current_date

            return result.days

    def edit(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'name':
                self.data[key] = Name(value)
                return self.data[key]
            elif key == 'phones':
                if key in self.data.keys():
                    for phone in value:
                        self.data[key].append(Phone(str(phone)))
                else:
                    self.data[key] = []
                    for phone in value:
                        self.data[key].append(Phone(str(phone)))
                return self.data[key]
            elif key == 'birthday':
                self.data[key] = Birthday(value)
                return self.data[key]
            elif key == 'email':
                self.data[key] = Email(value)
                return self.data[key]
            elif key == 'address':
                self.data[key] = Address(value)
                return self.data[key]

    def get_contact(self):
        return self.data
