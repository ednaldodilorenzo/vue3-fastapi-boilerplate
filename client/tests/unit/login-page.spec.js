import Login from "@/views/auth/login-new.vue";
import { shallowMount } from "@vue/test-utils";
import authService from "@/views/auth/auth.service";

describe.each`
  fillUsername | fillPassword | invalidFields
  ${false}     | ${false}     | ${2}
  ${true}      | ${false}     | ${1}
  ${false}     | ${true}      | ${1}
  ${true}      | ${true}      | ${0}
`("Login page fields", ({ fillUsername, fillPassword, invalidFields }) => {
  it(`should ${
    invalidFields === 0 ? "not " : ""
  }show mandatory fields message when ${invalidFields} fields are invalid`, async () => {
    const wrapper = shallowMount(Login, {
      global: {
        plugins: [],
      },
    });
    const authServiceSpy = jest.spyOn(authService, "login");

    const loginInput = wrapper.find('[data-test="input-email"]');
    expect(loginInput.exists()).toBe(true);
    if (fillUsername) {
      loginInput.element.value = "test@test.com";
      await loginInput.trigger("input");
    }

    const passwordInput = wrapper.find('[data-test="input-password"]');
    expect(passwordInput.exists()).toBe(true);
    if (fillPassword) {
      passwordInput.element.value = "test";
      await passwordInput.trigger("input");
    }
    const loginForm = wrapper.find("form");
    expect(loginForm.exists()).toBe(true);
    await loginForm.trigger("submit");

    const validationErrors = wrapper.findAll(".form-control:invalid");
    expect(validationErrors.length).toBe(invalidFields);

    // Se os campos estiverem preenchidos o serviço de login será chamado.
    expect(authServiceSpy).toHaveBeenCalledTimes(!invalidFields ? 1 : 0);
  });
});
