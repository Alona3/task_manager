from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, TaskType, Position, Worker, Team, Project, Tag
from .serializers import TaskSerializer, TaskTypeSerializer, PositionSerializer, WorkerSerializer, TeamSerializer, ProjectSerializer, TagSerializer
from django.http import JsonResponse


@login_required
def home_view(request):
    user = request.user
    completed_tasks = Task.objects.filter(assignees=user, is_completed=True)
    pending_tasks = Task.objects.filter(assignees=user, is_completed=False)
    tags = Tag.objects.all()
    tag_filter = request.GET.get('tag', '')

    if tag_filter:
        completed_tasks = completed_tasks.filter(tags__name=tag_filter)
        pending_tasks = pending_tasks.filter(tags__name=tag_filter)

    context = {
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'tags': tags,
        'tag_filter': tag_filter,
        'total_completed': completed_tasks.count(),
        'total_pending': pending_tasks.count(),
        'user_role': user.position.name if user.position else 'Worker',
    }

    return render(request, 'tasks/index.html', context)


@login_required
def worker_task_list(request):
    user = request.user
    completed_tasks = Task.objects.filter(assignees=user, is_completed=True)
    pending_tasks = Task.objects.filter(assignees=user, is_completed=False)

    context = {
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks
    }
    return render(request, 'tasks/worker_tasks.html', context)


@login_required
def completed_tasks(request):
    user = request.user
    tasks = Task.objects.filter(assignees=user, is_completed=True)
    return render(request, 'tasks/completed_tasks.html', {'tasks': tasks})


@login_required
def pending_tasks(request):
    user = request.user
    tasks = Task.objects.filter(assignees=user, is_completed=False)
    return render(request, 'tasks/pending_tasks.html', {'tasks': tasks})


@login_required
def task_detail(request, pk):
    task = Task.objects.get(id=pk)

    context = {
        'task': task,
        'assignees': task.assignees.all(),
        'project': task.project,
        'team': task.team,
        'tags': task.tags.all(),}

    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def ajax_task_list(request):
    user = request.user
    tag_filter = request.GET.get('tag', '')

    completed_tasks = Task.objects.filter(assignees=user, is_completed=True)
    pending_tasks = Task.objects.filter(assignees=user, is_completed=False)

    if tag_filter:
        completed_tasks = completed_tasks.filter(tags__name=tag_filter)
        pending_tasks = pending_tasks.filter(tags__name=tag_filter)

    data = {
        'completed_tasks': list(completed_tasks.values('id', 'name', 'due_date')),
        'pending_tasks': list(pending_tasks.values('id', 'name', 'due_date')),
    }

    return JsonResponse(data)


class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = Task.objects.all()
        tag_filter = self.request.GET.get('tag', '')

        if tag_filter:
            queryset = queryset.filter(tags__name=tag_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['tag_filter'] = self.request.GET.get('tag', '')
        context['total_tasks'] = self.get_queryset().count()
        return context


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["tags__name", "assignees__username", "project__name"]


class TaskTypeViewSet(viewsets.ModelViewSet):
    queryset = TaskType.objects.all()
    serializer_class = TaskTypeSerializer


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class ProjectTaskListView(ListView):
    model = Task
    template_name = "tasks/project_task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Task.objects.filter(project_id=project_id)


class TeamTaskListView(ListView):
    model = Task
    template_name = "tasks/team_task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return Task.objects.filter(team_id=team_id)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class WorkerTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/worker_tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["completed_tasks"] = self.get_queryset().filter(is_completed=True)
        context["pending_tasks"] = self.get_queryset().filter(is_completed=False)
        return context


class UserTaskListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)
