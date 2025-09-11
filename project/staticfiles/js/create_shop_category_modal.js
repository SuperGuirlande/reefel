// Récupérer le token CSRF
let csrftoken;
try {
    csrftoken = getCookie('csrftoken');
    console.log('Token CSRF:', csrftoken ? 'trouvé' : 'non trouvé');
} catch (error) {
    console.error('Erreur récupération token CSRF:', error);
}

// Vérifier que les fonctions nécessaires sont disponibles
if (typeof getCookie === 'undefined') {
    console.error('Fonction getCookie non trouvée - vérifiez que base.js est chargé');
}
if (typeof makeAjaxRequest === 'undefined') {
    console.error('Fonction makeAjaxRequest non trouvée - vérifiez que base.js est chargé');
}
if (typeof notifications === 'undefined') {
    console.error('Objet notifications non trouvé - vérifiez que notifications.js est chargé');
}

// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    const createCategoryModal = document.getElementById('create_category_modal')
    const modalTitle = document.getElementById('category_modal_title')
    const closeCategoryModalBtn = document.getElementById('close_category_modal_button')

    const createCategoryBtn = document.getElementById('create_category_button')
    const createSubCategoryBtn = document.getElementById('create_subcategory_button')

    const submitCategoryBtn = document.getElementById('submit_category_btn')
    const modalBtnText = submitCategoryBtn.querySelector('#modal_btn_text')
    const categoryInput = document.getElementById('category_input')

    // Éléments pour les sous-catégories
    const parentCategoryContainer = document.getElementById('parent_category_container')
    const parentCategorySelect = document.getElementById('parent_category_select')

    // Vérifier que tous les éléments existent
    if (!createCategoryModal || !closeCategoryModalBtn || !createCategoryBtn || !submitCategoryBtn || !categoryInput) {
        return; // Sortir si les éléments n'existent pas
    }

    let categoryName = ""

    // Ouvrir la modal pour les categories
    createCategoryBtn.addEventListener('click', function(event) {
        event.preventDefault();
        modalTitle.innerText = "Créer une catégorie"
        submitCategoryBtn.setAttribute('data-type', 'category')
        modalBtnText.innerText = "Nouvelle Catégorie"
        categoryInput.placeholder = "Nom de la catégorie";
        
        // Masquer le select de catégorie parent
        if (parentCategoryContainer) {
            parentCategoryContainer.classList.add('hidden')
        }
        
        createCategoryModal.classList.remove('hidden')
    })
    
    // Ouvrir la modal pour les souscategories
    createSubCategoryBtn.addEventListener('click', function(event) {
        event.preventDefault();
        modalTitle.innerText = "Créer une sous-catégorie"
        submitCategoryBtn.setAttribute('data-type', 'subcategory')
        modalBtnText.innerText = "Nouvelle Sous-Catégorie"
        categoryInput.placeholder = "Nom de la sous-catégorie";
        
        // Afficher le select de catégorie parent
        if (parentCategoryContainer) {
            parentCategoryContainer.classList.remove('hidden')
        }
        
        createCategoryModal.classList.remove('hidden')
    })

    // Fonction pour ajouter une option au select
    function addCategoryToSelect(categoryId, categoryName) {
        if (parentCategorySelect) {
            const option = document.createElement('option');
            option.value = categoryId;
            option.textContent = categoryName;
            parentCategorySelect.appendChild(option);
        }
    }

    // Soumettre la catégorie
    function submitCategory() {
        // Désactiver le bouton
        submitCategoryBtn.disabled = true;
        
        // Récupérer les données
        categoryName = categoryInput.value.trim()
        createCategoryUrl = submitCategoryBtn.getAttribute('data-url');
        dataType = submitCategoryBtn.getAttribute('data-type');
        
        // Récupérer la catégorie parent pour les sous-catégories
        let parentCategoryId = null;
        if (dataType === 'subcategory' && parentCategorySelect) {
            parentCategoryId = parentCategorySelect.value;
            if (!parentCategoryId) {
                alert('Veuillez sélectionner une catégorie parent');
                submitCategoryBtn.disabled = false;
                return;
            }
        }
        
        if (categoryName) {
            const requestData = {
                category_type: dataType,
                category_name: categoryName
            };
            
            // Ajouter l'ID de la catégorie parent si c'est une sous-catégorie
            if (parentCategoryId) {
                requestData.parent_category_id = parentCategoryId;
            }

            // Appeler la fonction ajax
            makeAjaxRequest(
                createCategoryUrl,
                'POST',
                requestData,
                // Fonction de succès
                function(response) {
                    console.log('Réponse reçue:', response);
                    try {
                        if (response.success) {
                            console.log('Succès confirmé, type:', dataType);
                            
                            // Réinitialiser le bouton
                            modalBtnText.textContent = dataType === 'category' ? 'Nouvelle Catégorie' : 'Nouvelle Sous-Catégorie';
                            submitCategoryBtn.disabled = false;

                            /// MODIFIER LE DOM ///
                            if (dataType == 'category') {
                                console.log('Traitement catégorie:', response.category);
                                handleNewCategory(response.category);
                            } else if (dataType == 'subcategory') {
                                console.log('Traitement sous-catégorie:', response.subcategory);
                                handleNewSubCategory(response.subcategory);
                            }

                            // Créer la notification JavaScript
                            const notificationText = dataType === 'category' 
                                ? "Nouvelle catégorie : " + categoryName
                                : "Nouvelle sous-catégorie : " + categoryName;
                            notifications.success(notificationText);
                            
                            // Vider les champs
                            categoryInput.value = ""
                            if (parentCategorySelect) parentCategorySelect.value = "";
                            
                            // Fermer la fenêtre
                            createCategoryModal.classList.add('hidden')

                        } else {
                            console.log('Échec:', response.error);
                            notifications.error(response.error);
                            submitCategoryBtn.disabled = false;
                            modalBtnText.textContent = dataType === 'category' ? 'Nouvelle Catégorie' : 'Nouvelle Sous-Catégorie';
                        }
                    } catch (error) {
                        console.error('Erreur dans le callback de succès:', error);
                        notifications.error('Erreur lors du traitement: ' + error.message);
                        submitCategoryBtn.disabled = false;
                        modalBtnText.textContent = dataType === 'category' ? 'Nouvelle Catégorie' : 'Nouvelle Sous-Catégorie';
                    }
                },
                function(error) {
                    notifications.error(error);
                    submitCategoryBtn.disabled = false;
                    modalBtnText.textContent = dataType === 'category' ? 'Nouvelle Catégorie' : 'Nouvelle Sous-Catégorie';
                }
            );
        } else {
            alert('Veuillez renseigner un nom pour la nouvelle ' + (dataType === 'category' ? 'catégorie' : 'sous-catégorie'))
            submitCategoryBtn.disabled = false;
        }
    }

    // Fonction pour gérer l'ajout d'une nouvelle catégorie dans le DOM
    function handleNewCategory(category) {
        const noCategoryMessage = document.getElementById('no_category');
        let categoriesContainer = document.getElementById('categories_container');

        // Masquer le message "aucune catégorie" s'il existe
        if (noCategoryMessage && !noCategoryMessage.classList.contains('hidden')) {
            noCategoryMessage.classList.add('hidden');
            
            // Créer le container de catégories
            const mainContainer = noCategoryMessage.parentElement;
            categoriesContainer = document.createElement('div');
            categoriesContainer.className = 'grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6';
            categoriesContainer.id = 'categories_container';
            mainContainer.appendChild(categoriesContainer);
        }

        // Créer la nouvelle carte de catégorie
        const categoryCard = document.createElement('div');
        categoryCard.className = 'category-card bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100';
        categoryCard.setAttribute('data-category-id', category.id);

        categoryCard.innerHTML = `
            <!-- Header de la catégorie -->
            <div class="bg-gradient-to-r from-minsk-500 to-minsk-600 p-4">
                <div class="flex items-center justify-between category-item">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                            <i class="fas fa-folder text-white text-lg"></i>
                        </div>
                        <div>
                            <h3 class="text-white font-bold text-lg">${category.name}</h3>
                            <p class="text-white text-opacity-80 text-sm">
                                0 sous-catégorie
                            </p>
                        </div>
                    </div>
                    <button class="delete-btn w-8 h-8 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center text-white transition-all duration-200 hover:scale-110"
                        onclick="deleteCategory(this, ${category.id}, '${category.name}', 'category')"
                        title="Supprimer la catégorie">
                        <i class="fas fa-trash text-sm"></i>
                    </button>
                </div>
            </div>

            <!-- Sous-catégories -->
            <div class="p-4">
                <div class="subcategories-container" data-parent-id="${category.id}">
                    <div class="text-center py-8">
                        <i class="fas fa-tags text-3xl text-gray-300 mb-3"></i>
                        <p class="text-gray-400 text-sm mb-4">Aucune sous-catégorie</p>
                        <button class="text-blue-500 hover:text-blue-600 text-sm font-medium transition-colors duration-200"
                            onclick="document.getElementById('create_subcategory_button').click()">
                            <i class="fas fa-plus mr-1"></i>
                            Ajouter une sous-catégorie
                        </button>
                    </div>
                </div>
            </div>
        `;

        if (categoriesContainer) {
            categoriesContainer.appendChild(categoryCard);
        }

        // Ajouter la nouvelle catégorie au select des sous-catégories
        addCategoryToSelect(category.id, category.name);
    }

    // Fonction pour gérer l'ajout d'une nouvelle sous-catégorie dans le DOM
    function handleNewSubCategory(subcategory) {
        try {
            console.log('Ajout sous-catégorie:', subcategory);
            const subcategoriesContainer = document.querySelector(`[data-parent-id="${subcategory.parent_id}"]`);
            
            if (!subcategoriesContainer) {
                console.error('Container sous-catégories non trouvé pour parent_id:', subcategory.parent_id);
                return;
            }

            // Chercher s'il y a déjà des sous-catégories ou si c'est le message vide
            let subcategoriesList = subcategoriesContainer.querySelector('.space-y-2');
            
            // S'il n'y a pas de liste, créer une nouvelle
            if (!subcategoriesList) {
                // Remplacer tout le contenu par une nouvelle liste
                subcategoriesContainer.innerHTML = '<div class="space-y-2"></div>';
                subcategoriesList = subcategoriesContainer.querySelector('.space-y-2');
            }

            // Créer le nouvel élément sous-catégorie
            const subCategoryElement = document.createElement('div');
            subCategoryElement.className = 'subcategory-item bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-lg p-3 flex items-center justify-between group transition-all duration-200';
            
            subCategoryElement.innerHTML = `
                <div class="flex items-center gap-3">
                    <div class="w-6 h-6 bg-blue-500 bg-opacity-20 rounded-full flex items-center justify-center">
                        <i class="fas fa-tag text-blue-600 text-xs"></i>
                    </div>
                    <span class="text-blue-800 font-medium">${subcategory.name}</span>
                </div>
                <button class="delete-btn w-6 h-6 bg-red-500 hover:bg-red-600 rounded-full flex items-center justify-center text-white transition-all duration-200 hover:scale-110"
                    onclick="deleteCategory(this, ${subcategory.id}, '${subcategory.name}', 'subcategory')"
                    title="Supprimer la sous-catégorie">
                    <i class="fas fa-times text-xs"></i>
                </button>
            `;

            subcategoriesList.appendChild(subCategoryElement);
            console.log('Sous-catégorie ajoutée au DOM');

            // Mettre à jour le compteur dans le header de la catégorie
            const categoryCard = subcategoriesContainer.closest('[data-category-id]');
            if (categoryCard) {
                const countElement = categoryCard.querySelector('.text-white.text-opacity-80');
                if (countElement) {
                    const currentCount = subcategoriesList.children.length;
                    countElement.textContent = `${currentCount} sous-catégorie${currentCount > 1 ? 's' : ''}`;
                    console.log('Compteur mis à jour:', currentCount);
                }
            }
        } catch (error) {
            console.error('Erreur dans handleNewSubCategory:', error);
            // Re-lancer l'erreur pour déclencher le catch de makeAjaxRequest
            throw error;
        }
    }

    ///// INPUTS /////

    // Soumettre par le bouton
    submitCategoryBtn.addEventListener('click', function(event) {
        event.preventDefault();
        submitCategory()
    })

    // Fermer la modal par le bouton
    closeCategoryModalBtn.addEventListener('click', function() {
        createCategoryModal.classList.add('hidden')
    })

    // UN SEUL listener pour les touches (Entrée ET Échap)
    document.addEventListener('keydown', function (event) {
        // Vérifier si la modal est ouverte
        if (!createCategoryModal.classList.contains('hidden')) {
            if (event.key === "Enter") {
                event.preventDefault();
                submitCategory()
            } else if (event.key === "Escape") {
                createCategoryModal.classList.add('hidden')
            }
        }
    })
})