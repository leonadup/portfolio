document.addEventListener('DOMContentLoaded', function() {
    // Activer le mode sombre si préféré par l'utilisateur
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    if (prefersDarkScheme.matches) {
        document.body.classList.add('dark-theme');
        document.getElementById('theme-toggle').checked = true;
    }

    // Animation des sections au défilement
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.fade-in').forEach(element => {
        observer.observe(element);
    });

    // Animation des barres de compétences
    const skillsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBars = entry.target.querySelectorAll('.progress');
                progressBars.forEach(bar => {
                    const width = bar.getAttribute('data-width');
                    setTimeout(() => {
                        bar.style.width = width;
                    }, 200);
                });
            }
        });
    }, { threshold: 0.5 });

    document.querySelectorAll('.skills-category').forEach(category => {
        skillsObserver.observe(category);
    });

    // Fonctionnalité de menu responsive
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        menuToggle.classList.toggle('active');
        
        // Changer l'icône du menu
        const icon = menuToggle.querySelector('i');
        if (navLinks.classList.contains('active')) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-times');
        } else {
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
        }
    });

    // Fermer le menu mobile après avoir cliqué sur un lien
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            menuToggle.classList.remove('active');
            menuToggle.querySelector('i').classList.remove('fa-times');
            menuToggle.querySelector('i').classList.add('fa-bars');
        });
    });

    // Navigation active au défilement
    const sections = document.querySelectorAll('section[id]');
    
    function highlightNavigation() {
        const scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                document.querySelector(`.nav-links a[href="#${sectionId}"]`).classList.add('active');
            } else {
                document.querySelector(`.nav-links a[href="#${sectionId}"]`).classList.remove('active');
            }
        });
    }
    
    window.addEventListener('scroll', highlightNavigation);

    // Toggle du thème clair/sombre
    const themeToggle = document.getElementById('theme-toggle');
    
    themeToggle.addEventListener('change', () => {
        document.body.classList.toggle('dark-theme');
        
        // Sauvegarder la préférence dans localStorage
        if (document.body.classList.contains('dark-theme')) {
            localStorage.setItem('theme', 'dark');
        } else {
            localStorage.setItem('theme', 'light');
        }
    });
    
    // Vérifier la préférence sauvegardée
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeToggle.checked = true;
    } else if (savedTheme === 'light') {
        document.body.classList.remove('dark-theme');
        themeToggle.checked = false;
    }

    // Filtrage des projets
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Enlever la classe active de tous les boutons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Ajouter la classe active au bouton cliqué
            button.classList.add('active');
            
            const filter = button.getAttribute('data-filter');
            
            projectCards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-category') === filter) {
                    card.style.display = 'flex';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 100);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });

    // Formulaire de contact avec validation améliorée
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validation de base
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const subject = document.getElementById('subject').value.trim();
            const message = document.getElementById('message').value.trim();
            
            let isValid = true;
            const errorMessages = [];
            
            // Réinitialiser les messages d'erreur
            document.querySelectorAll('.error-message').forEach(el => el.remove());
            document.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
            
            // Valider le nom
            if (name === '') {
                showError('name', 'Veuillez entrer votre nom');
                isValid = false;
            }
            
            // Valider l'email
            if (email === '') {
                showError('email', 'Veuillez entrer votre email');
                isValid = false;
            } else if (!isValidEmail(email)) {
                showError('email', 'Veuillez entrer un email valide');
                isValid = false;
            }
            
            // Valider le sujet
            if (subject === '') {
                showError('subject', 'Veuillez entrer un sujet');
                isValid = false;
            }
            
            // Valider le message
            if (message === '') {
                showError('message', 'Veuillez entrer votre message');
                isValid = false;
            } else if (message.length < 20) {
                showError('message', 'Votre message doit contenir au moins 20 caractères');
                isValid = false;
            }
            
            // Si tout est valide, envoyer le formulaire
            if (isValid) {
                // Animation de chargement
                const submitBtn = contactForm.querySelector('button[type="submit"]');
                const originalBtnText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi en cours...';
                submitBtn.disabled = true;
                
                // Simuler l'envoi (à remplacer par votre logique d'envoi réelle)
                setTimeout(() => {
                    // Afficher un message de succès
                    const successMessage = document.createElement('div');
                    successMessage.className = 'success-message';
                    successMessage.textContent = 'Votre message a été envoyé avec succès!';
                    contactForm.appendChild(successMessage);
                    
                    // Réinitialiser le formulaire
                    contactForm.reset();
                    
                    // Restaurer le bouton
                    submitBtn.innerHTML = originalBtnText;
                    submitBtn.disabled = false;
                    
                    // Faire disparaître le message de succès après 5 secondes
                    setTimeout(() => {
                        successMessage.style.opacity = '0';
                        setTimeout(() => {
                            successMessage.remove();
                        }, 300);
                    }, 5000);
                }, 2000);
                
                // Dans un cas réel, vous utiliseriez fetch ou XMLHttpRequest pour envoyer les données à votre serveur
                // Exemple avec fetch:
                /*
                fetch('votre-endpoint.php', {
                    method: 'POST',
                    body: new FormData(contactForm)
                })
                .then(response => response.json())
                .then(data => {
                    // Traitement de la réponse
                    if (data.success) {
                        // Message de succès
                    } else {
                        // Message d'erreur
                    }
                    submitBtn.innerHTML = originalBtnText;
                    submitBtn.disabled = false;
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    // Message d'erreur
                    submitBtn.innerHTML = originalBtnText;
                    submitBtn.disabled = false;
                });
                */
            }
        });
    }
    
    // Fonction d'aide pour valider les emails
    function isValidEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }
    
    // Fonction pour afficher une erreur
    function showError(inputId, message) {
        const input = document.getElementById(inputId);
        input.classList.add('error');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        input.parentNode.insertBefore(errorDiv, input.nextSibling);
    }

    // Animation du bouton retour en haut
    const backToTopBtn = document.getElementById('backToTop');
    
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });
        
        backToTopBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Animation des compétences au survol
    const skillItems = document.querySelectorAll('.skill-item');
    
    skillItems.forEach(item => {
        item.addEventListener('mouseenter', () => {
            item.querySelector('.progress').classList.add('highlight');
        });
        
        item.addEventListener('mouseleave', () => {
            item.querySelector('.progress').classList.remove('highlight');
        });
    });

    // Modales pour les projets
    const projectLinks = document.querySelectorAll('.project-card .view-details');
    const modalOverlay = document.querySelector('.modal-overlay');
    const modalCloseBtn = document.querySelector('.modal-close');
    
    if (projectLinks.length > 0 && modalOverlay) {
        projectLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                
                const projectId = link.getAttribute('data-project');
                const projectDetails = document.querySelector(`.project-details[data-project="${projectId}"]`);
                
                if (projectDetails) {
                    // Afficher les détails du projet dans la modale
                    document.querySelector('.modal-content').innerHTML = '';
                    document.querySelector('.modal-content').appendChild(projectDetails.cloneNode(true));
                    
                    // Afficher la modale
                    modalOverlay.classList.add('active');
                    document.body.style.overflow = 'hidden';
                    
                    // Animation d'entrée
                    setTimeout(() => {
                        document.querySelector('.modal').classList.add('active');
                    }, 10);
                }
            });
        });
        
        // Fermer la modale
        if (modalCloseBtn) {
            modalCloseBtn.addEventListener('click', () => {
                closeModal();
            });
        }
        
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });
        
        function closeModal() {
            document.querySelector('.modal').classList.remove('active');
            
            setTimeout(() => {
                modalOverlay.classList.remove('active');
                document.body.style.overflow = '';
            }, 300);
        }
    }

    // Initialiser un carrousel pour les témoignages (si présent)
    const testimonialsContainer = document.querySelector('.testimonials-carousel');
    
    if (testimonialsContainer) {
        let currentSlide = 0;
        const slides = testimonialsContainer.querySelectorAll('.testimonial');
        const totalSlides = slides.length;
        
        // Créer les boutons de navigation
        const prevBtn = document.createElement('button');
        prevBtn.className = 'carousel-nav prev';
        prevBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';
        
        const nextBtn = document.createElement('button');
        nextBtn.className = 'carousel-nav next';
        nextBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';
        
        testimonialsContainer.appendChild(prevBtn);
        testimonialsContainer.appendChild(nextBtn);
        
        // Créer les indicateurs
        const indicators = document.createElement('div');
        indicators.className = 'carousel-indicators';
        
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('span');
            dot.className = i === 0 ? 'dot active' : 'dot';
            dot.setAttribute('data-index', i);
            indicators.appendChild(dot);
        }
        
        testimonialsContainer.appendChild(indicators);
        
        // Fonction pour montrer un slide
        function showSlide(index) {
            if (index < 0) {
                currentSlide = totalSlides - 1;
            } else if (index >= totalSlides) {
                currentSlide = 0;
            } else {
                currentSlide = index;
            }
            
            const offset = -currentSlide * 100;
            testimonialsContainer.querySelector('.testimonials-wrapper').style.transform = `translateX(${offset}%)`;
            
            // Mettre à jour les indicateurs
            document.querySelectorAll('.carousel-indicators .dot').forEach((dot, i) => {
                if (i === currentSlide) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }
        
        // Événements des boutons
        prevBtn.addEventListener('click', () => {
            showSlide(currentSlide - 1);
        });
        
        nextBtn.addEventListener('click', () => {
            showSlide(currentSlide + 1);
        });
        
        // Événements des indicateurs
        document.querySelectorAll('.carousel-indicators .dot').forEach(dot => {
            dot.addEventListener('click', () => {
                const slideIndex = parseInt(dot.getAttribute('data-index'));
                showSlide(slideIndex);
            });
        });
        
        // Défilement automatique
        let autoSlide = setInterval(() => {
            showSlide(currentSlide + 1);
        }, 5000);
        
        // Arrêter le défilement au survol
        testimonialsContainer.addEventListener('mouseenter', () => {
            clearInterval(autoSlide);
        });
        
        testimonialsContainer.addEventListener('mouseleave', () => {
            autoSlide = setInterval(() => {
                showSlide(currentSlide + 1);
            }, 5000);
        });
        
        // Support tactile
        let touchStartX = 0;
        let touchEndX = 0;
        
        testimonialsContainer.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, {passive: true});
        
        testimonialsContainer.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, {passive: true});
        
        function handleSwipe() {
            if (touchEndX < touchStartX - 50) {
                showSlide(currentSlide + 1);
            } else if (touchEndX > touchStartX + 50) {
                showSlide(currentSlide - 1);
            }
        }
    }

    // Animation du texte de la bannière (si présent)
    const bannerText = document.querySelector('.banner-text h1');
    
    if (bannerText) {
        const text = bannerText.textContent;
        bannerText.innerHTML = '';
        
        for (let i = 0; i < text.length; i++) {
            const span = document.createElement('span');
            span.textContent = text[i];
            span.style.animationDelay = `${i * 0.05}s`;
            bannerText.appendChild(span);
        }
    }

    // Lazy loading pour les images
    if ('IntersectionObserver' in window) {
        const imgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                        img.classList.add('loaded');
                    }
                    
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imgObserver.observe(img);
        });
    } else {
        // Fallback pour les navigateurs qui ne supportent pas IntersectionObserver
        document.querySelectorAll('img[data-src]').forEach(img => {
            img.src = img.getAttribute('data-src');
            img.removeAttribute('data-src');
        });
    }
});