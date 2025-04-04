from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from management.models import ProjectType, Team, Position, Project


class LoginRequiredTest(TestCase):
    urls_without_pk = [
        "management:index",
        "management:project-type-list",
        "management:project-type-create",
        "management:team-list",
        "management:team-create",
        "management:worker-list",
        "management:worker-create",
        "management:position-list",
        "management:position-create",
        "management:project-list",
        "management:project-create",
    ]
    urls_with_pk = [
        "management:project-type-detail",
        "management:project-type-update",
        "management:project-type-delete",
        "management:team-detail",
        "management:team-update",
        "management:team-delete",
        "management:worker-detail",
        "management:worker-update",
        "management:worker-delete",
        "management:position-detail",
        "management:position-update",
        "management:position-delete",
        "management:project-detail",
        "management:project-update",
        "management:project-delete",
    ]

    def setUp(self) -> None:
        project_type = ProjectType.objects.create(pk=1, name="test_project_type")
        position = Position.objects.create(pk=1, name="test_position")
        self.worker = get_user_model().objects.create_user(
            pk=1, username="user", password="user12345", position=position
        )
        Project.objects.create(
            pk=1,
            name="test_project",
            description="test_description",
            deadline="2026-12-12",
            project_type=project_type,
        )
        Team.objects.create(pk=1, name="test_team", team_lead=self.worker)

    def test_redirect_for_unauthenticated_users_without_pk(self) -> None:
        """
        Ensure unauthenticated users are redirected to the login page
        for URLs that do not require a primary key.
        """
        for url in self.urls_without_pk:
            response = self.client.get(reverse(url))
            self.assertNotEqual(response.status_code, 200)
            self.assertIn(reverse("login"), response.url)

    def test_redirect_for_unauthenticated_users_with_pk(self) -> None:
        """
        Ensure unauthenticated users are redirected to the login page
        for URLs that require a primary key.
        """
        for url in self.urls_with_pk:
            response = self.client.get(reverse(url, args=[1]))
            self.assertEqual(response.status_code, 302)
            self.assertIn(reverse("login"), response.url)

    def test_success_response_for_authenticated_users_without_pk(self) -> None:
        """
        Ensure authenticated users can access URLs that do not require a primary key.
        """
        self.client.force_login(self.worker)

        for url in self.urls_without_pk:
            response = self.client.get(reverse(url))
            self.assertEqual(response.status_code, 200)

    def test_success_response_for_authenticated_users_with_pk(self) -> None:
        """
        Ensure authenticated users can access URLs that require a primary key.
        """
        self.client.force_login(self.worker)

        for url in self.urls_with_pk:
            response = self.client.get(reverse(url, args=[1]))
            self.assertEqual(response.status_code, 200)
