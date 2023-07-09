import logging

from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import FormView

from .forms import ProjectPledgeForm, AddProjectForm
from .models import Project, ProjectPledge

log = logging.getLogger(__name__)


class PledgeView(FormView):
    form_class = ProjectPledgeForm
    template_name = "giving/project_detail.html"

    def get_success_url(self):
        slug = self.kwargs.get("slug")
        if slug:
            url = reverse("giving:pledge-thanks", kwargs={"slug": slug})
        else:
            url = reverse("giving:project-list")
        return url

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get("slug")
        try:
            context["project"] = Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            log.warn("Project {slug} doesn't exist")
        return context


class ProjectListView(ListView):
    template_name = "giving/project_list.html"
    model = Project


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        initial_data = {"project": context.get("project")}
        if not self.request.user.is_anonymous:
            initial_data["pledgee"] = self.request.user
        context["form"] = ProjectPledgeForm(data=initial_data)
        return context


class LeaderboardView(DetailView):
    model = Project
    template_name = "giving/project_leaderboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = context.get("project")

        if project:
            context["leaderboard_amount"] = (
                project.projectpledge_set.values("house_choices").annotate(Sum("amount")).order_by("-amount__sum")
            )
            context["leaderboard_count"] = (
                project.projectpledge_set.values("house_choices").annotate(Count("amount")).order_by("-amount__count")
            )
        return context


class DonorWall(ListView):
    template_name = "giving/donor_wall.html"
    model = ProjectPledge
    paginate_by = 30

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ["title", "description"]

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)

        project_id = Project.objects.get(title=context.get("project"))

        project = get_object_or_404(Project, pk=project_id.id)
        initial_data = {"title": context.get("project"),
                        "description": project.description,}
        context["form"] = AddProjectForm(data=initial_data)
        return context
    
    def get_success_url(self):
        url = reverse("giving:project-list")
        return url
