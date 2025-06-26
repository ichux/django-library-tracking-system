from unittest.mock import patch

from rest_framework import status

from library.models import Book
from library.serializers import LoanSerializer
from library.tests.base import BaseLibraryAPITest


class LoanAPITests(BaseLibraryAPITest):
    @patch("library.tasks.send_mail")
    def test_send_loan_notification_task(self, mock_send_mail):
        from library.tasks import send_loan_notification

        send_loan_notification(self.loan.id)
        mock_send_mail.assert_called_once()

    def test_create_loan_invalid_book(self):
        """Test creating loan with non-existent book"""
        data = {"book_id": 999, "member_id": self.member.id}
        response = self.client.post("/api/loans/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("book_id", response.data)

    def test_loan_serializer(self):
        """Test LoanSerializer serialization and deserialization"""
        new_book = Book.objects.create(
            title="Serialized Loan Book",
            author=self.author,
            isbn="1122334455667",
            genre="nonfiction",
            available_copies=1,
        )
        data = {"book_id": new_book.id, "member_id": self.member.id}
        serializer = LoanSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        loan = serializer.save()
        self.assertFalse(loan.is_returned)
        serialized_data = LoanSerializer(loan).data
        self.assertEqual(serialized_data["book"]["title"], "Serialized Loan Book")
        self.assertEqual(serialized_data["member"]["user"]["username"], "tracker")
