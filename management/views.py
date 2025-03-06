from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from management.models import (
    ProjectType, Team, Worker, Position, Project
)
from management.forms import (
    WorkerCreationForm,
    TeamCreationForm,
    TeamUpdateForm,
    ProjectSearchForm,
    WorkerSearchForm
)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_teams = Team.objects.count()
    num_workers = Worker.objects.count()
    num_projects = Project.objects.count()
    context = {
        "num_teams": num_teams,
        "num_workers": num_workers,
        "num_projects": num_projects,
    }
    return render(
        request, "management/index.html", context=context
    )

def instruction_view(request: HttpRequest) -> HttpResponse:
    return render(request, "management/instruction.html")


class ProjectTypeListView(LoginRequiredMixin, generic.ListView):
    model = ProjectType
    template_name = "management/project_type_list.html"
    context_object_name = "project_type_list"
    queryset = ProjectType.objects.annotate(project_count=Count(
        "projects")).order_by("name")
    paginate_by = 15


class ProjectTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = ProjectType
    template_name = "management/project_type_detail.html"
    context_object_name = "project_type"


class ProjectTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = ProjectType
    fields = "__all__"
    template_name = "management/project_type_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:project-type-detail", kwargs={"pk": self.object.pk})


class ProjectTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ProjectType
    fields = "__all__"
    template_name = "management/project_type_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:project-type-detail", kwargs={"pk": self.object.pk})


class ProjectTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ProjectType
    context_object_name = "project_type"
    success_url = reverse_lazy("management:project-type-list")
    template_name = "management/project_type_confirm_delete.html"


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    queryset = Team.objects.select_related(
        "team_lead__position").annotate(member_count=Count("members")).order_by("name")
    paginate_by = 10


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related(
            "members__position", "projects").select_related("team_lead__position")


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreationForm
    template_name = "management/team_form.html"

    def form_valid(self, form) -> HttpResponse:
        response = super().form_valid(form)
        team = self.object

        team.members.set(form.cleaned_data["members"])
        team.projects.set(form.cleaned_data["projects"])

        return response

    def get_success_url(self) -> str:
        return reverse_lazy("management:team-detail", kwargs={"pk": self.object.pk})


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamUpdateForm
    template_name = "management/team_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:team-detail", kwargs={"pk": self.object.pk})


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    template_name = "management/team_confirm_delete.html"
    success_url = reverse_lazy("management:team-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(WorkerListView, self).get_context_data(**kwargs)
        search = self.request.GET.get("search", "")
        context["search"] = search
        context["search_form"] = WorkerSearchForm(
            initial={"search": search}
        )
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Worker.objects.exclude(position__name="admin").select_related("position")
        search_query = self.request.GET.get("search", "").strip()

        if search_query:
            search_values = search_query.split()
            filters = Q()

            if len(search_values) == 1:
                filters |= Q(first_name__icontains=search_values[0])
                filters |= Q(last_name__icontains=search_values[0])
                filters |= Q(position__name__icontains=search_values[0])

            elif len(search_values) == 2:
                filters |= Q(
                    first_name__icontains=search_values[0],
                    last_name__icontains=search_values[1]
                )
                filters |= Q(
                    first_name__icontains=search_values[1],
                    last_name__icontains=search_values[0]
                )

            elif len(search_values) == 3:
                filters |= Q(
                    first_name__icontains=search_values[0],
                    last_name__icontains=search_values[1],
                    position__name__icontains=search_values[2]
                )
                filters |= Q(
                    first_name__icontains=search_values[1],
                    last_name__icontains=search_values[0],
                    position__name__icontains=search_values[2]
                )
            elif len(search_values) > 3:
                return Worker.objects.none()
            queryset = queryset.filter(filters)

        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(
            "team").select_related("position")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm

    def get_success_url(self) -> str:
        return reverse_lazy("management:worker-detail", kwargs={"pk": self.object.pk})


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = ("username", "first_name", "last_name", "email", "position", "team")
    template_name = "management/worker_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("management:worker-list")
    template_name = "management/worker_confirm_delete.html"


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    queryset = Position.objects.exclude(
        name="admin").annotate(worker_count=Count("workers")).order_by("name")
    paginate_by = 15


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().prefetch_related("workers__team")

class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    template_name = "management/position_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:position-detail", kwargs={"pk": self.object.pk})


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    template_name = "management/position_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:position-detail", kwargs={"pk": self.object.pk})


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("management:position-list")
    template_name = "management/position_confirm_delete.html"


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super(ProjectListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = ProjectSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = ProjectSearchForm(self.request.GET)
        if form.is_valid():
            return Project.objects.filter(name__icontains=form.cleaned_data["name"])
        return Project.objects.all()



class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(
            "project_type").select_related("team")


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = "__all__"
    template_name = "management/project_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:project-detail", kwargs={"pk": self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"
    template_name = "management/project_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy("management:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("management:project-list")
    template_name = "management/project_confirm_delete.html"
