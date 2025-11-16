"""Handlers for user commands."""

from src.models.address_book import AddressBook, Record
from src.models.messages import Message, ErrorMessage, SuccessMessage, TableMessage
from src.utils import input_error


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
    return SuccessMessage(message)


@input_error('Contact')
def handle_change_contact_name(book: AddressBook, old_name: str, new_name: str):
    """
    Changes an existing contact's name.

    Args:
        book (AddressBook): The address book.
        old_name (str): The old contact name.
        new_name (str): The new contact name.

    Returns:
        str: The result message.
    """
    book.rename_record(old_name, new_name)

    return SuccessMessage("Contact updated")


@input_error('Contact')
def handle_change_contact_phone(book: AddressBook, name: str, old_phone: str, new_phone: str):
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
    return SuccessMessage("Contact updated")


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
    return Message(f"{name}: {', '.join(phone.value for phone in record.phones)}")  # type: ignore


@input_error('Contact')
def handle_all(book: AddressBook) -> Message:
    """
    Lists all contacts.

    Args:
        book (AddressBook): The address book.

    Returns:
        str: The list of contacts or message if none.
    """
    if not book.data:
        return Message("Address book is empty.")

    return TableMessage(book.to_list_of_dict())


@input_error('Contact')
def handle_search(book: AddressBook, query: str) -> Message:
    """
    Searches for contacts matching the query.

    Args:
        book (AddressBook): The address book.
        query (str): The search query.

    Returns:
        str: The search results or message if none.
    """
    records = book.search(query)

    if records:
        return TableMessage([record.to_dict() for record in records])
    return ErrorMessage(f'No contact found for "{query}"')


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
        return ErrorMessage("Contact not found")

    if record.birthday:
        return ErrorMessage("Birthday already set")

    record.add_birthday(birthday)
    return SuccessMessage("Birthday added")


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
        return ErrorMessage("Contact not found")

    if record.birthday is None:
        return ErrorMessage("Birthday not set")

    return Message(f"{name}'s birthday is {record.birthday}.")  # type: ignore


@input_error('Contact')
def handle_upcoming_birthdays(book: AddressBook, days: str = '7'):
    """
    Shows contacts with upcoming birthdays.

    Args:
        book (AddressBook): The address book.
        days (str): Number of days to look ahead for birthdays.

    Returns:
        str: The list of upcoming birthdays or message if none.
    """
    upcoming = book.get_upcoming_birthdays(days_ahead=int(days))
    if not upcoming:
        return ErrorMessage("No upcoming birthdays")

    return TableMessage(upcoming)


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
        return 'Birthday updated'
    return 'Contact not found'


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
        return 'Email updated'
    return 'Contact not found'


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
        return 'Address updated'
    return 'Contact not found'


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
        return 'Contact deleted'
    return 'Contact not found'


@input_error('Contact')
def handle_add_phone(book: AddressBook, name: str, phone: str):
    """
    Adds a phone to an existing contact.

    Args:
        book (AddressBook)
        name (str): contact name
        phone (str): phone to add

    Returns:
        str: result message
    """
    record = book.find(name)
    if record is None:
        return ErrorMessage("Contact not found")

    record.add_phone(phone)
    return SuccessMessage("Phone added")


@input_error('Contact')
def handle_remove_phone(book: AddressBook, name: str, phone: str):
    """
    Removes a phone from an existing contact.

    Args:
        book (AddressBook)
        name (str)
        phone (str)

    Returns:
        str
    """
    record = book.find(name)
    if record is None:
        return ErrorMessage("Contact not found")

    try:
        record.remove_phone(phone)
        return SuccessMessage("Phone removed")
    except KeyError:
        return ErrorMessage("Phone number not found")


commands: dict = {
    'add-contact': handle_add_contact,
    'change-name': handle_change_contact_name,
    'change-phone': handle_change_contact_phone,
    'show-phone': handle_phone,
    'add-phone': handle_add_phone,
    'remove-phone': handle_remove_phone,
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
