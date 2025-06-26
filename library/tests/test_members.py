from django.contrib.auth.models import User
from rest_framework import status

from library.models import Loan, Member
from library.serializers import MemberSerializer
from library.tests.base import BaseLibraryAPITest


class MemberAPITests(BaseLibraryAPITest):
    def test_create_member(self):
        """Test creating a new member via API"""
        new_user = User.objects.create_user(
            username="newuser", email="newuser@example.com", password="Test1234"
        )
        data = {"user_id": new_user.id}
        response = self.client.post("/api/members/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 2)
        member = Member.objects.get(user=new_user)
        self.assertIsNotNone(member.membership_date)

    def test_create_member_invalid_user(self):
        """Test creating member with non-existent user"""
        data = {"user_id": 999}
        response = self.client.post("/api/members/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user_id", response.data)

    def test_retrieve_member(self):
        """Test retrieving an existing member"""
        response = self.client.get(f"/api/members/{self.member.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "tracker")

    def test_delete_member(self):
        """Test deleting a member"""
        response = self.client.delete(f"/api/members/{self.member.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Member.objects.filter(id=self.member.id).exists())

    def test_delete_member_with_loans(self):
        """Test deleting a member with active loans (should cascade)"""
        response = self.client.delete(f"/api/members/{self.member.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Loan.objects.filter(member=self.member).exists())

    def test_member_serializer(self):
        """Test MemberSerializer serialization and deserialization"""
        new_user = User.objects.create_user(
            username="serialuser", email="serial@example.com", password="Test1234"
        )
        data = {"user_id": new_user.id}
        serializer = MemberSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        member = serializer.save()
        self.assertEqual(member.user.username, "serialuser")
        serialized_data = MemberSerializer(member).data
        self.assertEqual(serialized_data["user"]["email"], "serial@example.com")
