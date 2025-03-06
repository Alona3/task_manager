from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from management.models import Team, Worker, Position


class WorkerViewsTests(TestCase):
    @staticmethod
    def create_worker(
        username: str,
        first_name: str,
        last_name: str,
        position: Position,
        password: str = "test123user",
        team: Team = None,
    ) -> Worker:
        return Worker.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            position=position,
            team=team,
        )

    def setUp(self) -> None:
        self.position_1 = Position.objects.create(name="first_position")
        self.position_2 = Position.objects.create(name="second_position")
        self.worker_1 = self.create_worker(
            "first_worker", "Bob", "Black", self.position_1
        )
        self.worker_2 = self.create_worker(
            "second_worker", "Alice", "Smith", self.position_2
        )

        self.user = get_user_model().objects.create_user(
            username="user", password="user12345", position=self.position_1
        )
        self.client.force_login(self.user)

    def test_worker_list_view(self) -> None:
        workers = Worker.objects.all()
        url = reverse("management:worker-list")
        response = self.client.get(url)

        self.assertEqual(list(response.context["worker_list"]), list(workers))
        self.assertIn("search_form", response.context)

    def test_worker_list_view_search(self) -> None:
        url = reverse("management:worker-list")

        cases = [
            self.worker_1.first_name,
            self.worker_1.last_name,
            f"{self.worker_1.first_name} {self.worker_1.last_name}",
            f"{self.worker_1.first_name} {self.worker_1.last_name} {self.worker_1.position.name}",
            self.worker_1.position.name,
        ]

        for case in cases:
            response = self.client.get(url + f"?search={case}")
            self.assertContains(response, self.worker_1.first_name)
            self.assertNotContains(response, self.worker_2.first_name)

    def test_worker_list_view_search_boundary_cases(self) -> None:
        url = reverse("management:worker-list")

        response = self.client.get(url + f"?search=")
        self.assertContains(response, self.worker_1.first_name)
        self.assertContains(response, self.worker_2.first_name)

        response = self.client.get(url + f"?search=there are too long query")
        self.assertNotContains(response, self.worker_1.first_name)
        self.assertNotContains(response, self.worker_2.first_name)

    def test_worker_detail_view(self) -> None:
        team = Team.objects.create(name="test_team", team_lead=self.worker_2)
        self.worker_1.team = team
        self.worker_1.email = "test.user@example.com"
        self.worker_1.save()
        url = reverse("management:worker-detail", args=[self.worker_1.id])
        response = self.client.get(url)

        self.assertContains(response, self.worker_1.username)
        self.assertContains(response, self.worker_1.first_name)
        self.assertContains(response, self.worker_1.last_name)
        self.assertContains(response, self.worker_1.email)
        self.assertContains(response, self.worker_1.position.name)
        self.assertContains(response, self.worker_1.team)

    def test_worker_create_view(self) -> None:
        team = Team.objects.create(name="test_team", team_lead=self.worker_2)
        url = reverse("management:worker-create")

        form_data = {
            "username": "new_worker",
            "password1": "test123user",
            "password2": "test123user",
            "first_name": "John",
            "last_name": "Snow",
            "position": self.position_1.id,
            "team": team.id,
        }

        response = self.client.post(url, form_data)
        self.assertTrue(Worker.objects.filter(username=form_data["username"]).exists())
        worker = Worker.objects.get(username=form_data["username"])
        self.assertIn(
            reverse("management:worker-detail", args=[worker.id]), response.url
        )
        self.assertEqual(response.status_code, 302)

    def test_worker_update_view(self) -> None:
        team = Team.objects.create(name="updated_team", team_lead=self.worker_2)
        position = Position.objects.create(name="updated_position")

        form_data = {
            "username": "updated_worker",
            "first_name": "updated_first_name",
            "last_name": "updated_last_name",
            "email": "updated@email.com",
            "position": position.id,
            "team": team.id,
        }

        url = reverse("management:worker-update", args=[self.worker_1.id])
        response = self.client.post(url, form_data)
        self.worker_1.refresh_from_db()

        self.assertEqual(self.worker_1.username, form_data["username"])
        self.assertEqual(self.worker_1.first_name, form_data["first_name"])
        self.assertEqual(self.worker_1.last_name, form_data["last_name"])
        self.assertEqual(self.worker_1.email, form_data["email"])
        self.assertEqual(self.worker_1.position, position)
        self.assertEqual(self.worker_1.team, team)

        self.assertIn(
            reverse("management:worker-detail", args=[self.worker_1.id]), response.url
        )
        self.assertEqual(response.status_code, 302)

    def test_worker_delete_view(self) -> None:
        url = reverse("management:worker-delete", args=[self.worker_1.id])
        response = self.client.post(url)

        self.assertFalse(
            Worker.objects.filter(username=self.worker_1.username).exists()
        )
        self.assertIn(reverse("management:worker-list"), response.url)
        self.assertEqual(response.status_code, 302)
