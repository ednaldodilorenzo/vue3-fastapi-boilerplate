<template>
  <div class="text-center mt-2 mb-4">
    <h4 class="text-primary">Bem Vindo !</h4>
    <p class="text-muted">Entre para continuar no Gestor Paroquial.</p>
  </div>
  <div
    v-if="showInvalidLoginMessage"
    class="alert alert-warning alert-dismissible fade show"
    role="alert"
    data-test="msg-invalid-login"
  >
    <strong>Loging ou senha inválida!</strong>
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
        :focus="true"
        :errors="v$.form.email.$errors.map((error) => error.$message)"
        v-model="form.email"
        type="email"
        id="inputUsername"
        label="Email"
        name="email"
        class="form-control"
        data-test="input-email"
      />
    </div>
    <div class="mb-3" id="input-group-senha" role="group">
      <bootstrap-input
        :errors="v$.form.password.$errors.map((error) => error.$message)"
        v-model="form.password"
        type="password"
        id="inputPassword"
        label="Senha"
        name="senha"
        class="form-control"
        data-test="input-password"
        placeholder="Informe a senha"
      />
    </div>
    <div class="mb-3 form-check">
      <input type="checkbox" class="form-check-input" id="exampleCheck1" />
      <label class="form-check-label" for="exampleCheck1"
        >Lembrar meu usuário</label
      >
    </div>
    <button
      class="btn btn-primary d-block w-100 mb-3 mt-5"
      data-test="button-login"
      type="submit"
    >
      Entrar
    </button>
    <div class="mt-4 text-center">
      <p class="mb-0">
        <router-link to="/auth/recoverpwd" class="text-decoration-none">
          Esqueceu a Senha?</router-link
        >
      </p>
    </div>
  </form>
</template>
<script>
import { useLoadingScreen } from "@/components/loading/useLoadingScreen";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength, email, helpers } from "@vuelidate/validators";
import authService from "./auth.service";
import BootstrapInput from "@/components/BootstrapInput.vue";

export default {
  components: {
    BootstrapInput,
  },
  setup() {
    return { v$: useVuelidate(), loading: useLoadingScreen() };
  },
  data() {
    return {
      form: {
        email: "",
        password: "",
        food: null,
        checked: [],
      },
      showInvalidLoginMessage: false,
    };
  },
  validations() {
    return {
      form: {
        email: {
          required: helpers.withMessage("Por favor preencha o email", required),
          email: helpers.withMessage("Formato de email inválido", email),
        },
        password: {
          required: helpers.withMessage("Por favor preencha a senha", required),
          minLength: minLength(3),
        },
      },
    };
  },
  methods: {
    onSubmit() {
      this.v$.$validate();

      if (this.v$.$error) {
        return;
      }

      this.loading.show();
      const { email: username, password } = this.form;
      authService
        .login(username, password)
        .then((response) => {
          if (response) {
            this.$router.push("/");
          } else {
            this.showInvalidLoginMessage = true;
          }
        })
        .finally(() => {
          this.loading.hide();
        });
    },
  },
};
</script>
<style scoped>
.login-box {
  background: #fff !important;
}

input {
  background: inherit;
}
</style>
