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
        "nameLabel": "Votre nom :",
        "emailLabel": "Votre adresse email :",
        "subjectLabel": "Sujet :",
        "messageLabel": "Message :",
        "messagePlaceholder": "Votre message...",
        "sendButton": "Envoyer",
        
        // Footer
        // Projects
        "projects-tag": "Projets",
        "projects-title": "Projets réalisés",
        
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
        "nameLabel": "Your name:",
        "emailLabel": "Your email address:",
        "subjectLabel": "Subject:",
        "messageLabel": "Message:",
        "messagePlaceholder": "Your message...",
        "sendButton": "Send",
        
        // Footer
        // Projects
        "projects-tag": "Projects",
        "projects-title": "Completed Projects",
        
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
        "nameLabel": "Tu nombre:",
        "emailLabel": "Tu dirección de correo:",
        "subjectLabel": "Asunto:",
        "messageLabel": "Mensaje:",
        "messagePlaceholder": "Tu mensaje...",
        "sendButton": "Enviar",
        
        // Footer
        // Projects
        "projects-tag": "Proyectos",
        "projects-title": "Proyectos Realizados",
        
        // Footer
        "footer-student": "Estudiante de Informática",
        "footer-about": "Sobre mí",
        "footer-skills": "Habilidades",
        "footer-projects": "Proyectos",
        "footer-contact": "Contacto",
        "footer-rights": "© 2025 Léona Dupont. Todos los derechos reservados."
    },
    ko: {
        // Navigation
        "nav-home": "홈",
        "nav-about": "자기소개",
        "nav-experience": "직업 경험",
        "nav-education": "학력",
        "nav-skills": "기술",
        "nav-projects": "프로젝트",
        "nav-contact": "연락처",
        
        // Hero Section
        "hero-title": "레오나 뒤퐁의 포트폴리오",
        "hero-subtitle": "정보 공학 전공 학생",
        "hero-contact": "연락하기",
        "hero-projects": "내 프로젝트 보기",
        
        // About Section
        "about-tag": "소개",
        "about-title": "저에 대해",
        "about-p1": "현재 정보 공학 전공 3학년 학생으로서 웹 및 모바일 애플리케이션 개발, 데이터베이스 관리, 시스템 및 네트워크 관리, 사이버 보안 등 정보 기술의 다양한 분야에서 탄탄한 기술을 습득할 수 있는 실무 중심의 다각적인 프로그램을 공부하고 있습니다.",
        "about-p2": "다양한 팀 프로젝트와 실제 상황 시뮬레이션을 통해 팀 작업, 복잡한 문제 해결, 다양한 기술 환경에 적응하는 방법을 배우고 있습니다.",
        "about-p3": "학업 외에도 저는 주변 세계에 호기심을 가지고 열정을 가지고 있습니다. 여행하고, 새로운 문화를 발견하고, 다큐멘터리, 책 읽기, 영화 감상 등을 통해 지속적으로 배우는 것을 좋아합니다. 영화는 세상을 다른 관점에서 볼 수 있게 해주므로 특히 열심히 봅니다.",
        "stat-years": "공부 연도",
        "stat-projects": "완료한 프로젝트",
        "stat-tech": "습득한 기술",
        
        // Experience Section
        "exp-tag": "경험",
        "exp-title": "직업 경험",
        "exp-enedis-title": "Enedis 인턴십",
        "exp-enedis-date": "2025년 1월 - 2025년 4월",
        "exp-enedis-desc": "새로운 PKI로의 라우터 마이그레이션 지원.",
        "exp-enedis-more": "자세한 내용은 다음을 참조하세요",
        "exp-enedis-report": "인턴십 보고서",
        "exp-carrefour-title": "Carrefour",
        "exp-carrefour-date": "2023년 9월 - 2024년 8월",
        "exp-carrefour-li1": "계산대 담당자",
        "exp-carrefour-li2": "애프터서비스/차량 임차 담당자",
        "exp-carrefour-li3": "계산대 직원 및 접수 직원",
        "exp-carrefour-li4": "고객 관계, 조직, 적응",
        "exp-babysit-title": "아이돌봄",
        "exp-babysit-date": "2021년 - 현재",
        "exp-babysit-desc": "집에서 아이돌봄 및 관리 담당.",
        
        // Education Section
        "edu-tag": "학력",
        "edu-title": "학력",
        "edu-uni-title": "소르본 파리 노르 대학교, 빌타누즈 IUT",
        "edu-uni-date": "2022년 - 2026년",
        "edu-uni-degree": "정보 공학 학사",
        "edu-lycee-title": "프라고나르 고등학교, l'Isle Adam",
        "edu-lycee-date": "2021년 - 2022년",
        "edu-lycee-diploma": "바칼로레아 취득",
        "edu-lycee-li1": "우수한 성적으로 졸업",
        "edu-lycee-li2": "수학 및 정보 과학 선택",
        "edu-lycee-li3": "전문 분야: 고급 수학",
        
        // Skills Section
        "skills-tag": "전문 지식",
        "skills-title": "기술",
        "skills-prog": "프로그래밍 언어",
        "skills-web": "웹 기술",
        "skills-sys": "시스템 및 네트워크",
        "skills-tools": "사무실 도구 및 프로젝트 관리",

        // Contact Section
        "contactTag": "연락처",
        "contactTitle": "연락하세요",
        "contactSubtitle": "프로젝트나 기회에 대해 편하게 연락주세요.",
        
        // Form
        "nameLabel": "이름:",
        "emailLabel": "이메일 주소:",
        "subjectLabel": "제목:",
        "messageLabel": "메시지:",
        "messagePlaceholder": "메시지를 입력하세요...",
        "sendButton": "전송",
        
        // Footer
        // Projects
        "projects-tag": "프로젝트",
        "projects-title": "완료된 프로젝트",
        
        // Footer
        "footer-student": "정보 공학 전공 학생",
        "footer-about": "소개",
        "footer-skills": "기술",
        "footer-projects": "프로젝트",
        "footer-contact": "연락처",
        "footer-rights": "© 2025 레오나 뒤퐁. 모든 권리 보유."
    }
};

// Fonction principale pour traduire la page
function changeLanguage(lang) {
    // Sauvegarder la langue sélectionnée dans localStorage
    localStorage.setItem('selectedLanguage', lang);
    
    // Récupérer les traductions pour cette langue
    const t = translations[lang] || translations['fr'];
    
    // Navigation
    const navLinks = document.querySelectorAll('.nav-links a');
    const navTexts = ['nav-home', 'nav-about', 'nav-experience', 'nav-education', 'nav-skills', 'nav-projects'];
    navLinks.forEach((link, index) => {
        if (navTexts[index] && t[navTexts[index]]) {
            link.textContent = t[navTexts[index]];
        }
    });
    
    // Hero Section
    const heroH1 = document.querySelector('#hero h1');
    if (heroH1) heroH1.textContent = t['hero-title'] || heroH1.textContent;
    
    const heroSubtitle = document.querySelector('#hero .subtitle');
    if (heroSubtitle) heroSubtitle.textContent = t['hero-subtitle'] || heroSubtitle.textContent;
    
    const heroCTAButtons = document.querySelectorAll('#hero .cta-buttons a');
    if (heroCTAButtons.length > 0) {
        heroCTAButtons[0].textContent = t['hero-projects'] || 'Voir mes projets';
        if (heroCTAButtons.length > 1) {
            // Le deuxième bouton est le CV, on ne le traduit pas
        }
    }
    
    // About Section
    const aboutTag = document.querySelector('#presentation .section-tag');
    if (aboutTag) aboutTag.textContent = t['about-tag'] || aboutTag.textContent;
    
    const aboutH2 = document.querySelector('#presentation h2');
    if (aboutH2) aboutH2.textContent = t['about-title'] || aboutH2.textContent;
    
    // About paragraphs
    const aboutParas = document.querySelectorAll('#presentation .about-text > p');
    if (aboutParas.length > 0) aboutParas[0].textContent = t['about-p1'] || aboutParas[0].textContent;
    if (aboutParas.length > 1) aboutParas[1].textContent = t['about-p2'] || aboutParas[1].textContent;
    if (aboutParas.length > 2) aboutParas[2].textContent = t['about-p3'] || aboutParas[2].textContent;
    
    // About stats
    const stats = document.querySelectorAll('.stat-text');
    if (stats.length > 0) stats[0].textContent = t['stat-years'] || stats[0].textContent;
    if (stats.length > 1) stats[1].textContent = t['stat-projects'] || stats[1].textContent;
    if (stats.length > 2) stats[2].textContent = t['stat-tech'] || stats[2].textContent;
    
    // Experience Section
    const expTag = document.querySelector('#experiences .section-tag');
    if (expTag) expTag.textContent = t['exp-tag'] || expTag.textContent;
    
    const expH2 = document.querySelector('#experiences h2');
    if (expH2) expH2.textContent = t['exp-title'] || expH2.textContent;
    
    // Experience items - detailed translation
    const expCategories = document.querySelectorAll('#experiences .skills-category');
    if (expCategories.length > 0) {
        // Enedis
        expCategories[0].querySelector('h3').textContent = t['exp-enedis-title'];
        const enedisParagraphs = expCategories[0].querySelectorAll('p');
        if (enedisParagraphs.length > 0) {
            enedisParagraphs[0].innerHTML = '<strong>' + t['exp-enedis-date'] + '</strong>';
        }
        if (enedisParagraphs.length > 1) {
            enedisParagraphs[1].textContent = t['exp-enedis-desc'];
        }
        if (enedisParagraphs.length > 2) {
            enedisParagraphs[2].innerHTML = t['exp-enedis-more'] + ' <a href="Rapport de stage.pdf" target="_blank">' + t['exp-enedis-report'] + '</a>.';
        }
    }
    
    if (expCategories.length > 1) {
        // Carrefour
        expCategories[1].querySelector('h3').textContent = t['exp-carrefour-title'];
        const carrefourParagraphs = expCategories[1].querySelectorAll('p');
        if (carrefourParagraphs.length > 0) {
            carrefourParagraphs[0].innerHTML = '<strong>' + t['exp-carrefour-date'] + '</strong>';
        }
        
        const carrefourLi = expCategories[1].querySelectorAll('li');
        if (carrefourLi.length > 0) carrefourLi[0].textContent = t['exp-carrefour-li1'];
        if (carrefourLi.length > 1) carrefourLi[1].textContent = t['exp-carrefour-li2'];
        if (carrefourLi.length > 2) carrefourLi[2].textContent = t['exp-carrefour-li3'];
        if (carrefourLi.length > 3) carrefourLi[3].textContent = t['exp-carrefour-li4'];
    }
    
    if (expCategories.length > 2) {
        // Garde d'enfants
        expCategories[2].querySelector('h3').textContent = t['exp-babysit-title'];
        const babysitParagraphs = expCategories[2].querySelectorAll('p');
        if (babysitParagraphs.length > 0) {
            babysitParagraphs[0].innerHTML = '<strong>' + t['exp-babysit-date'] + '</strong>';
        }
        if (babysitParagraphs.length > 1) {
            babysitParagraphs[1].textContent = t['exp-babysit-desc'];
        }
    }
    
    // Education Section
    const eduTag = document.querySelector('#formations .section-tag');
    if (eduTag) eduTag.textContent = t['edu-tag'] || eduTag.textContent;
    
    const eduH2 = document.querySelector('#formations h2');
    if (eduH2) eduH2.textContent = t['edu-title'] || eduH2.textContent;
    
    // Education items
    const eduCategories = document.querySelectorAll('#formations .skills-category');
    if (eduCategories.length > 0) {
        const uniH3 = eduCategories[0].querySelector('h3');
        if (uniH3) uniH3.textContent = t['edu-uni-title'];
        
        const uniP = eduCategories[0].querySelector('p');
        if (uniP) {
            uniP.innerHTML = '<strong>' + t['edu-uni-date'] + '</strong> — ' + t['edu-uni-degree'];
        }
    }
    
    if (eduCategories.length > 1) {
        const lyceeH3 = eduCategories[1].querySelector('h3');
        if (lyceeH3) lyceeH3.textContent = t['edu-lycee-title'];
        
        const lyceeP = eduCategories[1].querySelector('p');
        if (lyceeP) {
            lyceeP.innerHTML = '<strong>' + t['edu-lycee-date'] + '</strong> — ' + t['edu-lycee-diploma'];
        }
        
        const lyceeLi = eduCategories[1].querySelectorAll('li');
        if (lyceeLi.length > 0) lyceeLi[0].textContent = t['edu-lycee-li1'];
        if (lyceeLi.length > 1) lyceeLi[1].textContent = t['edu-lycee-li2'];
        if (lyceeLi.length > 2) lyceeLi[2].textContent = t['edu-lycee-li3'];
    }
    
    // Skills Section
    const skillsTag = document.querySelector('#competences .section-tag');
    if (skillsTag) skillsTag.textContent = t['skills-tag'] || skillsTag.textContent;
    
    const skillsH2 = document.querySelector('#competences h2');
    if (skillsH2) skillsH2.textContent = t['skills-title'] || skillsH2.textContent;
    
    const skillsH3 = document.querySelectorAll('#competences .skills-category h3');
    if (skillsH3.length > 0) skillsH3[0].textContent = t['skills-prog'];
    if (skillsH3.length > 1) skillsH3[1].textContent = t['skills-web'];
    if (skillsH3.length > 2) skillsH3[2].textContent = t['skills-sys'];
    if (skillsH3.length > 3) skillsH3[3].textContent = t['skills-tools'];
    
    // Projects Section
    const projetsTag = document.querySelector('#projets .section-tag');
    if (projetsTag) projetsTag.textContent = t['projects-tag'] || projetsTag.textContent;
    
    const projetsH2 = document.querySelector('#projets h2');
    if (projetsH2) {
        projetsH2.textContent = t['projects-title'] || projetsH2.textContent;
    }
    
    // Footer Section
    const footerLogo = document.querySelector('.footer-logo p');
    if (footerLogo) footerLogo.textContent = t['footer-student'] || footerLogo.textContent;
    
    const footerLinks = document.querySelectorAll('.footer-links a');
    if (footerLinks.length > 0) footerLinks[0].textContent = t['footer-about'] || footerLinks[0].textContent;
    if (footerLinks.length > 1) footerLinks[1].textContent = t['footer-skills'] || footerLinks[1].textContent;
    if (footerLinks.length > 2) footerLinks[2].textContent = t['footer-projects'] || footerLinks[2].textContent;
    
    const footerBottom = document.querySelector('.footer-bottom p');
    if (footerBottom) footerBottom.textContent = t['footer-rights'] || footerBottom.textContent;
    
    // Mise à jour de la langue du documentement
    document.documentElement.lang = lang;
}

// Alias pour compatibilité avec le nom ancien
function translatePage(lang) {
    changeLanguage(lang);
}

// Détecter la langue préférée du navigateur
function detectBrowserLanguage() {
    const browserLang = navigator.language.split('-')[0];
    return ['fr', 'en', 'es', 'ko'].includes(browserLang) ? browserLang : 'fr';
}

// Initialiser la traduction lorsque le DOM est chargé
document.addEventListener('DOMContentLoaded', function() {
    // Récupérer la langue sauvegardée ou détecter celle du navigateur
    const savedLang = localStorage.getItem('selectedLanguage') || detectBrowserLanguage();
    
    // Initialiser le sélecteur de langue
    const languageSelector = document.getElementById('language-selector');
    if (languageSelector) {
        languageSelector.value = savedLang;
        
        // Appliquer la traduction initiale
        changeLanguage(savedLang);
        
        // Ajouter l'événement de changement de langue
        languageSelector.addEventListener('change', function() {
            changeLanguage(this.value);
        });
    }
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
  