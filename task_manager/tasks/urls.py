from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet,
    TaskTypeViewSet,
    PositionViewSet,
    WorkerViewSet,
    TeamViewSet,
    ProjectViewSet,
    TagViewSet,
    WorkerTaskListView,
    TaskListView,
    ProjectTaskListView,
    TeamTaskListView
)

app_name = 'tasks'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'task-types', TaskTypeViewSet)
router.register(r'positions', PositionViewSet)
router.register(r'workers', WorkerViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('worker-tasks/', WorkerTaskListView.as_view(), name='worker-task-list'),
    path('projects/<int:project_id>/tasks/', ProjectTaskListView.as_view(), name='project-task-list'),  # Додали
    path('teams/<int:team_id>/tasks/', TeamTaskListView.as_view(), name='team-task-list'),
]
