<script setup>
defineProps({ data: Object });
const stLabels = { pending: "Pendiente", in_progress: "En curso", done: "Completada" };
</script>
<template>
  <div class="card">
    <h2><span class="dot danger"></span>Tareas críticas y recomendaciones
      <span class="count" v-if="data.count">{{ data.count }} críticas</span></h2>

    <div class="crit-grid">
      <div class="crit-list">
        <div class="sub-h">Tareas críticas (prioridad descendente)</div>
        <div v-for="t in data.critical" :key="t.code" class="crit-item">
          <div class="crit-row1">
            <span class="pj" :class="t.project">{{ t.project==='PRIV'?'PR':'PB' }}</span>
            <span class="crit-code">{{ t.code }}</span>
            <span class="crit-score" :class="t.score>=120?'sev-high':t.score>=70?'sev-mid':'sev-low'">{{ t.score }}</span>
          </div>
          <div class="crit-name">{{ t.name }}</div>
          <div class="crit-reasons">
            <span v-for="(r,i) in t.reasons" :key="i" class="reason">{{ r }}</span>
          </div>
          <div class="crit-meta">{{ t.owner || 'sin responsable' }} · vence {{ t.due }} · {{ stLabels[t.status] }}</div>
        </div>
        <div v-if="!data.critical || !data.critical.length" class="empty">Sin tareas críticas 🎉</div>
      </div>

      <div class="rec-list">
        <div class="sub-h">Recomendaciones a realizar</div>
        <div v-for="(r,i) in data.recommendations" :key="i" class="rec-item" :class="'lvl-'+r.level">
          <span class="rec-badge">{{ r.level }}</span>
          <span class="rec-text">{{ r.text }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.dot.danger{background:var(--danger)}
.count{margin-left:auto;font-weight:700;text-transform:none;letter-spacing:0;font-size:11px;color:var(--danger);font-family:var(--mono)}
.crit-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.sub-h{font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--dim);margin-bottom:10px;font-weight:700}
.crit-list{max-height:380px;overflow-y:auto;padding-right:6px}
.crit-item{background:var(--panel2);border:1px solid var(--line);border-left:3px solid var(--danger);border-radius:8px;padding:10px 12px;margin-bottom:8px}
.crit-row1{display:flex;align-items:center;gap:8px;margin-bottom:4px}
.crit-code{font-family:var(--mono);font-size:12px;color:var(--mut);font-weight:700}
.crit-score{margin-left:auto;font-family:var(--mono);font-size:11px;font-weight:700;padding:2px 8px;border-radius:5px}
.sev-high{background:rgba(248,113,113,.2);color:var(--danger)}
.sev-mid{background:rgba(251,146,60,.2);color:var(--warn)}
.sev-low{background:rgba(131,152,184,.2);color:var(--mut)}
.crit-name{font-size:13px;color:var(--ink);margin-bottom:6px}
.crit-reasons{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:5px}
.reason{font-size:10px;background:rgba(248,113,113,.12);color:var(--danger);padding:2px 7px;border-radius:20px}
.crit-meta{font-size:10px;font-family:var(--mono);color:var(--dim)}
.pj{font-family:var(--mono);font-size:9px;font-weight:700;padding:2px 5px;border-radius:4px}
.pj.PRIV{background:var(--priv-d);color:var(--priv)}.pj.PUB{background:var(--pub-d);color:var(--pub)}
.rec-list{max-height:380px;overflow-y:auto}
.rec-item{display:flex;gap:10px;align-items:flex-start;padding:11px 12px;border-radius:8px;margin-bottom:8px;background:var(--panel2);border:1px solid var(--line)}
.rec-item.lvl-alta{border-left:3px solid var(--danger)}
.rec-item.lvl-media{border-left:3px solid var(--warn)}
.rec-item.lvl-ok{border-left:3px solid var(--ok)}
.rec-badge{font-size:9px;text-transform:uppercase;letter-spacing:.5px;font-weight:700;padding:3px 8px;border-radius:5px;flex-shrink:0}
.lvl-alta .rec-badge{background:rgba(248,113,113,.2);color:var(--danger)}
.lvl-media .rec-badge{background:rgba(251,146,60,.2);color:var(--warn)}
.lvl-ok .rec-badge{background:rgba(52,211,153,.2);color:var(--ok)}
.rec-text{font-size:12px;color:var(--ink);line-height:1.45}
.empty{text-align:center;color:var(--dim);padding:30px;font-family:var(--mono);font-size:12px}
@media(max-width:900px){.crit-grid{grid-template-columns:1fr}}
</style>
