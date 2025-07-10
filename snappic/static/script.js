document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const uploadStatus = document.getElementById('upload-status');
    const gallery = document.getElementById('gallery');

    if (uploadForm) {
        uploadForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(uploadForm);

            try {
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.success) {
                    uploadStatus.textContent = 'Bild erfolgreich hochgeladen!';
                    uploadForm.reset();
                } else {
                    uploadStatus.textContent = result.error || 'Upload fehlgeschlagen';
                }
            } catch (error) {
                uploadStatus.textContent = 'Fehler beim Upload';
                console.error('Upload error:', error);
            }
        });
    }

    if (gallery) {
        function refreshGallery() {
            fetch('/api/images')
                .then(response => response.json())
                .then(images => {
                    gallery.innerHTML = '';
                    images.forEach(image => {
                        const imgElement = document.createElement('div');
                        imgElement.innerHTML = `
                            <img src="/uploads/${image.filename}" alt="Gallery Image" class="gallery-image">
                            <div class="gallery-image-comment">${image.comment || ''}</div>
                        `;
                        gallery.appendChild(imgElement);
                    });
                })
                .catch(error => console.error('Gallery refresh error:', error));
        }

        // Initial gallery load
        refreshGallery();

        // Auto-refresh every 2 seconds
        setInterval(refreshGallery, 2000);
    }

    // Service Worker registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/service-worker.js')
                .then(registration => {
                    console.log('Service Worker registered:', registration);
                })
                .catch(error => {
                    console.log('Service Worker registration failed:', error);
                });
        });
    }
});