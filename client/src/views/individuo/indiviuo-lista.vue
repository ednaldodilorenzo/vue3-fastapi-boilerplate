<template>
  <!-- <base-list
    title="Indivíduos Cadastrados"
    :fields="[
      { title: 'ID', name: 'id' },
      { title: 'Nome', name: 'nome' },
      { title: 'Nome Usual', name: 'apelido' },
    ]"
    :actions="[
      {
        name: ROUTE_NAMES.EDIT,
        title: 'Editar Indivíduo',
        clazz: 'bx bxs-edit-alt',
        tooltip: 'Editar Indivíduo',
        dataTest: { name: 'btn-edit-individual', id: 'id' },
      },
    ]"
    :currentPage="currentPage"
    @page-change="getList"
    @search-input="searchFilter"
    @action-trigger="handleActionTrigger"
    @add-clicked="router.push({ name: ROUTE_NAMES.ADD })"
  >
  </base-list> -->
  <div class="card shadow mt-2">
    <div data-test="page-title" class="card-header fs-4">
      Individual Registration
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

            <a
              href="#"
              @click.prevent="router.push({ name: ROUTE_NAMES.ADD })"
              class="btn btn-primary"
              >+ Novo</a
            >
          </div>
          <div style="width: 85%">
            <input
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
        @trigger-page="onPageChange"
        :fields="[
          { title: 'ID', name: 'id' },
          { title: 'Nome', name: 'nome' },
          { title: 'Nome Usual', name: 'apelido' },
        ]"
        :items="items"
        :actions="[
          {
            name: ROUTE_NAMES.EDIT,
            title: 'Editar Indivíduo',
            clazz: 'bx bxs-edit-alt',
            tooltip: 'Editar Indivíduo',
            dataTest: { name: 'btn-edit-individual', id: 'id' },
            handler: handleEdit,
          },
        ]"
      ></bootstrap-table>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import BootstrapTable from "@/components/bootstrap-table.vue";
import { useLoadingScreen } from "@/components/loading/useLoadingScreen";
import individuoService from "./individuo.service";
import { ROUTE_NAMES } from "./routes.definition";

const loading = useLoadingScreen();
const router = useRouter();

const items = ref([]);

function getList(pageNumber = 1, pageSize = 10, filter = undefined) {
  loading.show();
  const params = { page: pageNumber, per_page: pageSize };
  if (filter) {
    params.search = filter;
  }
  individuoService
    .findAll(params)
    .then((resp) => {
      items.value = resp.items;
    })
    .finally(() => {
      loading.hide();
    });
}

// function searchFilter(value) {
//   getList(1, value);
// }

getList(1);

function handleEdit(itemClicked) {
  router.push({ name: ROUTE_NAMES.EDIT, params: { id: itemClicked.id } });
}
</script>
