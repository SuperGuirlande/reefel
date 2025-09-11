const modal = document.getElementById('image_modal')
const closeModalBtn = document.getElementById('close_modal_btn')
const image = document.getElementById('image')
const paragraph = document.getElementById('paragraph')

const thumb = document.getElementById('post_thumbnail')
const show = document.getElementById('show')


// Fermer la modal
closeModalBtn.addEventListener('click', function () {
    modal.classList.add('hidden')

})

document.addEventListener('keydown', function (event) {

    if (!modal.classList.contains('hidden')) {
        if (event.key === "Escape") {
            modal.classList.add('hidden')
        }
    }
})

// Afficher la modal lors du clique sur l'image
thumb.addEventListener('click', function () {
    // Récupérer l'url
    const url = thumb.dataset.imageUrl
    // Récupérer la caption
    const caption = thumb.dataset.caption
    // Mettre l'url en data de la modal
    image.src = url
    // Mettre la cation en data du <p>
    paragraph.textContent = caption
    // Mettre la cation en alt de l'image
    image.alt = caption
    // Montrer la modal
    modal.classList.remove('hidden')
})