from django.contrib.auth.models import User
from django.test import TestCase

from library.models import Author, Book, Loan, Member


class BaseLibraryAPITest(TestCase):
    def setUp(self):
        # Ensure test isolation by clearing out all data.
        self.inits()

        self.user = User.objects.create_user(
            username="tracker", email="tracker@packer.com", password="Track4B00k5"
        )
        self.member = Member.objects.create(user=self.user)
        self.author = Author.objects.create(first_name="iChux", last_name="Objects")
        self.book = Book.objects.create(
            title="We Code & Track v1",
            author=self.author,
            isbn="1111234567890",
            genre="biography",
            available_copies=2,
        )
        self.loan = Loan.objects.create(
            member=self.member,
            book=self.book,
        )

    @staticmethod
    def inits():
        Author.objects.all().delete()
        Book.objects.all().delete()
        Member.objects.all().delete()
        Loan.objects.all().delete()
        User.objects.all().delete()

    def tearDown(self):
        self.inits()
