<template>
  <div
    class="modal fade"
    tabindex="-1"
    aria-labelledby="dialogTitle"
    aria-hidden="true"
    ref="dialogModal"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="dialogTitle">{{ title }}</h5>
          <button
            type="button"
            class="btn-close"
            aria-label="Close"
            @click="onCancel"
          ></button>
        </div>
        <div class="modal-body">
          {{ message }}
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" @click="onCancel">Cancelar</button>
          <button class="btn btn-primary" @click="onConfirm">Confirmar</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
const props = defineProps({
  message: {
    type: String,
    required: false,
    default: "",
  },
  title: {
    type: String,
    required: false,
    default: "",
  },
  onCancel: {
    type: Function,
  },
  onConfirm: {
    type: Function,
  },
});
</script>
