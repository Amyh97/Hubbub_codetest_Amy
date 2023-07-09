from django.urls import path
from django.views.generic import TemplateView

from .views import DonorWall, LeaderboardView, PledgeView, ProjectDetailView, ProjectListView, ProjectUpdateView
app_name = "giving"
urlpatterns = [
    path("", ProjectListView.as_view(), name="project-list"),
    path("donor-wall/", DonorWall.as_view(), name="donor-wall"),
    path("<str:slug>/", ProjectDetailView.as_view(), name="project-detail"),
    path("<str:slug>/leaderboard/", LeaderboardView.as_view(), name="project-leaderboard"),
    path("<str:slug>/pledge/", PledgeView.as_view(), name="pledge"),
    path("<str:slug>/pledge/thanks/", TemplateView.as_view(template_name="giving/thanks.html"), name="pledge-thanks"),
    path("<str:slug>/update", ProjectUpdateView.as_view(), name="project-update"),
]
