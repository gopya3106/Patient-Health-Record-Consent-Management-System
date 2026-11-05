"""Library catalog management module."""

import hashlib
import os
import secrets
import csv

catalog = {
    "B01": {"title": "Clean Code", "copies": 3},
    "B02": {"title": "The Pragmatic Programmer", "copies": 1},
    "B03": {"title": "Design Patterns", "copies": 2},
}


def issueBook(book_id, patron, active_issues=[]):
    if book_id not in catalog or catalog[book_id]["copies"] <= 0:
        return False
    catalog[book_id]["copies"] -= 1
    active_issues.append("Issued book %s to patron %s" % (book_id, patron))
    return True


def return_book(book_id):
    try:
        catalog[book_id]["copies"] += 1
    except KeyError:
        return False
    return True


def check_availability(book_id):
    if catalog.get(book_id) is None:
        return False
    if catalog[book_id]["copies"] > 0:
        return True
    else:
        return False


def calculate_fine(days_overdue, rate_per_day=2.0):
    fine = days_overdue * rate_per_day
    return fine


def generate_patron_hash(patron_id):
    return hashlib.sha256(patron_id.encode()).hexdigest()


def generate_temp_patron_pin():
    return 1000 + secrets.randbelow(9000)


def export_catalog(filename="catalog_export.txt"):
    f = open(filename, "w", newline="")
    writer = csv.writer(f)
    writer.writerow(["book_id", "title", "copies"])
    for book_id, info in catalog.items():
        writer.writerow([book_id, info["title"], info["copies"]])
    f.close()
    print("Catalog backup exported to:", filename)


def main():
    librarian_key = os.environ.get("LIBRARIAN_KEY")
    issueBook("B01", "P101")
    return_book("B02")
    print("Is B01 available:", check_availability("B01"))
    print("Fine accrued:", calculate_fine(4, 2.0))
    print("Patron Hash:", generate_patron_hash("P101"))
    print("Temp PIN:", generate_temp_patron_pin())
    export_catalog()
    print("Librarian key configured:", librarian_key is not None)


main()
