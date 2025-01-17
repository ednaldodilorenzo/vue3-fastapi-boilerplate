<template>
  <base-register
    @submit="handleSubmit"
    @cancel-click="router.push({ name: ROUTE_NAMES.INDEX })"
    :title="individuoId ? 'Alterar Indivíduo' : 'Registrar Indivíduo'"
  >
    <div class="col-md-6">
      <bootstrap-input
        :errors="v$.nome?.$errors.map((error) => error.$message)"
        :focus="true"
        v-model="form.nome"
        id="iptNome"
        label="Nome"
        name="nome"
        class="form-control"
      />
    </div>
    <div class="col-md-6">
      <bootstrap-input
        :errors="v$.apelido?.$errors.map((error) => error.$message)"
        v-model="form.apelido"
        id="iptApelido"
        label="Nome Usual"
        name="apelido"
        class="form-control"
      />
    </div>
    <div class="col-md-6">
      <bootstrap-input
        :errors="v$.email?.$errors.map((error) => error.$message)"
        v-model="form.email"
        type="email"
        id="inputUsername"
        label="Email"
        name="email"
        class="form-control"
        data-test="input-email"
        placeholder="Informe o email..."
      />
    </div>
    <div class="col-md-6">
      <bootstrap-input
        :errors="v$.nascimento?.$errors.map((error) => error.$message)"
        v-model="form.nascimento"
        id="inputNascimento"
        label="Data de Nascimento"
        name="nascimento"
        class="form-control"
        data-test="input-born"
        placeholder="Informe a data de nascimento"
        type="date"
      />
    </div>
    <div class="col-md-6">
      <bootstrap-input
        :errors="v$.cpf?.$errors.map((error) => error.$message)"
        v-model="form.cpf"
        id="inputCPF"
        label="CPF"
        name="cpf"
        class="form-control"
        data-test="input-cpf"
        placeholder="Informe o CPF"
      />
    </div>
    <div class="col-md-6">
      <bootstrap-input
        :errors="v$.telefone?.$errors.map((error) => error.$message)"
        v-model="form.telefone"
        id="inputPhone"
        label="Telefone"
        name="telefone"
        class="form-control"
        data-test="input-phone"
        placeholder="Informe o telefone..."
      />
    </div>
  </base-register>
</template>
<script setup>
import BaseRegister from "@/components/base-register.vue";
import BootstrapInput from "@/components/BootstrapInput.vue";
import useForm from "@/components/userform-mixin";
import { helpers, required, email } from "@vuelidate/validators";
import { validateCPF } from "@/utils/validators";
import { ROUTE_NAMES } from "./routes.definition";
import { useRouter, useRoute } from "vue-router";
import individuoService from "./individuo.service";
import { useLoadingScreen } from "@/components/loading/useLoadingScreen";

const router = useRouter();
const route = useRoute();
const loading = useLoadingScreen();

const initForm = {
  id: null,
  email: "",
  nome: "",
  nascimento: "",
  telefone: "",
  apelido: "",
  cpf: "",
};

const validationRules = {
  email: {
    required: helpers.withMessage("Por favor preencha o email", required),
    email: helpers.withMessage("Formato de email inválido", email),
  },
  nome: {
    required: helpers.withMessage("Por favor preencha o nome", required),
  },
  apelido: {
    required: helpers.withMessage("Por favor preencha o nome usual", required),
  },
  nascimento: {
    required: helpers.withMessage(
      "Por favor preencha a data de nascimento",
      required
    ),
  },
  telefone: {
    required: helpers.withMessage("Por favor preencha o telefone", required),
  },
  cpf: {
    required: helpers.withMessage("Por favor preencha o CPF", required),
    cpfvalid: helpers.withMessage("Formato de CPF inválido", validateCPF),
  },
};

const { formData: form, v$, saveForm } = useForm(initForm, validationRules);

const individuoId = route.params.id;

if (individuoId) {
  loading.show();
  individuoService
    .findById(individuoId)
    .then((data) => {
      Object.assign(form, data);
    })
    .finally(() => {
      loading.hide();
    });
}

function handleSubmit() {
  loading.show();
  const method = individuoId
    ? saveForm(
        individuoService.update.bind(individuoService),
        individuoId,
        form
      )
    : saveForm(individuoService.create.bind(individuoService), form);

  method
    .then((value) => {
      if (value) router.push({ name: ROUTE_NAMES.INDEX });
    })
    .finally(() => {
      loading.hide();
    });
}
</script>
