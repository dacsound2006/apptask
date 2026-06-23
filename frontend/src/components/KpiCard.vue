<script setup>
defineProps({ cls: String, label: String, val: [Number, String], sub: String, active: Boolean });
</script>
<template>
  <div class="kpi" :class="[cls, { active }]">
    <div class="lbl">{{ label }}</div>
    <div class="val">{{ val ?? "—" }}</div>
    <div class="sub">{{ sub }}</div>
    <div class="bar"></div>
  </div>
</template>
<style scoped>
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;position:relative;overflow:hidden;cursor:pointer;transition:.15s}
.kpi:hover{border-color:var(--info);transform:translateY(-2px)}
.kpi.active{border-color:var(--info);box-shadow:0 0 0 1px var(--info) inset}
.lbl{font-size:11px;color:var(--mut);text-transform:uppercase;letter-spacing:.6px;font-weight:600}
.val{font-size:30px;font-weight:800;font-family:var(--mono);margin-top:6px;line-height:1}
.sub{font-size:11px;color:var(--dim);margin-top:6px;font-family:var(--mono)}
.bar{position:absolute;left:0;bottom:0;height:3px;width:100%}
.k-total .val{color:var(--ink)}.k-total .bar{background:var(--info)}
.k-week .val{color:var(--info)}.k-week .bar{background:var(--info)}
.k-late .val{color:var(--danger)}.k-late .bar{background:var(--danger)}
.k-pend .val{color:var(--warn)}.k-pend .bar{background:var(--warn)}
.k-prog .val{color:var(--pub)}.k-prog .bar{background:var(--pub)}
.k-done .val{color:var(--ok)}.k-done .bar{background:var(--ok)}
</style>
