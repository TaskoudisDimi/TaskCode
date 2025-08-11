const { createApp } = Vue;

createApp({
  data() {
    return {
      templates: [],
      currentIndex: 0,
      currentCategory: 'all',
      searchQuery: '',
      loadedTemplates: [],
      showModal: false,
      selectedTemplate: null,
      categories: ['all', 'business', 'eshop', 'generic', 'portfolio']
    };
  },
  computed: {
    filteredTemplates() {
      let filtered = this.templates;
      if (this.currentCategory !== 'all') {
        filtered = filtered.filter(template => template.category === this.currentCategory);
      }
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(template => 
          template.name.toLowerCase().includes(query) || 
          template.description.toLowerCase().includes(query)
        );
      }
      return filtered;
    }
  },
  methods: {
    async fetchTemplates() {
      try {
        const response = await fetch('/TaskCode-Site/template-paths.json');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        this.templates = await response.json();
      } catch (error) {
        console.error('Error fetching templates:', error);
        const container = document.getElementById('template-container');
        if (container) {
          container.innerHTML = '<div class="carousel-error">Failed to load templates. Please try again later.</div>';
        }
      }
    },
    filterTemplates(category) {
      this.currentIndex = 0;
      this.currentCategory = category;
      this.loadedTemplates = [];
    },
    prevTemplate() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    },
    nextTemplate() {
      if (this.currentIndex < this.filteredTemplates.length - 1) {
        this.currentIndex++;
      }
    },
    markLoaded(index) {
      if (!this.loadedTemplates.includes(index)) {
        this.loadedTemplates.push(index);
      }
    },
    openPreview(template) {
      this.selectedTemplate = template;
      this.showModal = true;
    },
    clearSearch() {
      this.searchQuery = '';
    }
  },
  mounted() {
    this.fetchTemplates();
    const params = new URLSearchParams(window.location.search);
    const category = params.get('category');
    if (this.categories.includes(category)) {
      this.currentCategory = category;
    }
  }
}).mount('#app');