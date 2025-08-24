const { createApp } = Vue;

createApp({
  data() {
    return {
      templates: [],
      searchQuery: '',
      currentCategory: 'all',
      categories: ['all', 'business', 'eshop', 'generic', 'portfolio'],
      loadedTemplates: [],
      templateLoadErrors: {}
    };
  },
  computed: {
    categorizedTemplates() {
      let filtered = this.templates;
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(template => 
          template.name.toLowerCase().includes(query) || 
          template.description.toLowerCase().includes(query)
        );
      }
      if (this.currentCategory !== 'all') {
        filtered = filtered.filter(template => template.category === this.currentCategory);
      }
      const categorized = {
        business: [], eshop: [], generic: [], portfolio: []
      };
      filtered.forEach(template => {
        categorized[template.category].push(template);
      });
      return categorized;
    }
  },
  methods: {
    async fetchTemplates() {
      try {
        const response = await fetch('/static/template-paths.json');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        this.templates = await response.json();
      } catch (error) {
        console.error('Error fetching templates:', error);
        this.templates.forEach((_, index) => {
          this.templateLoadErrors[index] = true;
        });
      }
    },
    markLoaded(index) {
      if (!this.loadedTemplates.includes(index)) {
        this.loadedTemplates.push(index);
        delete this.templateLoadErrors[index];
      }
    },
    handleError(index) {
      if (!this.templateLoadErrors[index]) {
        this.templateLoadErrors[index] = true;
      }
    },
    filterTemplates(category) {
      this.currentCategory = category;
      this.loadedTemplates = [];
      this.templateLoadErrors = {};
    },
    clearSearch() {
      this.searchQuery = '';
    }
  },
  mounted() {
    this.fetchTemplates();
  }
}).mount('#app');