"""Utility script to populate demo contacts and notes."""

from __future__ import annotations

from typing import Iterable, Sequence

from src.models.address_book import AddressBook, Record
from src.models.note_book import NoteBook, Note

CONTACTS_DATA: list[dict[str, Sequence[str] | str]] = [
    {
        "name": "Alice Johnson",
        "phones": ["5551230001"],
        "birthday": "14.02.1990",
        "email": "alice.johnson@example.com",
        "address": "123 Maple Street, Springfield",
    },
    {
        "name": "Brian Cooper",
        "phones": ["5551230002", "5551231002"],
        "birthday": "03.05.1985",
        "email": "brian.cooper@example.com",
        "address": "742 Evergreen Terrace, Shelbyville",
    },
    {
        "name": "Carla Mendes",
        "phones": ["5551230003"],
        "birthday": "27.11.1992",
        "email": "carla.mendes@example.com",
        "address": "8 Harbor Road, Lakeside",
    },
    {
        "name": "Bill Gates",
        "phones": ["5551230004"],
        "birthday": "09.01.1988",
        "email": "bill.gates@example.com",
        "address": "55 Microsoft Way, Redmond",
    },
    {
        "name": "Elena Rossi",
        "phones": ["5551230005"],
        "birthday": "18.07.1995",
        "email": "elena.rossi@example.com",
        "address": "21 Via Roma, Milan",
    },
    {
        "name": "Franklin Hayes",
        "phones": ["5551230006"],
        "birthday": "30.09.1980",
        "email": "frank.hayes@example.com",
        "address": "902 Market Street, Denver",
    },
    {
        "name": "Grace Lin",
        "phones": ["5551230007", "5551231007"],
        "birthday": "12.12.1993",
        "email": "grace.lin@example.com",
        "address": "400 Pacific Ave, San Francisco",
    },
    {
        "name": "Hiro Tanaka",
        "phones": ["5551230008"],
        "birthday": "04.04.1989",
        "email": "hiro.tanaka@example.com",
        "address": "3-2-1 Sakura Street, Tokyo",
    },
    {
        "name": "Isabella Duarte",
        "phones": ["5551230009"],
        "birthday": "22.08.1991",
        "email": "isabella.duarte@example.com",
        "address": "65 Avenida Paulista, Sao Paulo",
    },
    {
        "name": "Jamal Nasser",
        "phones": ["5551230010"],
        "birthday": "16.03.1987",
        "email": "jamal.nasser@example.com",
        "address": "77 Corniche Road, Abu Dhabi",
    },
]

NOTES_DATA: list[dict[str, Sequence[str] | str]] = [
    {
        "text": "Plan sprint backlog grooming agenda",
        "tags": ["planning", "agile", "team"],
    },
    {
        "text": "Draft Q2 marketing copy for landing page",
        "tags": ["marketing", "copy", "q2"],
    },
    {
        "text": "Outline talk for PyCon lightning session",
        "tags": ["conference", "python", "talk"],
    },
    {
        "text": "Assemble shopping list for camping weekend",
        "tags": ["personal", "camping", "shopping"],
    },
    {
        "text": "Collect favorite espresso recipes to test",
        "tags": ["coffee", "recipe", "fun"],
    },
    {
        "text": "Summarize customer interviews for release",
        "tags": ["research", "customers", "release"],
    },
    {
        "text": "Prepare training outline for support team",
        "tags": ["training", "support", "ops"],
    },
    {
        "text": "List follow-up tasks after board meeting",
        "tags": ["followup", "board", "tasks"],
    },
    {
        "text": "Sketch automations to triage inbound leads",
        "tags": ["automation", "sales", "ideas"],
    },
    {
        "text": "Curate books for leadership book club",
        "tags": ["books", "leadership", "club"],
    },
]


def _add_contact(record_data: dict[str, Sequence[str] | str]) -> Record:
    """Create a contact record from plain data."""

    record = Record(str(record_data["name"]))
    for phone in record_data.get("phones", []):
        record.add_phone(str(phone))
    record.add_birthday(str(record_data["birthday"]))
    record.add_email(str(record_data["email"]))
    record.add_address(str(record_data["address"]))
    return record


def populate_contacts(book: AddressBook, source: Iterable[dict[str, Sequence[str] | str]]) -> int:
    """Populate provided address book with sample contacts, skipping duplicates."""

    added = 0
    for contact in source:
        name = str(contact["name"])
        if book.find(name):
            continue
        record = _add_contact(contact)
        book.add_record(record)
        added += 1
    book.save()
    return added


def populate_notes(book: NoteBook, source: Iterable[dict[str, Sequence[str] | str]]) -> int:
    """Populate provided note book with sample notes, skipping duplicates."""

    added = 0
    existing_signatures = {
        (note.text, tuple(sorted(note.tags))) for note in book.data.values()
    }
    for note_payload in source:
        text = str(note_payload["text"])
        tags = {str(tag).strip().lower() for tag in note_payload.get("tags", [])}
        signature = (text, tuple(sorted(tags)))
        if signature in existing_signatures:
            continue
        note = Note(text)
        note.add_tags(tags)
        book.add_note(note)
        existing_signatures.add(signature)
        added += 1
    book.save()
    return added


def main() -> None:
    """Entry point for populating demo data sets."""

    address_book = AddressBook.load()
    note_book = NoteBook.load()
    contacts_added = populate_contacts(address_book, CONTACTS_DATA)
    notes_added = populate_notes(note_book, NOTES_DATA)
    print(
        f"Added {contacts_added} contacts and {notes_added} notes."
        " Run the assistant to see them."
    )


if __name__ == "__main__":
    main()
