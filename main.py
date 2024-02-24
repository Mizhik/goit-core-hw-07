import sys
from collections import UserDict
from decorator import input_error

from datetime import datetime as dtdt, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        if not self.is_valid():
            raise ValueError("Invalid name format. Name must not be empty.")
    
    def is_valid(self):
        return self.value.strip()
    
class Phone(Field):
    def __init__(self, phone):
        super().__init__(phone)
        if not self.is_valid():
            raise ValueError("Invalid phone format. Phone must be 10 digits.")
    
    def is_valid(self):
        return len(self.value) == 10 and self.value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = dtdt.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Phone not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    @input_error
    def add_birthday(self, args, book):
        name, bdate = args
        birthday = Birthday(bdate)

        if not self.birthday:
            self.birthday = birthday
            return "Birthday added."
        else:
            return "Already have"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if not self.data.pop(name, None):
            raise NameError("Contact not found")
    
    @input_error
    def get_upcoming_birthdays(self):
        tdate = dtdt.today().date()
        birthdays = []

        for record in self.values():
            bdate = record.birthday
            if bdate:
                bdate_this_year = bdate.value.replace(year=tdate.year)
                days_between = (bdate_this_year - tdate).days

                if 0 <= days_between <= 7:
                    birthdays.append({'name': record.name.value, 'birthday': bdate_this_year.strftime("%d.%m.%Y")})
        return birthdays

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone = args
    if name not in book:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."
    else:
        return "Already have"

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record
    return "Not found"

@input_error
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, phone)
        return "Contact changed."
    return "Not found"

@input_error
def all_contact(book):
    if book:
        result =""
        for record in book.values():
            result += f"{str(record)}\n"
        return result.strip()
    else:
        return "Not found"

@input_error
def add_birthday(args, book):
    name, bdate = args
    record = book.find(name)
    if record:
        return record.add_birthday([name, bdate], book)
    else:
        return "Contact not found"

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value.strftime("%d.%m.%Y")
    return "Not found"

def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    result = ""
    if upcoming_birthdays:
        for birthday_info in upcoming_birthdays:
            result += f"{birthday_info['name']}'s birthday is on {birthday_info['birthday']}\n"
        return result.strip()
    else:
        return "No upcoming birthdays."

    
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(all_contact(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()