// List of template files, organized by category
const templates = [
  // Business (2 templates)
  {
    name: "Business Landing",
    path: "/TaskCode/templates/Business/main/index.html",
    description: "A professional landing page for corporate businesses.",
    category: "business"
  },
  {
    name: "Startup Showcase",
    path: "/TaskCode/templates/Business/Unika Free Website Template - Free-CSS.com/unika-html/unika-html/index.html",
    description: "A dynamic template for startups to highlight services.",
    category: "business"
  },
  // eShop (8 templates)
  {
    name: "Fashion Store",
    path: "/TaskCode/static/templates/eshop/eshop1.html",
    description: "A stylish e-commerce template for fashion retail.",
    category: "eshop"
  },
  {
    name: "Electronics Shop",
    path: "/TaskCode/static/templates/eshop/eshop2.html",
    description: "A modern store template for tech products.",
    category: "eshop"
  },
  {
    name: "Grocery Market",
    path: "/TaskCode/static/templates/eshop/eshop3.html",
    description: "An online grocery store with easy navigation.",
    category: "eshop"
  },
  {
    name: "Jewelry Boutique",
    path: "/TaskCode/static/templates/eshop/eshop4.html",
    description: "A luxurious template for jewelry sales.",
    category: "eshop"
  },
  {
    name: "Bookstore",
    path: "/TaskCode/static/templates/eshop/eshop5.html",
    description: "A clean e-commerce template for books.",
    category: "eshop"
  },
  {
    name: "Furniture Store",
    path: "/TaskCode/static/templates/eshop/eshop6.html",
    description: "A template for home decor and furniture retail.",
    category: "eshop"
  },
  {
    name: "Sports Gear",
    path: "/TaskCode/static/templates/eshop/eshop7.html",
    description: "A vibrant store template for sports equipment.",
    category: "eshop"
  },
  {
    name: "Toy Shop",
    path: "/TaskCode/static/templates/eshop/eshop8.html",
    description: "A fun e-commerce template for toys and games.",
    category: "eshop"
  },
  // Generic (6 templates)
  {
    name: "Minimalist Landing",
    path: "/TaskCode/static/templates/generic/generic1.html",
    description: "A clean and simple landing page for any purpose.",
    category: "generic"
  },
  {
    name: "Event Page",
    path: "/TaskCode/static/templates/generic/generic2.html",
    description: "A template for promoting events and conferences.",
    category: "generic"
  },
  {
    name: "Blog Homepage",
    path: "/TaskCode/static/templates/generic/generic3.html",
    description: "A versatile blog template with article previews.",
    category: "generic"
  },
  {
    name: "Agency Site",
    path: "/TaskCode/static/templates/generic/generic4.html",
    description: "A template for creative agencies to showcase services.",
    category: "generic"
  },
  {
    name: "Non-Profit",
    path: "/TaskCode/static/templates/generic/generic5.html",
    description: "A template for charities and non-profit organizations.",
    category: "generic"
  },
  {
    name: "Personal Page",
    path: "/TaskCode/static/templates/generic/generic6.html",
    description: "A simple personal website template.",
    category: "generic"
  },
  // Portfolio (9 templates)
  {
    name: "Creative Portfolio",
    path: "/TaskCode/static/templates/portfolio/portfolio1.html",
    description: "A vibrant portfolio for artists and designers.",
    category: "portfolio"
  },
  {
    name: "Photography Gallery",
    path: "/TaskCode/static/templates/portfolio/portfolio2.html",
    description: "A template for showcasing photography work.",
    category: "portfolio"
  },
  {
    name: "Designer Portfolio",
    path: "/TaskCode/static/templates/portfolio/portfolio3.html",
    description: "A sleek portfolio for graphic designers.",
    category: "portfolio"
  },
  {
    name: "Freelancer Site",
    path: "/TaskCode/static/templates/portfolio/portfolio4.html",
    description: "A template for freelancers to display projects.",
    category: "portfolio"
  },
  {
    name: "Architect Portfolio",
    path: "/TaskCode/static/templates/portfolio/portfolio5.html",
    description: "A professional template for architects.",
    category: "portfolio"
  },
  {
    name: "Writer Portfolio",
    path: "/TaskCode/static/templates/portfolio/portfolio6.html",
    description: "A clean template for writers and authors.",
    category: "portfolio"
  },
  {
    name: "Musician Page",
    path: "/TaskCode/static/templates/portfolio/portfolio7.html",
    description: "A template for musicians to share their work.",
    category: "portfolio"
  },
  {
    name: "Videographer Portfolio",
    path: "/TaskCode/static/templates/portfolio/portfolio8.html",
    description: "A template for video content creators.",
    category: "portfolio"
  },
  {
    name: "Illustrator Portfolio",
    path: "/TaskCode/static/templates/portfolio/portfolio9.html",
    description: "A colorful portfolio for illustrators.",
    category: "portfolio"
  }
];

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
let currentIndex = 0;
let currentTemplates = templates;

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
document.addEventListener("DOMContentLoaded", () => {
  console.log("Initializing template carousel...");
  try {
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