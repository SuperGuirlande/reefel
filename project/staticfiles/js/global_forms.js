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
    
    // Gérer les checkboxes de catégories
    const categoryCheckboxes = document.querySelectorAll('#id_categories input[type="checkbox"]');
    console.log('Checkboxes de catégories trouvées:', categoryCheckboxes.length); // Debug
    
    categoryCheckboxes.forEach(function(checkbox) {
        // Fonction pour mettre à jour l'état visuel
        function updateCheckboxState() {
            const label = checkbox.parentElement; // Le label est le parent direct de l'input
            if (checkbox.checked) {
                label.style.backgroundColor = '#5f5df7'; // minsk-500
                label.style.borderColor = '#5f5df7';
                label.style.color = 'white';
                label.style.boxShadow = '0 4px 12px rgba(95, 93, 247, 0.3)';
                label.classList.add('selected'); // Ajouter la classe pour l'icône
            } else {
                label.style.backgroundColor = 'white';
                label.style.borderColor = '#adbcfd'; // minsk-100
                label.style.color = '';
                label.style.boxShadow = '';
                label.classList.remove('selected'); // Enlever la classe pour l'icône
            }
        }
        
        // Initialiser l'état au chargement
        updateCheckboxState();
        
        // Écouter les changements
        checkbox.addEventListener('change', updateCheckboxState);
    });
}); 