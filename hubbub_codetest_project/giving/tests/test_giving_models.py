import pytest
from django.utils.text import slugify

from hubbub_codetest_project.giving.models import Project, ProjectPledge


@pytest.mark.django_db
class TestProjectModel:
    def test_slugify(self):
        proj = Project(title="My new project", description="My new project")
        assert proj.slug == ""
        proj.save()
        proj.refresh_from_db()

        assert proj.slug == slugify(proj.title)

    def test_total(self):
        pledge_count = 3
        pledge_amount = 10
        proj = Project.objects.create(title="My new project", description="My new project")
        for x in range(pledge_count):
            proj.projectpledge_set.create(
                amount=pledge_amount, pledgee=f"Pledger {x}", house_choices=ProjectPledge.HOUSE_CHOICES[0][0]
            )

        assert proj.total() == pledge_count * pledge_amount

    def test_cache_key(self):
        proj = Project.objects.create(title="My new project", description="My new project")
        assert proj.cache_key() == f"project-total-{proj.pk}-{proj.slug}"
