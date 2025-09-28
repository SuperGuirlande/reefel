// Navbar Mobile - Reefel Workshop
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (!mobileMenuButton || !mobileMenu) return;
    
    const hamburgerIcon = mobileMenuButton.querySelector('svg:first-of-type');
    const closeIcon = mobileMenuButton.querySelector('svg:last-of-type');

    // Cacher le menu sur desktop (md et plus)
    function hideOnDesktop() {
        if (window.innerWidth >= 768) {
            mobileMenu.classList.add('hidden');
            if (hamburgerIcon) hamburgerIcon.classList.remove('hidden');
            if (closeIcon) closeIcon.classList.add('hidden');
        }
    }
    
    // Écouter les changements de taille d'écran
    window.addEventListener('resize', hideOnDesktop);
    hideOnDesktop(); // Appeler au chargement

    // Fonction pour fermer le menu
    function closeMenu() {
        mobileMenu.classList.add('hidden');
        if (hamburgerIcon) hamburgerIcon.classList.remove('hidden');
        if (closeIcon) closeIcon.classList.add('hidden');
    }

    // Fonction pour ouvrir le menu
    function openMenu() {
        mobileMenu.classList.remove('hidden');
        if (hamburgerIcon) hamburgerIcon.classList.add('hidden');
        if (closeIcon) closeIcon.classList.remove('hidden');
    }

    // Toggle du menu au clic sur le bouton
    mobileMenuButton.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        
        const isHidden = mobileMenu.classList.contains('hidden');
        if (isHidden) {
            openMenu();
        } else {
            closeMenu();
        }
    });

    // Fermer le menu quand on clique sur un lien
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', function() {
            closeMenu();
        });
    });

    // Fermer le menu quand on clique en dehors
    document.addEventListener('click', function(event) {
        if (mobileMenuButton && mobileMenu && 
            !mobileMenuButton.contains(event.target) && 
            !mobileMenu.contains(event.target)) {
            closeMenu();
        }
    });

    // Fermer le menu avec la touche Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && !mobileMenu.classList.contains('hidden')) {
            closeMenu();
        }
    });
});