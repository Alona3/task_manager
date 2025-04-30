from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from management.models import Position


class PositionViewsTests(TestCase):
    def setUp(self) -> None:
        self.position_1 = Position.objects.create(name="first_position")

        self.user = get_user_model().objects.create_user(
            username="user",
            password="user12345",
            first_name="John",
            last_name="Doe",
            position=self.position_1,
        )
        self.client.force_login(self.user)

    def test_position_list(self) -> None:
        Position.objects.create(name="second_position")
        positions = Position.objects.order_by("name")
        url = reverse("management:position-list")
        response = self.client.get(url)
        self.assertEqual(list(response.context["position_list"]), list(positions))

    def test_position_detail_view(self) -> None:
        url = reverse("management:position-detail", args=[self.position_1.id])
        response = self.client.get(url)
        self.assertContains(response, self.position_1.name)
        self.assertContains(response, f"{self.user.first_name} {self.user.last_name}")

    def test_position_create_view(self) -> None:
        url = reverse("management:position-create")
        response = self.client.post(url, {"name": "new_position"})
        self.assertTrue(Position.objects.filter(name="new_position").exists())
        position = Position.objects.get(name="new_position")
        self.assertIn(
            reverse("management:position-detail", args=[position.id]), response.url
        )
        self.assertEqual(response.status_code, 302)

    def test_position_update_view(self) -> None:
        url = reverse("management:position-update", args=[self.position_1.id])
        response = self.client.post(url, {"name": "updated_position"})
        self.position_1.refresh_from_db()
        self.assertEqual(self.position_1.name, "updated_position")
        self.assertIn(
            reverse("management:position-detail", args=[self.position_1.id]),
            response.url,
        )
        self.assertEqual(response.status_code, 302)

    def test_position_delete_view(self) -> None:
        url = reverse("management:position-delete", args=[self.position_1.id])
        response = self.client.post(url)
        self.assertFalse(Position.objects.filter(name=self.position_1.name).exists())
        self.assertIn(reverse("management:position-list"), response.url)
        self.assertEqual(response.status_code, 302)
