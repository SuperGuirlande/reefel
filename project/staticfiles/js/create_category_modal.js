

// Récupérer le token CSRF
const csrftoken = getCookie('csrftoken');

// Ouvrir la modal
document.getElementById('open_category_modal').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('category_modal').style.display = 'flex';
});

// Fermer la modal
document.getElementById('close_category_modal').addEventListener('click', function() {
    document.getElementById('category_modal').style.display = 'none';
});




// Créer une catégorie en AJAX
document.addEventListener('DOMContentLoaded', function() {
    // L'URL sera passée via un attribut data du bouton
    const submitBtn = document.getElementById('create_category_btn');
    const categoryNameInput = document.getElementById('category_name_input');
    const createCategoryUrl = submitBtn.getAttribute('data-url');
    const categoryGrid = document.getElementById('id_categories');

    submitBtn.addEventListener('click', function(e) {
        e.preventDefault();

        const categoryName = categoryNameInput.value;

        if (!categoryName) {
            alert('Veuillez entrer un nom de catégorie');
            return;
        }

        //Désactiver le bouto pêndant l'envoi de la requête
        submitBtn.disabled = true;
        submitBtn.querySelector('#create_category_btn_text').textContent = 'Ajout en cours...';

        //Envoyer la requête AJAX
        makeAjaxRequest(
            createCategoryUrl,
            'POST',
            {
                category_name: categoryName
            },
            // Fonction de succès
            function(response) {
                if (response.success) {
                    // Réinitialiser le bouton
                    submitBtn.querySelector('#create_category_btn_text').textContent = 'Ajouter la catégorie';
                    submitBtn.disabled = false;

                    // Afficher la notification
                    notifications.success('Catégorie créée avec succès !');     
                    // Fermer la modal
                    document.getElementById('category_modal').style.display = 'none';   
                    // Ajouter la nouvelle catégorie à la grid        

                    const newCategory = document.createElement('div');
                    newCategory.classList.add('flex', 'flex-col', 'gap-3');
                    newCategory.innerHTML = `
                        <label for="id_categories_${response.category.id}">
                            <input type="checkbox" name="categories" value="${response.category.id}" class="form-checkbox" id="id_categories_${response.category.id}" checked>
                            ${response.category.name}
                        </label>
                    `;
                    categoryGrid.appendChild(newCategory);

                    // Récupérer la nouvelle checkbox et son label
                    const newCheckbox = document.getElementById(`id_categories_${response.category.id}`);
                    const newLabel = newCheckbox.parentElement;

                    // Fonction pour mettre à jour l'état visuel (copié de global_forms.js)
                    function updateCheckboxState() {
                        if (newCheckbox.checked) {
                            newLabel.style.backgroundColor = '#5f5df7'; // minsk-500
                            newLabel.style.borderColor = '#5f5df7';
                            newLabel.style.color = 'white';
                            newLabel.style.boxShadow = '0 4px 12px rgba(95, 93, 247, 0.3)';
                            newLabel.classList.add('selected'); // Ajouter la classe pour l'icône
                        } else {
                            newLabel.style.backgroundColor = 'white';
                            newLabel.style.borderColor = '#adbcfd'; // minsk-100
                            newLabel.style.color = '';
                            newLabel.style.boxShadow = '';
                            newLabel.classList.remove('selected'); // Enlever la classe pour l'icône
                        }
                    }

                    // Initialiser l'état visuel (checkbox cochée par défaut)
                    updateCheckboxState();

                    // Ajouter l'event listener pour les futurs changements
                    newCheckbox.addEventListener('change', updateCheckboxState);

                    // Vider le champ de saisie
                    categoryNameInput.value = '';

                } else {
                    notifications.error(response.error);
                }
            },
            function(error) {
                notifications.error(error);
                submitBtn.disabled = false;
                submitBtn.querySelector('#create_category_btn_text').textContent = 'Ajouter la catégorie';

            }
        )
    });
    
});