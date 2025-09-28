
// create_category_modal.js - Gestion de la modale de création de catégorie

// Récupérer le token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Ouvrir la modal
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('category_modal');
    const openBtn = document.getElementById('open_category_modal');
    const closeBtn = document.getElementById('close_category_modal');
    const cancelBtn = document.getElementById('cancel_category_btn');
    
    if (openBtn) {
        openBtn.addEventListener('click', function(e) {
            e.preventDefault();
            modal.style.display = 'flex';
            modal.classList.remove('hidden');
            console.log('Modal ouverte');
        });
    }

    // Fermer la modal
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
            modal.classList.add('hidden');
        });
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function() {
            modal.style.display = 'none';
            modal.classList.add('hidden');
        });
    }

    // Fermer en cliquant à l'extérieur
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            modal.classList.add('hidden');
        }
    });

    // Créer une catégorie en AJAX
    const submitBtn = document.getElementById('create_category_btn');
    const categoryNameInput = document.getElementById('category_name_input');
    const message = document.getElementById('category-message');

    if (submitBtn && categoryNameInput) {
        submitBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Bouton créer cliqué');

            const categoryName = categoryNameInput.value.trim();

            if (!categoryName) {
                showMessage('Veuillez entrer un nom de catégorie', 'error');
                return;
            }

            // Désactiver le bouton pendant l'envoi de la requête
            submitBtn.disabled = true;
            const btnText = submitBtn.querySelector('#create_category_btn_text');
            if (btnText) {
                btnText.textContent = 'Création...';
            }

            // Envoyer la requête AJAX
            fetch(submitBtn.dataset.url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({name: categoryName})
            })
            .then(response => response.json())
            .then(response => {
                console.log('Réponse reçue:', response);
                
                if (response.success) {
                    showMessage('Catégorie créée avec succès !', 'success');
                    
                    // Ajouter la nouvelle catégorie à la grid
                    if (window.addCategoryToForm) {
                        window.addCategoryToForm({
                            id: response.category.id,
                            name: response.category.name
                        });
                    } else {
                        // Fallback si la fonction globale n'est pas disponible
                        addCategoryToGrid(response.category);
                    }

                    // Fermer la modal après un délai
                    setTimeout(() => {
                        modal.style.display = 'none';
                        modal.classList.add('hidden');
                        categoryNameInput.value = '';
                        message.classList.add('hidden');
                    }, 1000);

                } else {
                    showMessage(response.error || 'Erreur lors de la création', 'error');
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                showMessage('Erreur de connexion', 'error');
            })
            .finally(() => {
                submitBtn.disabled = false;
                if (btnText) {
                    btnText.textContent = 'Créer la catégorie';
                }
            });
        });
    }

    // Fonction pour afficher les messages
    function showMessage(text, type) {
        if (message) {
            message.className = `p-4 rounded-2xl ${type === 'success' ? 'bg-green-500/20 border border-green-500/30 text-green-300' : 'bg-red-500/20 border border-red-500/30 text-red-300'}`;
            message.textContent = text;
            message.classList.remove('hidden');
        }
    }

    // Fonction de fallback pour ajouter la catégorie
    function addCategoryToGrid(categoryData) {
        const categoryGrid = document.getElementById('id_categories');
        if (!categoryGrid) return;

        const newCategory = document.createElement('div');
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'categories';
        checkbox.value = categoryData.id;
        checkbox.id = `id_categories_${categoryData.id}`;
        checkbox.checked = true;
        
        const label = document.createElement('label');
        label.htmlFor = checkbox.id;
        label.textContent = categoryData.name;
        label.classList.add('selected');
        
        newCategory.appendChild(checkbox);
        newCategory.appendChild(label);
        categoryGrid.appendChild(newCategory);
        
        console.log('Catégorie ajoutée avec fallback');
    }
});