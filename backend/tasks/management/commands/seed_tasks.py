import json
from pathlib import Path
from django.core.management.base import BaseCommand
from tasks.models import Task

class Command(BaseCommand):
    help = "Carga las tareas del plan dual cloud desde tasks_seed.json"

    def handle(self, *args, **opts):
        path = Path(__file__).parent / "tasks_seed.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        created, updated = 0, 0
        for row in data:
            obj, was_created = Task.objects.update_or_create(
                code=row["code"],
                defaults={
                    "project": row["project"], "phase": row["phase"],
                    "name": row["name"], "owner": row["owner"],
                    "layer": row.get("layer", ""), "start": row["start"],
                    "due": row["due"], "status": row["status"],
                    "progress": row["progress"], "depends": row.get("depends", ""),
                },
            )
            created += was_created
            updated += not was_created
        self.stdout.write(self.style.SUCCESS(
            f"Tareas cargadas: {created} creadas, {updated} actualizadas (total {len(data)})"))
