from rest_framework import status

from library.models import Author, Book
from library.serializers import AuthorSerializer
from library.tests.base import BaseLibraryAPITest


class AuthorAPITests(BaseLibraryAPITest):
    def test_create_author(self):
        """Test creating a new author via API"""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "biography": "Test author biography",
        }
        response = self.client.post("/api/authors/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        author = Author.objects.get(first_name="John")
        self.assertEqual(author.last_name, "Doe")
        self.assertEqual(author.biography, "Test author biography")

    def test_create_author_invalid_data(self):
        """Test creating author with missing required fields"""
        data = {"first_name": ""}  # Missing last_name
        response = self.client.post("/api/authors/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("last_name", response.data)

    def test_retrieve_author(self):
        """Test retrieving an existing author"""
        response = self.client.get(f"/api/authors/{self.author.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "iChux")
        self.assertEqual(response.data["last_name"], "Objects")

    def test_retrieve_nonexistent_author(self):
        """Test retrieving a non-existent author"""
        response = self.client.get("/api/authors/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_author(self):
        """Test deleting an author"""
        response = self.client.delete(f"/api/authors/{self.author.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())

    def test_delete_author_with_books(self):
        """Test deleting an author with associated books (should cascade)"""
        Book.objects.create(
            title="Test Book", author=self.author, isbn="1234567890123", genre="fiction"
        )
        response = self.client.delete(f"/api/authors/{self.author.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(author=self.author).exists())

    def test_author_serializer(self):
        """Test AuthorSerializer serialization and deserialization"""
        data = {"first_name": "Jane", "last_name": "Smith", "biography": "New author"}
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        author = serializer.save()
        self.assertEqual(author.first_name, "Jane")
        serialized_data = AuthorSerializer(author).data
        self.assertEqual(serialized_data["last_name"], "Smith")
