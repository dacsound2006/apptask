from datetime import date, timedelta
from django.db.models import Count, Avg, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filterset_fields = ["project", "phase", "status", "owner"]
    search_fields = ["code", "name", "owner", "phase"]
    ordering_fields = ["due", "code", "progress", "status", "phase", "name"]

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        qs = Task.objects.all()
        today = date.today()
        week = today + timedelta(days=7)
        total = qs.count()
        done = qs.filter(status="done").count()
        inprog = qs.filter(status="in_progress").count()
        late = qs.exclude(status="done").filter(due__lt=today).count()
        pending = qs.filter(status="pending").exclude(due__lt=today).count()
        this_week = qs.exclude(status="done").filter(due__gte=today, due__lte=week).count()
        avg = qs.aggregate(a=Avg("progress"))["a"] or 0

        by_phase = list(
            qs.values("phase").annotate(
                total=Count("id"), avg=Avg("progress")
            ).order_by("phase")
        )
        deadlines = {"PRIV": date(2026, 7, 1), "PUB": date(2026, 7, 31)}
        by_project = []
        for code, label in Task.PROJECT:
            pq = qs.filter(project=code)
            ptot = pq.count()
            if not ptot:
                continue
            by_project.append({
                "project": code,
                "label": label,
                "total": ptot,
                "done": pq.filter(status="done").count(),
                "late": pq.exclude(status="done").filter(due__lt=today).count(),
                "pct": round(pq.aggregate(a=Avg("progress"))["a"] or 0, 1),
                "deadline": deadlines[code].isoformat(),
                "days_left": (deadlines[code] - today).days,
            })
        return Response({
            "total": total, "done": done, "in_progress": inprog,
            "late": late, "pending": pending, "this_week": this_week,
            "pct": round(avg, 1),
            "priv": qs.filter(project="PRIV").count(),
            "pub": qs.filter(project="PUB").count(),
            "by_phase": by_phase, "by_project": by_project,
        })

    @action(detail=False, methods=["get"])
    def critical(self, request):
        """Calcula tareas críticas y recomendaciones accionables.
        Criticidad por: atraso, nº de tareas que dependen de ella (bloqueo),
        y cercanía/desfase frente al cierre del proyecto."""
        today = date.today()
        deadlines = {"PRIV": date(2026, 7, 1), "PUB": date(2026, 7, 31)}
        tasks = list(Task.objects.all())

        # cuántas tareas dependen de cada código (impacto de bloqueo)
        blockers = {}
        for t in tasks:
            for dep in [d.strip() for d in (t.depends or "").split(",") if d.strip()]:
                blockers[dep] = blockers.get(dep, 0) + 1

        scored = []
        for t in tasks:
            if t.status == "done":
                continue
            score = 0
            reasons = []
            days_over = (today - t.due).days
            if days_over > 0:
                score += 40 + min(days_over, 30)
                reasons.append(f"atrasada {days_over} día(s)")
            blocks = blockers.get(t.code, 0)
            if blocks:
                score += blocks * 15
                reasons.append(f"bloquea {blocks} tarea(s)")
            dl = deadlines.get(t.project)
            days_to_dl = (dl - today).days
            if days_to_dl <= 21 and t.status != "done":
                score += 20
                reasons.append(f"cierre del proyecto en {days_to_dl} día(s)")
            if t.status == "pending" and days_over > 0:
                score += 10
                reasons.append("sin iniciar")
            if t.due > dl:
                score += 25
                reasons.append("vence después del cierre del proyecto")
            if score > 0:
                scored.append({
                    "code": t.code, "name": t.name, "project": t.project,
                    "phase": t.phase, "owner": t.owner, "due": t.due.isoformat(),
                    "status": t.status, "progress": t.progress,
                    "blocks": blocks, "score": score, "reasons": reasons,
                })
        scored.sort(key=lambda x: x["score"], reverse=True)

        # recomendaciones agregadas
        recs = []
        late_qs = [s for s in scored if "atrasada" in " ".join(s["reasons"])]
        if late_qs:
            top = late_qs[0]
            recs.append({
                "level": "alta",
                "text": f"Priorizar {len(late_qs)} tarea(s) atrasada(s). La más crítica es {top['code']} "
                        f"({top['name']}), responsable {top['owner'] or 'sin asignar'}.",
            })
        big_blockers = [s for s in scored if s["blocks"] >= 2]
        if big_blockers:
            recs.append({
                "level": "alta",
                "text": f"Desbloquear cuanto antes {', '.join(b['code'] for b in big_blockers[:3])}: "
                        f"habilitan múltiples tareas dependientes.",
            })
        over_dl = [s for s in scored if "después del cierre" in " ".join(s["reasons"])]
        if over_dl:
            recs.append({
                "level": "media",
                "text": f"{len(over_dl)} tarea(s) vencen después del cierre comprometido. "
                        f"Revisar reprogramación o recursos adicionales.",
            })
        for code, label in Task.PROJECT:
            pend = [t for t in tasks if t.project == code and t.status != "done"]
            dl = deadlines[code]
            days_to_dl = (dl - today).days
            if pend and days_to_dl >= 0:
                recs.append({
                    "level": "media" if days_to_dl > 14 else "alta",
                    "text": f"{label}: {len(pend)} tarea(s) abiertas y {days_to_dl} día(s) para el cierre "
                            f"({dl.isoformat()}). Mantener el ritmo de cierre semanal.",
                })
        if not scored:
            recs.append({"level": "ok", "text": "Sin tareas críticas. El plan está al día."})

        return Response({"critical": scored[:12], "count": len(scored), "recommendations": recs})

    @action(detail=False, methods=["get"])
    def week(self, request):
        today = date.today()
        week = today + timedelta(days=7)
        qs = self.queryset.exclude(status="done").filter(due__gte=today, due__lte=week)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["get"])
    def late(self, request):
        qs = self.queryset.exclude(status="done").filter(due__lt=date.today())
        return Response(self.get_serializer(qs, many=True).data)
