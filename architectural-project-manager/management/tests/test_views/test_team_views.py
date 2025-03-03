from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from management.models import ProjectType, Team, Worker, Position, Project


class TeamViewsTests(TestCase):
    def create_worker(
        self, username: str, password: str = "test123user", team: Team = None
    ) -> Worker:
        return Worker.objects.create_user(
            username=username, password=password, position=self.position, team=team
        )

    def create_project(
        self,
        name: str,
        description: str = "test_description",
        deadline: str = "2027-12-12",
        team: Team = None,
    ) -> Project:
        return Project.objects.create(
            name=name,
            description=description,
            deadline=deadline,
            project_type=self.project_type,
            team=team,
        )

    @staticmethod
    def create_team(name: str, team_lead: Worker) -> Team:
        return Team.objects.create(name=name, team_lead=team_lead)

    def setUp(self) -> None:
        self.position = Position.objects.create(name="test_position")
        self.project_type = ProjectType.objects.create(name="test_project_type")

        self.team_lead1 = self.create_worker("first_team_lead")
        self.team_1 = self.create_team("first_team", team_lead=self.team_lead1)

        self.worker1 = self.create_worker("first_worker", team=self.team_1)
        self.worker2 = self.create_worker("second_worker", team=self.team_1)

        self.project1 = self.create_project("first_project", team=self.team_1)
        self.project2 = self.create_project("second_project", team=self.team_1)

        self.user = get_user_model().objects.create_user(
            username="user", password="user12345", position=self.position
        )
        self.client.force_login(self.user)

    def test_team_list_view(self) -> None:
        self.team_lead2 = self.create_worker("second_team_lead")
        self.team_2 = self.create_team("second_team", team_lead=self.team_lead2)

        teams = Team.objects.order_by("name")
        url = reverse("management:team-list")
        response = self.client.get(url)
        self.assertEqual(list(response.context["team_list"]), list(teams))

    def test_team_detail_view(self) -> None:
        url = reverse("management:team-detail", args=[self.team_1.id])
        response = self.client.get(url)

        self.assertContains(response, self.team_1.name)
        self.assertContains(response, self.team_1.team_lead)

        self.assertContains(response, self.worker1)
        self.assertContains(response, self.worker2)

        self.assertContains(response, self.project1)
        self.assertContains(response, self.project2)

    def test_team_create_view(self) -> None:
        team_lead = self.create_worker("test_team_lead")
        worker = self.create_worker("test_worker")
        project = self.create_project("test_project")

        form_data = {
            "name": "new_team",
            "team_lead": team_lead.id,
            "workers": [worker.id],
            "projects": [project.id],
        }

        url = reverse("management:team-create")
        response = self.client.post(url, form_data)

        self.assertTrue(Team.objects.filter(name=form_data["name"]).exists())
        team = Team.objects.get(name=form_data["name"])
        self.assertIn(reverse("management:team-detail", args=[team.id]), response.url)
        self.assertEqual(response.status_code, 302)

    def test_team_update_view(self) -> None:
        team_lead = self.create_worker("updated_team_lead")
        worker = self.create_worker("updated_worker")
        project = self.create_project("updated_project")

        form_data = {
            "name": "updated_team_name",
            "team_lead": team_lead.id,
            "members": [worker.id],
            "projects": [project.id],
        }

        url = reverse("management:team-update", args=[self.team_1.id])
        response = self.client.post(url, form_data)
        self.team_1.refresh_from_db()

        self.assertEqual(self.team_1.name, form_data["name"])
        self.assertEqual(self.team_1.team_lead, team_lead)
        self.assertEqual(
            list(self.team_1.members.all()),
            list(Worker.objects.filter(username=worker.username)),
        )
        self.assertEqual(
            list(self.team_1.projects.all()),
            list(Project.objects.filter(name=project.name)),
        )
        self.assertIn(
            reverse("management:team-detail", args=[self.team_1.id]), response.url
        )
        self.assertEqual(response.status_code, 302)

    def test_team_delete_view(self) -> None:
        url = reverse("management:team-delete", args=[self.team_1.id])
        response = self.client.post(url)

        self.assertFalse(Team.objects.filter(id=self.team_1.id).exists())
        self.assertIn(reverse("management:team-list"), response.url)
        self.assertEqual(response.status_code, 302)
