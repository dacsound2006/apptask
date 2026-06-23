<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import api from "./api";
import Chart from "chart.js/auto";
import KpiCard from "./components/KpiCard.vue";
import TaskTable from "./components/TaskTable.vue";
import TaskModal from "./components/TaskModal.vue";
import GanttChart from "./components/GanttChart.vue";
import ProgressPanel from "./components/ProgressPanel.vue";
import CriticalPanel from "./components/CriticalPanel.vue";

const tasks = ref([]);
const dash = ref({});
const crit = ref({ critical: [], recommendations: [], count: 0 });
const tab = ref("dashboard");
const filter = ref({ q: "", project: "all", phase: "all", kpi: "all" });
const modal = ref({ open: false, isNew: false, task: {} });
const cPhase = ref(null), cStatus = ref(null);
let chPhase = null, chStatus = null;

const today = new Date("2026-06-17T12:00:00");
const todayLabel = today.toLocaleDateString("es-CO", {
  weekday: "long", year: "numeric", month: "long", day: "numeric" });

async function load() {
  tasks.value = await api.list();
  dash.value = await api.dashboard();
  crit.value = await api.critical();
  await nextTick();
  draw();
}

const phases = computed(() => [...new Set(tasks.value.map((t) => t.phase))]);

const filtered = computed(() => {
  let r = tasks.value.slice();
  const f = filter.value;
  if (f.project !== "all") r = r.filter((t) => t.project === f.project);
  if (f.phase !== "all") r = r.filter((t) => t.phase === f.phase);
  if (f.kpi === "late") r = r.filter((t) => t.is_late);
  else if (f.kpi === "week") r = r.filter((t) => inWeek(t));
  else if (f.kpi === "pending") r = r.filter((t) => t.status === "pending" && !t.is_late);
  else if (f.kpi === "in_progress") r = r.filter((t) => t.status === "in_progress");
  else if (f.kpi === "done") r = r.filter((t) => t.status === "done");
  if (f.q) {
    const q = f.q.toLowerCase();
    r = r.filter((t) => (t.name + t.owner + t.code + t.phase).toLowerCase().includes(q));
  }
  return r;
});

function daysTo(d) { return Math.ceil((new Date(d + "T12:00:00") - today) / 86400000); }
function inWeek(t) { return t.status !== "done" && daysTo(t.due) >= 0 && daysTo(t.due) <= 7; }
function setKpi(k) { filter.value.kpi = filter.value.kpi === k ? "all" : k; }

function openNew() {
  modal.value = { open: true, isNew: true, task: {
    code: "NEW-" + (tasks.value.length + 1), project: "PRIV", phase: "", name: "",
    owner: "", layer: "", start: "2026-06-17", due: "2026-06-24",
    status: "pending", progress: 0, depends: "" } };
}
function openEdit(t) { modal.value = { open: true, isNew: false, task: { ...t } }; }

async function save(t) {
  if (t.status === "done") t.progress = 100;
  if (modal.value.isNew) await api.create(t);
  else await api.update(t.id, t);
  modal.value.open = false;
  await load();
}
async function del(t) {
  if (confirm("Eliminar " + t.code + "?")) { await api.remove(t.id); await load(); }
}
async function cycleStatus(t) {
  const seq = ["pending", "in_progress", "done"];
  const ns = seq[(seq.indexOf(t.status) + 1) % 3];
  await api.update(t.id, { status: ns, progress: ns === "done" ? 100 : ns === "in_progress" ? (t.progress || 50) : 0 });
  await load();
}
function exportCSV() {
  const h = ["code","project","phase","name","owner","start","due","status","progress"];
  const rows = [h.join(",")].concat(filtered.value.map((t) =>
    h.map((k) => '"' + ("" + t[k]).replace(/"/g, '""') + '"').join(",")));
  const blob = new Blob([rows.join("\n")], { type: "text/csv" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob); a.download = "tareas_dualcloud.csv"; a.click();
}

function css(v) { return getComputedStyle(document.documentElement).getPropertyValue(v).trim(); }
function draw() {
  if (!cPhase.value || !cStatus.value) return;
  const order = ["Iniciación","Diseño","Impl. KIO","Impl. ILKARI","Casos de uso","Cierre","Implementación","Pruebas","Go-live"];
  const ph = (dash.value.by_phase || []).slice().sort((a, b) => order.indexOf(a.phase) - order.indexOf(b.phase));
  if (chPhase) chPhase.destroy();
  chPhase = new Chart(cPhase.value, {
    type: "bar",
    data: { labels: ph.map((p) => p.phase), datasets: [{
      label: "% avance", data: ph.map((p) => Math.round(p.avg)),
      backgroundColor: ph.map((p) => (Math.round(p.avg) === 100 ? css("--ok") : css("--info"))),
      borderRadius: 5 }] },
    options: { indexAxis: "y", responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false },
        tooltip: { callbacks: { afterLabel: (c) => ph[c.dataIndex].total + " tareas" } } },
      scales: { x: { max: 100, grid: { color: css("--line") }, ticks: { color: css("--dim"), callback: (v) => v + "%" } },
        y: { grid: { display: false }, ticks: { color: css("--mut"), font: { size: 11 } } } } },
  });
  if (chStatus) chStatus.destroy();
  const d = dash.value;
  chStatus = new Chart(cStatus.value, {
    type: "doughnut",
    data: { labels: ["Completadas", "En curso", "Pendientes", "Atrasadas"],
      datasets: [{ data: [d.done, d.in_progress, d.pending, d.late],
        backgroundColor: [css("--ok"), css("--info"), css("--warn"), css("--danger")],
        borderColor: css("--panel"), borderWidth: 3 }] },
    options: { responsive: true, maintainAspectRatio: false, cutout: "62%",
      plugins: { legend: { position: "bottom",
        labels: { color: css("--mut"), padding: 14, font: { size: 11 }, usePointStyle: true } } } },
  });
}

onMounted(load);

function goTab(t) {
  tab.value = t;
  if (t === "dashboard") nextTick(draw);
}
</script>

<template>
  <div class="wrap">
    <header>
      <div class="brand">
        <div class="logo">IX</div>
        <div><h1>Control de Tareas · Despliegue Dual Cloud</h1>
        <p>INTERNEXA · Arquitectura de Portafolio · Django + Vue</p></div>
      </div>
      <div class="clock">
        <div class="d">{{ todayLabel }}</div>
        <div class="t">Privado → 01 jul · Público → 31 jul 2026</div>
      </div>
    </header>

    <div class="kpis">
      <KpiCard cls="k-total" label="Total tareas" :val="dash.total" :sub="`${dash.priv} priv · ${dash.pub} púb`"
        :active="filter.kpi==='all'" @click="setKpi('all')" />
      <KpiCard cls="k-week" label="Esta semana" :val="dash.this_week" sub="vencen 7 días"
        :active="filter.kpi==='week'" @click="setKpi('week')" />
      <KpiCard cls="k-late" label="Atrasadas" :val="dash.late" sub="venc. < hoy"
        :active="filter.kpi==='late'" @click="setKpi('late')" />
      <KpiCard cls="k-pend" label="Pendientes" :val="dash.pending" sub="sin iniciar"
        :active="filter.kpi==='pending'" @click="setKpi('pending')" />
      <KpiCard cls="k-prog" label="En curso" :val="dash.in_progress" sub="activas"
        :active="filter.kpi==='in_progress'" @click="setKpi('in_progress')" />
      <KpiCard cls="k-done" label="Completadas" :val="dash.done" :sub="`${dash.pct}% avance`"
        :active="filter.kpi==='done'" @click="setKpi('done')" />
    </div>

    <ProgressPanel :by-project="dash.by_project || []" :overall="dash.pct || 0" />

    <div class="tabs">
      <button :class="{on:tab==='dashboard'}" @click="goTab('dashboard')">Dashboard</button>
      <button :class="{on:tab==='gantt'}" @click="goTab('gantt')">Gantt</button>
      <button :class="{on:tab==='critical'}" @click="goTab('critical')">Críticas y recomendaciones</button>
    </div>

    <template v-if="tab==='dashboard'">
    <div class="grid2">
      <div class="card"><h2><span class="dot"></span>Avance por fase</h2>
        <div class="chart-box tall"><canvas ref="cPhase"></canvas></div></div>
      <div class="card"><h2><span class="dot"></span>Estado general</h2>
        <div class="chart-box"><canvas ref="cStatus"></canvas></div></div>
    </div>

    <TaskTable :tasks="filtered" :total="tasks.length" :phases="phases" v-model:filter="filter"
      @new="openNew" @edit="openEdit" @cycle="cycleStatus" @del="del" @export="exportCSV" />
    </template>

    <GanttChart v-else-if="tab==='gantt'" :tasks="tasks" />

    <CriticalPanel v-else-if="tab==='critical'" :data="crit" />

    <div class="footer">Conectado al backend Django REST · {{ tasks.length }} tareas · fuente única tasks_seed.json</div>

    <TaskModal v-if="modal.open" :data="modal" :phases="phases"
      @save="save" @close="modal.open=false" />
  </div>
</template>

<style>
:root{
  --bg:#0a0f1a;--panel:#111a2b;--panel2:#0e1626;--line:#1f2d44;
  --ink:#e6edf6;--mut:#8398b8;--dim:#5a6f8f;
  --priv:#34d399;--priv-d:#10583f;--pub:#a78bfa;--pub-d:#3b2a63;
  --warn:#fb923c;--danger:#f87171;--ok:#34d399;--info:#60a5fa;
  --mono:'SF Mono',ui-monospace,'Cascadia Code',Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;
  background-image:radial-gradient(circle at 20% -10%,rgba(52,211,153,.06),transparent 40%),
                   radial-gradient(circle at 90% 0%,rgba(167,139,250,.06),transparent 40%);min-height:100vh}
.wrap{max-width:1400px;margin:0 auto;padding:20px}
header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;
  padding:18px 22px;background:linear-gradient(135deg,var(--panel),var(--panel2));
  border:1px solid var(--line);border-radius:14px;margin-bottom:18px}
.brand{display:flex;align-items:center;gap:14px}
.logo{width:42px;height:42px;border-radius:10px;background:linear-gradient(135deg,var(--priv),var(--info));
  display:grid;place-items:center;font-weight:800;color:#04121c;font-size:18px;letter-spacing:-1px}
.brand h1{font-size:17px;font-weight:700;letter-spacing:-.3px}
.brand p{font-size:11px;color:var(--mut);font-family:var(--mono);text-transform:uppercase;letter-spacing:1px;margin-top:2px}
.clock{text-align:right;font-family:var(--mono)}
.clock .d{font-size:12px;color:var(--mut)}.clock .t{font-size:13px;color:var(--info);font-weight:600}
.kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:18px}
.tabs{display:flex;gap:6px;margin:18px 0;background:var(--panel2);border:1px solid var(--line);border-radius:11px;padding:5px;width:fit-content}
.tabs button{background:none;border:none;color:var(--mut);padding:9px 18px;font-size:13px;font-weight:600;cursor:pointer;border-radius:8px;font-family:var(--sans)}
.tabs button.on{background:var(--info);color:#04121c}
.tabs button:hover:not(.on){color:var(--ink)}
.grid2{display:grid;grid-template-columns:1.3fr 1fr;gap:16px;margin-bottom:18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px}
.card h2{font-size:13px;text-transform:uppercase;letter-spacing:.8px;color:var(--mut);margin-bottom:14px;font-weight:700;display:flex;align-items:center;gap:8px}
.card h2 .dot{width:7px;height:7px;border-radius:50%;background:var(--info)}
.chart-box{position:relative;height:240px}.chart-box.tall{height:300px}
.footer{text-align:center;color:var(--dim);font-size:11px;font-family:var(--mono);padding:20px}
@media(max-width:1000px){.kpis{grid-template-columns:repeat(3,1fr)}.grid2{grid-template-columns:1fr}}
@media(max-width:560px){.kpis{grid-template-columns:repeat(2,1fr)}}
</style>
