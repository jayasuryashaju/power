from django.db import models
from django.utils import timezone

class Visitor(models.Model):
    date = models.DateField(default=timezone.now)
    visit_count = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - Visits: {self.visit_count}, Unique Visitors: {self.unique_visitors}"
