// Gestion des champs de fichier avec aperçu
document.addEventListener('DOMContentLoaded', function() {

    
    // Cibler directement le champ thumbnail par son nom
    const thumbnailInput = document.querySelector('input[type="file"][name="thumbnail"]');
    
    if (!thumbnailInput) {
        return;
    }
    
    // Récupérer les éléments directement par ID
    const previewContainer = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const buttonText = document.getElementById('button-text');
    const fileName = document.getElementById('file-name');
    
    if (!previewContainer || !previewImg || !buttonText || !fileName) {
        return;
    }
    
    thumbnailInput.addEventListener('change', function() {
        console.log('Changement de fichier détecté'); // Debug
        const file = this.files[0];
        console.log('Fichier sélectionné:', file); // Debug
        
        if (file && file.type.startsWith('image/')) {
            console.log('Image valide détectée'); // Debug
            
            // Créer l'URL de l'image
            const reader = new FileReader();
            
            reader.onload = function(e) {
                console.log('Image chargée'); // Debug
                
                // Afficher l'aperçu
                previewImg.src = e.target.result;
                previewContainer.classList.remove('hidden');
                
                // Changer le texte du bouton
                buttonText.textContent = 'Modifier l\'image';
                
                // Afficher le nom du fichier
                fileName.textContent = file.name;
                fileName.classList.remove('text-gray-600');
                fileName.classList.add('text-green-600');
            };
            
            reader.readAsDataURL(file);
            
        } else if (file) {
            console.log('Fichier non-image'); // Debug
            
            // Fichier non-image
            previewContainer.classList.add('hidden');
            buttonText.textContent = 'Choisir une image';
            fileName.textContent = file.name + ' (Fichier non valide)';
            fileName.classList.remove('text-green-600');
            fileName.classList.add('text-red-600');
            
        } else {
            console.log('Aucun fichier'); // Debug
            
            // Aucun fichier
            previewContainer.classList.add('hidden');
            buttonText.textContent = 'Choisir une image';
            fileName.textContent = 'Aucun fichier choisi';
            fileName.classList.remove('text-green-600', 'text-red-600');
            fileName.classList.add('text-gray-600');
        }
    });
    
    // === GESTION DES CHECKBOXES MULTIPLES ===
    
    // Fonction pour initialiser les checkboxes
    function initializeCheckboxes() {
        const categoryCheckboxes = document.querySelectorAll('#id_categories input[type="checkbox"]');
        console.log('Checkboxes de catégories trouvées:', categoryCheckboxes.length);
        
        categoryCheckboxes.forEach(function(checkbox) {
            // Retirer les anciens event listeners
            checkbox.removeEventListener('change', handleCheckboxChange);
            
            // Fonction pour mettre à jour l'état visuel
            function updateCheckboxState() {
                const label = checkbox.nextElementSibling; // Le label suit l'input
                if (label && label.tagName === 'LABEL') {
                    if (checkbox.checked) {
                        label.classList.add('selected');
                    } else {
                        label.classList.remove('selected');
                    }
                }
            }
            
            // Créer la fonction de gestion
            function handleCheckboxChange() {
                console.log('Checkbox changé:', checkbox.checked, checkbox.value);
                updateCheckboxState();
                triggerContainerResize();
            }
            
            // Stocker la référence pour pouvoir la retirer
            checkbox.handleCheckboxChange = handleCheckboxChange;
            
            // Initialiser l'état au chargement
            updateCheckboxState();
            
            // Écouter les changements
            checkbox.addEventListener('change', handleCheckboxChange);
        });
    }
    
    // Fonction pour déclencher le redimensionnement du conteneur
    function triggerContainerResize() {
        const container = document.getElementById('id_categories');
        if (container) {
            // Forcer le recalcul des dimensions
            container.style.height = 'auto';
            const height = container.scrollHeight;
            container.style.height = height + 'px';
            
            // Remettre en auto après une courte pause
            setTimeout(() => {
                container.style.height = 'auto';
            }, 100);
        }
    }
    
    // Initialiser les checkboxes au chargement
    initializeCheckboxes();
    
    // Observer les changements DOM pour les nouvelles catégories
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                // Réinitialiser les checkboxes quand de nouveaux éléments sont ajoutés
                setTimeout(initializeCheckboxes, 50);
            }
        });
    });
    
    const categoriesContainer = document.getElementById('id_categories');
    if (categoriesContainer) {
        observer.observe(categoriesContainer, {
            childList: true,
            subtree: true
        });
    }
    
    // Fonction globale pour ajouter une catégorie dynamiquement
    window.addCategoryToForm = function(categoryData) {
        const container = document.getElementById('id_categories');
        if (!container) return;
        
        console.log('Ajout de la catégorie:', categoryData);
        
        // Créer le nouveau div
        const categoryDiv = document.createElement('div');
        
        // Créer le checkbox
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'categories';
        checkbox.value = categoryData.id;
        checkbox.id = `id_categories_${categoryData.id}`;
        checkbox.checked = true; // Sélectionné par défaut
        
        // Créer le label
        const label = document.createElement('label');
        label.htmlFor = checkbox.id;
        label.textContent = categoryData.name;
        
        // Assembler
        categoryDiv.appendChild(checkbox);
        categoryDiv.appendChild(label);
        
        // Ajouter au conteneur
        container.appendChild(categoryDiv);
        
        // Réinitialiser les checkboxes pour prendre en compte le nouveau
        setTimeout(initializeCheckboxes, 50);
        
        console.log('Catégorie ajoutée au formulaire');
    };
}); 