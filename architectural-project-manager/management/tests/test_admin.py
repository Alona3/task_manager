from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime

from management.models import Position, ProjectType, Project, Team, Worker


class AdminPositionTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="test_position")

    def test_position_name_should_be_in_search_field(self) -> None:
        """
        Test that position's name is in search_field on position's list page
        """
        url = reverse("admin:management_position_changelist")
        response = self.client.get(url, {"q": self.position.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.position.name)


class AdminProjectTypeTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        self.project_type = ProjectType.objects.create(name="test_project_type")

    def test_project_type_name_should_be_in_search_field(self) -> None:
        """
        Test that name of project type is in search_field on
        list page of project types
        """
        url = reverse("admin:management_projecttype_changelist")
        response = self.client.get(url, {"q": self.project_type.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project_type.name)


class AdminTeamTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        team_lead = Worker.objects.create(username="test_team_lead")
        self.team = Team.objects.create(name="test_name", team_lead=team_lead)

    def test_team_attributes_listed(self) -> None:
        """
        Test that team's name, team_lead, number_of_members
        is correctly displayed in list_display
        """
        url = reverse("admin:management_team_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.team.name)
        self.assertContains(response, self.team.team_lead)
        self.assertContains(response, self.team.number_of_members)



class AdminWorkerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        position = Position.objects.create(name="test_position")
        self.worker = get_user_model().objects.create_user(
            username="user",
            password="user12345",
            first_name="test_first",
            last_name="test_last",
            email="worker@test.com",
            position=position
        )

    def test_worker_attributes_listed(self) -> None:
        """
        Test that worker's username, email, position is correctly
        displayed in list_display
        """
        url = reverse("admin:management_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.username)
        self.assertContains(response, self.worker.email)
        self.assertContains(response, self.worker.position.name)


    def test_get_full_name_method(self) -> None:
        """
        Test that get_full_name is correctly displayed in list_display
        """
        url = reverse("admin:management_worker_changelist")
        response = self.client.get(url)
        expected_result = f"{self.worker.first_name} {self.worker.last_name}"
        self.assertContains(response, expected_result)

    def test_worker_attributes_in_search_field(self) -> None:
        """
        Test that worker's username, first_name, last_name, position
        is in search_field on worker's list_page
        """
        url = reverse("admin:management_worker_changelist")

        params = (
            self.worker.username,
            self.worker.first_name,
            self.worker.last_name,
            self.worker.position.name
        )

        for param in params:
            response = self.client.get(url, {"q": param})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, param)


    def test_worker_detail_position_listed(self) -> None:
        """
        Test that worker's position is on worker detail admin page
        """
        url = reverse("admin:management_worker_change", args=[self.worker.id])
        response = self.client.get(url)
        self.assertContains(response, self.worker.position.name)

    def test_worker_create_attributes_listed(self) -> None:
        """
        Test that worker's first_name, last_name, email, position
        is on worker admin page
        """
        url = reverse("admin:management_worker_add")
        response = self.client.get(url)

        fields = (
            'name="first_name"',
            'name="last_name"',
            'name="email"',
            'name="position"'
        )

        for field in fields:
            self.assertContains(response, field)


class AdminProjectTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_admin",
            password="test123admin"
        )
        self.client.force_login(self.admin_user)
        project_type = ProjectType.objects.create(name="test_project_type")
        team = Team.objects.create(name="test_name")
        self.project = Project.objects.create(
            name="test_project",
            description="test_description",
            deadline="2025-11-12",
            project_type=project_type,
            team=team
        )

    def test_project_attributes_listed(self) -> None:
        """
        Test that project's name, project_type, deadline, priority,
        is_completed is correctly displayed in list_display
        """
        url = reverse("admin:management_project_changelist")
        response = self.client.get(url)

        formatted_deadline = datetime.strptime(
            self.project.deadline, '%Y-%m-%d').strftime('%b. %d, %Y')
        project_priority = self.project.get_priority_display()

        self.assertContains(response, self.project.name)
        self.assertContains(response, self.project.team)
        self.assertContains(response, formatted_deadline)
        self.assertContains(response, project_priority)
        self.assertContains(response, self.project.is_completed)

    def test_project_attributes_in_search_field(self) -> None:
        """
        Test that project's name and name of project_type is in
        search_field on project's list_page
        """
        url = reverse("admin:management_project_changelist")

        response = self.client.get(url, {"q": self.project.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)

        response = self.client.get(url, {"q": self.project.project_type.name})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.project_type.name)
