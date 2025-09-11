// Fonction pour récupérer les cookies
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

// Fonction générique pour les requêtes AJAX avec fetch
function makeAjaxRequest(url, method, data, successCallback, errorCallback) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    };

    if (method !== 'GET' && data) {
        options.body = JSON.stringify(data);
    }

    fetch(url, options)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (successCallback) successCallback(data);
            } else {
                if (errorCallback) errorCallback(data.error);
            }
        })
        .catch(error => {
            console.error('Erreur AJAX:', error);
            if (errorCallback) errorCallback('Erreur de connexion');
        });
}