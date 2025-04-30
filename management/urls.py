from django.urls import path

from management.views import (
    index,
    instruction_view,
    ProjectTypeListView,
    TeamListView,
    WorkerListView,
    PositionListView,
    ProjectListView,
    TeamDetailView,
    WorkerDetailView,
    ProjectDetailView,
    PositionDetailView,
    ProjectTypeDetailView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
    WorkerCreateView,
    PositionCreateView,
    WorkerUpdateView,
    WorkerDeleteView,
    PositionUpdateView,
    PositionDeleteView,
    ProjectTypeCreateView,
    ProjectTypeUpdateView,
    ProjectTypeDeleteView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView
)


urlpatterns = [
    path("", index, name="index"),
    path("instruction/", instruction_view, name="instruction"),

    path("project-types/", ProjectTypeListView.as_view(), name="project-type-list"),
    path("project-types/<int:pk>", ProjectTypeDetailView.as_view(), name="project-type-detail"),
    path("project-types/create/", ProjectTypeCreateView.as_view(), name="project-type-create"),
    path("project-types/<int:pk>/update/", ProjectTypeUpdateView.as_view(), name="project-type-update"),
    path("project-types/<int:pk>/delete/", ProjectTypeDeleteView.as_view(), name="project-type-delete"),

    path("teams/", TeamListView.as_view(), name="team-list"),
    path("teams/<int:pk>/", TeamDetailView.as_view(), name="team-detail"),
    path("teams/create/", TeamCreateView.as_view(), name="team-create"),
    path("teams/<int:pk>/update/", TeamUpdateView.as_view(), name="team-update"),
    path("teams/<int:pk>/delete/", TeamDeleteView.as_view(), name="team-delete"),

    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/update/", WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker-delete"),

    path("positions/", PositionListView.as_view(), name="position-list"),
    path("positions/<int:pk>/", PositionDetailView.as_view(), name="position-detail"),
    path("positions/create/", PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/update/", PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", PositionDeleteView.as_view(), name="position-delete"),

    path("projects/", ProjectListView.as_view(), name="project-list"),
    path("projects/<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("projects/create/", ProjectCreateView.as_view(), name="project-create"),
    path("projects/<int:pk>/update/", ProjectUpdateView.as_view(), name="project-update"),
    path("projects/<int:pk>/delete/", ProjectDeleteView.as_view(), name="project-delete"),
]

app_name = "management"
