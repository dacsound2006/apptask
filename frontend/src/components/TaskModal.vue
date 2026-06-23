<script setup>
const props = defineProps({ data: Object, phases: Array });
const emit = defineEmits(["save", "close"]);
</script>
<template>
  <div class="modal" @click.self="emit('close')">
    <div class="box">
      <h3>{{ data.isNew ? "Nueva tarea" : "Editar tarea " + data.task.code }}</h3>
      <div class="fld"><label>Nombre de la tarea</label>
        <input v-model="data.task.name" placeholder="Describe la tarea"></div>
      <div class="fld row">
        <div><label>Código</label><input v-model="data.task.code"></div>
        <div><label>Proyecto</label><select v-model="data.task.project">
          <option value="PRIV">Cloud Privado</option><option value="PUB">Cloud Público</option></select></div>
      </div>
      <div class="fld row">
        <div><label>Fase</label><input v-model="data.task.phase" list="phaselist">
          <datalist id="phaselist"><option v-for="p in phases" :key="p" :value="p"></option></datalist></div>
        <div><label>Responsable</label><input v-model="data.task.owner"></div>
      </div>
      <div class="fld row">
        <div><label>Inicio</label><input type="date" v-model="data.task.start"></div>
        <div><label>Vence</label><input type="date" v-model="data.task.due"></div>
      </div>
      <div class="fld"><label>Estado</label><select v-model="data.task.status">
        <option value="pending">Pendiente</option><option value="in_progress">En curso</option><option value="done">Completada</option></select></div>
      <div class="fld"><label>Avance — {{ data.task.progress }}%</label>
        <input type="range" min="0" max="100" step="5" v-model.number="data.task.progress" style="width:100%"></div>
      <div class="modal-act">
        <button class="btn ghost" @click="emit('close')">Cancelar</button>
        <button class="btn" @click="emit('save', data.task)">{{ data.isNew ? "Crear tarea" : "Guardar cambios" }}</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
.modal{position:fixed;inset:0;background:rgba(4,8,16,.75);display:grid;place-items:center;z-index:50;padding:20px}
.box{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:24px;width:520px;max-width:100%;max-height:90vh;overflow:auto}
h3{font-size:16px;margin-bottom:18px}
.fld{margin-bottom:14px}
.fld label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--mut);margin-bottom:6px;font-weight:600}
.fld input,.fld select{width:100%;background:var(--panel2);border:1px solid var(--line);color:var(--ink);padding:10px 12px;border-radius:9px;font-size:13px;outline:none}
.fld input:focus,.fld select:focus{border-color:var(--info)}
.fld.row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.modal-act{display:flex;justify-content:space-between;gap:10px;margin-top:20px}
.btn{background:var(--info);color:#04121c;border:none;padding:10px 16px;border-radius:9px;font-weight:700;font-size:13px;cursor:pointer}
.btn:hover{filter:brightness(1.1)}.btn.ghost{background:var(--panel2);color:var(--ink);border:1px solid var(--line)}
</style>
