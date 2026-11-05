"""Library catalog management module."""

import hashlib
import os
import secrets
import csv

catalog = {
    "B01": {"title": "Clean Code", "copies": 3, "total": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1, "total": 1},
    "B03": {"title": "Design Patterns", "copies": 2, "total": 2},
}


def issue_book(book_id, patron, active_issues=None):
    """Issue one copy of a book to a patron.

    Returns True if a copy was issued, False if the book is unknown or
    no copies are available. A log entry is appended to active_issues
    when a list is supplied.
    """
    if active_issues is None:
        active_issues = []
    if book_id not in catalog or catalog[book_id]["copies"] <= 0:
        return False
    catalog[book_id]["copies"] -= 1
    active_issues.append(f"Issued book {book_id} to patron {patron}")
    return True


def return_book(book_id):
    """Return one copy of a book to the catalog.

    Returns False if the book is unknown or all copies are already on
    the shelf, so the copy count can never exceed the library's stock.
    """
    book = catalog.get(book_id)
    if book is None or book["copies"] >= book["total"]:
        return False
    book["copies"] += 1
    return True


def check_availability(book_id):
    """Return True if at least one copy of the book is available."""
    book = catalog.get(book_id)
    return book is not None and book["copies"] > 0


def calculate_fine(days_overdue, rate_per_day=2.0):
    """Return the overdue fine for the given number of days."""
    return days_overdue * rate_per_day


def generate_patron_hash(patron_id):
    """Return a SHA-256 hex digest identifying a patron."""
    return hashlib.sha256(patron_id.encode()).hexdigest()


def generate_temp_patron_pin():
    """Return a cryptographically secure four-digit temporary PIN."""
    return 1000 + secrets.randbelow(9000)


def export_catalog(filename="catalog_export.txt"):
    """Write the catalog to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["book_id", "title", "copies"])
        for book_id, info in catalog.items():
            writer.writerow([book_id, info["title"], info["copies"]])
    print("Catalog backup exported to:", filename)


def main():
    """Run a short demonstration of the catalog functions."""
    librarian_key = os.environ.get("LIBRARIAN_KEY")
    issue_log = []
    print("Issued B01:", issue_book("B01", "P101", issue_log))
    print("Returned B02:", return_book("B02"))
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4, 2.0))
    print("Patron Hash:", generate_patron_hash("P101"))
    print("Temp PIN:", generate_temp_patron_pin())
    export_catalog()
    print("Librarian key configured:", librarian_key is not None)


if __name__ == "__main__":
    main()
