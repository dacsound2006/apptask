<script setup>
import { ref, computed } from "vue";
const props = defineProps({ tasks: Array, total: Number, phases: Array, filter: Object });
const emit = defineEmits(["new", "edit", "cycle", "del", "export", "update:filter"]);
const sort = ref({ key: "due", dir: 1 });
const stLabels = { pending: "Pendiente", in_progress: "En curso", done: "Completada" };

const sorted = computed(() => {
  const r = props.tasks.slice();
  r.sort((a, b) => {
    let x = a[sort.value.key], y = b[sort.value.key];
    if (typeof x === "string") { x = x.toLowerCase(); y = (y || "").toLowerCase(); }
    return (x > y ? 1 : x < y ? -1 : 0) * sort.value.dir;
  });
  return r;
});
function sortBy(k) { if (sort.value.key === k) sort.value.dir *= -1; else sort.value = { key: k, dir: 1 }; }
function upd(k, v) { emit("update:filter", { ...props.filter, [k]: v }); }
function barColor(t) {
  return t.is_late ? "var(--danger)" : t.status === "done" ? "var(--ok)" : t.status === "in_progress" ? "var(--info)" : "var(--warn)";
}
</script>
<template>
  <div class="card">
    <h2><span class="dot"></span>Tareas
      <span style="color:var(--dim);font-weight:400;text-transform:none;letter-spacing:0">— {{ tasks.length }} de {{ total }}</span></h2>
    <div class="toolbar">
      <input type="search" :value="filter.q" @input="upd('q',$event.target.value)" placeholder="Buscar tarea, responsable, código…">
      <div class="seg">
        <button :class="{on:filter.project==='all'}" @click="upd('project','all')">Todos</button>
        <button :class="{on:filter.project==='PRIV'}" @click="upd('project','PRIV')">Privado</button>
        <button :class="{on:filter.project==='PUB'}" @click="upd('project','PUB')">Público</button>
      </div>
      <select :value="filter.phase" @change="upd('phase',$event.target.value)">
        <option value="all">Todas las fases</option>
        <option v-for="p in phases" :key="p" :value="p">{{ p }}</option>
      </select>
      <button class="btn" @click="$emit('new')">+ Nueva tarea</button>
      <button class="btn ghost" @click="$emit('export')">Exportar CSV</button>
    </div>
    <table>
      <thead><tr>
        <th @click="sortBy('code')">Código</th><th>Proy</th>
        <th @click="sortBy('name')">Tarea</th><th @click="sortBy('phase')">Fase</th>
        <th @click="sortBy('owner')">Responsable</th><th @click="sortBy('due')">Vence</th>
        <th @click="sortBy('progress')">Avance</th><th @click="sortBy('status')">Estado</th><th></th>
      </tr></thead>
      <tbody>
        <tr v-for="t in sorted" :key="t.id" :class="{'late-row':t.is_late}">
          <td class="code">{{ t.code }}</td>
          <td><span class="pj" :class="t.project">{{ t.project==='PRIV'?'PRIV':'PÚB' }}</span></td>
          <td>{{ t.name }}</td>
          <td style="color:var(--mut)">{{ t.phase }}</td>
          <td style="color:var(--mut)">{{ t.owner }}</td>
          <td class="code" :style="{color:t.is_late?'var(--danger)':'var(--mut)'}">{{ t.due }}</td>
          <td><span class="prog"><i :style="{width:t.progress+'%',background:barColor(t)}"></i></span>
            <span class="code" style="margin-left:6px">{{ t.progress }}%</span></td>
          <td><span class="tag" :class="t.is_late?'st-late':'st-'+t.status">{{ t.is_late?'Atrasada':stLabels[t.status] }}</span></td>
          <td><div class="row-act">
            <button class="icon" @click="$emit('edit',t)" title="Editar">✎</button>
            <button class="icon" @click="$emit('cycle',t)" title="Cambiar estado">⟳</button>
            <button class="icon" @click="$emit('del',t)" title="Eliminar">✕</button>
          </div></td>
        </tr>
        <tr v-if="!tasks.length"><td colspan="9"><div class="empty">Sin tareas para este filtro</div></td></tr>
      </tbody>
    </table>
  </div>
</template>
<style scoped>
.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
.toolbar input,.toolbar select{background:var(--panel2);border:1px solid var(--line);color:var(--ink);padding:9px 12px;border-radius:9px;font-size:13px;outline:none}
.toolbar input:focus,.toolbar select:focus{border-color:var(--info)}
.toolbar input[type=search]{flex:1;min-width:180px}
.seg{display:flex;background:var(--panel2);border:1px solid var(--line);border-radius:9px;overflow:hidden}
.seg button{background:none;border:none;color:var(--mut);padding:9px 14px;font-size:12px;font-weight:600;cursor:pointer}
.seg button.on{background:var(--info);color:#04121c}
.btn{background:var(--info);color:#04121c;border:none;padding:10px 16px;border-radius:9px;font-weight:700;font-size:13px;cursor:pointer}
.btn:hover{filter:brightness(1.1)}.btn.ghost{background:var(--panel2);color:var(--ink);border:1px solid var(--line)}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;padding:10px 12px;font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim);border-bottom:1px solid var(--line);font-weight:700;cursor:pointer;white-space:nowrap}
th:hover{color:var(--ink)}
td{padding:11px 12px;border-bottom:1px solid var(--panel2);vertical-align:middle}
tr:hover td{background:var(--panel2)}
.code{font-family:var(--mono);font-size:12px;color:var(--mut)}
.pj{font-family:var(--mono);font-size:10px;font-weight:700;padding:3px 7px;border-radius:5px}
.pj.PRIV{background:var(--priv-d);color:var(--priv)}.pj.PUB{background:var(--pub-d);color:var(--pub)}
.tag{font-size:10px;padding:3px 8px;border-radius:20px;font-weight:600;white-space:nowrap}
.st-done{background:rgba(52,211,153,.15);color:var(--ok)}
.st-in_progress{background:rgba(96,165,250,.15);color:var(--info)}
.st-pending{background:rgba(251,146,60,.15);color:var(--warn)}
.st-late{background:rgba(248,113,113,.15);color:var(--danger)}
.prog{height:6px;width:80px;background:var(--panel2);border-radius:6px;overflow:hidden;display:inline-block;vertical-align:middle}
.prog i{display:block;height:100%;border-radius:6px}
.late-row td{box-shadow:inset 3px 0 0 var(--danger)}
.row-act{display:flex;gap:6px}
.icon{background:var(--panel2);border:1px solid var(--line);color:var(--mut);width:30px;height:30px;border-radius:7px;cursor:pointer;font-size:13px;display:grid;place-items:center}
.icon:hover{color:var(--ink);border-color:var(--info)}
.empty{text-align:center;color:var(--dim);padding:40px;font-family:var(--mono)}
</style>
