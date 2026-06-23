<script setup>
defineProps({ byProject: Array, overall: Number });
function ring(pct) {
  const r = 26, c = 2 * Math.PI * r;
  return { dash: c, offset: c * (1 - pct / 100) };
}
</script>
<template>
  <div class="card">
    <h2><span class="dot"></span>% de avance</h2>
    <div class="prog-wrap">
      <div class="overall">
        <svg viewBox="0 0 64 64" class="ring">
          <circle cx="32" cy="32" r="26" class="ring-bg"/>
          <circle cx="32" cy="32" r="26" class="ring-fg ov"
            :stroke-dasharray="ring(overall).dash" :stroke-dashoffset="ring(overall).offset"/>
        </svg>
        <div class="ring-label"><b>{{ overall }}%</b><span>global</span></div>
      </div>
      <div class="proj-list">
        <div v-for="p in byProject" :key="p.project" class="proj-item">
          <div class="proj-top">
            <span class="pj" :class="p.project">{{ p.label }}</span>
            <span class="proj-pct">{{ p.pct }}%</span>
          </div>
          <div class="proj-bar"><i :class="p.project" :style="{width:p.pct+'%'}"></i></div>
          <div class="proj-meta">
            <span>{{ p.done }}/{{ p.total }} tareas</span>
            <span :class="{warn:p.late>0}">{{ p.late }} atrasadas</span>
            <span :class="{warn:p.days_left<=14}">{{ p.days_left }}d al cierre</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.prog-wrap{display:flex;gap:20px;align-items:center}
.overall{position:relative;width:84px;height:84px;flex-shrink:0}
.ring{width:84px;height:84px;transform:rotate(-90deg)}
.ring-bg{fill:none;stroke:var(--panel2);stroke-width:6}
.ring-fg{fill:none;stroke-width:6;stroke-linecap:round;transition:stroke-dashoffset .6s}
.ring-fg.ov{stroke:var(--info)}
.ring-label{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.ring-label b{font-size:20px;font-family:var(--mono);color:var(--ink)}
.ring-label span{font-size:9px;color:var(--dim);text-transform:uppercase;letter-spacing:.5px}
.proj-list{flex:1;display:flex;flex-direction:column;gap:14px}
.proj-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px}
.pj{font-family:var(--mono);font-size:11px;font-weight:700;padding:3px 8px;border-radius:5px}
.pj.PRIV{background:var(--priv-d);color:var(--priv)}.pj.PUB{background:var(--pub-d);color:var(--pub)}
.proj-pct{font-family:var(--mono);font-size:14px;font-weight:700;color:var(--ink)}
.proj-bar{height:7px;background:var(--panel2);border-radius:6px;overflow:hidden}
.proj-bar i{display:block;height:100%;border-radius:6px}
.proj-bar i.PRIV{background:var(--priv)}.proj-bar i.PUB{background:var(--pub)}
.proj-meta{display:flex;gap:14px;margin-top:6px;font-size:10px;font-family:var(--mono);color:var(--dim)}
.proj-meta .warn{color:var(--danger)}
</style>
