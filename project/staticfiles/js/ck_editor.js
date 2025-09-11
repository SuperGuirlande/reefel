document.addEventListener('DOMContentLoaded', function() {
    // Trouver tous les éléments oembed pour tous les fournisseurs
    const oembeds = document.querySelectorAll('figure.media oembed[url]');
    
    oembeds.forEach(function(oembed) {
        const url = oembed.getAttribute('url');
        if (!url) return;
        
        let embedUrl = '';
        
        // Gestion Dailymotion
        if (url.includes('dai.ly') || url.includes('dailymotion.com')) {
            let videoId = '';
            if (url.includes('dai.ly')) {
                videoId = url.split('/').pop();
            } else if (url.includes('dailymotion.com')) {
                videoId = url.split('/').pop().split('_')[0];
            }
            if (videoId) {
                embedUrl = `https://www.dailymotion.com/embed/video/${videoId}`;
            }
        }
        
        // Gestion YouTube
        else if (url.includes('youtube.com') || url.includes('youtu.be')) {
            let videoId = '';
            if (url.includes('youtu.be/')) {
                videoId = url.split('youtu.be/')[1].split('?')[0];
            } else if (url.includes('youtube.com/watch?v=')) {
                videoId = url.split('v=')[1].split('&')[0];
            } else if (url.includes('youtube.com/embed/')) {
                videoId = url.split('embed/')[1].split('?')[0];
            }
            if (videoId) {
                embedUrl = `https://www.youtube.com/embed/${videoId}`;
            }
        }
        
        // Gestion Vimeo
        else if (url.includes('vimeo.com')) {
            const videoId = url.split('/').pop().split('?')[0];
            if (videoId) {
                embedUrl = `https://player.vimeo.com/video/${videoId}`;
            }
        }
        
        if (!embedUrl) return;
        
        // Créer un conteneur pour remplacer oembed
        const container = document.createElement('div');
        container.style.position = 'relative';
        container.style.paddingBottom = '56.25%';
        container.style.height = '0';
        container.style.overflow = 'hidden';
        container.style.width = '100%';
        
        // Créer l'iframe
        const iframe = document.createElement('iframe');
        iframe.src = embedUrl;
        iframe.style.position = 'absolute';
        iframe.style.top = '0';
        iframe.style.left = '0';
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.setAttribute('frameborder', '0');
        iframe.setAttribute('allowfullscreen', '');
        iframe.setAttribute('allow', 'autoplay; encrypted-media');
        
        // Ajouter l'iframe au conteneur
        container.appendChild(iframe);
        
        // Remplacer l'élément oembed par le conteneur
        oembed.parentNode.replaceChild(container, oembed);
    });
});