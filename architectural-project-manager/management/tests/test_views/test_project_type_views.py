from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from management.models import ProjectType, Position


class ProjectTypeViewsTests(TestCase):
    def setUp(self) -> None:
        self.project_type1 = ProjectType.objects.create(name="project_type1")
        self.project_type2 = ProjectType.objects.create(name="project_type2")

        position = Position.objects.create(name="test_position")
        self.user = get_user_model().objects.create_user(
            username="user", password="user12345", position=position
        )
        self.client.force_login(self.user)

    def test_project_type_list_view(self) -> None:
        project_types = ProjectType.objects.order_by("name")
        url = reverse("management:project-type-list")
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["project_type_list"]), list(project_types)
        )

    def test_project_type_detail_view(self) -> None:
        url = reverse("management:project-type-detail", args=[self.project_type1.id])
        response = self.client.get(url)
        self.assertContains(response, self.project_type1.name)

    def test_project_type_create_view(self) -> None:
        url = reverse("management:project-type-create")
        response = self.client.post(url, {"name": "test_project_type"})
        self.assertTrue(ProjectType.objects.filter(name="test_project_type").exists())
        project_type = ProjectType.objects.get(name="test_project_type")
        self.assertIn(
            reverse("management:project-type-detail", args=[project_type.id]),
            response.url,
        )
        self.assertEqual(response.status_code, 302)

    def test_project_type_update_view(self) -> None:
        url = reverse("management:project-type-update", args=[self.project_type1.id])
        response = self.client.post(url, {"name": "updated_project_type"})
        self.project_type1.refresh_from_db()
        self.assertEqual(self.project_type1.name, "updated_project_type")
        self.assertIn(
            reverse("management:project-type-detail", args=[self.project_type1.id]),
            response.url,
        )
        self.assertEqual(response.status_code, 302)

    def test_project_type_delete_view(self) -> None:
        url = reverse("management:project-type-delete", args=[self.project_type1.id])
        response = self.client.post(url)
        self.assertFalse(ProjectType.objects.filter(id=self.project_type1.id).exists())
        self.assertIn(reverse("management:project-type-list"), response.url)
        self.assertEqual(response.status_code, 302)
