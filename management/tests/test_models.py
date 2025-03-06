from django.test import TestCase
from django.contrib.auth import get_user_model
from management.models import (
    ProjectType, Position, Project, Team, Worker
)


class ProjectTypeTest(TestCase):
    def test_str_method(self) -> None:
        project_type = ProjectType.objects.create(name="test")
        self.assertEqual(str(project_type), project_type.name)


class TeamTests(TestCase):
    def setUp(self) -> None:
        self.team = Team.objects.create(name="test_name")

    def test_str_method(self) -> None:
        self.assertEqual(str(self.team), self.team.name)

    def test_number_of_members(self) -> None:
        Worker.objects.create(username="username1", team=self.team)
        Worker.objects.create(username="username2", team=self.team)
        self.assertEqual(self.team.number_of_members, 2)


class WorkerTest(TestCase):
    def test_str_method(self) -> None:
        position = Position.objects.create(name="test")
        worker = get_user_model().objects.create(
            username="user",
            password="user12345",
            first_name="test_first",
            last_name="test_last",
            position=position,
        )
        self.assertEqual(
            str(worker),
            f"{worker.first_name} {worker.last_name} ({worker.position.name})",
        )

    def test_create_worker_with_team_and_position(self) -> None:
        team = Team.objects.create(name="test_name")
        position = Position.objects.create(name="test")

        worker = get_user_model().objects.create_user(
            username="user",
            password="user12345",
            team=team,
            position=position,
        )

        self.assertEqual(worker.position, position)
        self.assertEqual(worker.team, team)


class PositionTest(TestCase):
    def test_str_method(self) -> None:
        position = Position.objects.create(name="test")
        self.assertEqual(str(position), position.name)


class ProjectTest(TestCase):
    def test_str_method(self) -> None:
        project_type = ProjectType.objects.create(name="test")
        project = Project.objects.create(
            name="test",
            description="test description",
            deadline="2024-12-12",
            project_type=project_type,
        )
        self.assertEqual(str(project), project.name)
