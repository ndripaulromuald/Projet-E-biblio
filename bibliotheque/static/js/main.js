// ========================================
// MENU MOBILE
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileNav = document.getElementById('mobileNav');

    if (mobileMenuBtn && mobileNav) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileNav.classList.toggle('active');

            // Animation du bouton hamburger
            this.classList.toggle('active');
        });

        // Fermer le menu quand on clique sur un lien
        const mobileLinks = mobileNav.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileNav.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            });
        });
    }
});

// ========================================
// AUTO-FERMETURE DES MESSAGES
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');

    messages.forEach(message => {
        // Fermeture automatique après 5 secondes
        setTimeout(() => {
            message.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
});

// Animation de sortie
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ========================================
// VALIDATION FORMULAIRE CÔTÉ CLIENT
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const fileInput = form.querySelector('input[type="file"][accept=".pdf"]');

            if (fileInput && fileInput.files.length > 0) {
                const file = fileInput.files[0];
                const maxSize = 50 * 1024 * 1024; // 50 MB

                // Vérifier la taille
                if (file.size > maxSize) {
                    e.preventDefault();
                    alert('Le fichier PDF est trop volumineux. Taille maximale : 50 MB');
                    return false;
                }

                // Vérifier le type
                if (file.type !== 'application/pdf') {
                    e.preventDefault();
                    alert('Veuillez sélectionner un fichier PDF valide.');
                    return false;
                }
            }

            // Vérifier l'image de couverture
            const imageInput = form.querySelector('input[type="file"][accept="image/*"]');
            if (imageInput && imageInput.files.length > 0) {
                const file = imageInput.files[0];
                const maxSize = 5 * 1024 * 1024; // 5 MB

                if (file.size > maxSize) {
                    e.preventDefault();
                    alert('L\'image est trop volumineuse. Taille maximale : 5 MB');
                    return false;
                }

                if (!file.type.startsWith('image/')) {
                    e.preventDefault();
                    alert('Veuillez sélectionner une image valide (JPG, PNG).');
                    return false;
                }
            }
        });
    });
});

// ========================================
// CONFIRMATION SUPPRESSION
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const deleteLinks = document.querySelectorAll('a[href*="supprimer"]');

    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!this.closest('.delete-container')) {
                if (!confirm('Êtes-vous sûr de vouloir supprimer ce livre ?')) {
                    e.preventDefault();
                }
            }
        });
    });
});

// ========================================
// PRÉVISUALISATION D'IMAGE
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept="image/*"]');

    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];

            if (file) {
                // Supprimer l'ancienne prévisualisation si elle existe
                const oldPreview = this.parentElement.querySelector('.image-preview');
                if (oldPreview) {
                    oldPreview.remove();
                }

                // Créer la nouvelle prévisualisation
                const reader = new FileReader();
                reader.onload = function(event) {
                    const preview = document.createElement('div');
                    preview.className = 'image-preview';
                    preview.style.marginTop = '10px';
                    preview.innerHTML = `
                        <img src="${event.target.result}"
                             style="max-width: 200px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
                             alt="Prévisualisation">
                    `;
                    input.parentElement.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        });
    });
});

// ========================================
// SMOOTH SCROLL
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

// ========================================
// COMPTEUR DE CARACTÈRES POUR TEXTAREA
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea');

    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            const counter = document.createElement('div');
            counter.className = 'char-counter';
            counter.style.fontSize = '14px';
            counter.style.color = '#666';
            counter.style.marginTop = '5px';
            counter.textContent = `0 / ${maxLength} caractères`;

            textarea.parentElement.appendChild(counter);

            textarea.addEventListener('input', function() {
                const length = this.value.length;
                counter.textContent = `${length} / ${maxLength} caractères`;

                if (length > maxLength * 0.9) {
                    counter.style.color = '#e74c3c';
                } else {
                    counter.style.color = '#666';
                }
            });
        }
    });
});

// ========================================
// LOADER POUR UPLOAD DE FICHIERS
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form[enctype="multipart/form-data"]');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const fileInputs = form.querySelectorAll('input[type="file"]');
            let hasFile = false;

            fileInputs.forEach(input => {
                if (input.files.length > 0) {
                    hasFile = true;
                }
            });

            if (hasFile) {
                // Créer un loader
                const loader = document.createElement('div');
                loader.className = 'upload-loader';
                loader.style.cssText = `
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.8);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    z-index: 9999;
                    color: white;
                `;
                loader.innerHTML = `
                    <div style="font-size: 48px; margin-bottom: 20px;">📤</div>
                    <div style="font-size: 24px; margin-bottom: 10px;">Upload en cours...</div>
                    <div style="font-size: 16px; opacity: 0.8;">Veuillez patienter, ne fermez pas cette page.</div>
                `;

                document.body.appendChild(loader);
            }
        });
    });
});

// ========================================
// RECHERCHE EN TEMPS RÉEL (OPTIONNEL)
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');

    if (searchInput && searchInput.form) {
        let timeout = null;

        searchInput.addEventListener('input', function() {
            clearTimeout(timeout);

            // Attendre 500ms après que l'utilisateur ait arrêté de taper
            timeout = setTimeout(() => {
                if (this.value.length >= 3 || this.value.length === 0) {
                    // Soumettre automatiquement le formulaire
                    // this.form.submit();
                }
            }, 500);
        });
    }
});

console.log('🚀 E-Biblio JavaScript chargé avec succès!');