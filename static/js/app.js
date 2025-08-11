const { createApp } = Vue;

createApp({
  data() {
    return {
      taglines: [
        'Build the Future with AIWebWorks',
        'Innovate. Create. Celebrate.',
        'Your Vision, Our Code.',
        'AI-Powered Digital Excellence'
      ],
      currentTaglineIndex: 0,
      featuredTemplates: [],
      loadedTemplates: [],
      templateLoadErrors: {},
      showTemplateModal: false,
      selectedTemplate: null,
      businessType: '',
      idea: '',
      formStep: 1,
      inquiryForm: {
        name: '',
        email: '',
        projectType: '',
        description: ''
      },
      formErrors: {},
      showChat: false,
      chatInput: '',
      chatMessages: [
        { text: 'Hello! How can AIWebWorks help you today?', from: 'bot' }
      ]
    };
  },
  computed: {
    currentTagline() {
      return this.taglines[this.currentTaglineIndex];
    }
  },
  methods: {
    async fetchTemplates() {
      try {
        const response = await fetch('/TaskCode-Site/template-paths.json');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const allTemplates = await response.json();
        this.featuredTemplates = allTemplates.slice(0, 3); // Show 3 templates
        // Add timeout for loading
        this.featuredTemplates.forEach((_, index) => {
          setTimeout(() => {
            if (!this.loadedTemplates.includes(index) && !this.templateLoadErrors[index]) {
              this.templateLoadErrors[index] = true;
            }
          }, 5000); // 5-second timeout
        });
      } catch (error) {
        console.error('Error fetching templates:', error);
        this.featuredTemplates.forEach((_, index) => {
          this.templateLoadErrors[index] = true;
        });
      }
    },
    markTemplateLoaded(index) {
      if (!this.loadedTemplates.includes(index)) {
        this.loadedTemplates.push(index);
        delete this.templateLoadErrors[index];
      }
    },
    handleTemplateError(index) {
      this.templateLoadErrors[index] = true;
    },
    openTemplateModal(template) {
      this.selectedTemplate = template;
      this.showTemplateModal = true;
    },
    generateIdea() {
      const ideas = {
        retail: 'Launch a sleek e-shop with AI-driven product recommendations and automated inventory syncing.',
        tech: 'Build a dynamic startup site with integrated AI chatbots and real-time user analytics.',
        creative: 'Create a vibrant portfolio showcasing your work with interactive galleries and client testimonials.',
        nonprofit: 'Develop a donation-focused site with automated donor tracking and personalized thank-you emails.',
        portfolio: 'Craft a minimalist portfolio with 3D project previews and seamless social media integration.'
      };
      this.idea = ideas[this.businessType] || 'Please select a business type to generate an idea.';
    },
    nextStep() {
      this.formErrors = {};
      if (!this.inquiryForm.name.trim()) {
        this.formErrors.name = 'Name is required';
        return;
      }
      if (!this.inquiryForm.email.trim()) {
        this.formErrors.email = 'Email is required';
        return;
      }
      if (!/^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(this.inquiryForm.email)) {
        this.formErrors.email = 'Invalid email format';
        return;
      }
      this.formStep = 2;
    },
    submitInquiry() {
      this.formErrors = {};
      if (!this.inquiryForm.projectType) {
        this.formErrors.projectType = 'Project type is required';
        return;
      }
      if (!this.inquiryForm.description.trim()) {
        this.formErrors.description = 'Description is required';
        return;
      }
      // Simulate form submission
      alert('Inquiry submitted successfully!');
      this.inquiryForm = { name: '', email: '', projectType: '', description: '' };
      this.formStep = 1;
    },
    toggleChat() {
      this.showChat = !this.showChat;
    },
    submitChat(e) {
      if (e.key === 'Enter' && this.chatInput.trim()) {
        this.chatMessages.push({ text: this.chatInput, from: 'user' });
        // Simulate bot response
        setTimeout(() => {
          this.chatMessages.push({ text: 'Thanks for your message! How about starting a project with us?', from: 'bot' });
        }, 1000);
        this.chatInput = '';
      }
    },
    scrollToInquire() {
      const inquireSection = document.querySelector('#inquire');
      inquireSection.scrollIntoView({ behavior: 'smooth' });
    }
  },
  mounted() {
    this.fetchTemplates();
    // Cycle through taglines
    setInterval(() => {
      this.currentTaglineIndex = (this.currentTaglineIndex + 1) % this.taglines.length;
    }, 5000);
  }
}).mount('#app');