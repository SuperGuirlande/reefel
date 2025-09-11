const reefel = document.getElementById("reefel");
const workshop = document.getElementById("workshop");

// Éléments de la partie gauche
const paintBg = document.getElementById("paint-bg");
const ship = document.getElementById("ship");
const graffiti = document.getElementById("graffiti");

// Éléments de la partie droite
const subtitle = document.querySelector('.animate-subtitle');
const locationCard = document.querySelector('.animate-location');
const services = document.querySelectorAll('.animate-services .flex.items-center.text-slate-200.group');
const buttons = document.querySelectorAll('.animate-buttons button');

// Debug - vérifier si les éléments sont trouvés
console.log('Services trouvés:', services.length);
console.log('Services:', services);

// Configuration initiale des éléments (opacity-0 déjà dans le HTML)
gsap.set(services, {y: 30});
gsap.set(buttons, {y: 20});
gsap.set(subtitle, {y: 30});
gsap.set(locationCard, {y: 20});
gsap.set(paintBg, {scale: 0.8, rotation: -10});
gsap.set(ship, {y: 100, x: -200, rotation: 5});
gsap.set(graffiti, {scale: 0.5, rotation: -15});

const tl = gsap.timeline({ease: 'power3.inOut'});

// Animation de la partie gauche
tl.to(paintBg, {opacity: 1, scale: 1, rotation: 0, duration: 1.2, ease: 'back.out(1.7)'})
  .to(ship, {opacity: 1, y: 0, x: 0, rotation: 0, duration: 1, ease: 'bounce.out'}, "-=0.8")
  .to(graffiti, {opacity: 1, scale: 1, rotation: 0, duration: 0.8, ease: 'elastic.out(1, 0.3)'}, "-=0.6")

// Animation des titres principaux
  .from(reefel, {opacity: 0, x: -260, duration: 1}, "-=0.4")
  .from(workshop, {opacity: 0, x: 60, duration: 1}, "-=0.5")
  
  // Animation du sous-titre
  .to(subtitle, {opacity: 1, y: 0, duration: 0.8}, "-=0.3")
  
  // Animation de la localisation
  .to(locationCard, {opacity: 1, y: 0, duration: 0.6}, "-=0.2")
  
  // Animation des services (staggered)
  .to(services, {
    opacity: 1, 
    y: 0, 
    duration: 0.6,
    stagger: 0.1
  }, "-=1")
  
  // Animation des boutons
  .to(buttons, {
    opacity: 1,
    y: 0,
    duration: 0.5,
    stagger: 0.1
  }, "-=1");

// Carrousel Galerie
let currentSlide = 0;
const totalSlides = 14; // Nombre total de slides
const carousel = document.getElementById('carousel');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const dots = document.querySelectorAll('.carousel-dot');

// Fonction pour mettre à jour le carrousel
function updateCarousel() {
    const translateX = -currentSlide * 100;
    carousel.style.transform = `translateX(${translateX}%)`;
    
    // Mettre à jour les dots
    dots.forEach((dot, index) => {
        if (index === currentSlide) {
            dot.classList.add('active', 'bg-orange-500');
            dot.classList.remove('bg-slate-300');
        } else {
            dot.classList.remove('active', 'bg-orange-500');
            dot.classList.add('bg-slate-300');
        }
    });
}

// Navigation précédente
prevBtn.addEventListener('click', () => {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    updateCarousel();
});

// Navigation suivante
nextBtn.addEventListener('click', () => {
    currentSlide = (currentSlide + 1) % totalSlides;
    updateCarousel();
});

// Navigation par dots
dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        currentSlide = index;
        updateCarousel();
    });
});

// Auto-play (optionnel)
let autoPlayInterval;
function startAutoPlay() {
    autoPlayInterval = setInterval(() => {
        currentSlide = (currentSlide + 1) % totalSlides;
        updateCarousel();
    }, 5000); // Change de slide toutes les 5 secondes
}

function stopAutoPlay() {
    clearInterval(autoPlayInterval);
}

// Démarrer l'auto-play
startAutoPlay();

// Arrêter l'auto-play au survol
const carouselContainer = document.querySelector('.relative.max-w-6xl.mx-auto');
carouselContainer.addEventListener('mouseenter', stopAutoPlay);
carouselContainer.addEventListener('mouseleave', startAutoPlay);

// Initialiser le carrousel
updateCarousel();