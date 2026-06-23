from django.db import models
from datetime import date

class Task(models.Model):
    PROJECT = [("PRIV", "Cloud Privado"), ("PUB", "Cloud Público")]
    STATUS = [("pending", "Pendiente"), ("in_progress", "En curso"), ("done", "Completada")]

    code = models.CharField(max_length=20, unique=True)
    project = models.CharField(max_length=4, choices=PROJECT)
    phase = models.CharField(max_length=40)
    name = models.CharField(max_length=200)
    owner = models.CharField(max_length=60, blank=True)
    layer = models.CharField(max_length=40, blank=True)
    start = models.DateField()
    due = models.DateField()
    status = models.CharField(max_length=12, choices=STATUS, default="pending")
    progress = models.PositiveSmallIntegerField(default=0)
    depends = models.CharField(max_length=80, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due", "code"]

    def __str__(self):
        return f"{self.code} · {self.name}"

    @property
    def is_late(self):
        return self.status != "done" and self.due < date.today()

    def save(self, *args, **kwargs):
        if self.status == "done":
            self.progress = 100
        super().save(*args, **kwargs)
