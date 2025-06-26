let templates = [];
let currentIndex = 0;
let currentTemplates = [];

// Fetch templates from JSON file
async function fetchTemplates() {
  try {
    const response = await fetch('/TaskCode-Site/template-paths.json');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    templates = await response.json();
    currentTemplates = templates;
  } catch (error) {
    console.error('Error fetching templates:', error);
    const container = document.getElementById('template-container');
    if (container) {
      container.innerHTML = '<div class="carousel-error">Failed to load templates. Please try again later.</div>';
    }
  }
}

// Load template previews into carousel
function loadTemplates(filteredTemplates) {
  const container = document.getElementById("template-container");
  if (!container) {
    console.error("Template container not found!");
    return;
  }
  container.innerHTML = ""; // Clear existing content

  if (filteredTemplates.length === 0) {
    container.innerHTML = '<div class="carousel-error">No templates found for this category.</div>';
    return;
  }

  filteredTemplates.forEach(template => {
    const templateDiv = document.createElement("div");
    templateDiv.className = "carousel-card";

    templateDiv.innerHTML = `
      <iframe src="${template.path}" title="${template.name}" class="template-preview"></iframe>
      <h3>${template.name}</h3>
      <p>${template.description}</p>
      <a href="${template.path}" target="_blank" class="open-template-link">Open Template</a>
    `;

    // Handle iframe loading errors
    const iframe = templateDiv.querySelector("iframe");
    iframe.onerror = () => {
      console.error(`Failed to load template: ${template.path}`);
      iframe.outerHTML = `<div class="carousel-error">Error loading ${template.name}</div>`;
    };

    container.appendChild(templateDiv);
  });
}

// Carousel navigation
function updateCarousel() {
  const container = document.getElementById("template-container");
  if (!container || currentTemplates.length === 0) return;
  container.style.transform = `translateX(-${currentIndex * 100}%)`;
}

// Filter templates by category
function filterTemplates(category) {
  currentIndex = 0; // Reset to first template
  currentTemplates = category === "all" ? templates : templates.filter(template => template.category === category);
  loadTemplates(currentTemplates);
  updateCarousel();

  // Update active button
  document.querySelectorAll(".category-btn").forEach(btn => {
    btn.classList.remove("active");
    btn.classList.add("bg-gray-300", "text-gray-700");
    btn.classList.remove("bg-teal-500", "text-white");
  });
  const activeBtn = document.querySelector(`.category-btn[data-category="${category}"]`);
  if (activeBtn) {
    activeBtn.classList.add("active", "bg-teal-500", "text-white");
    activeBtn.classList.remove("bg-gray-300", "text-gray-700");
  }
}

// Navigation button listeners
function setupNavigation() {
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");

  if (!prevBtn || !nextBtn) {
    console.error("Navigation buttons not found!");
    return;
  }

  prevBtn.addEventListener("click", () => {
    if (currentIndex > 0) {
      currentIndex--;
      updateCarousel();
    }
  });

  nextBtn.addEventListener("click", () => {
    if (currentIndex < currentTemplates.length - 1) {
      currentIndex++;
      updateCarousel();
    }
  });
}

// Parse URL query parameter for initial category
function getInitialCategory() {
  const params = new URLSearchParams(window.location.search);
  const category = params.get("category");
  return ["business", "eshop", "generic", "portfolio"].includes(category) ? category : "all";
}

// Initialize
document.addEventListener("DOMContentLoaded", async () => {
  console.log("Initializing template carousel...");
  try {
    await fetchTemplates();
    const initialCategory = getInitialCategory();
    filterTemplates(initialCategory);
    setupNavigation();
  } catch (error) {
    console.error("Error initializing carousel:", error);
    const container = document.getElementById("template-container");
    if (container) {
      container.innerHTML = '<div class="carousel-error">Failed to load templates. Please try again later.</div>';
    }
  }
});