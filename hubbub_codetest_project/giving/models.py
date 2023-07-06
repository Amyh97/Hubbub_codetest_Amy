import logging

from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.utils.text import slugify

LOG = logging.getLogger(__name__)


class AuditModelMixin(models.Model):
    AUDIT_MODEL_UPDATE_FIELDS = ["created", "modified"]
    created = models.DateTimeField(blank=True, default=timezone.now)
    modified = models.DateTimeField(blank=True, default=timezone.now)

    class Meta:
        abstract = True
        get_latest_by = "modified"
        ordering = ("-modified", "-created")

    def save(self, *args, **kwargs):
        try:
            # don't allow update_fields to bypass these audit fields
            update_fields = kwargs.get("update_fields", None) + self.AUDIT_MODEL_UPDATE_FIELDS
        except TypeError:
            pass
        else:
            kwargs.update({"update_fields": update_fields})

        now = timezone.now()
        if not self.id:
            self.created = now
        self.modified = now

        super().save(*args, **kwargs)


class Project(AuditModelMixin):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title

    def total(self):
        value = self.projectpledge_set.aggregate(Sum("amount")).get("amount__sum", 0)
        return value or 0

    def save(self, *args, **kwargs):
        if not self.pk or not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class ProjectPledge(AuditModelMixin):
    HOUSE_CHOICES = (
        ("Gryffindor", "Gryffindor"),
        ("Hufflepuff", "Hufflepuff"),
        ("Ravenclaw", "Ravenclaw"),
        ("Slytherin", "Slytherin"),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    pledgee = models.CharField(max_length=250, blank=True, help_text="Name you wish to pledge under")
    house_choices = models.CharField(
        choices=HOUSE_CHOICES, max_length=50, help_text="School house you want to support", blank=True
    )

    def __str__(self):
        return f"Pledge of £{self.amount} for {self.project.title}"
