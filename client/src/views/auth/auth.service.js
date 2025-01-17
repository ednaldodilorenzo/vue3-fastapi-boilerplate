import requester from "@/utils/request";
import store from "@/store/index";
import Cookies from "js-cookie";

const authService = {
  login: (username, password) => {
    return requester
      .post("/auth/v1/login", {
        usuario: username,
        senha: password,
      })
      .then((response) => {
        const user = response.data;
        store.dispatch("currentUser/setUser", {
          id: user.id_usuario,
          name: user.nome_usuario,
          role: user.papel,
        });
        Cookies.set("jwtToken", user.token, {
          expires: 1, // Optional: set cookie expiration time in days
          secure: true, // Optional: ensures the cookie is only sent over HTTPS
          sameSite: "Strict", // Optional: prevent CSRF attacks by restricting cross-site access
        });
        return true;
      })
      .catch((err) => {
        if (err.status === 401) {
          return false;
        }
      });
  },
  logout: () => {
    Cookies.remove("jwtToken");
    return store.dispatch("currentUser/setUser", null);
  },
  signup: (token, user) => {
    console.log("Entrou no signup");
    return requester.post(`/auth/v1/signup/${token}`, user);
  },
  sendEmail: async (id, email) => {
    const resp = await requester.post(`/auth/v1/email/${id}/gestor`, {
      email: email,
    });
    return resp.data;
  },
};

export default authService;
