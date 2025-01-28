<template>
  <div class="card shadow mt-2">
    <div data-test="page-title" class="card-header fs-4">
      {{ title }}
    </div>
    <div class="card-body">
      <nav class="navbar bg-body-tertiary mb-3">
        <div class="d-flex w-100">
          <div style="width: 15%">
            <a
              href="javascript:void(0)"
              v-if="showBack"
              @click="clickBack"
              class="btn btn-outline-primary me-2"
              ><i class="bx bx-arrow-back"></i
            ></a>

            <a href="#" @click="clickNew()" class="btn btn-primary">+ Novo</a>
          </div>
          <div style="width: 85%">
            <input
              v-if="showFilter"
              v-autofocus
              v-model="searchQuery"
              class="form-control me-2 w-75"
              type="search"
              name="filtro"
              placeholder="Pesquisar"
              aria-label="Search"
            />
          </div>
        </div>
      </nav>

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
