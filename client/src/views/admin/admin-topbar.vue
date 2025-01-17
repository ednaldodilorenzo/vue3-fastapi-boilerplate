<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary shadow">
    <div class="container-fluid">
      <button
        type="button"
        class="btn btn-icon btn-topbar btn-ghost-secondary rounded-circle"
        @click="toggleMenu()"
        data-toggle="fullscreen"
      >
        <i class="bx bx-menu bx-sm"></i>
      </button>
      <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Link</a>
          </li>
          <li class="nav-item">
            <a class="nav-link disabled" aria-disabled="true">Disabled</a>
          </li>
        </ul>
        <div>
          <button
            type="button"
            class="btn btn-icon btn-topbar btn-ghost-secondary rounded-circle"
            data-toggle="fullscreen"
          >
            <i class="bx bx-fullscreen fs-4"></i>
          </button>
          <button
            type="button"
            class="btn btn-icon btn-topbar btn-ghost-secondary rounded-circle"
            data-toggle="fullscreen"
          >
            <i class="bx bx-bell fs-4"></i>
          </button>
          <button
            type="button"
            data-test="button-logout"
            class="btn btn-icon btn-topbar btn-ghost-secondary rounded-circle"
            data-toggle="fullscreen"
            @click="logout()"
          >
            <i class="bx bx-exit fs-4"></i>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
import authService from "@/views/auth/auth.service";
import { ROUTE_NAMES as AUTH_ROUTES } from "@/views/auth/routes.definition";

export default {
  name: "admin-topbar",
  emits: ["collapse-click"],
  methods: {
    logout() {
      authService.logout().then(() => {
        this.$router.push({ name: AUTH_ROUTES.LOGIN });
      });
    },
    toggleMenu() {
      this.$emit("collapse-click");
    },
  },
};
</script>
