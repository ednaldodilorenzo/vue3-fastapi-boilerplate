import { createRouter, createWebHistory } from "vue-router";
import { VIEW_ROUTES } from "./routes";
import { ADMIN_ROUTES } from "./admin-routes";
import { checkAuth } from "./guards";

const routes = [
  {
    path: "/",
    name: "admin",
    component: () => import("@/views/admin/admin-layout.vue"),
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: "/denied",
        name: "denied",
        component: () => import("@/views/access-denied.vue"),
      },
      ...ADMIN_ROUTES,
    ],
  },
  ...VIEW_ROUTES,
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(checkAuth);

export default router;
