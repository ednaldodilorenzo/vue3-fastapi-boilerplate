import store from "../store/index";

const authPermission = (el, biding) => {
  const elementPermissions = biding.value;
  const user = store.getters["currentUser/getUser"];
  el.style.display =
    elementPermissions && !elementPermissions.includes(user.role)
      ? "none"
      : "block";
};

export default authPermission;
