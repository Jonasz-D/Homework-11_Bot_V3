from collections import UserDict
from datetime import datetime
import re

def input_error(func):
    def inner(base_command, command, contacts):
        try:
            return func(base_command, command, contacts)
        except KeyError:
            return 'The command is not exist'
            
        except ValueError:
            return 'Phone number must consist of numbers'
        
        except IndexError:
            return 'Not given name or phone number'

    return inner


class Field:
    def __init__(self, value):
        self.value = value
    

class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

        if not self.value.isdigit():
            raise ValueError
        else:
            self.value = value

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        birthday = re.split(r'[\D]+', value)

        if len(birthday[0]) <= 2:
            birthday.reverse()
        self.birthday = datetime(year= int(birthday[0]), month= int(birthday[1]), day=int(birthday[2])).date()

class Record:
    def __init__(self, contact_name):
        self.name = Name(contact_name).value
        self.phone_num = []
        self.birthday = None

    def add_phone(self, phone):
        self.phone_num.append(Phone(phone).value)

    def remove_phone(self, phone):
        self.phone_num.remove(Phone(phone).value)

    def change_phone(self, phone, new_phone):
        self.phone_num.remove(Phone(phone).value)
        self.phone_num.append(Phone(new_phone).value)

    def set_birthday(self, birthday):
        if self.birthday == None:
            self.birthday = Birthday(birthday).birthday
        else:
            return f'You have already entered contact\'s birthday date'
        
    def days_to_birthday(self):
        if self.birthday != None:
            todays_date = datetime.today().date()
            abs_birthday_date = self.birthday.replace(year=todays_date.year)

            if abs_birthday_date < todays_date:
                abs_birthday_date = self.birthday.replace(year=todays_date.year + 1)

            days_to_birthday  = abs(todays_date - abs_birthday_date).days
            return days_to_birthday
        else:
            return f'Unknown contact\'s birthday date'
            


        

class AdressBook(UserDict):
    def add_record(self, name):
        self.data[Record(name).name] = Record(name)

    def show_all(self):
        all_contacts = ''
        for contact, phones in self.data.items():
            all_contacts += f'Name: {str(contact):<10} Phone number: {phones.phone_num}\n'

        return all_contacts
    
def hello(command, contacts):
    return 'How can I help you?'

def create_contact(command, contacts):
    name = command[1]
    if list(contacts.keys()) == []:
        return contacts.add_record(name)

    for contact in contacts.keys():
        if name == str(contact):
            return 'The contact already exists'
        
    return contacts.add_record(name)

def add_phone(command, contacts):
    name, phone = command[1], command[2]
    for contact, phones in contacts.items():
        if name == str(contact) and phone not in phones.phone_num:
            phones.add_phone(phone)
            return
      
    return "The contact doesn't exists or phone number was already added"

def change_phone_num(command, contacts):
    name, phone_num, new_phone = command[1], command[2], command[3]
    
    for contact, phones in contacts.items():
        if name == str(contact) and phone_num in phones.phone_num:
            phones.change_phone(phone_num, new_phone)
            return
    return "The contact or phone number doesn't exists"

def show_contact(command, contacts):
    name = command[1]
    for contact, phones in contacts.items():
        if name == str(contact):
            return f'contact name: {str(contact)}; phones: {phones.phone_num}'
    
    return f"contact name: {name} doesn't exists"

def delete_phone(command, contacts):
    name, phone = command[1], command[2]
    for contact, phones in contacts.items():
        if name == str(contact) and phone in (phones.phone_num):
            phones.remove_phone(phone)
            return
        
    return "The contact or phone number doesn't exists"
    
def show_all(command, contacts):
    return contacts.show_all()

def end_program(command, contacts):
    return False

def accepted_commands(command, contacts):
    commands = (list(OPERATIONS.keys()))
    message = ''
    for command in commands:
        message += f'"{command}" '
        
    return f"Accepted commands: {message}"


OPERATIONS = {
    'accepted_commands':accepted_commands,
    'hello': hello,
    'create_contact': create_contact,
    'add_phone': add_phone,
    'change_phone_num': change_phone_num,
    'show_contact': show_contact,
    'delete_phone': delete_phone,
    'show_all': show_all,
    'good_bye': end_program, 
    'close': end_program, 
    'exit': end_program, 
    '.': end_program, 
}

@input_error
def handler_command(base_command, command, contacts):
    return OPERATIONS[base_command](command, contacts)

def main():
    flag = True
    contacts = AdressBook()
    print(accepted_commands(OPERATIONS, contacts))
    while flag:
        command = input('Write your command: ').lower().strip().split()

        try:
            base_command = command[0]
        except IndexError:
            continue

        handler = handler_command(base_command, command, contacts)

        if isinstance(handler, str):
            print(handler)
        
        elif isinstance(handler, bool):
            flag = handler

        else:
            handler


# if __name__ == '__main__':
#     main()

adres = AdressBook()
record = Record('Adam')
record.set_birthday('20/5.1990')
print(record.days_to_birthday())