// Système de notifications
class NotificationManager {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Créer le conteneur des notifications s'il n'existe pas
        if (!this.container) { 
            this.container = document.createElement('div');
            this.container.id = 'notification-container';
            this.container.className = 'fixed top-4 right-4 z-50 space-y-2';
            document.body.appendChild(this.container);
        }
    }

    show(message, type = 'success', duration = 3000) {
        const notification = document.createElement('div');
        
        // Classes de base pour la notification
        const baseClasses = 'relative px-6 py-4 rounded-lg shadow-xl transform transition-all duration-300 ease-in-out translate-x-full opacity-0 max-w-sm overflow-hidden';
        
        // Classes selon le type de message
        const typeClasses = {
            'success': 'bg-green-500 text-white border-l-4 border-green-400',
            'error': 'bg-red-500 text-white border-l-4 border-red-400',
            'warning': 'bg-yellow-500 text-white border-l-4 border-yellow-400',
            'info': 'bg-blue-500 text-white border-l-4 border-blue-400'
        };

        notification.className = `${baseClasses} ${typeClasses[type] || typeClasses['info']}`;
        
        // Contenu de la notification avec overlay progressive
        notification.innerHTML = `
            <!-- Contenu principal -->
            <div class="relative z-10">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <div class="mr-3">
                            ${this.getIcon(type)}
                        </div>
                        <div class="text-sm font-medium">
                            ${message}
                        </div>
                    </div>
                    <button class="ml-4 text-white hover:text-gray-200 focus:outline-none transition-colors duration-200 hover:scale-110 transform" onclick="this.parentElement.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            
            <!-- Overlay progressive coloré -->
            <div class="progress-overlay absolute inset-0 transition-all ease-linear ${this.getOverlayClass(type)}" style="width: 0%; transition-duration: ${duration}ms;"></div>
        `;

        // Ajouter au conteneur
        this.container.appendChild(notification);

        // Animation d'entrée
        setTimeout(() => {
            notification.classList.remove('translate-x-full', 'opacity-0');
            notification.classList.add('translate-x-0', 'opacity-100');
        }, 10);

        // Démarrer l'animation de l'overlay progressive
        const progressOverlay = notification.querySelector('.progress-overlay');
        let timeoutId;
        let isPaused = false;
        
        // Fonction pour démarrer l'overlay
        const startProgress = () => {
            progressOverlay.style.width = '100%';
            
            // Timer pour la suppression automatique
            timeoutId = setTimeout(() => {
                if (!isPaused) {
                    this.hide(notification);
                }
            }, duration + 100);
        };

        // Démarrer l'overlay après un court délai
        setTimeout(startProgress, 100);

        // Effet de hover - pause l'overlay
        notification.addEventListener('mouseenter', () => {
            isPaused = true;
            notification.classList.add('scale-105');
            
            // Pauser l'animation CSS
            progressOverlay.style.animationPlayState = 'paused';
            progressOverlay.style.transitionPlayState = 'paused';
            
            // Annuler le timeout de suppression
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
        });

        notification.addEventListener('mouseleave', () => {
            isPaused = false;
            notification.classList.remove('scale-105');
            
            // Reprendre l'animation CSS
            progressOverlay.style.animationPlayState = 'running';
            progressOverlay.style.transitionPlayState = 'running';
            
            // Relancer le timer avec le temps restant approximatif
            timeoutId = setTimeout(() => {
                this.hide(notification);
            }, 1000); // 1 seconde de grâce après hover
        });

        return notification;
    }

    hide(notification) {
        notification.classList.add('translate-x-full', 'opacity-0');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }

    getIcon(type) {
        const icons = {
            'success': '<i class="fas fa-check-circle"></i>',
            'error': '<i class="fas fa-exclamation-circle"></i>',
            'warning': '<i class="fas fa-exclamation-triangle"></i>',
            'info': '<i class="fas fa-info-circle"></i>'
        };
        return icons[type] || icons['info'];
    }

    getOverlayClass(type) {
        const overlayClasses = {
            'success': 'bg-green-600 bg-opacity-40',
            'error': 'bg-red-600 bg-opacity-40',
            'warning': 'bg-yellow-600 bg-opacity-40',
            'info': 'bg-blue-600 bg-opacity-40'
        };
        return overlayClasses[type] || overlayClasses['info'];
    }

    // Méthodes raccourcies
    success(message, duration = 3000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 3000) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration = 3000) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 3000) {
        return this.show(message, 'info', duration);
    }
}

// Initialiser le gestionnaire de notifications
const notifications = new NotificationManager();

// Fonction pour traiter les messages Django
function processDjangoMessages() {
    const djangoMessages = document.querySelectorAll('.django-message');
    
    djangoMessages.forEach(messageElement => {
        const message = messageElement.textContent.trim();
        const messageType = messageElement.getAttribute('data-type') || 'info';
        
        // Mapper les types Django vers nos types
        const typeMapping = {
            'success': 'success',
            'error': 'error', 
            'warning': 'warning',
            'info': 'info',
            'debug': 'info'
        };
        
        notifications.show(message, typeMapping[messageType] || 'info');
        
        // Cacher l'élément Django original
        messageElement.style.display = 'none';
    });
}

// Lancer le traitement au chargement de la page
document.addEventListener('DOMContentLoaded', processDjangoMessages);

// Exposer les notifications globalement
window.notifications = notifications; 