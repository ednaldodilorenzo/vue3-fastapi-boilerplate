<template>
  <div class="text-center mt-2">
    <h4 class="text-primary">Criar uma Conta</h4>
    <p class="text-muted">Tenha acesso grátis ao Iappointment.</p>
  </div>
  <form
    :class="{
      'was-validated': v$.$dirty ? true : false,
    }"
    @submit.stop.prevent="onSubmit"
    novalidate
  >
    <div class="mb-3" id="groupName" role="group">
      <label for="inputName" class="form-label">Nome</label>
      <input
        class="form-control"
        id="inputName"
        type="text"
        placeholder="Nome do usuário"
        required
        aria-required="true"
        v-model="form.name"
        data-test="input-name"
      />
      <div class="invalid-feedback">Campo obrigatório</div>
    </div>
    <div class="mb-3" id="groupUsername" role="group">
      <label for="inputUsername" class="form-label">Email</label>
      <input
        class="form-control"
        id="inputUsername"
        type="email"
        placeholder="Enter email"
        required
        aria-required="true"
        v-model="form.email"
        data-test="input-email"
      />
      <div class="invalid-feedback" id="live-feedback-email">
        Formato de email inválido
      </div>
    </div>
    <div class="mb-3" id="input-group-senha" role="group">
      <label for="inputPassword" class="form-label">Senha</label>
      <input
        class="form-control"
        id="inputPassword"
        type="password"
        placeholder="Enter name"
        required
        aria-required="true"
        v-model="form.password"
        data-test="input-password"
      />
      <div class="invalid-feedback" id="live-feedback-password">
        Campo obrigatório
      </div>
    </div>
    <div class="mb-3" id="input-group-confirm" role="group">
      <label for="inputConfirm" class="form-label">Confirmar senha</label>
      <input
        class="form-control"
        id="inputConfirm"
        type="password"
        placeholder="Entre a confirmação da senha"
        required
        aria-required="true"
        v-model="form.confirmPassword"
        data-test="input-confirm"
      />
      <div class="invalid-feedback">Campo obrigatório</div>
    </div>
    <div class="mb-3 form-check">
      <input type="checkbox" class="form-check-input" id="exampleCheck1" />
      <label class="form-check-label" for="exampleCheck1"
        >Aceito os termos de serviço.</label
      >
    </div>
    <button
      class="btn btn-primary d-block w-100 mb-3 mt-5"
      data-test="button-login"
      type="submit"
    >
      Registar
    </button>
    <div class="mt-4 text-center">
      <p class="mb-0">
        Já possui uma conta?
        <router-link to="/login" class="fw-medium text-primary">
          Entrar</router-link
        >
      </p>
    </div>
  </form>
</template>
<script>
import { useLoadingScreen } from "@/components/loading/useLoadingScreen";
import LoadingScreen from "@/components/loading-screen.vue";
import { useVuelidate } from "@vuelidate/core";
import { required, minLength, email } from "@vuelidate/validators";
import authService from "./auth.service";
import { ROUTE_NAMES } from "./routes.definition";
import { useToast } from "vue-toastification";

export default {
  components: {
    LoadingScreen,
  },
  setup() {
    const toast = useToast();

    return { v$: useVuelidate(), toast: toast, loading: useLoadingScreen() };
  },
  data() {
    return {
      form: {
        name: null,
        email: null,
        password: null,
        confirmPassword: null,
      },
    };
  },
  validations() {
    return {
      form: {
        name: {
          required,
        },
        email: {
          required,
          email,
        },
        password: {
          required,
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
      authService
        .signup(this.form)
        .then(() => {
          this.toast.success("Usuário registrado com sucesso!", {
            position: "top-center",
            timeout: 3000,
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
          this.$router.push({ name: ROUTE_NAMES.INDEX });
        })
        .catch((err) => {
          console.log(err.response.status);
        })
        .finally(() => {
          this.loading.hide();
        });
    },
  },
};
</script>
<style scoped>
.register-box {
  background: #fff !important;
}

input {
  background: inherit;
}
</style>
