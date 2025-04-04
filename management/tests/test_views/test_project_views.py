from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from datetime import datetime

from management.models import ProjectType, Team, Position, Project


class ProjectViewsTests(TestCase):
    def setUp(self) -> None:
        self.project_type = ProjectType.objects.create(name="test_project_type")
        self.position = Position.objects.create(name="test_position")
        self.user = get_user_model().objects.create_user(
            username="user", password="user12345", position=self.position
        )
        self.team = Team.objects.create(name="test_team", team_lead=self.user)

        self.project_1 = Project.objects.create(
            name="first_project",
            description="test_description",
            deadline="2027-12-12",
            project_type=self.project_type,
            team=self.team
        )
        self.project_2 = Project.objects.create(
            name="second_project",
            description="test_description",
            deadline="2027-12-12",
            project_type=self.project_type,
            team=self.team
        )
        self.client.force_login(self.user)

    def test_project_list_view(self) -> None:
        projects = Project.objects.all()
        url = reverse("management:project-list")
        response = self.client.get(url)

        self.assertEqual(list(response.context["project_list"]), list(projects))
        self.assertIn("search_form", response.context)

    def test_project_list_view_search_by_name(self) -> None:
        url = reverse("management:project-list")

        response = self.client.get(url + f"?name={self.project_1.name}")
        self.assertContains(response, self.project_1.name)
        self.assertNotContains(response, self.project_2.name)

        response = self.client.get(url + f"?name={self.project_2.name}")
        self.assertContains(response, self.project_2.name)
        self.assertNotContains(response, self.project_1.name)

    def test_project_list_view_search_boundary_cases(self) -> None:
        url = reverse("management:project-list")

        response = self.client.get(url + "?name=")
        self.assertContains(response, self.project_1.name)
        self.assertContains(response, self.project_2.name)

        response = self.client.get(url + "?name=this project does not exist")
        self.assertNotContains(response, self.project_1.name)
        self.assertNotContains(response, self.project_2.name)

    def test_project_detail_view(self) -> None:
        url = reverse("management:project-detail", args=[self.project_1.id])
        response = self.client.get(url)

        formatted_deadline = datetime.strptime(
            self.project_1.deadline, '%Y-%m-%d').strftime('%b. %d, %Y')
        project_priority = self.project_1.get_priority_display()
        project_status = "Completed" if self.project_1.is_completed else "Pending"

        self.assertContains(response, self.project_1.name)
        self.assertContains(response, self.project_1.description)
        self.assertContains(response, formatted_deadline)
        self.assertContains(response, project_status)
        self.assertContains(response, project_priority)
        self.assertContains(response, self.project_1.project_type)
        self.assertContains(response, self.project_1.team)

    def test_project_create_view(self) -> None:
        form_data = {
            "name": "new_project",
            "description": "test_description",
            "deadline": "2027-12-12",
            "priority": "MP",
            "project_type": self.project_type.id,
            "team": self.team.id
        }

        url = reverse("management:project-create")
        response = self.client.post(url, form_data)

        self.assertTrue(Project.objects.filter(name=form_data["name"]).exists())
        project = Project.objects.get(name=form_data["name"])
        self.assertIn(
            reverse("management:project-detail", args=[project.id]),
            response.url
        )
        self.assertEqual(response.status_code, 302)

    def test_project_update_view(self) -> None:
        new_project_type = ProjectType.objects.create(name="updated_project_type")
        new_team_lead = get_user_model().objects.create_user(
            username="test_user_2", password="test123user", position=self.position
        )
        new_team = Team.objects.create(name="updated_team", team_lead=new_team_lead)

        form_data = {
            "name": "updated_project",
            "description": "updated_description",
            "deadline": "2030-12-12",
            "is_completed": True,
            "priority": "CR",
            "project_type": new_project_type.id,
            "team": new_team.id
        }

        url = reverse("management:project-update", args=[self.project_1.id])
        response = self.client.post(url, form_data)
        self.project_1.refresh_from_db()

        formated_deadline = datetime.strptime(form_data["deadline"], "%Y-%m-%d").date()

        self.assertEqual(self.project_1.name, form_data["name"])
        self.assertEqual(self.project_1.description, form_data["description"])
        self.assertEqual(self.project_1.deadline, formated_deadline)
        self.assertEqual(self.project_1.is_completed, form_data["is_completed"])
        self.assertEqual(self.project_1.priority, form_data["priority"])
        self.assertEqual(self.project_1.project_type, new_project_type)
        self.assertEqual(self.project_1.team, new_team)

        self.assertIn(
            reverse("management:project-detail", args=[self.project_1.id]),
            response.url
        )
        self.assertEqual(response.status_code, 302)

    def test_project_delete_view(self) -> None:
        url = reverse("management:project-delete", args=[self.project_1.id])
        response = self.client.post(url)

        self.assertFalse(Project.objects.filter(name=self.project_1.name).exists())
        self.assertIn(reverse("management:project-list"), response.url)
        self.assertEqual(response.status_code, 302)
