from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    is_late = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = ["id", "code", "project", "phase", "name", "owner", "layer",
                  "start", "due", "status", "progress", "depends", "is_late",
                  "created", "updated"]
