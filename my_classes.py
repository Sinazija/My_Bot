from datetime import datetime
import re
from abc import ABC, ABCMeta, abstractmethod


class BaseField:
    def __init__(self, value):
        self.value = value
        self.__private_value = None


class Name(BaseField):

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


class Phone(BaseField):

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


class Birthday(BaseField):
    @property
    def value(self):
        return self.__private_value

    @value.setter
    def value(self, new_birthday):
        if new_birthday == '':
            self.__private_value = new_birthday
        else:
            self.validate_date(new_birthday)

    def validate_date(self, date_string):
        try:
            datetime.strptime(date_string, '%d-%m-%Y')
            self.__private_value = date_string
        except ValueError:
            raise BirthdayError('Enter correct birthday date')

    def __repr__(self):
        return f'{self.value}'


class Email(BaseField):
    def __init__(self, email=''):
        self.__private_value = None
        self.value = email

    @property
    def value(self):
        return self.__private_value

    @value.setter
    def value(self, new_email):
        if new_email == '':
            self.__private_value = new_email
        else:
            self.validate_email(new_email)

    def validate_email(self, email):
        mail = bool(
            re.search(r"[a-zA-Z]+[\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}", email))
        if not mail:
            raise EmailError('Enter correct email')
        self.__private_value = email

    def __repr__(self):
        return f'{self.value}'


class Address(BaseField):
    def __init__(self, address=''):
        self.__private_value = None
        self.value = address

    @property
    def address(self):
        return self.__private_value

    @address.setter
    def address(self, new_address):
        if new_address == '':
            self.__private_value = new_address
        else:
            self.validate_address(new_address)

    def validate_address(self, address):
        adr = bool(
            re.search(r'^[A-Za-z0-9\s.,-]+ \d+[A-Za-z]* [A-Za-z\s]+$', address))
        if not adr:
            raise AddressError('Enter correct address')
        self.__private_value = address

    def __repr__(self):
        return f'{self.value}'


class AbstractContact(ABC):
    @abstractmethod
    def add_phone(self):
        pass

    @abstractmethod
    def delete_phone(self):
        pass

    @abstractmethod
    def edit_phone(self):
        pass

    @abstractmethod
    def get_contact(self):
        pass

    @abstractmethod
    def add_birthday(self):
        pass

    @abstractmethod
    def add_address(self):
        pass

    @abstractmethod
    def add_email(self):
        pass


class NumberPhoneError(Exception):
    pass


class BirthdayError(Exception):
    pass


class EmailError(Exception):
    pass


class AddressError(Exception):
    pass


class AddressBook(AbstractContact):
    def __init__(self, **kwargs):
        self.data = {
            'name': Name(kwargs.get('name')),
            'phones': [Phone(str(phone)) for phone in kwargs.get('phones', [])],
            'birthday': Birthday(kwargs.get('birthday')),
            'email': Email(kwargs.get('email')),
            'address': Address(kwargs.get('address'))
        }

    def __repr__(self):
        return f'{self.data["name"]}, {self.data["birthday"]}'

    def add_phone(self, phone):
        if phone:
            self.data['phones'].append(Phone(str(phone)))
        return self.data['phones']

    def delete_phone(self, phone: Phone):
        for p in self.data['phones']:
            if str(p) == phone:
                self.data['phones'].remove(p)

    def edit_phone(self, **kwargs):
        for p in self.data['phones']:
            if str(p) == kwargs['old_phone']:
                self.data['phones'][self.data['phones'].index(
                    p)] = Phone(kwargs['new_phone'])

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
        if 'birthday' in self.data:
            current_date = datetime.now()
            data_birthday = datetime.strptime(
                str(self.data['birthday']), '%d-%m-%Y')
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
                    self.data[key] = [Phone(str(phone)) for phone in value]
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
