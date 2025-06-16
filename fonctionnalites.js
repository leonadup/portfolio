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

// Dictionnaire de traduction
const translations = {
    fr: {
        // Navigation
        "nav-home": "Accueil",
        "nav-about": "Présentation",
        "nav-experience": "Expériences",
        "nav-education": "Formations",
        "nav-skills": "Compétences",
        "nav-projects": "Projets",
        "nav-contact": "Contact",
        
        // Hero Section
        "hero-title": "Portfolio de Léona Dupont",
        "hero-subtitle": "Étudiante en BUT Informatique",
        "hero-contact": "Me contacter",
        "hero-projects": "Voir mes projets",
        
        // About Section
        "about-tag": "À propos",
        "about-title": "À propos de moi",
        "about-p1": "Je suis actuellement étudiante en deuxième année d'un BUT Informatique, une formation professionnalisante et polyvalente qui me permet d'acquérir des compétences solides dans divers domaines de l'informatique, tels que le développement d'applications web et mobiles, la gestion de bases de données, l'administration de systèmes et réseaux, ou encore la cybersécurité.",
        "about-p2": "À travers les nombreux projets en groupe et les mises en situation réelles, j'apprends à travailler en équipe, à résoudre des problèmes complexes et à m'adapter à des environnements techniques variés.",
        "about-p3": "Au-delà de mes études, je suis une personne curieuse et passionnée par le monde qui m'entoure. J'aime voyager, découvrir de nouvelles cultures et m'instruire en permanence, que ce soit à travers des documentaires, des lectures ou des films que je regarde d'ailleurs avec avidité, car ils me permettent aussi de voir le monde sous un autre angle.",
        "stat-years": "Années d'études",
        "stat-projects": "Projets réalisés",
        "stat-tech": "Technologies maîtrisées",
        
        // Experience Section
        "exp-tag": "Expériences",
        "exp-title": "Expériences professionnelles",
        "exp-enedis-title": "Stagiaire chez Enedis",
        "exp-enedis-date": "Janvier 2025 - Avril 2025",
        "exp-enedis-desc": "Aide à la migration de routeur vers une nouvelle PKI.",
        "exp-enedis-more": "Pour plus d'informations, veuillez consulter",
        "exp-enedis-report": "mon rapport de stage",
        "exp-carrefour-title": "Carrefour",
        "exp-carrefour-date": "Septembre 2023 - Août 2024",
        "exp-carrefour-li1": "Responsable de caisse",
        "exp-carrefour-li2": "Responsable du SAV / location de véhicules",
        "exp-carrefour-li3": "Hôtesse de caisse et d'accueil",
        "exp-carrefour-li4": "Relation clientèle, organisation, adaptation",
        "exp-babysit-title": "Garde d'enfants",
        "exp-babysit-date": "2021 - Aujourd'hui",
        "exp-babysit-desc": "Responsable de garde et gestion d'enfants à domicile.",
        
        // Education Section
        "edu-tag": "Parcours",
        "edu-title": "Mes Formations",
        "edu-uni-title": "Université Sorbonne Paris Nord, IUT de Villetaneuse",
        "edu-uni-date": "2022 - 2026",
        "edu-uni-degree": "BUT Informatique",
        "edu-lycee-title": "Lycée Fragonard, l'Isle Adam",
        "edu-lycee-date": "2021 - 2022",
        "edu-lycee-diploma": "Baccalauréat obtenu",
        "edu-lycee-li1": "Mention assez bien",
        "edu-lycee-li2": "Option Mathématiques et NSI",
        "edu-lycee-li3": "Spécialisation : Mathématiques expertes",
        
        // Skills Section
        "skills-tag": "Expertises",
        "skills-title": "Mes compétences",
        "skills-prog": "Langages de programmation",
        "skills-web": "Technologies Web",
        "skills-sys": "Systèmes & Réseaux",
        "skills-tools": "Outils bureautiques & gestion de projet",

        // Contact Section
        "contactTag": "Contact",
        "contactTitle": "Me contacter",
        "contactSubtitle": "N'hésitez pas à me contacter pour discuter de vos projets ou opportunités.",
        
        // Form
        "emailLabel": "Votre adresse email :",
        "subjectLabel": "Sujet :",
        "messageLabel": "Message :",
        "messagePlaceholder": "Votre message...",
        "sendButton": "Envoyer",
        
        // Footer
        "footer-student": "Étudiante en BUT Informatique",
        "footer-about": "À propos",
        "footer-skills": "Compétences",
        "footer-projects": "Projets",
        "footer-contact": "Contact",
        "footer-rights": "© 2025 Léona Dupont. Tous droits réservés."
    },
    en: {
        // Navigation
        "nav-home": "Home",
        "nav-about": "About",
        "nav-experience": "Professional Experience",
        "nav-education": "Education",
        "nav-skills": "Skills",
        "nav-projects": "Projects",
        "nav-contact": "Contact",
        
        // Hero Section
        "hero-title": "Léona Dupont's Portfolio",
        "hero-subtitle": "Computer Science Student",
        "hero-contact": "Contact Me",
        "hero-projects": "View My Projects",
        
        // About Section
        "about-tag": "About",
        "about-title": "About Me",
        "about-p1": "I am currently a second-year student pursuing a Bachelor's Degree in Computer Science, a professional and versatile program that allows me to acquire solid skills in various fields of computer science, such as web and mobile application development, database management, system and network administration, or cybersecurity.",
        "about-p2": "Through numerous group projects and real-world simulations, I learn to work in teams, solve complex problems, and adapt to various technical environments.",
        "about-p3": "Beyond my studies, I am a curious person passionate about the world around me. I love traveling, discovering new cultures, and constantly learning, whether through documentaries, readings, or films that I watch avidly, as they also allow me to see the world from a different perspective.",
        "stat-years": "Years of Study",
        "stat-projects": "Completed Projects",
        "stat-tech": "Mastered Technologies",
        
        // Experience Section
        "exp-tag": "Experience", 
        "exp-title": "Professional Experience",
        "exp-enedis-title": "Intern at Enedis",
        "exp-enedis-date": "January 2025 - April 2025",
        "exp-enedis-desc": "Assistance with router migration to a new PKI.",
        "exp-enedis-more": "For more information, please see",
        "exp-enedis-report": "my internship report",
        "exp-carrefour-title": "Carrefour",
        "exp-carrefour-date": "September 2023 - August 2024",
        "exp-carrefour-li1": "Cashier Manager",
        "exp-carrefour-li2": "After-sales Service / Vehicle Rental Manager",
        "exp-carrefour-li3": "Cashier and Reception Host",
        "exp-carrefour-li4": "Customer relations, organization, adaptation",
        "exp-babysit-title": "Childcare",
        "exp-babysit-date": "2021 - Present",
        "exp-babysit-desc": "Responsible for childcare and management at home.",
        
        // Education Section
        "edu-tag": "Education",
        "edu-title": "My Education",
        "edu-uni-title": "Sorbonne Paris Nord University, IUT Villetaneuse",
        "edu-uni-date": "2022 - 2026",
        "edu-uni-degree": "Bachelor's in Computer Science",
        "edu-lycee-title": "Fragonard High School, l'Isle Adam",
        "edu-lycee-date": "2021 - 2022",
        "edu-lycee-diploma": "Baccalaureate obtained",
        "edu-lycee-li1": "With honors",
        "edu-lycee-li2": "Mathematics and Computer Science option",
        "edu-lycee-li3": "Specialization: Advanced Mathematics",
        
        // Skills Section
        "skills-tag": "Expertise",
        "skills-title": "My Skills",
        "skills-prog": "Programming Languages",
        "skills-web": "Web Technologies",
        "skills-sys": "Systems & Networks",
        "skills-tools": "Office Tools & Project Management",

        // Contact Section
        "contactTag": "Contact",
        "contactTitle": "Get in touch",
        "contactSubtitle": "Don't hesitate to contact me to discuss your projects or opportunities.",
        
        // Form
        "emailLabel": "Your email address:",
        "subjectLabel": "Subject:",
        "messageLabel": "Message:",
        "messagePlaceholder": "Your message...",
        "sendButton": "Send",
        
        // Footer
        "footer-student": "Computer Science Student",
        "footer-about": "About",
        "footer-skills": "Skills",
        "footer-projects": "Projects",
        "footer-contact": "Contact",
        "footer-rights": "© 2025 Léona Dupont. All rights reserved."
    },
    es: {
        // Navigation
        "nav-home": "Inicio",
        "nav-about": "Presentación",
        "nav-experience": "Experiencia Profesional",
        "nav-education": "Formación",
        "nav-skills": "Habilidades",
        "nav-projects": "Proyectos",
        "nav-contact": "Contacto",
        
        // Hero Section
        "hero-title": "Portfolio de Léona Dupont",
        "hero-subtitle": "Estudiante de Informática",
        "hero-contact": "Contactarme",
        "hero-projects": "Ver mis proyectos",
        
        // About Section
        "about-tag": "Sobre mí",
        "about-title": "Sobre mí",
        "about-p1": "Actualmente soy estudiante de segundo año de Informática, una formación profesionalizante y polivalente que me permite adquirir habilidades sólidas en diversos campos de la informática, como el desarrollo de aplicaciones web y móviles, la gestión de bases de datos, la administración de sistemas y redes, o la ciberseguridad.",
        "about-p2": "A través de numerosos proyectos grupales y situaciones reales, aprendo a trabajar en equipo, resolver problemas complejos y adaptarme a diversos entornos técnicos.",
        "about-p3": "Más allá de mis estudios, soy una persona curiosa y apasionada por el mundo que me rodea. Me encanta viajar, descubrir nuevas culturas y educarme constantemente, ya sea a través de documentales, lecturas o películas que veo ávidamente, ya que también me permiten ver el mundo desde otra perspectiva.",
        "stat-years": "Años de estudio",
        "stat-projects": "Proyectos realizados",
        "stat-tech": "Tecnologías dominadas",
        
        // Experience Section
        "exp-tag": "Experiencia",
        "exp-title": "Experiencia Profesional",
        "exp-enedis-title": "Prácticas en Enedis",
        "exp-enedis-date": "Enero 2025 - Abril 2025",
        "exp-enedis-desc": "Ayuda en la migración de router a una nueva PKI.",
        "exp-enedis-more": "Para más información, consulte",
        "exp-enedis-report": "mi informe de prácticas",
        "exp-carrefour-title": "Carrefour",
        "exp-carrefour-date": "Septiembre 2023 - Agosto 2024",
        "exp-carrefour-li1": "Responsable de caja",
        "exp-carrefour-li2": "Responsable de servicio posventa / alquiler de vehículos",
        "exp-carrefour-li3": "Azafata de caja y recepción",
        "exp-carrefour-li4": "Relación con clientes, organización, adaptación",
        "exp-babysit-title": "Cuidado de niños",
        "exp-babysit-date": "2021 - Actualidad",
        "exp-babysit-desc": "Responsable del cuidado y gestión de niños a domicilio.",
        
        // Education Section
        "edu-tag": "Formación",
        "edu-title": "Mi Formación",
        "edu-uni-title": "Universidad Sorbonne Paris Nord, IUT de Villetaneuse",
        "edu-uni-date": "2022 - 2026",
        "edu-uni-degree": "Grado en Informática",
        "edu-lycee-title": "Liceo Fragonard, l'Isle Adam",
        "edu-lycee-date": "2021 - 2022",
        "edu-lycee-diploma": "Bachillerato obtenido",
        "edu-lycee-li1": "Mención bastante bien",
        "edu-lycee-li2": "Opción Matemáticas e Informática",
        "edu-lycee-li3": "Especialización: Matemáticas avanzadas",
        
        // Skills Section
        "skills-tag": "Experiencia",
        "skills-title": "Mis Habilidades",
        "skills-prog": "Lenguajes de programación",
        "skills-web": "Tecnologías Web",
        "skills-sys": "Sistemas y Redes",
        "skills-tools": "Herramientas ofimáticas y gestión de proyectos",

        // Contact Section
        "contactTag": "Contacto",
        "contactTitle": "Contáctame",
        "contactSubtitle": "No dudes en contactarme para discutir tus proyectos u oportunidades.",
        
        // Form
        "emailLabel": "Tu dirección de correo:",
        "subjectLabel": "Asunto:",
        "messageLabel": "Mensaje:",
        "messagePlaceholder": "Tu mensaje...",
        "sendButton": "Enviar",
        
        // Footer
        "footer-student": "Estudiante de Informática",
        "footer-about": "Sobre mí",
        "footer-skills": "Habilidades",
        "footer-projects": "Proyectos",
        "footer-contact": "Contacto",
        "footer-rights": "© 2025 Léona Dupont. Todos los derechos reservados."
    },
    ja: {
        // Navigation
        "nav-home": "ホーム",
        "nav-about": "自己紹介",
        "nav-experience": "職務経験",
        "nav-education": "学歴",
        "nav-skills": "スキル",
        "nav-projects": "プロジェクト",
        "nav-contact": "お問い合わせ",
        
        // Hero Section
        "hero-title": "レオナ・デュポンのポートフォリオ",
        "hero-subtitle": "情報工学専攻の学生",
        "hero-contact": "お問い合わせ",
        "hero-projects": "プロジェクトを見る",
        
        // About Section
        "about-tag": "自己紹介",
        "about-title": "私について",
        "about-p1": "現在、情報工学専攻の2年生として、ウェブおよびモバイルアプリケーション開発、データベース管理、システムおよびネットワーク管理、サイバーセキュリティなど、情報技術のさまざまな分野で確かなスキルを身につけることができる、実践的で多面的なプログラムを学んでいます。",
        "about-p2": "グループプロジェクトや実際のシミュレーションを通じて、チームでの作業、複雑な問題解決、さまざまな技術的環境への適応を学んでいます。",
        "about-p3": "学業以外では、周囲の世界に好奇心を持ち、情熱を注いでいます。旅行や新しい文化の発見が好きで、ドキュメンタリー、読書、映画などを通じて常に学び続けています。映画は世界を違った視点から見ることができるので、特に熱心に観ています。",
        "stat-years": "学習年数",
        "stat-projects": "完了したプロジェクト",
        "stat-tech": "習得した技術",
        
        // Experience Section
        "exp-tag": "経験",
        "exp-title": "職務経験",
        "exp-enedis-title": "Enedisでのインターン",
        "exp-enedis-date": "2025年1月 - 2025年4月",
        "exp-enedis-desc": "新しいPKIへのルーター移行の支援。",
        "exp-enedis-more": "詳細については、こちらをご覧ください",
        "exp-enedis-report": "インターンシップレポート",
        "exp-carrefour-title": "カルフール",
        "exp-carrefour-date": "2023年9月 - 2024年8月",
        "exp-carrefour-li1": "レジ責任者",
        "exp-carrefour-li2": "アフターサービス/車両レンタル責任者",
        "exp-carrefour-li3": "レジ係および受付係",
        "exp-carrefour-li4": "顧客対応、組織、適応",
        "exp-babysit-title": "子守り",
        "exp-babysit-date": "2021年 - 現在",
        "exp-babysit-desc": "自宅での子供の世話と管理を担当。",
        
        // Education Section
        "edu-tag": "学歴",
        "edu-title": "学歴",
        "edu-uni-title": "ソルボンヌ・パリ・ノール大学、ヴィルタヌーズIUT",
        "edu-uni-date": "2022年 - 2026年",
        "edu-uni-degree": "情報工学学士",
        "edu-lycee-title": "フラゴナール高校、リル・アダム",
        "edu-lycee-date": "2021年 - 2022年",
        "edu-lycee-diploma": "バカロレア取得",
        "edu-lycee-li1": "優良の成績で卒業",
        "edu-lycee-li2": "数学と情報科学のオプション",
        "edu-lycee-li3": "専門：高度な数学",
        
        // Skills Section
        "skills-tag": "専門知識",
        "skills-title": "スキル",
        "skills-prog": "プログラミング言語",
        "skills-web": "ウェブ技術",
        "skills-sys": "システム＆ネットワーク",
        "skills-tools": "オフィスツール＆プロジェクト管理",

        // Contact Section
        "contactTag": "お問い合わせ",
        "contactTitle": "ご連絡ください",
        "contactSubtitle": "プロジェクトや機会についてお気軽にご相談ください。",
        
        // Form
        "emailLabel": "メールアドレス：",
        "subjectLabel": "件名：",
        "messageLabel": "メッセージ：",
        "messagePlaceholder": "メッセージをご入力ください...",
        "sendButton": "送信",
        
        // Footer
        "footer-student": "情報工学専攻の学生",
        "footer-about": "自己紹介",
        "footer-skills": "スキル",
        "footer-projects": "プロジェクト",
        "footer-contact": "お問い合わせ",
        "footer-rights": "© 2025 レオナ・デュポン. 全著作権所有."
    }
};

// Fonction pour traduire la page
function translatePage(lang) {
    // Sauvegarder la langue sélectionnée dans localStorage
    localStorage.setItem('selectedLanguage', lang);
    
    // Traduire tous les éléments avec un attribut data-translate
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            // Vérifier le type d'élément pour définir correctement le contenu
            if (element.tagName === 'INPUT' && element.type === 'submit' || element.tagName === 'INPUT' && element.type === 'button') {
                element.value = translations[lang][key];
            } else {
                element.innerHTML = translations[lang][key];
            }
        }
    });
    
    // Mise à jour de la classe active sur le sélecteur de langue
    document.querySelectorAll('#language-selector option').forEach(option => {
        if (option.value === lang) {
            option.selected = true;
        }
    });
}

// Fonction pour ajouter les attributs data-translate aux éléments HTML
function prepareTranslation() {
    // Navigation
    document.querySelector('.nav-links li:nth-child(1) a').setAttribute('data-translate', 'nav-home');
    document.querySelector('.nav-links li:nth-child(2) a').setAttribute('data-translate', 'nav-about');
    document.querySelector('.nav-links li:nth-child(3) a').setAttribute('data-translate', 'nav-experience');
    document.querySelector('.nav-links li:nth-child(4) a').setAttribute('data-translate', 'nav-education');
    document.querySelector('.nav-links li:nth-child(5) a').setAttribute('data-translate', 'nav-skills');
    document.querySelector('.nav-links li:nth-child(6) a').setAttribute('data-translate', 'nav-projects');
    document.querySelector('.nav-links li:nth-child(7) a').setAttribute('data-translate', 'nav-contact');
    
    // Hero Section
    document.querySelector('#hero h1').setAttribute('data-translate', 'hero-title');
    document.querySelector('#hero .subtitle').setAttribute('data-translate', 'hero-subtitle');
    document.querySelector('#hero .primary-btn').setAttribute('data-translate', 'hero-contact');
    document.querySelector('#hero .secondary-btn').setAttribute('data-translate', 'hero-projects');
    
    // About Section
    document.querySelector('#presentation .section-tag').setAttribute('data-translate', 'about-tag');
    document.querySelector('#presentation h2').setAttribute('data-translate', 'about-title');
    
    const aboutParagraphs = document.querySelectorAll('#presentation .about-text p');
    if (aboutParagraphs.length >= 3) {
        aboutParagraphs[0].setAttribute('data-translate', 'about-p1');
        aboutParagraphs[1].setAttribute('data-translate', 'about-p2');
        aboutParagraphs[2].setAttribute('data-translate', 'about-p3');
    }
    
    const stats = document.querySelectorAll('.stat-text');
    if (stats.length >= 3) {
        stats[0].setAttribute('data-translate', 'stat-years');
        stats[1].setAttribute('data-translate', 'stat-projects');
        stats[2].setAttribute('data-translate', 'stat-tech');
    }
    
    // Experience Section
    document.querySelector('#experiences .section-tag').setAttribute('data-translate', 'exp-tag');
    document.querySelector('#experiences h2').setAttribute('data-translate', 'exp-title');
    
    const expCategories = document.querySelectorAll('#experiences .skills-category');
    if (expCategories.length >= 3) {
        // Enedis
        expCategories[0].querySelector('h3').setAttribute('data-translate', 'exp-enedis-title');
        const enedisP = expCategories[0].querySelectorAll('p');
        if (enedisP.length >= 2) {
            enedisP[0].innerHTML = '<strong data-translate="exp-enedis-date">Janvier 2025 - Avril 2025</strong>';
            enedisP[1].setAttribute('data-translate', 'exp-enedis-desc');
            // Pour le lien du rapport, on doit gérer différemment
            if (enedisP[2]) {
                const linkText = enedisP[2].innerHTML.split('<a')[0];
                const linkElement = enedisP[2].querySelector('a');
                const linkHref = linkElement ? linkElement.getAttribute('href') : '#';
                enedisP[2].innerHTML = '<span data-translate="exp-enedis-more">Pour plus d\'informations, veuillez consulter</span> <a href="' + linkHref + '" target="_blank" data-translate="exp-enedis-report">mon rapport de stage</a>.';
            }
        }
        
        // Carrefour
        expCategories[1].querySelector('h3').setAttribute('data-translate', 'exp-carrefour-title');
        const carrefourP = expCategories[1].querySelector('p');
        if (carrefourP) {
            carrefourP.innerHTML = '<strong data-translate="exp-carrefour-date">Septembre 2023 - Août 2024</strong>';
        }
        
        const carrefourLi = expCategories[1].querySelectorAll('li');
        if (carrefourLi.length >= 4) {
            carrefourLi[0].setAttribute('data-translate', 'exp-carrefour-li1');
            carrefourLi[1].setAttribute('data-translate', 'exp-carrefour-li2');
            carrefourLi[2].setAttribute('data-translate', 'exp-carrefour-li3');
            carrefourLi[3].setAttribute('data-translate', 'exp-carrefour-li4');
        }
        
        // Garde d'enfants
        expCategories[2].querySelector('h3').setAttribute('data-translate', 'exp-babysit-title');
        const babysitP = expCategories[2].querySelectorAll('p');
        if (babysitP.length >= 2) {
            babysitP[0].innerHTML = '<strong data-translate="exp-babysit-date">2021 - Aujourd\'hui</strong>';
            babysitP[1].setAttribute('data-translate', 'exp-babysit-desc');
        }
    }
    
    // Education Section
    document.querySelector('#formations .section-tag').setAttribute('data-translate', 'edu-tag');
    document.querySelector('#formations h2').setAttribute('data-translate', 'edu-title');
    
    const eduCategories = document.querySelectorAll('#formations .skills-category');
    if (eduCategories.length >= 2) {
        // Université
        eduCategories[0].querySelector('h3').setAttribute('data-translate', 'edu-uni-title');
        const uniP = eduCategories[0].querySelector('p');
        if (uniP) {
            uniP.innerHTML = '<strong data-translate="edu-uni-date">2022 - 2026</strong> — <span data-translate="edu-uni-degree">BUT Informatique</span>';
        }
        
        // Lycée
        eduCategories[1].querySelector('h3').setAttribute('data-translate', 'edu-lycee-title');
        const lyceeP = eduCategories[1].querySelector('p');
        if (lyceeP) {
            lyceeP.innerHTML = '<strong data-translate="edu-lycee-date">2021 - 2022</strong> — <span data-translate="edu-lycee-diploma">Baccalauréat obtenu</span>';
        }
        
        const lyceeLi = eduCategories[1].querySelectorAll('li');
        if (lyceeLi.length >= 3) {
            lyceeLi[0].setAttribute('data-translate', 'edu-lycee-li1');
            lyceeLi[1].setAttribute('data-translate', 'edu-lycee-li2');
            lyceeLi[2].setAttribute('data-translate', 'edu-lycee-li3');
        }
    }
    
    // Skills Section
    document.querySelector('#competences .section-tag').setAttribute('data-translate', 'skills-tag');
    document.querySelector('#competences h2').setAttribute('data-translate', 'skills-title');
    
    const skillsCategories = document.querySelectorAll('#competences .skills-category h3');
    if (skillsCategories.length >= 4) {
        skillsCategories[0].setAttribute('data-translate', 'skills-prog');
        skillsCategories[1].setAttribute('data-translate', 'skills-web');
        skillsCategories[2].setAttribute('data-translate', 'skills-sys');
        skillsCategories[3].setAttribute('data-translate', 'skills-tools');
    }
    
    // Footer
    document.querySelector('.footer-logo p').setAttribute('data-translate', 'footer-student');
    
    const footerLinks = document.querySelectorAll('.footer-links a');
    if (footerLinks.length >= 4) {
        footerLinks[0].setAttribute('data-translate', 'footer-about');
        footerLinks[1].setAttribute('data-translate', 'footer-skills');
        footerLinks[2].setAttribute('data-translate', 'footer-projects');
        footerLinks[3].setAttribute('data-translate', 'footer-contact');
    }
    
    document.querySelector('.footer-bottom p').setAttribute('data-translate', 'footer-rights');
}

// Détecter la langue préférée du navigateur
function detectBrowserLanguage() {
    const browserLang = navigator.language.split('-')[0];
    return ['fr', 'en', 'es', 'ja'].includes(browserLang) ? browserLang : 'fr';
}

// Initialiser la traduction lorsque le DOM est chargé
document.addEventListener('DOMContentLoaded', function() {
    // Préparer les éléments pour la traduction
    prepareTranslation();
    
    // Récupérer la langue sauvegardée ou détecter celle du navigateur
    const savedLang = localStorage.getItem('selectedLanguage') || detectBrowserLanguage();
    
    // Initialiser le sélecteur de langue
    const languageSelector = document.getElementById('language-selector');
    languageSelector.value = savedLang;
    
    // Appliquer la traduction initiale
    translatePage(savedLang);
    
    // Ajouter l'événement de changement de langue
    languageSelector.addEventListener('change', function() {
        translatePage(this.value);
    });
});

/* AJOUT : configuration Particles.js */
document.addEventListener('DOMContentLoaded', function () {
    particlesJS("particles-js", {
      particles: {
        number: { value: 80, density: { enable: true, value_area: 800 } },
        color: { value: "#00ffff" },
        shape: {
          type: "circle",
          stroke: { width: 0, color: "#000000" },
          polygon: { nb_sides: 5 }
        },
        opacity: { value: 0.5, random: false },
        size: { value: 3, random: true },
        line_linked: {
          enable: true,
          distance: 150,
          color: "#00ffff",
          opacity: 0.4,
          width: 1
        },
        move: {
          enable: true,
          speed: 3,
          direction: "none",
          random: false,
          straight: false,
          bounce: true
        }
      },
      interactivity: {
        detect_on: "canvas",
        events: {
          onhover: { enable: true, mode: "grab" },
          onclick: { enable: true, mode: "push" },
          resize: true
        },
        modes: {
          grab: { distance: 140, line_linked: { opacity: 1 } },
          push: { particles_nb: 4 }
        }
      },
      retina_detect: true
    });
  });
  