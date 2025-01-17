<template>
  <div class="shadow side-bar responsive" :class="{ visible: menuShown }">
    <h1 class="fs-4 text-center mb-0 p-3" style="color: white">GesPar</h1>
    <div class="fs-6 text-center" style="color: white">
      {{ currentUser?.name }}
    </div>
    <hr class="text-white" />
    <small class="d-inline-block p-2" style="color: #abb9e8; font-weight: bold"
      >Menu</small
    >
    <ul class="nav nav-pills flex-column mb-auto">
      <li class="nav-item">
        <a href="#" class="nav-link text-white" aria-current="page">
          <i class="bx bx-home me-2"></i>Home</a
        >
      </li>
      <li
        class="nav-item"
        v-for="menuItem in filterMenus()"
        :key="menuItem.name"
      >
        <router-link
          data-test="menu-item"
          :to="menuItem"
          class="nav-link text-white"
        >
          <i :class="[menuItem.meta.icon]" class="bx me-2"></i
          >{{ menuItem.meta.label }}
        </router-link>
      </li>
    </ul>
  </div>
</template>
<script>
import { SIDEBAR_ROUTES } from "@/router/sidebar-routes";
import { shallowRef } from "vue";
import { mapGetters } from "vuex";

export default {
  props: {
    menuShown: {
      required: false,
      default: false,
    },
  },
  computed: {
    ...mapGetters({ currentUser: "currentUser/getUser" }),
  },
  methods: {
    filterMenus() {
      const user = this.currentUser;
      return this.menuItems.filter(
        (menuItem) =>
          !menuItem.meta?.roleList ||
          menuItem.meta?.roleList?.includes(user?.role)
      );
    },
  },
  setup() {
    const menuItems = shallowRef(SIDEBAR_ROUTES);
    return { menuItems };
  },
};
</script>
<style scoped>
.side-bar {
  opacity: 0;
  transition: min-width 0.2s ease-out, opacity 0.2s ease-in;
  min-width: 0;
  width: 0;
  background: #484be5;
}

.side-bar.visible {
  min-width: 250px;
  width: 0;
  opacity: 1;
}
</style>
