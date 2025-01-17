import { reactive } from "vue";
import useVuelidate from "@vuelidate/core";
import { useToast } from "vue-toastification";

export default function useForm(initialFormData, validationRules) {
  const toast = useToast();
  // Convert the initial form data to a reactive object
  const formData = reactive({ ...initialFormData });

  // Initializing Vuelidate with the passed validation rules and form data
  const v$ = useVuelidate(validationRules, formData);

  // Method to reset the form and validation state
  const resetForm = () => {
    // Reset the formData to its initial state
    Object.keys(initialFormData).forEach((key) => {
      console.log(initialFormData[key], formData[key]);
      formData[key] = initialFormData[key];
    });
    v$.value.$reset(); // Reset the validation state
  };

  // Method to handle form submission
  const saveForm = (onSubmit, ...args) => {
    v$.value.$touch(); // Mark all fields as touched to trigger validation
    if (v$.value.$pending) {
      return Promise.resolve(null); // Validation is still pending
    }
    if (v$.value.$invalid) {
      return Promise.resolve(null);
    }

    // This is done because passing the promise method causes it to be executed even if the validation fails.
    //const boundMethod = onSubmit.bind(caller);
    return onSubmit(...args).then(() => {
      toast.success("Deu certo", {
        position: "top-center",
        timeout: 5000,
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

      return true;
    });
  };

  return {
    formData, // Return formData as reactive refs
    v$, // Return Vuelidate instance
    saveForm,
    resetForm,
  };
}
