from rest_framework import status

from library.models import Book, Loan
from library.serializers import BookSerializer
from library.tests.base import BaseLibraryAPITest


class BookAPITests(BaseLibraryAPITest):
    def test_create_book(self):
        """Test creating a new book via API"""
        data = {
            "title": "New Book",
            "author_id": self.author.id,
            "isbn": "1234567890123",
            "genre": "fiction",
            "available_copies": 1,
        }
        response = self.client.post("/api/books/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        book = Book.objects.get(title="New Book")
        self.assertEqual(book.isbn, "1234567890123")

    def test_create_book_invalid_genre(self):
        """Test creating book with invalid genre"""
        data = {
            "title": "Invalid Genre Book",
            "author_id": self.author.id,
            "isbn": "1234567890123",
            "genre": "invalid_genre",
            "available_copies": 1,
        }
        response = self.client.post("/api/books/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("genre", response.data)

    def test_loan_book(self):
        """Test loaning a book"""
        data = {"member_id": self.member.id}
        response = self.client.post(
            f"/api/books/{self.book.id}/loan/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 1)
        self.assertTrue(
            Loan.objects.filter(
                book=self.book, member=self.member, is_returned=False
            ).exists()
        )

    def test_loan_book_no_copies(self):
        """Test loaning a book with no available copies"""
        self.book.available_copies = 0
        self.book.save()
        data = {"member_id": self.member.id}
        response = self.client.post(
            f"/api/books/{self.book.id}/loan/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No available copies", response.data["error"])

    def test_loan_book_nonexistent_member(self):
        """Test loaning a book to a non-existent member"""
        data = {"member_id": 999}
        response = self.client.post(
            f"/api/books/{self.book.id}/loan/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Member does not exist", response.data["error"])

    def test_return_book(self):
        """Test returning a book"""
        data = {"member_id": self.member.id}
        response = self.client.post(
            f"/api/books/{self.book.id}/return_book/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.loan.refresh_from_db()
        self.assertEqual(self.book.available_copies, 3)
        self.assertTrue(self.loan.is_returned)
        self.assertIsNotNone(self.loan.return_date)

    def test_return_nonexistent_loan(self):
        """Test returning a non-existent loan"""
        data = {"member_id": self.member.id}
        self.loan.is_returned = True
        self.loan.save()
        response = self.client.post(
            f"/api/books/{self.book.id}/return_book/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Active loan does not exist", response.data["error"])

    def test_book_serializer(self):
        """Test BookSerializer serialization and deserialization"""
        data = {
            "title": "Serialized Book",
            "author_id": self.author.id,
            "isbn": "9876543210123",
            "genre": "sci-fi",
            "available_copies": 1,
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.title, "Serialized Book")
        serialized_data = BookSerializer(book).data
        self.assertEqual(serialized_data["author"]["id"], self.author.id)
