<template>
  <div class="modal fade" style="display: block" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button
            type="button"
            class="btn-close"
            @click="onClose"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <slot></slot>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="onClose">
            Fechar
          </button>
          <button type="button" class="btn btn-primary" @click="onConfirm">
            Salvar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
const props = defineProps({
  title: {
    type: String,
    required: false,
    default: "",
  },
  onClose: {
    type: Function,
  },
  onConfirm: {
    type: Function,
  },
});
</script>
