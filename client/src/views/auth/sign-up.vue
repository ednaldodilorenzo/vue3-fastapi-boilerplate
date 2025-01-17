<template>
  <div class="text-center mt-2 mb-4">
    <h4 class="text-primary">Bem Vindo !</h4>
    <p class="text-muted">Registre-se no Gestor Paroquial.</p>
  </div>
  <div
    v-if="showValidationMessage"
    class="alert alert-warning alert-dismissible fade show"
    role="alert"
    data-test="msg-invalid-login"
  >
    <strong>{{ validationMessage }}</strong>
    <button
      type="button"
      class="btn-close"
      data-bs-dismiss="alert"
      aria-label="Close"
    ></button>
  </div>
  <form @submit.stop.prevent="onSubmit" novalidate>
    <div class="mb-3" id="groupUsername" role="group">
      <bootstrap-input
        :errors="v$.email.$errors.map((error) => error.$message)"
        v-model="form.email"
        type="email"
        id="inputUsername"
        label="Email"
        name="email"
        class="form-control"
        data-test="input-email"
        placeholder="Informe o email..."
        disabled
      />
    </div>
    <div class="mb-3" role="group">
      <bootstrap-input
        :errors="v$.nome.$errors.map((error) => error.$message)"
        v-model="form.nome"
        id="inputNome"
        label="Nome"
        name="nome"
        class="form-control"
        data-test="input-name"
        placeholder="Informe o nome"
      />
    </div>
    <div class="mb-3" role="group">
      <bootstrap-input
        :errors="v$.nascimento.$errors.map((error) => error.$message)"
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
    <div class="mb-3" role="group">
      <bootstrap-input
        :errors="v$.cpf.$errors.map((error) => error.$message)"
        v-model="form.cpf"
        id="inputCPF"
        label="CPF"
        name="cpf"
        class="form-control"
        data-test="input-cpf"
        placeholder="Informe o CPF"
      />
    </div>
    <div class="mb-3" role="group">
      <bootstrap-input
        :errors="v$.telefone.$errors.map((error) => error.$message)"
        v-model="form.telefone"
        id="inputPhone"
        label="Telefone"
        name="telefone"
        class="form-control"
        data-test="input-phone"
        placeholder="Informe o telefone..."
      />
    </div>
    <div class="mb-3" id="input-group-senha" role="group">
      <bootstrap-input
        :errors="v$.senha.$errors.map((error) => error.$message)"
        v-model="form.senha"
        type="password"
        id="inputPassword"
        label="Senha"
        name="senha"
        class="form-control"
        data-test="input-password"
        placeholder="Informe a senha"
      />
    </div>

    <div class="mb-3" role="group">
      <bootstrap-input
        :errors="v$.confirmacao.$errors.map((error) => error.$message)"
        v-model="form.confirmacao"
        type="password"
        id="inputConfirm"
        label="Confirmar Senha"
        name="confirmar"
        class="form-control"
        data-test="input-confirmar"
        placeholder="Confirme a senha"
      />
    </div>
    <button
      class="btn btn-primary d-block w-100 mb-3 mt-5"
      data-test="button-login"
      type="submit"
    >
      Registrar
    </button>
    <div class="mt-4 text-center">
      <p class="mb-0">
        Já fez o cadastro?
        <router-link to="/auth/login" class="text-decoration-none">
          Ir para o login</router-link
        >
      </p>
    </div>
  </form>
</template>
<script setup>
import { useLoadingScreen } from "@/components/loading/useLoadingScreen";
import { ref, computed } from "vue";
import individuoService from "@/views/individuo/individuo.service";
import authService from "./auth.service";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "vue-toastification";
import BootstrapInput from "@/components/BootstrapInput.vue";
import { useVuelidate } from "@vuelidate/core";
import { ROUTE_NAMES } from "./routes.definition";
import { HTTP_STATUS_CODE } from "@/utils/constants";
import {
  required,
  minLength,
  email,
  helpers,
  sameAs,
} from "@vuelidate/validators";
import { validateCPF } from "@/utils/validators";

const showValidationMessage = ref(false);
const validationMessage = ref("");
const form = ref({
  email: "",
  senha: "",
  confirmacao: "",
  nome: "",
  nascimento: "",
  telefone: "",
  nomeUsual: "",
  cpf: "",
});

const route = useRoute();
const router = useRouter();
const toast = useToast();
const loading = useLoadingScreen();

const token = route.params.token;

individuoService.findByToken(token).then((resp) => {
  form.value = { ...form.value, ...resp };
});

const rules = computed(() => ({
  email: {
    required: helpers.withMessage("Por favor preencha o email", required),
    email: helpers.withMessage("Formato de email inválido", email),
  },
  senha: {
    required: helpers.withMessage("Por favor preencha a senha", required),
    minLength: helpers.withMessage(
      "A senha deve ter pelo menos 3 caracteres.",
      minLength(3)
    ),
  },
  confirmacao: {
    required: helpers.withMessage("Por favor preencha a senha", required),
    sameAsPassword: helpers.withMessage(
      "A confirmação deve ser igual a senha.",
      sameAs(form.value.senha)
    ),
  },
  nome: {
    required: helpers.withMessage(
      "Por favor preencha o nome do usuário",
      required
    ),
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
}));

const v$ = useVuelidate(rules, form);

function onSubmit() {
  v$.value.$validate();

  if (v$.value.$error) {
    return;
  }

  loading.show();

  authService
    .signup(token, form.value)
    .then(() => {
      console.log("Entrou no then");
      toast.success("Usuário registrado com sucesso!", {
        position: "top-center",
        timeout: 5000,
        closeOnClick: true,
        pauseOnFocusLoss: true,
        pauseOnHover: true,
        draggable: true,
        draggablePercent: 0.6,
        showCloseButtonOnHover: false,
        hideProgressBar: true,
        closeButton: "button",
        icon: true,
        rtl: false,
      });
      router.push({ name: ROUTE_NAMES.LOGIN });
    })
    .catch((err) => {
      console.dir(err);
      if (err.response.status === HTTP_STATUS_CODE.UNPROCESSABLE_ENTITY) {
        validationMessage.value = err.response.data.message;
        showValidationMessage.value = true;
      }
    })
    .finally(() => {
      loading.hide();
    });
}
</script>
