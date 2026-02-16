/**
 * E-BIBLIO - JAVASCRIPT CORRIGÉ
 * Sans cursor personnalisé, optimisé et performant
 * @version 2.1
 */

// ========================================
// CONFIGURATION GLOBALE
// ========================================
const EBiblio = {
    animations: {
        duration: 300,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
    },
    particles: {
        count: 30, // Réduit pour meilleures performances
        colors: ['#667eea', '#764ba2', '#4facfe']
    }
};

// ========================================
// PARTICULES ANIMÉES D'ARRIÈRE-PLAN
// ========================================
class ParticleSystem {
    constructor() {
        this.particles = [];
        this.init();
    }

    init() {
        // Créer le canvas
        this.canvas = document.createElement('canvas');
        this.canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            opacity: 0.3;
        `;
        document.body.insertBefore(this.canvas, document.body.firstChild);

        this.ctx = this.canvas.getContext('2d');
        this.resize();
        this.createParticles();
        this.animate();

        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        const particleCount = window.innerWidth < 768 ? 15 : 30; // Moins sur mobile

        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                radius: Math.random() * 2 + 1,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                color: EBiblio.particles.colors[Math.floor(Math.random() * EBiblio.particles.colors.length)]
            });
        }
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;

            // Rebondir sur les bords
            if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;

            // Dessiner la particule
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = particle.color;
            this.ctx.fill();

            // Connecter les particules proches
            this.particles.forEach(other => {
                const dx = particle.x - other.x;
                const dy = particle.y - other.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 120) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(other.x, other.y);
                    this.ctx.strokeStyle = `${particle.color}${Math.floor((1 - distance / 120) * 25).toString(16)}`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            });
        });

        requestAnimationFrame(() => this.animate());
    }
}

// Initialiser les particules
document.addEventListener('DOMContentLoaded', () => {
    new ParticleSystem();
});

// ========================================
// EFFET DE PARALLAXE SUR LE HERO
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const hero = document.querySelector('.hero');

    if (hero) {
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const scrolled = window.pageYOffset;
                    const parallax = scrolled * 0.3;
                    hero.style.transform = `translateY(${parallax}px)`;
                    hero.style.opacity = Math.max(0, 1 - (scrolled / 500));
                    ticking = false;
                });
                ticking = true;
            }
        });
    }
});

// ========================================
// MENU MOBILE AVANCÉ
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileNav = document.getElementById('mobileNav');
    const body = document.body;

    if (mobileMenuBtn && mobileNav) {
        mobileMenuBtn.addEventListener('click', function() {
            const isActive = mobileNav.classList.toggle('active');
            this.classList.toggle('active');

            // Bloquer le scroll
            body.style.overflow = isActive ? 'hidden' : '';

            // Animation des liens
            if (isActive) {
                const links = mobileNav.querySelectorAll('a');
                links.forEach((link, index) => {
                    link.style.opacity = '0';
                    link.style.transform = 'translateX(-20px)';
                    setTimeout(() => {
                        link.style.transition = 'all 0.3s ease';
                        link.style.opacity = '1';
                        link.style.transform = 'translateX(0)';
                    }, index * 50);
                });
            }
        });

        // Fermer en cliquant sur un lien
        mobileNav.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', function() {
                mobileNav.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                body.style.overflow = '';
            });
        });

        // Fermer en cliquant en dehors
        document.addEventListener('click', function(e) {
            if (mobileNav.classList.contains('active') &&
                !mobileNav.contains(e.target) &&
                !mobileMenuBtn.contains(e.target)) {
                mobileNav.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
                body.style.overflow = '';
            }
        });
    }
});

// ========================================
// HEADER SCROLL EFFECT
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('.header');

    if (header) {
        let lastScroll = 0;
        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const currentScroll = window.pageYOffset;

                    if (currentScroll > 50) {
                        header.classList.add('scrolled');
                    } else {
                        header.classList.remove('scrolled');
                    }

                    // Hide/show header on scroll
                    if (currentScroll > lastScroll && currentScroll > 500) {
                        header.style.transform = 'translateY(-100%)';
                    } else {
                        header.style.transform = 'translateY(0)';
                    }

                    lastScroll = currentScroll;
                    ticking = false;
                });
                ticking = true;
            }
        });
    }
});

// ========================================
// ANIMATIONS AU SCROLL (INTERSECTION OBSERVER)
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(30px)';

                setTimeout(() => {
                    entry.target.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observer les éléments
    const elementsToAnimate = document.querySelectorAll('.book-card, .category-card, .section-title, .stat-card');
    elementsToAnimate.forEach((element, index) => {
        element.style.transitionDelay = `${index * 30}ms`;
        observer.observe(element);
    });
});

// ========================================
// MESSAGES AVEC AUTO-DISMISS
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.message');

    messages.forEach((message, index) => {
        message.style.animationDelay = `${index * 100}ms`;

        // Barre de progression
        const progressBar = document.createElement('div');
        progressBar.style.cssText = `
            position: absolute;
            bottom: 0;
            left: 0;
            height: 3px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 100%;
            transform-origin: left;
            animation: progress 5s linear forwards;
        `;
        message.appendChild(progressBar);

        // Auto-dismiss
        setTimeout(() => {
            message.style.animation = 'slideOutRight 0.5s ease forwards';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });
});

// Animations CSS dynamiques
const progressStyle = document.createElement('style');
progressStyle.textContent = `
    @keyframes progress {
        from { transform: scaleX(1); }
        to { transform: scaleX(0); }
    }
    @keyframes slideOutRight {
        to {
            transform: translateX(120%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(progressStyle);

// ========================================
// VALIDATION FORMULAIRE
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');

        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateInput(this);
            });

            input.addEventListener('input', function() {
                if (this.classList.contains('error')) {
                    validateInput(this);
                }
            });
        });

        form.addEventListener('submit', function(e) {
            let isValid = true;

            inputs.forEach(input => {
                if (!validateInput(input)) {
                    isValid = false;
                }
            });

            // Validation fichiers
            const fileInput = form.querySelector('input[type="file"][accept*="pdf"]');
            if (fileInput && fileInput.files.length > 0) {
                const file = fileInput.files[0];
                const maxSize = 50 * 1024 * 1024; // 50 MB

                if (file.size > maxSize) {
                    e.preventDefault();
                    showNotification('Le fichier PDF est trop volumineux (max 50 MB)', 'error');
                    isValid = false;
                }

                if (file.type !== 'application/pdf') {
                    e.preventDefault();
                    showNotification('Veuillez sélectionner un fichier PDF valide', 'error');
                    isValid = false;
                }
            }

            // Validation image
            const imageInput = form.querySelector('input[type="file"][accept*="image"]');
            if (imageInput && imageInput.files.length > 0) {
                const file = imageInput.files[0];
                const maxSize = 5 * 1024 * 1024; // 5 MB

                if (file.size > maxSize) {
                    e.preventDefault();
                    showNotification('L\'image est trop volumineuse (max 5 MB)', 'error');
                    isValid = false;
                }
            }

            if (!isValid) {
                e.preventDefault();
            }
        });
    });

    function validateInput(input) {
        const value = input.value.trim();
        let isValid = true;
        let message = '';

        // Supprimer anciennes erreurs
        const oldError = input.parentElement.querySelector('.validation-error');
        if (oldError) oldError.remove();
        input.classList.remove('error');

        // Validation
        if (input.hasAttribute('required') && !value) {
            isValid = false;
            message = 'Ce champ est obligatoire';
        } else if (input.type === 'email' && value && !isValidEmail(value)) {
            isValid = false;
            message = 'Email invalide';
        } else if (input.type === 'password' && value.length > 0 && value.length < 8) {
            isValid = false;
            message = 'Minimum 8 caractères';
        }

        if (!isValid) {
            input.classList.add('error');
            const error = document.createElement('div');
            error.className = 'validation-error';
            error.textContent = message;
            error.style.cssText = `
                color: #ef4444;
                font-size: 0.875rem;
                margin-top: 0.25rem;
                animation: shake 0.3s ease;
            `;
            input.parentElement.appendChild(error);
        }

        return isValid;
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
});

// Animation shake
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    input.error,
    textarea.error,
    select.error {
        border-color: #ef4444 !important;
        animation: shake 0.3s ease;
    }
`;
document.head.appendChild(shakeStyle);

// ========================================
// PRÉVISUALISATION D'IMAGE
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');

    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];

            if (file) {
                // Supprimer ancienne preview
                const oldPreview = this.parentElement.querySelector('.image-preview');
                if (oldPreview) oldPreview.remove();

                // Créer preview
                const reader = new FileReader();
                reader.onload = function(event) {
                    const preview = document.createElement('div');
                    preview.className = 'image-preview';
                    preview.style.cssText = `
                        margin-top: 1rem;
                        animation: fadeInUp 0.5s ease;
                    `;
                    preview.innerHTML = `
                        <div style="position: relative; display: inline-block;">
                            <img src="${event.target.result}"
                                 style="max-width: 200px; max-height: 200px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.2);"
                                 alt="Prévisualisation">
                            <div style="margin-top: 0.5rem; font-size: 0.875rem; color: #64748b;">
                                ${file.name} (${(file.size / 1024).toFixed(2)} KB)
                            </div>
                        </div>
                    `;
                    input.parentElement.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        });
    });
});

// ========================================
// LOADER POUR UPLOAD
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const uploadForms = document.querySelectorAll('form[enctype="multipart/form-data"]');

    uploadForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const fileInputs = form.querySelectorAll('input[type="file"]');
            let hasFile = false;

            fileInputs.forEach(input => {
                if (input.files.length > 0) hasFile = true;
            });

            if (hasFile) {
                showLoader();
            }
        });
    });
});

function showLoader() {
    const loader = document.createElement('div');
    loader.className = 'upload-loader';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 99999;
        animation: fadeIn 0.3s ease;
    `;

    loader.innerHTML = `
        <div style="
            width: 60px;
            height: 60px;
            border: 4px solid rgba(102, 126, 234, 0.2);
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1.5rem;
        "></div>
        <div style="color: white; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">
            Upload en cours...
        </div>
        <div style="color: rgba(255, 255, 255, 0.7); font-size: 1rem;">
            Veuillez patienter
        </div>
    `;

    const spinStyle = document.createElement('style');
    spinStyle.textContent = `
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    `;
    document.head.appendChild(spinStyle);

    document.body.appendChild(loader);
}

// ========================================
// SYSTÈME DE NOTIFICATIONS
// ========================================
function showNotification(message, type = 'info') {
    const container = document.querySelector('.messages-container') || createNotificationContainer();

    const notification = document.createElement('div');
    notification.className = `message message-${type}`;
    notification.style.cssText = `
        background: white;
        padding: 1.25rem;
        border-radius: 1rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        animation: slideInRight 0.5s ease;
        border-left: 4px solid ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#06b6d4'};
    `;

    const icons = {
        success: '✓',
        error: '✕',
        warning: '⚠',
        info: 'ℹ'
    };

    notification.innerHTML = `
        <span style="font-size: 1.5rem; flex-shrink: 0;">${icons[type] || icons.info}</span>
        <span style="flex: 1;">${message}</span>
        <button onclick="this.parentElement.remove()" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #94a3b8; padding: 0;">×</button>
    `;

    container.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.5s ease forwards';
        setTimeout(() => notification.remove(), 500);
    }, 5000);
}

function createNotificationContainer() {
    const container = document.createElement('div');
    container.className = 'messages-container';
    container.style.cssText = `
        position: fixed;
        top: 100px;
        right: 1.5rem;
        z-index: 9999;
        max-width: 400px;
    `;
    document.body.appendChild(container);
    return container;
}

// Animation notification
const notifStyle = document.createElement('style');
notifStyle.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(notifStyle);

// ========================================
// SMOOTH SCROLL
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
// COMPTEUR ANIMÉ
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('.stat-value');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.textContent) || 0;
                animateCounter(counter, 0, target, 2000);
                observer.unobserve(counter);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
});

function animateCounter(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            element.textContent = end;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

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

// Compteur de caractères pour commentaire
const commentaireInput = document.querySelector('textarea[name="commentaire"]');
if (commentaireInput) {
    const charCount = document.querySelector('.char-count');
    commentaireInput.addEventListener('input', function() {
        if (charCount) {
            charCount.textContent = `${this.value.length} / 500 caractères`;
        }
    });
}
// ========================================
// LOG DE SUCCÈS
// ========================================
console.log('%c🚀 E-Biblio v2.1 (Optimisé)', 'font-size: 18px; font-weight: bold; color: #667eea;');
console.log('%c✨ JavaScript chargé - Cursor désactivé', 'font-size: 12px; color: #764ba2;');