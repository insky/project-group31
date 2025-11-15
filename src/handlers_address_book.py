"""Handlers for user commands."""

from address_book import AddressBook, Record
from utils import input_error
from output import simple_messege


@input_error('Contact')
def handle_add_contact(book: AddressBook, name: str, phone: str | None, email: str | None = None):
    """
    Adds a new contact or update existing contact's phone number.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        phone (str | None): The phone number.
        email (str | None): The email address.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    message = "Contact updated"

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
    if phone:
        record.add_phone(phone)
    if email:
        record.add_email(email)
    simple_messege(message)


@input_error('Contact')
def handle_change_contact(book: AddressBook, name: str, old_phone: str, new_phone: str):
    """
    Changes an existing contact's phone number.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        old_phone (str): The old phone number.
        new_phone (str): The new phone number.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)  # type: ignore
    simple_messege("Contact updated")


@input_error('Contact')
def handle_phone(book: AddressBook, name: str):
    """
    Gets the phone numbers of a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.

    Returns:
        str: The phone numbers or error message.
    """
    record = book.find(name)
    line =  f"{name}: {', '.join(phone.value for phone in record.phones)}"  # type: ignore
    simple_messege(line)


@input_error('Contact')
def handle_all(book: AddressBook):
    """
    Lists all contacts.

    Args:
        book (AddressBook): The address book.

    Returns:
        str: The list of contacts or message if none.
    """
    return str(book)


@input_error('Contact')
def handle_search(book: AddressBook, query: str) -> str:
    """
    Searches for contacts matching the query.

    Args:
        book (AddressBook): The address book.
        query (str): The search query.

    Returns:
        str: The search results or message if none.
    """
    records = book.search(query)

    output = []
    if records:
        for record in records:
            output.append(str(record))
        return '\n- '.join(output)
    line=  f'No contact found for "{query}"'
    simple_messege(line)


@input_error('Contact')
def handle_add_birthday(book: AddressBook, name: str, birthday: str):
    """
    Adds a birthday for a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        birthday (str): The birthday in DD.MM.YYYY format.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record is None:
        simple_messege("Contact not found")

    if record.birthday:
        simple_messege("Birthday already set")

    record.add_birthday(birthday)
    simple_messege("Birthday added")


@input_error('Contact')
def handle_show_birthday(book: AddressBook, name: str):
    """
    Shows the birthday of a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.

    Returns:
        str: The birthday or error message.
    """
    record = book.find(name)
    if record is None:
        simple_messege("Contact not found")

    if record.birthday is None:
        simple_messege("Birthday not set")

    line =  f"{name}'s birthday is {record.birthday}."  # type: ignore
    simple_messege(line)


@input_error('Contact')
def handle_upcoming_birthdays(book: AddressBook):
    """
    Shows contacts with upcoming birthdays.

    Args:
        book (AddressBook): The address book.

    Returns:
        str: The list of upcoming birthdays or message if none.
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        simple_messege("No upcoming birthdays")

    result = []
    for item in upcoming:
        result.append(f"{item['name']}: {item['congratulation_day'].strftime('%d.%m.%Y')}")
    return "\n".join(result)


@input_error('Contact')
def handle_update_birthday(book: AddressBook, name: str, birthday: str):
    """
    Updates the birthday for a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        birthday (str): The new birthday in DD.MM.YYYY format.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        simple_messege('Birthday updated')
    simple_messege('Contact not found')


@input_error('Contact')
def handle_update_email(book: AddressBook, name: str, email: str):
    """
    Updates the email for a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        email (str): The new email address.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record:
        record.add_email(email)
        simple_messege('Email updated')
    simple_messege('Contact not found')


@input_error('Contact')
def handle_update_address(book: AddressBook, name: str, address: str):
    """
    Updates the address for a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        address (str): The new address.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record:
        record.add_address(address)
        simple_messege('Address updated')
    simple_messege('Contact not found')


@input_error('Contact')
def handle_delete(book: AddressBook, name: str):
    """
    Deletes a contact by name.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record:
        book.delete(name)
        simple_messege('Contact deleted')
    simple_messege('Contact not found')


commands: dict = {
    'add-contact': handle_add_contact,
    'change-contact': handle_change_contact,
    'show-phone': handle_phone,
    'all-contacts': handle_all,
    'add-birthday': handle_add_birthday,
    'show-birthday': handle_show_birthday,
    'update-birthday': handle_update_birthday,
    'birthdays': handle_upcoming_birthdays,
    'search-contact': handle_search,
    'delete-contact': handle_delete,
    'update-email': handle_update_email,
    'update-address': handle_update_address,
}
