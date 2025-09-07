const { createApp, ref } = Vue;

createApp({
  setup() {
    const appElement = document.getElementById('app');
    const templates = ref(JSON.parse(appElement.dataset.templates));
    const selectedTemplate = ref(null);
    const customColor = ref("#ffffff");
    const customImages = ref({ banner: null, logo: null });
    const domain = ref({ hasDomain: "no", name: "", hostingProvider: "", notes: "" });
    const form = ref({ name: "", email: "", message: "" });

    const selectTemplate = (template) => {
      selectedTemplate.value = template;
    };

    const handleImageUpload = (type) => (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          customImages.value[type] = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };

    const submitCustomization = () => {
      alert(`Thank you, ${form.value.name}! Your customization details have been received. Our team will contact you at ${form.value.email} to finalize your project with domain: ${domain.value.name}.`);
      form.value = { name: "", email: "", message: "" };
      selectedTemplate.value = null;
      customColor.value = "#ffffff";
      customImages.value = { banner: null, logo: null };
      domain.value = { hasDomain: "no", name: "", hostingProvider: "", notes: "" };
    };

    return { templates, selectedTemplate, customColor, customImages, domain, form, selectTemplate, handleImageUpload, submitCustomization };
  }
}).mount('#app');