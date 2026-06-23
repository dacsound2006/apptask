<script setup>
import { computed, ref } from "vue";
const props = defineProps({ tasks: Array });
const today = new Date("2026-06-17T12:00:00");

// rango temporal: enero 2026 -> 31 jul 2026
const start = new Date("2026-01-01T00:00:00");
const end = new Date("2026-07-31T23:59:59");
const totalDays = (end - start) / 86400000;

const groupBy = ref("phase"); // phase | project

const rows = computed(() => {
  const r = props.tasks.filter((t) => t.start && t.due);
  return r.slice().sort((a, b) => new Date(a.start) - new Date(b.start));
});

// meses para el encabezado
const months = computed(() => {
  const out = [];
  let d = new Date(start);
  while (d <= end) {
    const next = new Date(d.getFullYear(), d.getMonth() + 1, 1);
    const segEnd = next > end ? end : next;
    const left = ((d - start) / 86400000 / totalDays) * 100;
    const width = ((segEnd - d) / 86400000 / totalDays) * 100;
    out.push({ label: d.toLocaleDateString("es-CO", { month: "short" }), left, width });
    d = next;
  }
  return out;
});

function bar(t) {
  const s = new Date(t.start + "T00:00:00");
  const e = new Date(t.due + "T23:59:59");
  const left = Math.max(0, ((s - start) / 86400000 / totalDays) * 100);
  const width = Math.max(1.2, ((e - s) / 86400000 / totalDays) * 100);
  return { left: left + "%", width: width + "%" };
}
function barClass(t) {
  if (t.is_late) return "b-late";
  if (t.status === "done") return "b-done";
  if (t.status === "in_progress") return "b-prog";
  return "b-pend";
}
const todayLeft = computed(() => ((today - start) / 86400000 / totalDays) * 100 + "%");
// líneas de cierre
const privLine = computed(() => ((new Date("2026-07-01") - start) / 86400000 / totalDays) * 100 + "%");
const pubLine = computed(() => ((new Date("2026-07-31") - start) / 86400000 / totalDays) * 100 + "%");
</script>

<template>
  <div class="card">
    <h2><span class="dot"></span>Cronograma Gantt
      <span class="legend">
        <i class="b-done"></i>Completada <i class="b-prog"></i>En curso
        <i class="b-pend"></i>Pendiente <i class="b-late"></i>Atrasada
      </span>
    </h2>
    <div class="gantt">
      <div class="g-head">
        <div class="g-label-col">Tarea</div>
        <div class="g-timeline">
          <div v-for="(m,i) in months" :key="i" class="g-month"
            :style="{left:m.left+'%',width:m.width+'%'}">{{ m.label }}</div>
        </div>
      </div>
      <div class="g-body">
        <div class="g-today" :style="{left:todayLeft}" title="Hoy 17-jun"></div>
        <div class="g-deadline priv" :style="{left:privLine}" title="Cierre privado 01-jul"></div>
        <div class="g-deadline pub" :style="{left:pubLine}" title="Cierre público 31-jul"></div>
        <div v-for="t in rows" :key="t.id" class="g-row">
          <div class="g-label-col">
            <span class="pj" :class="t.project">{{ t.project==='PRIV'?'PR':'PB' }}</span>
            <span class="g-code">{{ t.code }}</span>
            <span class="g-name">{{ t.name }}</span>
          </div>
          <div class="g-track">
            <div class="g-bar" :class="barClass(t)" :style="bar(t)">
              <span class="g-pct" v-if="t.progress">{{ t.progress }}%</span>
              <i class="g-fill" :style="{width:t.progress+'%'}"></i>
            </div>
          </div>
        </div>
        <div v-if="!rows.length" class="empty">Sin tareas para mostrar</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.legend{margin-left:auto;font-weight:400;text-transform:none;letter-spacing:0;font-size:11px;color:var(--mut);display:flex;align-items:center;gap:6px}
.legend i{width:12px;height:10px;border-radius:3px;display:inline-block;margin-left:8px}
.b-done{background:var(--ok)}.b-prog{background:var(--info)}.b-pend{background:var(--warn)}.b-late{background:var(--danger)}
.gantt{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
.g-head{display:flex;position:sticky;top:0;background:var(--panel2);border-bottom:1px solid var(--line);z-index:3}
.g-label-col{width:300px;min-width:300px;padding:8px 12px;font-size:11px;color:var(--dim);display:flex;align-items:center;gap:7px}
.g-timeline{position:relative;flex:1;height:30px;min-width:560px}
.g-month{position:absolute;top:0;height:30px;border-left:1px solid var(--line);font-size:10px;color:var(--mut);padding:8px 0 0 5px;text-transform:uppercase;letter-spacing:.5px}
.g-body{position:relative}
.g-row{display:flex;border-bottom:1px solid var(--panel2);min-height:34px;align-items:center}
.g-row:hover{background:var(--panel2)}
.g-code{font-family:var(--mono);font-size:11px;color:var(--mut);white-space:nowrap}
.g-name{font-size:12px;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.g-track{position:relative;flex:1;height:34px;min-width:560px}
.g-bar{position:absolute;top:7px;height:20px;border-radius:5px;display:flex;align-items:center;overflow:hidden;opacity:.9}
.g-bar.b-done{background:rgba(52,211,153,.25)}
.g-bar.b-prog{background:rgba(96,165,250,.25)}
.g-bar.b-pend{background:rgba(251,146,60,.25)}
.g-bar.b-late{background:rgba(248,113,113,.3)}
.g-fill{position:absolute;left:0;top:0;height:100%;border-radius:5px;opacity:.7}
.b-done .g-fill{background:var(--ok)}.b-prog .g-fill{background:var(--info)}
.b-pend .g-fill{background:var(--warn)}.b-late .g-fill{background:var(--danger)}
.g-pct{position:relative;z-index:2;font-size:9px;font-family:var(--mono);color:var(--ink);padding-left:5px;font-weight:700}
.pj{font-family:var(--mono);font-size:9px;font-weight:700;padding:2px 5px;border-radius:4px}
.pj.PRIV{background:var(--priv-d);color:var(--priv)}.pj.PUB{background:var(--pub-d);color:var(--pub)}
.g-today{position:absolute;top:0;bottom:0;width:2px;background:var(--info);z-index:2;box-shadow:0 0 6px var(--info)}
.g-deadline{position:absolute;top:0;bottom:0;width:0;border-left:2px dashed;z-index:2}
.g-deadline.priv{border-color:var(--priv)}.g-deadline.pub{border-color:var(--pub)}
.empty{text-align:center;color:var(--dim);padding:30px;font-family:var(--mono)}
</style>
