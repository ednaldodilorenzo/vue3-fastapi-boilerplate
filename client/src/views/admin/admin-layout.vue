<template>
  <div class="d-flex min-vh-100">
    <adminSidebar :menuShown="showMenu" />
    <main class="d-flex flex-column w-100">
      <adminTopbar @collapse-click="topBarCollapseClick()" />
      <div class="p-3">
        <router-view />
      </div>
      <adminFooter />
    </main>
  </div>
</template>
<script>
import adminFooter from "./admin-footer.vue";
import adminTopbar from "./admin-topbar.vue";
import adminSidebar from "./admin-sidebar.vue";

export default {
  components: {
    adminFooter,
    adminTopbar,
    adminSidebar,
  },
  data() {
    return {
      showMenu: true,
    };
  },
  methods: {
    topBarCollapseClick() {
      this.showMenu = !this.showMenu;
    },
  },
  created() {
    this.showMenu = window.innerWidth > 700 ? this.showMenu : false;
    window.addEventListener("resize", () => {
      const width = window.innerWidth;
      if (width < 700) {
        this.showMenu = false;
      } else {
        this.showMenu = true && this.showMenu;
      }
    });
  },
};
</script>
