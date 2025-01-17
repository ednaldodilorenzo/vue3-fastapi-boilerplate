<template>
  <base-list
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
  </base-list>
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import BaseList from "@/components/base-list.vue";
import { useLoadingScreen } from "@/components/loading/useLoadingScreen";
import individuoService from "./individuo.service";
import { ROUTE_NAMES } from "./routes.definition";

const loading = useLoadingScreen();
const router = useRouter();

const currentPage = ref({
  items: [],
  page: 1,
});

function getList(pageNumber, filter = undefined) {
  loading.show();
  const params = { page: pageNumber, per_page: 10 };
  if (filter) {
    params.search = filter;
  }
  individuoService
    .findAll(params)
    .then((resp) => {
      currentPage.value = resp;
    })
    .finally(() => {
      loading.hide();
    });
}

function searchFilter(value) {
  getList(1, value);
}

getList(1);

function handleActionTrigger(action, id) {
  if (action === ROUTE_NAMES.EDIT)
    router.push({ name: ROUTE_NAMES.EDIT, params: { id: id } });
}
</script>
