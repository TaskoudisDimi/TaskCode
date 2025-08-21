const { createApp } = Vue;

createApp({
  data() {
    return {
      taglines: [
        'Build the Future with Task-Code',
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
      showChat: false,
      chatInput: '',
      chatMessages: [
        { text: 'Hello! How can Task-Code help you today?', from: 'bot' }
      ],
      currentBannerIndex: 0,
      bannerInterval: null
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
        const response = await fetch('/static/template-paths.json');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const allTemplates = await response.json();
        this.featuredTemplates = allTemplates.slice(0, 3);
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
      if (!this.templateLoadErrors[index]) {
        this.templateLoadErrors[index] = true;
      }
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
    toggleChat() {
      this.showChat = !this.showChat;
    },
    submitChat(e) {
      if (e.key === 'Enter' && this.chatInput.trim()) {
        this.chatMessages.push({ text: this.chatInput, from: 'user' });
        setTimeout(() => {
          this.chatMessages.push({ text: 'Thanks for your message! How about starting a project with us?', from: 'bot' });
        }, 1000);
        this.chatInput = '';
      }
    },
    scrollToVision() {
      const visionSection = document.querySelector('#vision');
      visionSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    },
    scrollToInquire() {
      const inquireSection = document.querySelector('#inquire');
      inquireSection.scrollIntoView({ behavior: 'smooth' });
    },
    startBannerRotation() {
      this.bannerInterval = setInterval(() => {
        const bannerSlides = document.querySelectorAll('.banner-slide');
        bannerSlides.forEach(slide => slide.classList.remove('active'));
        this.currentBannerIndex = (this.currentBannerIndex + 1) % bannerSlides.length;
        bannerSlides[this.currentBannerIndex].classList.add('active');
      }, 5000);
    }
  },
  mounted() {
    this.fetchTemplates();
    setInterval(() => {
      this.currentTaglineIndex = (this.currentTaglineIndex + 1) % this.taglines.length;
    }, 5000);
    this.startBannerRotation();
  }
}).mount('#app');