import { ROLES } from "@/utils/constants";

const namespace = "individuo";

const ROUTE_NAMES = {
  INDEX: namespace,
  ADD: `${namespace}-add`,
  EDIT: `${namespace}-edit`,
};

const ROUTES_DEFINITIONS = [
  {
    path: "/individuos",
    name: ROUTE_NAMES.INDEX,
    component: () => import("./indiviuo-lista.vue"),
    meta: {
      roleList: [ROLES.GESTOR],
      label: "Indivíduos",
      icon: "bx bxs-contact",
    },
  },
  {
    path: "/individuos/novo",
    name: ROUTE_NAMES.ADD,
    component: () => import("./individuo-change.vue"),
    meta: {
      roleList: [ROLES.GESTOR],
      label: "Indivíduos",
    },
  },
  {
    path: "/individuos/:id",
    name: ROUTE_NAMES.EDIT,
    component: () => import("./individuo-change.vue"),
    meta: {
      roleList: [ROLES.GESTOR],
      label: "Indivíduos",
    },
  },
];

export { ROUTE_NAMES, ROUTES_DEFINITIONS };
