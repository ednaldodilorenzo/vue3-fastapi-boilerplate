<template>
  <div class="card shadow mt-2">
    <div data-test="page-title" class="card-header fs-4">
      {{ title }}
    </div>
    <div class="card-body">
      <bootstrap-table
        @search-input="emmitSearchInput"
        @trigger-page="onPageChange"
        @new-clicked="onAddClicked"
        @action-clicked="onActionTriggered"
        :fields="fields"
        :page="currentPage"
        :actions="actions"
      ></bootstrap-table>
    </div>
  </div>
</template>
<script setup>
import BootstrapTable from "./bootstrap-table";

const emit = defineEmits([
  "search-input",
  "page-change",
  "add-clicked",
  "action-trigger",
]);

defineProps({
  title: String,
  actions: Array,
  fields: Array,
  currentPage: Object,
});

function emmitSearchInput(value) {
  emit("search-input", value);
}

function onPageChange(pageNumber, filter) {
  emit("page-change", pageNumber, filter);
}

function onAddClicked() {
  emit("add-clicked");
}

function onActionTriggered(action, id) {
  emit("action-trigger", action, id);
}
</script>
