import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_system.settings")
django.setup()

from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APIClient

from library.models import Author, Book, Loan, Member
from library.tasks import check_overdue_loans


def make_api_request(client, method, url, data=None, style="json"):
    """Utility function to make API requests and handle responses."""
    method_func = getattr(client, method.lower())
    response = method_func(url, data, format=style)
    status_code = response.status_code
    response_data = (
        response.json() if status_code in (200, 201) else {"error": response.json()}
    )
    print(f"{method.upper()} {url} (Status: {status_code}):", response_data)
    return response_data, status_code


def create_user(username, email, password="password123"):
    """Create a user and return the User object."""
    return User.objects.create_user(username=username, email=email, password=password)


def create_member(user):
    """Create a member for a given user."""
    return Member.objects.create(user=user)


def create_author(first_name, last_name):
    """Create an author."""
    return Author.objects.create(first_name=first_name, last_name=last_name)


def create_book(title, author, isbn, genre, available_copies):
    """Create a book."""
    return Book.objects.create(
        title=title,
        author=author,
        isbn=isbn,
        genre=genre,
        available_copies=available_copies,
    )


def create_loan(book, member, due_date, is_returned=False, remainder_sent=False):
    """Create a loan."""
    return Loan.objects.create(
        book=book,
        member=member,
        due_date=due_date,
        is_returned=is_returned,
        remainder_sent=remainder_sent,
    )


def clear_all_data():
    """Clear all data from the database."""
    User.objects.all().delete()
    Member.objects.all().delete()
    Author.objects.all().delete()
    Book.objects.all().delete()
    Loan.objects.all().delete()


def main():
    # Clear existing data
    clear_all_data()

    # Create sample data
    users = [
        create_user("main1", "main_one@example.com"),
        create_user("main2", "main_two@example.com"),
    ]
    members = [create_member(user) for user in users]

    authors = [create_author("Main", "One"), create_author("Jane", "Doe")]

    books = [
        create_book("We Code & Track v1", authors[0], "1111234567890", "biography", 2),
        create_book("Python Adventures", authors[1], "2221234567890", "sci-fi", 3),
        create_book("Code Chronicles", authors[0], "3331234567890", "biography", 1),
        create_book("Space Coding", authors[1], "4441234567890", "sci-fi", 2),
        create_book("Life in Code", authors[0], "5551234567890", "biography", 1),
    ]

    loans = [
        create_loan(
            books[0],
            members[0],
            timezone.now().date() - timedelta(days=1),
            is_returned=False,
            remainder_sent=False,
        ),
        create_loan(
            books[1],
            members[0],
            timezone.now().date() + timedelta(days=7),
            is_returned=False,
            remainder_sent=False,
        ),
        create_loan(
            books[0],
            members[1],
            timezone.now().date() + timedelta(days=7),
            is_returned=False,
            remainder_sent=False,
        ),
    ]

    # Print summary of created data
    print("Sample data created:")
    print(f"Users: {User.objects.count()}")
    print(f"Members: {Member.objects.count()}")
    print(f"Authors: {Author.objects.count()}")
    print(f"Books: {Book.objects.count()}")
    print(f"Loans: {Loan.objects.count()}")

    # Initialize API client
    client = APIClient()

    # Demonstrate check_overdue_loans task
    print("\nRunning check_overdue_loans task...")
    check_overdue_loans()
    loans[0].refresh_from_db()
    print(f"Loan {loans[0].id} remainder_sent status: {loans[0].remainder_sent}")

    # Demonstrate TopActiveMembersView
    print("\nFetching top active members...")
    make_api_request(client, "GET", "/api/top-active-members/")

    # Demonstrate extending a loan's due date
    print("\nExtending due date for loan2...")
    make_api_request(
        client,
        "POST",
        f"/api/loans/{loans[1].id}/extend_due_date/",
        {"additional_days": 5},
    )
    loans[1].refresh_from_db()
    print(f"Loan {loans[1].id} new due date: {loans[1].due_date}")

    # Demonstrate pagination
    print("\nDemonstrating pagination on books endpoint...")
    make_api_request(client, "GET", "/api/books/", {"page": 1, "page_size": 2})

    # Calculate total pages
    response, status_code = make_api_request(
        client, "GET", "/api/books/", {"page_size": 2}
    )
    if status_code == 200:
        count = response.get("count", 0)
        page_size = 2
        total_pages = (count + page_size - 1) // page_size
        print(f"Total books: {count}, Total pages with page_size=2: {total_pages}")

    # Demonstrate filtering with DjangoFilterBackend
    print("\nDemonstrating filtering by genre and author__last_name...")
    filter_params = [
        {"genre": "biography"},
        {"author__last_name": "Doe"},
        {"genre": "sci-fi", "author__last_name": "Doe"},
    ]
    for params in filter_params:
        param_str = "&".join(f"{k}={v}" for k, v in params.items())
        make_api_request(client, "GET", f"/api/books/?{param_str}")


if __name__ == "__main__":
    main()
