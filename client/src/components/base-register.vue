<template>
  <div class="card shadow mt-2">
    <div data-test="page-title" class="card-header fs-4">
      {{ title }}
    </div>
    <div class="card-body">
      <form @submit.stop.prevent="onSubmit" class="row g-3 mb-3">
        <slot></slot>
        <hr class="my-4" />
        <div class="row">
          <div class="col-6">
            <div class="d-grid gap-2 d-md-flex justify-content-md-start">
              <a
                style="width: 100px"
                class="btn btn-secondary"
                data-test="btn-cancel"
                type="button"
                @click="onCancelClick"
                >Cancelar</a
              >
            </div>
          </div>
          <div class="col-6">
            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <button
                data-test="btn-save"
                type="submit"
                style="width: 100px"
                class="btn btn-success"
              >
                Salvar
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
<script setup>
defineProps({
  title: String,
});

const emit = defineEmits(["cancel-click", "submit"]);

function onCancelClick() {
  emit("cancel-click");
}

function onSubmit() {
  emit("submit");
}
</script>
