document.addEventListener('DOMContentLoaded', function() {
    // Activer le mode sombre si préféré par l'utilisateur
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    if (prefersDarkScheme.matches) {
        document.body.classList.add('dark-theme');
        document.getElementById('theme-toggle').checked = true;
    }

    // Barre de progression du défilement et ombre du header
    const scrollProgress = document.querySelector('.scroll-progress');
    const headerEl = document.querySelector('header');

    function updateScrollEffects() {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;

        if (scrollProgress) {
            scrollProgress.style.width = progress + '%';
        }

        if (headerEl) {
            headerEl.classList.toggle('scrolled', scrollTop > 50);
        }
    }

    window.addEventListener('scroll', updateScrollEffects);
    updateScrollEffects();

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

    if (menuToggle && navLinks) {
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
    }

    // Navigation active au défilement
    const sections = document.querySelectorAll('section[id]');

    function highlightNavigation() {
        if (!navLinks) return;
        const scrollPosition = window.scrollY + 100;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            const navLink = document.querySelector(`.nav-links a[href="#${sectionId}"]`);
            if (!navLink) return;

            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLink.classList.add('active');
            } else {
                navLink.classList.remove('active');
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
        "hero-greeting": "Bonjour, je suis",
        "hero-title": "Léona Dupont",
        "hero-subtitle": "Étudiante en BUT Informatique",
        "hero-contact": "Me contacter",
        "hero-projects": "Voir mes projets",
        
        // About Section
        "about-tag": "À propos",
        "about-title": "À propos de moi",
        "about-p1": "Je suis actuellement étudiante en troisième année d'un BUT Informatique, une formation professionnalisante et polyvalente qui me permet d'acquérir des compétences solides dans divers domaines de l'informatique, tels que le développement d'applications web et mobiles, la gestion de bases de données, l'administration de systèmes et réseaux, ou encore la cybersécurité.",
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
        "footer-rights": "© 2026 Léona Dupont. Tous droits réservés.",

        // Nouveaux contenus (mécanisme générique data-i18n)
        "nav-travel": "Voyages",
        "about-p4": "Je suis actuellement à la recherche d'un stage de 4 à 6 mois, à partir du 9 mars 2026, pour mettre en pratique l'ensemble de ces compétences sur des projets concrets.",
        "exp-hackathon-title": "Hackathon « Nuit de l'informatique »",
        "exp-hackathon-date": "Décembre 2025",
        "exp-hackathon-desc": "Participation à un hackathon de 24h en équipe : conception, développement et présentation d'un prototype fonctionnel devant un jury, dans un temps limité.",
        "skills-bdd": "Bases de données",
        "skills-mobile": "Développement mobile & Outils",
        "skills-langues": "Langues",
        "skill-api": "Intégration d'API",
        "skill-agile": "Méthodologie Agile",
        "lang-fr": "Français — langue maternelle",
        "lang-en": "Anglais — niveau B2",
        "lang-es": "Espagnol — niveau A2",
        "lang-ko": "Coréen — niveau A2",
        "lang-ja": "Japonais — niveau A1",
        "proj-cta": "Voir le projet",
        "tag-group-7": "Groupe de 7",
        "tag-group-5": "Groupe de 5",
        "tag-individual": "Travail individuel",
        "back-to-projects": "Retour aux projets",
        "travel-tag": "Carnet de voyage",
        "travel-title": "Pays visités",
        "travel-intro": "Passionnée de voyages, j'ai eu la chance de découvrir les pays ci-dessous. Survolez une carte pour découvrir (bientôt) mes photos prises sur place !",
        "travel-soon": "Photos à venir",
        "travel-home": "Domicile",
        "map-legend-visited": "Pays visités",
        "map-legend-unvisited": "Non visités",
        "map-extra-label": "Également visités (trop petits pour apparaître sur la carte) :",
        "travel-modal-soon": "Le récit de ce voyage et les photos associées arrivent bientôt !",
        "nav-future": "Avenir",
        "future-title": "Projets d'avenir",
        "future-text": "<p>À partir d'août 2026, je vais partir un an en Corée du Sud dans le cadre d'un Programme Vacances Travail (PVT).</p><p>L'objectif de cette année sera avant tout de m'immerger dans le pays : améliorer mon niveau de coréen, m'habituer au mode de vie sur place et découvrir la culture du quotidien, au-delà de mes précédents voyages.</p><p>À l'issue de ce PVT, je souhaite intégrer un master en cybersécurité à Séoul. J'ai adoré ma précédente expérience en Corée du Sud, et je considère que c'est l'un des meilleurs pays pour étudier et travailler dans le domaine de la cybersécurité.</p>",
        "future-stat-destination-value": "🇰🇷 Corée du Sud",
        "future-stat-destination-label": "Destination",
        "future-stat-departure": "Départ en PVT",
        "future-stat-duration": "Durée du PVT",
        "proj-section-context": "Contexte",
        "proj-section-objectifs": "Objectifs",
        "proj-section-realisation": "Réalisation",
        "proj-section-role": "Mon rôle",
        "proj-section-resultats": "Résultats",

        // Projet : Calculatrice Java
        "proj-calc-title": "Calculatrice Java",
        "proj-calc-tagline": "Une calculatrice en Java capable d'évaluer et d'afficher des expressions arithmétiques complexes, conçue selon le patron de conception Composite.",
        "proj-calc-context": "<p>Ce projet a été réalisé durant le second semestre de la première année de BUT Informatique, dans le cadre d'une SAÉ en binôme. L'objectif était de découvrir la programmation orientée objet en Java à travers un cas concret : la modélisation et l'évaluation d'expressions mathématiques.</p>",
        "proj-calc-objectifs": "<p>Construire une calculatrice capable de :</p><ul><li>Représenter des expressions mathématiques composées de nombres et d'opérations (addition, soustraction, multiplication, division)</li><li>Afficher ces expressions sous forme textuelle, avec parenthésage automatique</li><li>Calculer récursivement leur résultat</li><li>Gérer proprement les cas d'erreur, comme la division par zéro</li></ul>",
        "proj-calc-realisation": "<p>Nous avons mis en place une architecture orientée objet basée sur le patron de conception <strong>Composite</strong> :</p><ul><li>Une interface <code>Expression</code>, commune à tous les éléments du calcul</li><li>La classe <code>Nombre</code>, représentant les valeurs terminales (les feuilles de l'arbre d'expression)</li><li>Une classe abstraite <code>Operation</code>, dont héritent <code>Addition</code>, <code>Soustraction</code>, <code>Multiplication</code> et <code>Division</code>, chacune combinant deux sous-expressions</li></ul><p>Chaque expression sait à la fois calculer sa valeur (de manière récursive) et générer sa propre représentation textuelle, par exemple <code>((17 - 2) / (2 + 3)) = 3</code>. La division par zéro est détectée et gérée via une exception dédiée plutôt que de faire planter le programme.</p>",
        "proj-calc-role": "<p>En binôme, j'ai participé à la conception de la hiérarchie de classes <code>Expression</code> / <code>Operation</code> / <code>Nombre</code>, ainsi qu'à l'implémentation de plusieurs opérations et à la gestion des erreurs (division par zéro). Ce projet a été ma première véritable mise en pratique de la programmation orientée objet : héritage, polymorphisme et conception récursive.</p>",
        "proj-calc-resultats": "<p>Le résultat est une calculatrice fonctionnelle capable d'évaluer des expressions imbriquées de complexité arbitraire et d'en afficher une représentation lisible. Ce projet m'a permis de bien comprendre l'intérêt du patron Composite pour modéliser des structures récursives.</p>",

        // Projet : Implémentation d'un besoin client
        "proj-client-title": "Implémentation d'un besoin client",
        "proj-client-tagline": "Détection de communautés dans un réseau d'amitié, modélisé en Python à l'aide de dictionnaires.",
        "proj-client-context": "<p>Cette SAÉ de première année consistait à répondre à un besoin client autour de l'analyse de réseaux sociaux : à partir d'une liste de relations d'amitié, déterminer les groupes de personnes qui se connaissent toutes mutuellement, appelés « communautés ».</p>",
        "proj-client-objectifs": "<p>Le projet, réalisé en binôme, visait à :</p><ul><li>Modéliser un réseau d'amis sous forme de dictionnaire Python (chaque personne associée à la liste de ses amis)</li><li>Construire ce réseau automatiquement à partir d'une liste de paires d'amis</li><li>Identifier les communautés, c'est-à-dire les groupes où chaque membre est ami avec tous les autres membres du groupe</li><li>Valider le fonctionnement du programme à l'aide de tests unitaires</li></ul>",
        "proj-client-realisation": "<p>Nous avons développé une fonction <code>create_network</code> qui construit le réseau d'amitié sous forme de dictionnaire à partir d'une liste de paires (par exemple <code>{\"Alice\": [\"Bob\", \"Dominique\"], ...}</code>), puis un algorithme de détection de communautés qui parcourt ce réseau pour regrouper les personnes mutuellement connectées entre elles.</p><p>L'ensemble du code a été validé par une suite de tests unitaires (<code>test_community_detection.py</code>), couvrant différents cas de figure : réseaux vides, communautés isolées, ou personnes appartenant à plusieurs groupes.</p>",
        "proj-client-role": "<p>En binôme, j'ai travaillé sur la conception des structures de données (dictionnaires représentant le réseau), sur l'algorithme de détection des communautés et sur l'écriture des tests unitaires permettant de vérifier sa robustesse sur différents jeux de données.</p>",
        "proj-client-resultats": "<p>Le programme final identifie correctement les communautés d'un réseau d'amis fourni en entrée, et l'ensemble des tests unitaires passe avec succès. Ce projet a renforcé ma maîtrise des structures de données Python et des bonnes pratiques de test.</p>",

        // Projet : Jeu du pingouin
        "proj-pingouin-title": "Jeu du pingouin",
        "proj-pingouin-tagline": "Un petit jeu interactif en HTML, CSS et JavaScript : un pingouin qui se déplace pour attraper des poissons.",
        "proj-pingouin-context": "<p>Ce projet est un mini-jeu front-end développé en HTML, CSS et JavaScript, pensé comme un exercice de manipulation du DOM, d'animations et d'événements en temps réel dans le navigateur.</p>",
        "proj-pingouin-objectifs": "<p>L'objectif était de créer un jeu simple mais fonctionnel :</p><ul><li>Un pingouin positionné dans une scène (un bassin), pouvant se déplacer verticalement</li><li>Des poissons apparaissant aléatoirement et traversant l'écran</li><li>Une interaction au clavier fluide et bornée à la zone de jeu</li></ul>",
        "proj-pingouin-realisation": "<p>Le pingouin (représenté par un SVG) se déplace de 30 pixels vers le haut ou vers le bas à chaque pression sur les touches flèches, avec une zone de déplacement limitée pour qu'il reste dans le bassin. En parallèle, un poisson est généré toutes les 500 millisecondes à une hauteur aléatoire, traverse l'écran grâce à une animation CSS, puis est automatiquement retiré du DOM après 2 secondes pour éviter toute accumulation d'éléments.</p>",
        "proj-pingouin-role": "<p>J'ai conçu l'ensemble du jeu : la mise en page de la scène en HTML/CSS, l'intégration des éléments graphiques en SVG (pingouin, poissons, eau), et la logique JavaScript de déplacement, de génération aléatoire et de nettoyage des éléments.</p>",
        "proj-pingouin-resultats": "<p>Le résultat est un mini-jeu fluide et amusant, qui m'a permis de manipuler en profondeur le DOM, les événements clavier, les animations CSS et la gestion du cycle de vie d'éléments générés dynamiquement.</p>",

        // Projet : SérendIA
        "proj-serendia-title": "SérendIA",
        "proj-serendia-desc": "Application mobile Flutter de recommandation de voyage, développée en groupe de 7, avec moteur de recommandation vectoriel et mini-jeu de swipe pour affiner les suggestions.",
        "proj-serendia-tagline": "Une application mobile Flutter qui recommande des destinations de voyage personnalisées grâce à un moteur de recommandation basé sur un profil vectoriel.",
        "proj-serendia-context": "<p>SérendIA est une application développée dans le cadre d'une SAÉ de troisième année de BUT, en équipe de 7 personnes. Le projet visait à concevoir une application de recommandation de destinations de voyage, capable de s'adapter aux préférences de chaque utilisateur au fil de ses interactions.</p>",
        "proj-serendia-objectifs": "<p>Le projet s'est déroulé en plusieurs phases :</p><ul><li><strong>Phase 1 — Fondations &amp; données</strong> : mise en place de l'architecture de l'application et préparation des jeux de données de destinations</li><li><strong>Phase 2 — Moteur de recommandation V1</strong> : conception d'un premier algorithme de recommandation basé sur les préférences utilisateur</li><li><strong>Phase 3 — Moteur amélioré &amp; expérience utilisateur</strong> : affinement du moteur de recommandation et amélioration de l'interface et des interactions</li></ul>",
        "proj-serendia-realisation": "<p>Chaque utilisateur est représenté par un <code>UserProfileVector</code>, un vecteur de préférences sur plusieurs axes (Culture, Aventure, Détente, Budget). Les destinations sont comparées à ce profil grâce à une approche de <strong>« Soft Filtering »</strong> : plutôt que d'exclure strictement les destinations qui ne correspondent pas parfaitement au profil, elles sont simplement pénalisées dans le classement, ce qui permet de garder une diversité de suggestions.</p><p>Un <code>UserInteractionService</code> met à jour ce profil en continu à partir des retours de l'utilisateur, notamment via un mini-jeu de swipe permettant de noter cinq destinations proposées. Les données sont stockées localement dans une base <strong>SQLite</strong> (via le package <code>sqflite</code>), et des scripts Python (<code>check_db.py</code>, <code>jsonl_to_csv.py</code>) ont été utilisés pour préparer et vérifier les jeux de données de destinations.</p>",
        "proj-serendia-role": "<p>Au sein de cette équipe de 7, j'ai contribué au développement de l'application Flutter/Dart, notamment sur la logique de profil utilisateur et la préparation des données via les scripts Python, en collaboration étroite avec le reste de l'équipe pour intégrer ces éléments au moteur de recommandation.</p>",
        "proj-serendia-resultats": "<p>Le résultat est une application mobile fonctionnelle, capable de proposer des destinations personnalisées et de faire évoluer ses recommandations au fil des interactions de l'utilisateur. Ce projet m'a permis de travailler sur un développement mobile complet en équipe nombreuse, de la base de données locale jusqu'à l'interface utilisateur.</p>",

        // Projet : Vélib'
        "proj-velib-title": "Vélib'",
        "proj-velib-desc": "Refonte complète de l'application Vélib', en groupe de 5, avec l'API officielle Vélib' Métropole : nouveau design et nouvelles fonctionnalités.",
        "proj-velib-tagline": "Une refonte complète de l'application Vélib', avec un nouveau design et de nouvelles fonctionnalités basées sur l'API officielle Vélib' Métropole.",
        "proj-velib-context": "<p>Dans le cadre d'un projet en équipe de 5, nous nous sommes inspirés de l'application officielle Vélib' pour en recréer entièrement notre propre version, en s'appuyant sur les API ouvertes de Vélib' Métropole pour récupérer les données en temps réel des stations.</p>",
        "proj-velib-objectifs": "<p>L'objectif n'était pas de simplement reproduire l'application existante, mais de la repenser :</p><ul><li>Revoir entièrement le design (couleurs, mise en page, expérience utilisateur)</li><li>Ajouter de nouvelles fonctionnalités absentes de l'application originale</li><li>Exploiter les données en temps réel de l'API Vélib' Métropole (disponibilité des vélos mécaniques et électriques, places libres, etc.)</li></ul>",
        "proj-velib-realisation": "<p>Nous avons conçu une nouvelle interface avec une identité visuelle propre, en travaillant sur la palette de couleurs, la lisibilité des informations et la navigation entre les écrans. Côté fonctionnalités, l'application récupère et affiche en temps réel l'état des stations (vélos disponibles, places libres, type de vélo) via l'API Vélib' Métropole, et propose de nouvelles fonctionnalités pensées par l'équipe pour améliorer l'expérience par rapport à l'application existante.</p>",
        "proj-velib-role": "<p>Au sein de cette équipe de 5, j'ai participé à la conception du nouveau design de l'application (charte graphique, écrans) ainsi qu'à l'intégration des données de l'API Vélib' Métropole dans l'interface.</p>",
        "proj-velib-resultats": "<p>Le résultat est une application repensée, à la fois plus agréable à utiliser et enrichie de nouvelles fonctionnalités, tout en s'appuyant sur des données réelles et à jour. Ce projet a été l'occasion de travailler en équipe sur l'ensemble du cycle d'un projet applicatif : conception, design, intégration d'API et développement.</p>",

        // Projet : Diagrammes de Voronoï
        "proj-voronoi-title": "Diagrammes de Voronoï",
        "proj-voronoi-desc": "Implémentation individuelle de l'algorithme de Fortune en Python pour générer et exporter des diagrammes de Voronoï, dans le cadre d'une SAÉ de groupe.",
        "proj-watchout-title": "Watch Out",
        "proj-watchout-desc": "Petit jeu vidéo d'horreur en 2D réalisé pour l'école : on explore une forêt sombre à la recherche de chiffres cachés afin de composer un code et s'échapper avant la fin du temps imparti.",
        "proj-watchout-tagline": "Petit jeu vidéo d'horreur en 2D développé en Python avec Pygame, dans le cadre d'un projet multimédia scolaire.",
        "proj-watchout-context": "<p>Ce projet a été réalisé dans le cadre d'un projet multimédia scolaire. L'objectif était de concevoir un petit jeu vidéo complet, de l'histoire jusqu'à la mécanique de jeu, en passant par les graphismes, les sons et l'interface.</p>",
        "proj-watchout-objectifs": "<p>L'objectif était de créer un jeu d'horreur en 2D capable de :</p><ul><li>Faire explorer plusieurs scènes reliées entre elles (forêt, chemin, maison hantée)</li><li>Cacher des indices (chiffres) dans le décor que le joueur doit retrouver</li><li>Mettre en place un système de code à entrer avant la fin d'un minuteur</li><li>Créer une ambiance angoissante grâce aux graphismes, à la musique et à des apparitions surprises</li></ul>",
        "proj-watchout-realisation": "<p>J'ai développé le jeu avec Python et la bibliothèque Pygame. Le joueur explore plusieurs scènes liées par des zones cliquables, doit repérer 3 chiffres cachés dans le décor, puis les saisir sur un écran de code avant la fin d'un minuteur de 20 secondes. Pour renforcer l'ambiance, j'ai ajouté une musique d'ambiance, des fantômes semi-transparents qui se déplacent vers le joueur, ainsi que des apparitions aléatoires à l'écran.</p><p>J'ai également créé des scripts annexes (<code>localisation_pixel.py</code>, <code>modifier_image.py</code>) pour repérer précisément la position des indices dans les images et préparer les assets graphiques.</p>",
        "proj-watchout-role": "<p>Ce projet a été réalisé de manière individuelle : conception du scénario, développement du gameplay en Python/Pygame, gestion des assets (images, polices, musique) et mise en place de l'ambiance sonore et visuelle.</p>",
        "proj-watchout-resultats": "<p>Le résultat est un petit jeu jouable de bout en bout : une introduction, trois scènes explorables, une mécanique de recherche d'indices, un écran de code avec minuteur, ainsi qu'un écran de victoire et un écran de game over. Ce projet m'a permis de découvrir le développement de jeux vidéo avec Pygame et de travailler sur la gestion d'assets multimédias (images, polices, musique).</p>",
        "proj-voronoi-tagline": "Génération de diagrammes de Voronoï en Python à partir de l'algorithme de Fortune, avec export SVG et PNG.",
        "proj-voronoi-context": "<p>Ce projet s'inscrit dans une SAÉ de groupe portant sur les diagrammes de Voronoï, une structure de géométrie algorithmique utilisée pour partitionner un plan en régions à partir d'un ensemble de points. J'ai pris en charge, de façon individuelle, la deuxième phase du projet : l'implémentation de l'algorithme de génération.</p>",
        "proj-voronoi-objectifs": "<p>L'objectif de cette phase était d'implémenter un générateur de diagrammes de Voronoï performant, capable de :</p><ul><li>Calculer un diagramme de Voronoï à partir d'un ensemble de points grâce à l'algorithme de Fortune (algorithme de balayage)</li><li>Représenter les cellules, sommets et arêtes du diagramme à l'aide de structures de données dédiées</li><li>Exporter le résultat sous forme d'image (SVG et PNG)</li></ul>",
        "proj-voronoi-realisation": "<p>J'ai implémenté une classe <code>FortuneAlgorithm</code>, héritant d'une classe générique <code>VoronoiGenerator</code>, qui met en œuvre l'algorithme de balayage de Fortune : une ligne de balayage horizontale parcourt le plan et construit progressivement le diagramme à partir des points fournis. Les éléments géométriques (points, arêtes) sont représentés par des classes dédiées <code>Point</code> et <code>Edge</code>, avec des fonctions utilitaires de géométrie regroupées dans <code>geometry_utils</code>.</p><p>Pour visualiser les résultats, j'ai développé des exporteurs dédiés permettant de générer le diagramme final au format <strong>SVG</strong> et <strong>PNG</strong>.</p>",
        "proj-voronoi-role": "<p>Cette phase du projet a été réalisée de manière individuelle au sein d'une SAÉ de groupe. J'ai conçu et implémenté l'algorithme de Fortune ainsi que les modules de géométrie et d'export associés, en m'appuyant sur les bases posées lors de la première phase du projet.</p>",
        "proj-voronoi-resultats": "<p>Le résultat est un générateur capable de produire des diagrammes de Voronoï corrects à partir de n'importe quel ensemble de points, exportables directement en SVG ou PNG. Ce projet m'a permis d'approfondir mes connaissances en géométrie algorithmique et en structures de données complexes.</p>"
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
        "hero-greeting": "Hi, I'm",
        "hero-title": "Léona Dupont",
        "hero-subtitle": "Computer Science Student",
        "hero-contact": "Contact Me",
        "hero-projects": "View My Projects",
        
        // About Section
        "about-tag": "About",
        "about-title": "About Me",
        "about-p1": "I am currently a third-year student pursuing a Bachelor's Degree in Computer Science, a professional and versatile program that allows me to acquire solid skills in various fields of computer science, such as web and mobile application development, database management, system and network administration, or cybersecurity.",
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
        "footer-rights": "© 2026 Léona Dupont. All rights reserved.",

        // New content (generic data-i18n mechanism)
        "nav-travel": "Travels",
        "about-p4": "I am currently looking for a 4 to 6 month internship, starting on March 9, 2026, to put all these skills into practice on real-world projects.",
        "exp-hackathon-title": "Hackathon \"Nuit de l'informatique\"",
        "exp-hackathon-date": "December 2025",
        "exp-hackathon-desc": "Took part in a 24-hour team hackathon: designing, developing and presenting a functional prototype to a jury within a limited time.",
        "skills-bdd": "Databases",
        "skills-mobile": "Mobile Development & Tools",
        "skills-langues": "Languages",
        "skill-api": "API Integration",
        "skill-agile": "Agile Methodology",
        "lang-fr": "French — native language",
        "lang-en": "English — B2 level",
        "lang-es": "Spanish — A2 level",
        "lang-ko": "Korean — A2 level",
        "lang-ja": "Japanese — A1 level",
        "proj-cta": "View project",
        "tag-group-7": "Group of 7",
        "tag-group-5": "Group of 5",
        "tag-individual": "Individual work",
        "back-to-projects": "Back to projects",
        "travel-tag": "Travel journal",
        "travel-title": "Countries visited",
        "travel-intro": "Passionate about travel, I've had the chance to discover the countries below. Hover over a card to discover (soon) my photos taken there!",
        "travel-soon": "Photos coming soon",
        "travel-home": "Home",
        "map-legend-visited": "Visited countries",
        "map-legend-unvisited": "Not visited",
        "map-extra-label": "Also visited (too small to appear on the map):",
        "travel-modal-soon": "The story of this trip and the related photos are coming soon!",
        "nav-future": "Future",
        "future-title": "Future Plans",
        "future-text": "<p>Starting in August 2026, I will spend a year in South Korea as part of a Working Holiday Program (PVT).</p><p>The main goal of this year will be to immerse myself in the country: improve my Korean language skills, get used to daily life there, and discover the local culture beyond my previous trips.</p><p>After this Working Holiday year, I hope to join a cybersecurity master's program in Seoul. I loved my previous experience in South Korea, and I consider it one of the best countries to study and work in cybersecurity.</p>",
        "future-stat-destination-value": "🇰🇷 South Korea",
        "future-stat-destination-label": "Destination",
        "future-stat-departure": "Working Holiday departure",
        "future-stat-duration": "Working Holiday duration",
        "proj-section-context": "Context",
        "proj-section-objectifs": "Objectives",
        "proj-section-realisation": "Implementation",
        "proj-section-role": "My role",
        "proj-section-resultats": "Results",

        // Project: Java Calculator
        "proj-calc-title": "Java Calculator",
        "proj-calc-tagline": "A Java calculator capable of evaluating and displaying complex arithmetic expressions, designed using the Composite design pattern.",
        "proj-calc-context": "<p>This project was carried out during the second semester of the first year of BUT Informatique, as part of a school project done in pairs. The goal was to discover object-oriented programming in Java through a concrete case: modeling and evaluating mathematical expressions.</p>",
        "proj-calc-objectifs": "<p>Build a calculator capable of:</p><ul><li>Representing mathematical expressions made up of numbers and operations (addition, subtraction, multiplication, division)</li><li>Displaying these expressions as text, with automatic parenthesization</li><li>Recursively computing their result</li><li>Properly handling error cases, such as division by zero</li></ul>",
        "proj-calc-realisation": "<p>We set up an object-oriented architecture based on the <strong>Composite</strong> design pattern:</p><ul><li>An <code>Expression</code> interface, common to all elements of the calculation</li><li>The <code>Nombre</code> class, representing terminal values (the leaves of the expression tree)</li><li>An abstract <code>Operation</code> class, inherited by <code>Addition</code>, <code>Soustraction</code>, <code>Multiplication</code> and <code>Division</code>, each combining two sub-expressions</li></ul><p>Each expression can both compute its value (recursively) and generate its own textual representation, for example <code>((17 - 2) / (2 + 3)) = 3</code>. Division by zero is detected and handled via a dedicated exception rather than crashing the program.</p>",
        "proj-calc-role": "<p>Working in pairs, I took part in designing the <code>Expression</code> / <code>Operation</code> / <code>Nombre</code> class hierarchy, as well as implementing several operations and handling errors (division by zero). This project was my first real hands-on practice with object-oriented programming: inheritance, polymorphism and recursive design.</p>",
        "proj-calc-resultats": "<p>The result is a functional calculator capable of evaluating nested expressions of arbitrary complexity and displaying a readable representation of them. This project helped me fully understand the value of the Composite pattern for modeling recursive structures.</p>",

        // Project: Implementing a Client Requirement
        "proj-client-title": "Implementing a Client Requirement",
        "proj-client-tagline": "Community detection in a friendship network, modeled in Python using dictionaries.",
        "proj-client-context": "<p>This first-year academic project involved addressing a client need related to social network analysis: given a list of friendship relationships, determine the groups of people who all mutually know each other, called \"communities\".</p>",
        "proj-client-objectifs": "<p>The project, carried out in pairs, aimed to:</p><ul><li>Model a network of friends as a Python dictionary (each person mapped to their list of friends)</li><li>Build this network automatically from a list of friend pairs</li><li>Identify communities, i.e. groups where every member is friends with all other members of the group</li><li>Validate the program's behavior using unit tests</li></ul>",
        "proj-client-realisation": "<p>We developed a <code>create_network</code> function that builds the friendship network as a dictionary from a list of pairs (for example <code>{\"Alice\": [\"Bob\", \"Dominique\"], ...}</code>), then a community detection algorithm that traverses this network to group together people who are mutually connected.</p><p>The entire codebase was validated by a suite of unit tests (<code>test_community_detection.py</code>), covering various scenarios: empty networks, isolated communities, or people belonging to multiple groups.</p>",
        "proj-client-role": "<p>Working in pairs, I worked on the design of the data structures (dictionaries representing the network), on the community detection algorithm, and on writing the unit tests used to verify its robustness across different datasets.</p>",
        "proj-client-resultats": "<p>The final program correctly identifies the communities within a given friend network, and all unit tests pass successfully. This project strengthened my command of Python data structures and good testing practices.</p>",

        // Project: Penguin Game
        "proj-pingouin-title": "Penguin Game",
        "proj-pingouin-tagline": "A small interactive game in HTML, CSS and JavaScript: a penguin that moves around to catch fish.",
        "proj-pingouin-context": "<p>This project is a front-end mini-game developed in HTML, CSS and JavaScript, designed as an exercise in DOM manipulation, animations and real-time events in the browser.</p>",
        "proj-pingouin-objectifs": "<p>The goal was to create a simple but functional game:</p><ul><li>A penguin positioned in a scene (a pool), able to move vertically</li><li>Fish appearing at random and crossing the screen</li><li>Smooth keyboard interaction, bounded to the game area</li></ul>",
        "proj-pingouin-realisation": "<p>The penguin (represented by an SVG) moves 30 pixels up or down with each press of the arrow keys, within a limited movement area so it stays within the pool. At the same time, a fish is generated every 500 milliseconds at a random height, crosses the screen using a CSS animation, and is automatically removed from the DOM after 2 seconds to prevent any buildup of elements.</p>",
        "proj-pingouin-role": "<p>I designed the entire game: the layout of the scene in HTML/CSS, the integration of the SVG graphic elements (penguin, fish, water), and the JavaScript logic for movement, random generation and cleanup of elements.</p>",
        "proj-pingouin-resultats": "<p>The result is a smooth and fun mini-game, which allowed me to work in depth with the DOM, keyboard events, CSS animations and the lifecycle management of dynamically generated elements.</p>",

        // Project: SérendIA
        "proj-serendia-title": "SérendIA",
        "proj-serendia-desc": "Flutter mobile travel recommendation app, developed in a group of 7, with a vector-based recommendation engine and a swipe mini-game to refine suggestions.",
        "proj-serendia-tagline": "A Flutter mobile app that recommends personalized travel destinations using a recommendation engine based on a vector profile.",
        "proj-serendia-context": "<p>SérendIA is an application developed as part of a third-year BUT academic project, in a team of 7. The project aimed to design a travel destination recommendation app capable of adapting to each user's preferences over the course of their interactions.</p>",
        "proj-serendia-objectifs": "<p>The project unfolded in several phases:</p><ul><li><strong>Phase 1 — Foundations &amp; data</strong>: setting up the application's architecture and preparing the destination datasets</li><li><strong>Phase 2 — Recommendation engine V1</strong>: designing a first recommendation algorithm based on user preferences</li><li><strong>Phase 3 — Improved engine &amp; user experience</strong>: refining the recommendation engine and improving the interface and interactions</li></ul>",
        "proj-serendia-realisation": "<p>Each user is represented by a <code>UserProfileVector</code>, a preference vector across several axes (Culture, Adventure, Relaxation, Budget). Destinations are compared to this profile using a <strong>\"Soft Filtering\"</strong> approach: rather than strictly excluding destinations that don't perfectly match the profile, they are simply penalized in the ranking, which keeps a diversity of suggestions.</p><p>A <code>UserInteractionService</code> continuously updates this profile based on user feedback, in particular through a swipe mini-game allowing the user to rate five suggested destinations. The data is stored locally in an <strong>SQLite</strong> database (via the <code>sqflite</code> package), and Python scripts (<code>check_db.py</code>, <code>jsonl_to_csv.py</code>) were used to prepare and verify the destination datasets.</p>",
        "proj-serendia-role": "<p>Within this team of 7, I contributed to the development of the Flutter/Dart application, particularly on the user profile logic and data preparation via the Python scripts, working closely with the rest of the team to integrate these elements into the recommendation engine.</p>",
        "proj-serendia-resultats": "<p>The result is a functional mobile application capable of suggesting personalized destinations and evolving its recommendations based on the user's interactions. This project allowed me to work on a complete mobile development project within a large team, from the local database to the user interface.</p>",

        // Project: Vélib'
        "proj-velib-title": "Vélib'",
        "proj-velib-desc": "Complete redesign of the Vélib' app, in a group of 5, using the official Vélib' Métropole API: new design and new features.",
        "proj-velib-tagline": "A complete redesign of the Vélib' app, with a new design and new features based on the official Vélib' Métropole API.",
        "proj-velib-context": "<p>As part of a project in a team of 5, we drew inspiration from the official Vélib' app to fully recreate our own version, relying on the open APIs of Vélib' Métropole to retrieve real-time station data.</p>",
        "proj-velib-objectifs": "<p>The goal was not simply to reproduce the existing app, but to rethink it:</p><ul><li>Completely overhaul the design (colors, layout, user experience)</li><li>Add new features missing from the original app</li><li>Make use of real-time data from the Vélib' Métropole API (availability of mechanical and electric bikes, free docks, etc.)</li></ul>",
        "proj-velib-realisation": "<p>We designed a new interface with its own visual identity, working on the color palette, the readability of information and navigation between screens. On the feature side, the app retrieves and displays the real-time status of stations (available bikes, free docks, bike type) via the Vélib' Métropole API, and offers new features designed by the team to improve the experience compared to the existing app.</p>",
        "proj-velib-role": "<p>Within this team of 5, I took part in designing the app's new look (visual identity, screens) as well as integrating Vélib' Métropole API data into the interface.</p>",
        "proj-velib-resultats": "<p>The result is a redesigned app, both more pleasant to use and enriched with new features, while relying on real and up-to-date data. This project was an opportunity to work as a team across the entire lifecycle of an application project: design, UI, API integration and development.</p>",

        // Project: Voronoi Diagrams
        "proj-voronoi-title": "Voronoi Diagrams",
        "proj-voronoi-desc": "Individual implementation of Fortune's algorithm in Python to generate and export Voronoi diagrams, as part of a group academic project.",
        "proj-watchout-title": "Watch Out",
        "proj-watchout-desc": "Small 2D horror video game made for school: explore a dark forest to find hidden digits, compose a code and escape before time runs out.",
        "proj-watchout-tagline": "Small 2D horror video game built in Python with Pygame, made for a school multimedia project.",
        "proj-watchout-context": "<p>This project was carried out as part of a school multimedia project. The goal was to design a complete small video game, from the storyline to the gameplay mechanics, including graphics, sound and interface.</p>",
        "proj-watchout-objectifs": "<p>The goal was to create a 2D horror game able to:</p><ul><li>Let the player explore several connected scenes (forest, path, haunted house)</li><li>Hide clues (digits) in the scenery that the player has to find</li><li>Implement a code system to enter before a timer runs out</li><li>Build a tense atmosphere through graphics, music and jump-scare apparitions</li></ul>",
        "proj-watchout-realisation": "<p>I developed the game in Python using the Pygame library. The player explores several scenes linked by clickable areas, has to spot 3 hidden digits in the scenery, then enter them on a code screen before a 20-second timer runs out. To reinforce the atmosphere, I added background music, semi-transparent ghosts moving toward the player, and random apparitions on screen.</p><p>I also wrote helper scripts (<code>localisation_pixel.py</code>, <code>modifier_image.py</code>) to precisely locate the clues in the images and prepare the graphic assets.</p>",
        "proj-watchout-role": "<p>This project was carried out individually: designing the storyline, developing the gameplay in Python/Pygame, managing the assets (images, fonts, music) and setting up the sound and visual atmosphere.</p>",
        "proj-watchout-resultats": "<p>The result is a small game playable from start to finish: an introduction, three explorable scenes, a clue-hunting mechanic, a code screen with a timer, as well as a victory screen and a game-over screen. This project allowed me to discover video game development with Pygame and to work on managing multimedia assets (images, fonts, music).</p>",
        "proj-voronoi-tagline": "Generating Voronoi diagrams in Python using Fortune's algorithm, with SVG and PNG export.",
        "proj-voronoi-context": "<p>This project is part of a group academic project on Voronoi diagrams, an algorithmic geometry structure used to partition a plane into regions from a set of points. I individually took charge of the second phase of the project: implementing the generation algorithm.</p>",
        "proj-voronoi-objectifs": "<p>The goal of this phase was to implement an efficient Voronoi diagram generator, capable of:</p><ul><li>Computing a Voronoi diagram from a set of points using Fortune's algorithm (a sweep line algorithm)</li><li>Representing the cells, vertices and edges of the diagram using dedicated data structures</li><li>Exporting the result as an image (SVG and PNG)</li></ul>",
        "proj-voronoi-realisation": "<p>I implemented a <code>FortuneAlgorithm</code> class, inheriting from a generic <code>VoronoiGenerator</code> class, which implements Fortune's sweep line algorithm: a horizontal sweep line moves across the plane and progressively builds the diagram from the provided points. Geometric elements (points, edges) are represented by dedicated <code>Point</code> and <code>Edge</code> classes, with utility geometry functions grouped in <code>geometry_utils</code>.</p><p>To visualize the results, I developed dedicated exporters to generate the final diagram in <strong>SVG</strong> and <strong>PNG</strong> format.</p>",
        "proj-voronoi-role": "<p>This phase of the project was carried out individually within a group academic project. I designed and implemented Fortune's algorithm as well as the associated geometry and export modules, building on the foundations laid during the first phase of the project.</p>",
        "proj-voronoi-resultats": "<p>The result is a generator capable of producing correct Voronoi diagrams from any set of points, exportable directly to SVG or PNG. This project allowed me to deepen my knowledge of algorithmic geometry and complex data structures.</p>"
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
        "hero-greeting": "Hola, soy",
        "hero-title": "Léona Dupont",
        "hero-subtitle": "Estudiante de Informática",
        "hero-contact": "Contactarme",
        "hero-projects": "Ver mis proyectos",
        
        // About Section
        "about-tag": "Sobre mí",
        "about-title": "Sobre mí",
        "about-p1": "Actualmente soy estudiante de tercer año de Informática, una formación profesionalizante y polivalente que me permite adquirir habilidades sólidas en diversos campos de la informática, como el desarrollo de aplicaciones web y móviles, la gestión de bases de datos, la administración de sistemas y redes, o la ciberseguridad.",
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
        "footer-rights": "© 2026 Léona Dupont. Todos los derechos reservados.",

        // Nuevos contenidos (mecanismo genérico data-i18n)
        "nav-travel": "Viajes",
        "about-p4": "Actualmente estoy buscando unas prácticas de 4 a 6 meses, a partir del 9 de marzo de 2026, para poner en práctica todas estas competencias en proyectos concretos.",
        "exp-hackathon-title": "Hackathon « Nuit de l'informatique »",
        "exp-hackathon-date": "Diciembre de 2025",
        "exp-hackathon-desc": "Participación en un hackathon de 24 horas en equipo: diseño, desarrollo y presentación de un prototipo funcional ante un jurado, en un tiempo limitado.",
        "skills-bdd": "Bases de datos",
        "skills-mobile": "Desarrollo móvil y herramientas",
        "skills-langues": "Idiomas",
        "skill-api": "Integración de API",
        "skill-agile": "Metodología Ágil",
        "lang-fr": "Francés — lengua materna",
        "lang-en": "Inglés — nivel B2",
        "lang-es": "Español — nivel A2",
        "lang-ko": "Coreano — nivel A2",
        "lang-ja": "Japonés — nivel A1",
        "proj-cta": "Ver el proyecto",
        "tag-group-7": "Grupo de 7",
        "tag-group-5": "Grupo de 5",
        "tag-individual": "Trabajo individual",
        "back-to-projects": "Volver a los proyectos",
        "travel-tag": "Diario de viaje",
        "travel-title": "Países visitados",
        "travel-intro": "Apasionada por los viajes, he tenido la oportunidad de descubrir los países que aparecen a continuación. Pasa el ratón por encima de una tarjeta para descubrir (próximamente) mis fotos tomadas allí.",
        "travel-soon": "Fotos próximamente",
        "travel-home": "Domicilio",
        "map-legend-visited": "Países visitados",
        "map-legend-unvisited": "No visitados",
        "map-extra-label": "También visitados (demasiado pequeños para aparecer en el mapa):",
        "travel-modal-soon": "¡La historia de este viaje y las fotos relacionadas llegarán pronto!",
        "nav-future": "Futuro",
        "future-title": "Proyectos futuros",
        "future-text": "<p>A partir de agosto de 2026, pasaré un año en Corea del Sur en el marco de un Programa Vacaciones y Trabajo (PVT).</p><p>El objetivo principal de este año será sumergirme en el país: mejorar mi nivel de coreano, acostumbrarme a la vida diaria allí y descubrir la cultura local más allá de mis viajes anteriores.</p><p>Al finalizar este PVT, espero ingresar a un máster en ciberseguridad en Seúl. Adoré mi experiencia anterior en Corea del Sur, y considero que es uno de los mejores países para estudiar y trabajar en ciberseguridad.</p>",
        "future-stat-destination-value": "🇰🇷 Corea del Sur",
        "future-stat-destination-label": "Destino",
        "future-stat-departure": "Salida en PVT",
        "future-stat-duration": "Duración del PVT",
        "proj-section-context": "Contexto",
        "proj-section-objectifs": "Objetivos",
        "proj-section-realisation": "Realización",
        "proj-section-role": "Mi papel",
        "proj-section-resultats": "Resultados",

        // Proyecto: Calculadora Java
        "proj-calc-title": "Calculadora Java",
        "proj-calc-tagline": "Una calculadora en Java capaz de evaluar y mostrar expresiones aritméticas complejas, diseñada según el patrón de diseño Composite.",
        "proj-calc-context": "<p>Este proyecto se realizó durante el segundo semestre del primer año del BUT Informática, en el marco de un proyecto académico en pareja. El objetivo era descubrir la programación orientada a objetos en Java a través de un caso concreto: la modelización y evaluación de expresiones matemáticas.</p>",
        "proj-calc-objectifs": "<p>Construir una calculadora capaz de:</p><ul><li>Representar expresiones matemáticas compuestas de números y operaciones (suma, resta, multiplicación, división)</li><li>Mostrar estas expresiones en forma textual, con paréntesis automáticos</li><li>Calcular recursivamente su resultado</li><li>Gestionar correctamente los casos de error, como la división por cero</li></ul>",
        "proj-calc-realisation": "<p>Implementamos una arquitectura orientada a objetos basada en el patrón de diseño <strong>Composite</strong>:</p><ul><li>Una interfaz <code>Expression</code>, común a todos los elementos del cálculo</li><li>La clase <code>Nombre</code>, que representa los valores terminales (las hojas del árbol de expresión)</li><li>Una clase abstracta <code>Operation</code>, de la que heredan <code>Addition</code>, <code>Soustraction</code>, <code>Multiplication</code> y <code>Division</code>, cada una combinando dos subexpresiones</li></ul><p>Cada expresión sabe tanto calcular su valor (de forma recursiva) como generar su propia representación textual, por ejemplo <code>((17 - 2) / (2 + 3)) = 3</code>. La división por cero se detecta y se gestiona mediante una excepción dedicada en lugar de hacer fallar el programa.</p>",
        "proj-calc-role": "<p>En pareja, participé en el diseño de la jerarquía de clases <code>Expression</code> / <code>Operation</code> / <code>Nombre</code>, así como en la implementación de varias operaciones y en la gestión de errores (división por cero). Este proyecto fue mi primera puesta en práctica real de la programación orientada a objetos: herencia, polimorfismo y diseño recursivo.</p>",
        "proj-calc-resultats": "<p>El resultado es una calculadora funcional capaz de evaluar expresiones anidadas de complejidad arbitraria y mostrar una representación legible de ellas. Este proyecto me permitió comprender bien la utilidad del patrón Composite para modelizar estructuras recursivas.</p>",

        // Proyecto: Implementación de una necesidad de cliente
        "proj-client-title": "Implementación de una necesidad de cliente",
        "proj-client-tagline": "Detección de comunidades en una red de amistad, modelizada en Python mediante diccionarios.",
        "proj-client-context": "<p>Este proyecto académico de primer año consistía en responder a una necesidad de cliente relacionada con el análisis de redes sociales: a partir de una lista de relaciones de amistad, determinar los grupos de personas que se conocen todas mutuamente, llamados «comunidades».</p>",
        "proj-client-objectifs": "<p>El proyecto, realizado en pareja, tenía como objetivo:</p><ul><li>Modelizar una red de amigos en forma de diccionario Python (cada persona asociada a la lista de sus amigos)</li><li>Construir esta red automáticamente a partir de una lista de pares de amigos</li><li>Identificar las comunidades, es decir, los grupos en los que cada miembro es amigo de todos los demás miembros del grupo</li><li>Validar el funcionamiento del programa mediante pruebas unitarias</li></ul>",
        "proj-client-realisation": "<p>Desarrollamos una función <code>create_network</code> que construye la red de amistad en forma de diccionario a partir de una lista de pares (por ejemplo <code>{\"Alice\": [\"Bob\", \"Dominique\"], ...}</code>), y luego un algoritmo de detección de comunidades que recorre esta red para agrupar a las personas mutuamente conectadas entre sí.</p><p>Todo el código fue validado mediante una suite de pruebas unitarias (<code>test_community_detection.py</code>), que cubre diferentes casos: redes vacías, comunidades aisladas o personas que pertenecen a varios grupos.</p>",
        "proj-client-role": "<p>En pareja, trabajé en el diseño de las estructuras de datos (diccionarios que representan la red), en el algoritmo de detección de comunidades y en la escritura de las pruebas unitarias que permiten verificar su robustez en distintos conjuntos de datos.</p>",
        "proj-client-resultats": "<p>El programa final identifica correctamente las comunidades de una red de amigos proporcionada como entrada, y todas las pruebas unitarias se ejecutan con éxito. Este proyecto reforzó mi dominio de las estructuras de datos de Python y de las buenas prácticas de testing.</p>",

        // Proyecto: Juego del pingüino
        "proj-pingouin-title": "Juego del pingüino",
        "proj-pingouin-tagline": "Un pequeño juego interactivo en HTML, CSS y JavaScript: un pingüino que se desplaza para atrapar peces.",
        "proj-pingouin-context": "<p>Este proyecto es un mini-juego front-end desarrollado en HTML, CSS y JavaScript, pensado como un ejercicio de manipulación del DOM, animaciones y eventos en tiempo real en el navegador.</p>",
        "proj-pingouin-objectifs": "<p>El objetivo era crear un juego sencillo pero funcional:</p><ul><li>Un pingüino situado en una escena (un estanque), que puede desplazarse verticalmente</li><li>Peces que aparecen aleatoriamente y atraviesan la pantalla</li><li>Una interacción por teclado fluida y limitada a la zona de juego</li></ul>",
        "proj-pingouin-realisation": "<p>El pingüino (representado mediante un SVG) se desplaza 30 píxeles hacia arriba o hacia abajo con cada pulsación de las teclas de flecha, con una zona de desplazamiento limitada para que permanezca dentro del estanque. En paralelo, se genera un pez cada 500 milisegundos a una altura aleatoria, que atraviesa la pantalla gracias a una animación CSS, y luego se elimina automáticamente del DOM tras 2 segundos para evitar cualquier acumulación de elementos.</p>",
        "proj-pingouin-role": "<p>Diseñé todo el juego: la maquetación de la escena en HTML/CSS, la integración de los elementos gráficos en SVG (pingüino, peces, agua) y la lógica JavaScript de desplazamiento, generación aleatoria y limpieza de elementos.</p>",
        "proj-pingouin-resultats": "<p>El resultado es un mini-juego fluido y divertido, que me permitió trabajar en profundidad el DOM, los eventos de teclado, las animaciones CSS y la gestión del ciclo de vida de elementos generados dinámicamente.</p>",

        // Proyecto: SérendIA
        "proj-serendia-title": "SérendIA",
        "proj-serendia-desc": "Aplicación móvil Flutter de recomendación de viajes, desarrollada en grupo de 7, con un motor de recomendación vectorial y un mini-juego de swipe para refinar las sugerencias.",
        "proj-serendia-tagline": "Una aplicación móvil Flutter que recomienda destinos de viaje personalizados gracias a un motor de recomendación basado en un perfil vectorial.",
        "proj-serendia-context": "<p>SérendIA es una aplicación desarrollada en el marco de un proyecto académico de tercer año del BUT, en un equipo de 7 personas. El proyecto consistía en diseñar una aplicación de recomendación de destinos de viaje, capaz de adaptarse a las preferencias de cada usuario a lo largo de sus interacciones.</p>",
        "proj-serendia-objectifs": "<p>El proyecto se desarrolló en varias fases:</p><ul><li><strong>Fase 1 — Fundamentos y datos</strong>: puesta en marcha de la arquitectura de la aplicación y preparación de los conjuntos de datos de destinos</li><li><strong>Fase 2 — Motor de recomendación V1</strong>: diseño de un primer algoritmo de recomendación basado en las preferencias del usuario</li><li><strong>Fase 3 — Motor mejorado y experiencia de usuario</strong>: refinamiento del motor de recomendación y mejora de la interfaz y de las interacciones</li></ul>",
        "proj-serendia-realisation": "<p>Cada usuario está representado por un <code>UserProfileVector</code>, un vector de preferencias sobre varios ejes (Cultura, Aventura, Relax, Presupuesto). Los destinos se comparan con este perfil mediante un enfoque de <strong>«Soft Filtering»</strong>: en lugar de excluir estrictamente los destinos que no corresponden perfectamente al perfil, simplemente se penalizan en la clasificación, lo que permite mantener una diversidad de sugerencias.</p><p>Un <code>UserInteractionService</code> actualiza este perfil de forma continua a partir de los comentarios del usuario, en particular mediante un mini-juego de swipe que permite valorar cinco destinos propuestos. Los datos se almacenan localmente en una base de datos <strong>SQLite</strong> (mediante el paquete <code>sqflite</code>), y se utilizaron scripts de Python (<code>check_db.py</code>, <code>jsonl_to_csv.py</code>) para preparar y verificar los conjuntos de datos de destinos.</p>",
        "proj-serendia-role": "<p>Dentro de este equipo de 7, contribuí al desarrollo de la aplicación Flutter/Dart, en particular en la lógica del perfil de usuario y la preparación de los datos mediante los scripts de Python, en estrecha colaboración con el resto del equipo para integrar estos elementos en el motor de recomendación.</p>",
        "proj-serendia-resultats": "<p>El resultado es una aplicación móvil funcional, capaz de proponer destinos personalizados y de hacer evolucionar sus recomendaciones a lo largo de las interacciones del usuario. Este proyecto me permitió trabajar en un desarrollo móvil completo en un equipo numeroso, desde la base de datos local hasta la interfaz de usuario.</p>",

        // Proyecto: Vélib'
        "proj-velib-title": "Vélib'",
        "proj-velib-desc": "Rediseño completo de la aplicación Vélib', en grupo de 5, con la API oficial de Vélib' Métropole: nuevo diseño y nuevas funcionalidades.",
        "proj-velib-tagline": "Un rediseño completo de la aplicación Vélib', con un nuevo diseño y nuevas funcionalidades basadas en la API oficial de Vélib' Métropole.",
        "proj-velib-context": "<p>En el marco de un proyecto en equipo de 5, nos inspiramos en la aplicación oficial de Vélib' para recrear por completo nuestra propia versión, apoyándonos en las API abiertas de Vélib' Métropole para obtener los datos en tiempo real de las estaciones.</p>",
        "proj-velib-objectifs": "<p>El objetivo no era simplemente reproducir la aplicación existente, sino repensarla:</p><ul><li>Revisar por completo el diseño (colores, maquetación, experiencia de usuario)</li><li>Añadir nuevas funcionalidades ausentes en la aplicación original</li><li>Aprovechar los datos en tiempo real de la API de Vélib' Métropole (disponibilidad de bicicletas mecánicas y eléctricas, plazas libres, etc.)</li></ul>",
        "proj-velib-realisation": "<p>Diseñamos una nueva interfaz con una identidad visual propia, trabajando en la paleta de colores, la legibilidad de la información y la navegación entre pantallas. En cuanto a las funcionalidades, la aplicación obtiene y muestra en tiempo real el estado de las estaciones (bicicletas disponibles, plazas libres, tipo de bicicleta) a través de la API de Vélib' Métropole, y ofrece nuevas funcionalidades pensadas por el equipo para mejorar la experiencia respecto a la aplicación existente.</p>",
        "proj-velib-role": "<p>Dentro de este equipo de 5, participé en el diseño del nuevo aspecto de la aplicación (identidad gráfica, pantallas), así como en la integración de los datos de la API de Vélib' Métropole en la interfaz.</p>",
        "proj-velib-resultats": "<p>El resultado es una aplicación repensada, más agradable de usar y enriquecida con nuevas funcionalidades, basándose en datos reales y actualizados. Este proyecto fue la ocasión de trabajar en equipo en todo el ciclo de un proyecto de aplicación: diseño, identidad visual, integración de API y desarrollo.</p>",

        // Proyecto: Diagramas de Voronoi
        "proj-voronoi-title": "Diagramas de Voronoi",
        "proj-voronoi-desc": "Implementación individual del algoritmo de Fortune en Python para generar y exportar diagramas de Voronoi, en el marco de un proyecto académico de grupo.",
        "proj-watchout-title": "Watch Out",
        "proj-watchout-desc": "Pequeño videojuego de terror en 2D creado para la escuela: explora un bosque oscuro para encontrar dígitos ocultos, compón un código y escapa antes de que se acabe el tiempo.",
        "proj-watchout-tagline": "Pequeño videojuego de terror en 2D desarrollado en Python con Pygame, para un proyecto multimedia escolar.",
        "proj-watchout-context": "<p>Este proyecto se realizó en el marco de un proyecto multimedia escolar. El objetivo era diseñar un pequeño videojuego completo, desde la historia hasta la mecánica de juego, pasando por los gráficos, el sonido y la interfaz.</p>",
        "proj-watchout-objectifs": "<p>El objetivo era crear un juego de terror en 2D capaz de:</p><ul><li>Permitir explorar varias escenas conectadas (bosque, camino, casa encantada)</li><li>Esconder pistas (cifras) en el decorado que el jugador debe encontrar</li><li>Implementar un sistema de código que introducir antes de que se acabe un temporizador</li><li>Crear una atmósfera angustiante gracias a los gráficos, la música y apariciones repentinas</li></ul>",
        "proj-watchout-realisation": "<p>Desarrollé el juego con Python y la biblioteca Pygame. El jugador explora varias escenas conectadas mediante zonas pulsables, debe localizar 3 cifras ocultas en el decorado y luego introducirlas en una pantalla de código antes de que termine un temporizador de 20 segundos. Para reforzar la atmósfera, añadí música de ambiente, fantasmas semitransparentes que se desplazan hacia el jugador y apariciones aleatorias en pantalla.</p><p>También creé scripts auxiliares (<code>localisation_pixel.py</code>, <code>modifier_image.py</code>) para localizar con precisión las pistas en las imágenes y preparar los recursos gráficos.</p>",
        "proj-watchout-role": "<p>Este proyecto se realizó de forma individual: diseño del guion, desarrollo de la jugabilidad en Python/Pygame, gestión de los recursos (imágenes, fuentes, música) y creación de la atmósfera sonora y visual.</p>",
        "proj-watchout-resultats": "<p>El resultado es un pequeño juego jugable de principio a fin: una introducción, tres escenas explorables, una mecánica de búsqueda de pistas, una pantalla de código con temporizador, así como una pantalla de victoria y otra de game over. Este proyecto me permitió descubrir el desarrollo de videojuegos con Pygame y trabajar en la gestión de recursos multimedia (imágenes, fuentes, música).</p>",
        "proj-voronoi-tagline": "Generación de diagramas de Voronoi en Python a partir del algoritmo de Fortune, con exportación a SVG y PNG.",
        "proj-voronoi-context": "<p>Este proyecto se enmarca en un proyecto académico de grupo sobre los diagramas de Voronoi, una estructura de geometría algorítmica utilizada para dividir un plano en regiones a partir de un conjunto de puntos. Me encargué, de forma individual, de la segunda fase del proyecto: la implementación del algoritmo de generación.</p>",
        "proj-voronoi-objectifs": "<p>El objetivo de esta fase era implementar un generador de diagramas de Voronoi eficiente, capaz de:</p><ul><li>Calcular un diagrama de Voronoi a partir de un conjunto de puntos mediante el algoritmo de Fortune (algoritmo de barrido)</li><li>Representar las celdas, vértices y aristas del diagrama mediante estructuras de datos dedicadas</li><li>Exportar el resultado en forma de imagen (SVG y PNG)</li></ul>",
        "proj-voronoi-realisation": "<p>Implementé una clase <code>FortuneAlgorithm</code>, que hereda de una clase genérica <code>VoronoiGenerator</code>, que pone en práctica el algoritmo de barrido de Fortune: una línea de barrido horizontal recorre el plano y construye progresivamente el diagrama a partir de los puntos proporcionados. Los elementos geométricos (puntos, aristas) se representan mediante clases dedicadas <code>Point</code> y <code>Edge</code>, con funciones utilitarias de geometría agrupadas en <code>geometry_utils</code>.</p><p>Para visualizar los resultados, desarrollé exportadores dedicados que permiten generar el diagrama final en formato <strong>SVG</strong> y <strong>PNG</strong>.</p>",
        "proj-voronoi-role": "<p>Esta fase del proyecto se realizó de forma individual dentro de un proyecto académico de grupo. Diseñé e implementé el algoritmo de Fortune, así como los módulos de geometría y exportación asociados, basándome en lo establecido durante la primera fase del proyecto.</p>",
        "proj-voronoi-resultats": "<p>El resultado es un generador capaz de producir diagramas de Voronoi correctos a partir de cualquier conjunto de puntos, exportables directamente en SVG o PNG. Este proyecto me permitió profundizar mis conocimientos en geometría algorítmica y estructuras de datos complejas.</p>"
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
        "hero-greeting": "안녕하세요, 저는",
        "hero-title": "Léona Dupont",
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
        "footer-rights": "© 2026 레오나 뒤퐁. 모든 권리 보유.",

        // 신규 콘텐츠 (범용 data-i18n 메커니즘)
        "nav-travel": "여행",
        "about-p4": "저는 현재 2026년 3월 9일부터 4~6개월간의 인턴십을 찾고 있으며, 이를 통해 이러한 모든 역량을 실제 프로젝트에 적용해보고자 합니다.",
        "exp-hackathon-title": "해커톤 « Nuit de l'informatique »",
        "exp-hackathon-date": "2025년 12월",
        "exp-hackathon-desc": "팀으로 24시간 동안 진행된 해커톤 참가: 제한된 시간 안에 기능성 프로토타입을 설계, 개발하고 심사위원 앞에서 발표했습니다.",
        "skills-bdd": "데이터베이스",
        "skills-mobile": "모바일 개발 & 도구",
        "skills-langues": "언어",
        "skill-api": "API 연동",
        "skill-agile": "애자일 방법론",
        "lang-fr": "프랑스어 — 모국어",
        "lang-en": "영어 — B2 수준",
        "lang-es": "스페인어 — A2 수준",
        "lang-ko": "한국어 — A2 수준",
        "lang-ja": "일본어 — A1 수준",
        "proj-cta": "프로젝트 보기",
        "tag-group-7": "7인 그룹",
        "tag-group-5": "5인 그룹",
        "tag-individual": "개인 작업",
        "back-to-projects": "프로젝트로 돌아가기",
        "travel-tag": "여행 일기",
        "travel-title": "방문한 국가",
        "travel-intro": "여행을 좋아하는 저는 아래 국가들을 직접 방문할 기회가 있었습니다. 카드 위에 마우스를 올리면 (곧) 그곳에서 찍은 제 사진을 확인할 수 있습니다!",
        "travel-soon": "사진 준비 중",
        "travel-home": "거주지",
        "map-legend-visited": "방문한 국가",
        "map-legend-unvisited": "미방문 국가",
        "map-extra-label": "또한 방문 (지도에 표시하기엔 너무 작은 지역):",
        "travel-modal-soon": "이 여행에 대한 이야기와 관련 사진은 곧 추가될 예정입니다!",
        "nav-future": "미래 계획",
        "future-title": "미래 계획",
        "future-text": "<p>2026년 8월부터 워킹 홀리데이(PVT) 프로그램을 통해 한국에서 1년을 보낼 예정입니다.</p><p>이 1년의 주요 목표는 한국 생활에 적응하고, 한국어 실력을 향상시키며, 이전 여행에서 경험하지 못한 현지 문화를 발견하는 것입니다.</p><p>워킹 홀리데이를 마친 후에는 서울에서 사이버보안 석사 과정에 진학하고자 합니다. 한국에서의 이전 경험이 정말 좋았고, 사이버보안을 공부하고 일하기에 가장 좋은 나라 중 하나라고 생각합니다.</p>",
        "future-stat-destination-value": "🇰🇷 대한민국",
        "future-stat-destination-label": "목적지",
        "future-stat-departure": "워킹 홀리데이 출발",
        "future-stat-duration": "워킹 홀리데이 기간",
        "proj-section-context": "배경",
        "proj-section-objectifs": "목표",
        "proj-section-realisation": "구현 내용",
        "proj-section-role": "저의 역할",
        "proj-section-resultats": "결과",

        // 프로젝트: Java 계산기
        "proj-calc-title": "Java 계산기",
        "proj-calc-tagline": "복잡한 산술 표현식을 계산하고 표시할 수 있는 Java 계산기로, Composite 디자인 패턴에 따라 설계되었습니다.",
        "proj-calc-context": "<p>이 프로젝트는 BUT Informatique 1학년 2학기에 2인 1조로 진행한 학업 프로젝트로 수행되었습니다. 목표는 수학적 표현식의 모델링과 계산이라는 구체적인 사례를 통해 Java 객체지향 프로그래밍을 배우는 것이었습니다.</p>",
        "proj-calc-objectifs": "<p>다음을 수행할 수 있는 계산기를 만드는 것이 목표였습니다:</p><ul><li>숫자와 연산(덧셈, 뺄셈, 곱셈, 나눗셈)으로 구성된 수학적 표현식 표현하기</li><li>자동 괄호 처리를 통해 이러한 표현식을 텍스트 형태로 표시하기</li><li>재귀적으로 결과 계산하기</li><li>0으로 나누기 등의 오류 상황을 적절히 처리하기</li></ul>",
        "proj-calc-realisation": "<p>저희는 <strong>Composite</strong> 디자인 패턴을 기반으로 한 객체지향 아키텍처를 구축했습니다:</p><ul><li>계산의 모든 요소에 공통적인 <code>Expression</code> 인터페이스</li><li>최종값(표현식 트리의 리프 노드)을 나타내는 <code>Nombre</code> 클래스</li><li><code>Addition</code>, <code>Soustraction</code>, <code>Multiplication</code>, <code>Division</code>이 상속하는 추상 클래스 <code>Operation</code>으로, 각각 두 개의 하위 표현식을 결합합니다</li></ul><p>각 표현식은 자신의 값을 (재귀적으로) 계산하는 동시에 자체 텍스트 표현을 생성할 수 있으며, 예를 들어 <code>((17 - 2) / (2 + 3)) = 3</code>과 같은 형태입니다. 0으로 나누는 경우는 프로그램을 중단시키지 않고 전용 예외를 통해 감지 및 처리됩니다.</p>",
        "proj-calc-role": "<p>2인 1조로 작업하면서 저는 <code>Expression</code> / <code>Operation</code> / <code>Nombre</code> 클래스 계층 구조 설계에 참여했으며, 여러 연산의 구현과 오류 처리(0으로 나누기)도 담당했습니다. 이 프로젝트는 상속, 다형성, 재귀적 설계를 포함한 객체지향 프로그래밍을 처음으로 실제로 적용해본 경험이었습니다.</p>",
        "proj-calc-resultats": "<p>결과적으로 임의의 복잡도를 가진 중첩 표현식을 계산하고 그 결과를 읽기 쉬운 형태로 표시할 수 있는 기능성 계산기를 완성했습니다. 이 프로젝트를 통해 재귀적 구조를 모델링하는 데 있어 Composite 패턴의 유용성을 잘 이해할 수 있었습니다.</p>",

        // 프로젝트: 고객 요구사항 구현
        "proj-client-title": "고객 요구사항 구현",
        "proj-client-tagline": "Python에서 딕셔너리를 사용하여 모델링한 친구 관계망에서의 커뮤니티 탐지.",
        "proj-client-context": "<p>1학년 때 진행한 이 학업 프로젝트는 소셜 네트워크 분석과 관련된 고객 요구사항에 대응하는 것이었습니다: 친구 관계 목록을 바탕으로 서로 모두 아는 사람들의 그룹, 즉 '커뮤니티'를 찾아내는 것입니다.</p>",
        "proj-client-objectifs": "<p>2인 1조로 진행한 이 프로젝트의 목표는 다음과 같았습니다:</p><ul><li>친구 관계망을 Python 딕셔너리 형태로 모델링하기(각 사람을 그 친구 목록과 연결)</li><li>친구 쌍 목록으로부터 이 관계망을 자동으로 구축하기</li><li>커뮤니티, 즉 그룹 내 모든 구성원이 서로 친구인 그룹을 식별하기</li><li>단위 테스트를 통해 프로그램의 동작을 검증하기</li></ul>",
        "proj-client-realisation": "<p>저희는 친구 쌍 목록(예: <code>{\"Alice\": [\"Bob\", \"Dominique\"], ...}</code>)으로부터 딕셔너리 형태로 친구 관계망을 구축하는 <code>create_network</code> 함수를 개발했고, 이어서 이 관계망을 탐색하여 서로 연결된 사람들을 그룹화하는 커뮤니티 탐지 알고리즘을 개발했습니다.</p><p>전체 코드는 단위 테스트 모음(<code>test_community_detection.py</code>)을 통해 검증되었으며, 빈 관계망, 고립된 커뮤니티, 여러 그룹에 속하는 사람 등 다양한 경우를 다루었습니다.</p>",
        "proj-client-role": "<p>2인 1조로 작업하면서 저는 데이터 구조 설계(관계망을 나타내는 딕셔너리), 커뮤니티 탐지 알고리즘, 그리고 다양한 데이터셋에 대한 견고성을 검증하는 단위 테스트 작성을 담당했습니다.</p>",
        "proj-client-resultats": "<p>최종 프로그램은 입력된 친구 관계망의 커뮤니티를 정확하게 식별하며, 모든 단위 테스트가 성공적으로 통과합니다. 이 프로젝트를 통해 Python 데이터 구조와 테스트 모범 사례에 대한 이해를 더욱 강화할 수 있었습니다.</p>",

        // 프로젝트: 펭귄 게임
        "proj-pingouin-title": "펭귄 게임",
        "proj-pingouin-tagline": "HTML, CSS, JavaScript로 만든 작은 인터랙티브 게임: 펭귄이 움직이며 물고기를 잡습니다.",
        "proj-pingouin-context": "<p>이 프로젝트는 HTML, CSS, JavaScript로 개발된 프론트엔드 미니 게임으로, 브라우저에서의 DOM 조작, 애니메이션, 실시간 이벤트 처리를 연습하기 위해 고안되었습니다.</p>",
        "proj-pingouin-objectifs": "<p>목표는 간단하지만 제대로 동작하는 게임을 만드는 것이었습니다:</p><ul><li>장면(수조) 안에 배치되어 수직으로 움직일 수 있는 펭귄</li><li>화면을 가로질러 무작위로 나타나는 물고기</li><li>게임 영역 내로 제한되는 부드러운 키보드 상호작용</li></ul>",
        "proj-pingouin-realisation": "<p>펭귄(SVG로 표현)은 화살표 키를 누를 때마다 위 또는 아래로 30픽셀씩 이동하며, 수조 안에 머물도록 이동 범위가 제한됩니다. 동시에 500밀리초마다 무작위 높이에서 물고기가 생성되어 CSS 애니메이션을 통해 화면을 가로지르며, 요소가 누적되지 않도록 2초 후 DOM에서 자동으로 제거됩니다.</p>",
        "proj-pingouin-role": "<p>저는 게임 전체를 설계했습니다: HTML/CSS로 장면을 구성하고, SVG로 그래픽 요소(펭귄, 물고기, 물)를 통합하고, 이동, 무작위 생성, 요소 정리를 위한 JavaScript 로직을 작성했습니다.</p>",
        "proj-pingouin-resultats": "<p>결과적으로 부드럽고 재미있는 미니 게임이 완성되었으며, 이를 통해 DOM 조작, 키보드 이벤트, CSS 애니메이션, 그리고 동적으로 생성된 요소의 생명주기 관리에 대해 깊이 있게 다룰 수 있었습니다.</p>",

        // 프로젝트: SérendIA
        "proj-serendia-title": "SérendIA",
        "proj-serendia-desc": "벡터 기반 추천 엔진과 제안을 세밀화하기 위한 스와이프 미니 게임을 갖춘, 7인 그룹으로 개발한 여행 추천 Flutter 모바일 앱.",
        "proj-serendia-tagline": "벡터 기반 사용자 프로필을 활용한 추천 엔진을 통해 맞춤형 여행지를 추천하는 Flutter 모바일 앱입니다.",
        "proj-serendia-context": "<p>SérendIA는 BUT 3학년 학업 프로젝트로 7인 팀이 개발한 애플리케이션입니다. 이 프로젝트의 목표는 사용자와의 상호작용에 따라 각 사용자의 선호도에 적응할 수 있는 여행지 추천 애플리케이션을 설계하는 것이었습니다.</p>",
        "proj-serendia-objectifs": "<p>프로젝트는 여러 단계로 진행되었습니다:</p><ul><li><strong>1단계 — 기초 &amp; 데이터</strong>: 애플리케이션 아키텍처 구축 및 여행지 데이터셋 준비</li><li><strong>2단계 — 추천 엔진 V1</strong>: 사용자 선호도를 기반으로 한 초기 추천 알고리즘 설계</li><li><strong>3단계 — 엔진 개선 &amp; 사용자 경험</strong>: 추천 엔진 개선 및 인터페이스와 상호작용 향상</li></ul>",
        "proj-serendia-realisation": "<p>각 사용자는 여러 축(문화, 모험, 휴식, 예산)에 대한 선호도 벡터인 <code>UserProfileVector</code>로 표현됩니다. 여행지는 <strong>'Soft Filtering'</strong>(소프트 필터링) 방식을 통해 이 프로필과 비교됩니다: 프로필과 완전히 일치하지 않는 여행지를 엄격하게 제외하는 대신, 단순히 순위에서 페널티를 부여함으로써 제안의 다양성을 유지합니다.</p><p><code>UserInteractionService</code>는 사용자의 피드백을 바탕으로 이 프로필을 지속적으로 업데이트하며, 특히 다섯 개의 추천 여행지를 평가할 수 있는 스와이프 미니 게임을 통해 이루어집니다. 데이터는 <strong>SQLite</strong> 데이터베이스(<code>sqflite</code> 패키지 사용)에 로컬로 저장되며, Python 스크립트(<code>check_db.py</code>, <code>jsonl_to_csv.py</code>)를 사용하여 여행지 데이터셋을 준비하고 검증했습니다.</p>",
        "proj-serendia-role": "<p>이 7인 팀에서 저는 Flutter/Dart 애플리케이션 개발에 기여했으며, 특히 사용자 프로필 로직과 Python 스크립트를 통한 데이터 준비를 담당하면서 이를 추천 엔진에 통합하기 위해 팀의 나머지 구성원들과 긴밀히 협력했습니다.</p>",
        "proj-serendia-resultats": "<p>결과적으로 맞춤형 여행지를 제안하고 사용자와의 상호작용에 따라 추천 내용을 발전시킬 수 있는 기능성 모바일 애플리케이션이 완성되었습니다. 이 프로젝트를 통해 로컬 데이터베이스부터 사용자 인터페이스까지, 대규모 팀에서의 전체 모바일 개발 과정을 경험할 수 있었습니다.</p>",

        // 프로젝트: Vélib'
        "proj-velib-title": "Vélib'",
        "proj-velib-desc": "Vélib' Métropole 공식 API를 활용하여 5인 그룹으로 진행한 Vélib' 애플리케이션의 전면 리뉴얼: 새로운 디자인과 새로운 기능.",
        "proj-velib-tagline": "Vélib' Métropole 공식 API를 기반으로 새로운 디자인과 새로운 기능을 갖춘 Vélib' 애플리케이션의 전면 리뉴얼입니다.",
        "proj-velib-context": "<p>5인 팀 프로젝트로, 저희는 공식 Vélib' 애플리케이션에서 영감을 받아 자체적인 버전을 완전히 새롭게 만들었으며, Vélib' Métropole의 오픈 API를 활용하여 정류장의 실시간 데이터를 가져왔습니다.</p>",
        "proj-velib-objectifs": "<p>목표는 기존 애플리케이션을 단순히 재현하는 것이 아니라 새롭게 재구성하는 것이었습니다:</p><ul><li>디자인 전반(색상, 레이아웃, 사용자 경험)을 새롭게 검토하기</li><li>기존 애플리케이션에 없던 새로운 기능 추가하기</li><li>Vélib' Métropole API의 실시간 데이터(일반 자전거 및 전기 자전거의 이용 가능 여부, 빈 자리 등) 활용하기</li></ul>",
        "proj-velib-realisation": "<p>저희는 색상 팔레트, 정보의 가독성, 화면 간 탐색을 고려하여 고유한 비주얼 아이디를 갖춘 새로운 인터페이스를 설계했습니다. 기능 측면에서는 애플리케이션이 Vélib' Métropole API를 통해 정류장 상태(이용 가능한 자전거, 빈 자리, 자전거 종류)를 실시간으로 가져와 표시하며, 기존 애플리케이션 대비 사용자 경험을 개선하기 위해 팀에서 고안한 새로운 기능들을 제공합니다.</p>",
        "proj-velib-role": "<p>이 5인 팀에서 저는 애플리케이션의 새로운 디자인(그래픽 가이드라인, 화면) 설계와 Vélib' Métropole API 데이터를 인터페이스에 통합하는 작업에 참여했습니다.</p>",
        "proj-velib-resultats": "<p>결과적으로 사용성이 개선되고 새로운 기능이 추가된 애플리케이션이 완성되었으며, 실제 최신 데이터를 기반으로 동작합니다. 이 프로젝트는 설계, 디자인, API 연동, 개발에 이르는 애플리케이션 프로젝트의 전체 과정을 팀 단위로 경험할 수 있는 기회였습니다.</p>",

        // 프로젝트: 보로노이 다이어그램
        "proj-voronoi-title": "보로노이 다이어그램",
        "proj-voronoi-desc": "그룹 학업 프로젝트의 일환으로, Python으로 Fortune 알고리즘을 개인적으로 구현하여 보로노이 다이어그램을 생성하고 내보냅니다.",
        "proj-watchout-title": "Watch Out",
        "proj-watchout-desc": "학교 과제로 만든 작은 2D 호러 게임: 어두운 숲을 탐험하며 숨겨진 숫자를 찾아 코드를 완성하고, 시간이 끝나기 전에 탈출해야 합니다.",
        "proj-watchout-tagline": "학교 멀티미디어 프로젝트로 Python과 Pygame으로 제작한 작은 2D 호러 비디오 게임입니다.",
        "proj-watchout-context": "<p>이 프로젝트는 학교 멀티미디어 프로젝트의 일환으로 진행되었습니다. 목표는 이야기부터 게임 메커니즘, 그래픽, 사운드, 인터페이스까지 포함한 완성도 있는 작은 비디오 게임을 디자인하는 것이었습니다.</p>",
        "proj-watchout-objectifs": "<p>목표는 다음을 수행할 수 있는 2D 호러 게임을 만드는 것이었습니다:</p><ul><li>서로 연결된 여러 장면(숲, 길, 흉가)을 탐험할 수 있게 하기</li><li>플레이어가 찾아야 할 숫자 힌트를 배경에 숨기기</li><li>타이머가 끝나기 전에 입력해야 하는 코드 시스템 구현하기</li><li>그래픽, 음악, 갑작스러운 출현을 통해 긴장감 있는 분위기 조성하기</li></ul>",
        "proj-watchout-realisation": "<p>Python과 Pygame 라이브러리를 사용해 게임을 개발했습니다. 플레이어는 클릭 가능한 영역으로 연결된 여러 장면을 탐험하며, 배경에 숨겨진 숫자 3개를 찾은 뒤 20초 타이머가 끝나기 전에 코드 화면에 입력해야 합니다. 분위기를 강화하기 위해 배경 음악, 플레이어를 향해 움직이는 반투명 유령, 화면에 무작위로 나타나는 형상을 추가했습니다.</p><p>또한 이미지 속 힌트의 위치를 정확히 파악하고 그래픽 리소스를 준비하기 위한 보조 스크립트(<code>localisation_pixel.py</code>, <code>modifier_image.py</code>)도 작성했습니다.</p>",
        "proj-watchout-role": "<p>이 프로젝트는 개인적으로 진행했습니다: 시나리오 구상, Python/Pygame을 이용한 게임플레이 개발, 리소스(이미지, 폰트, 음악) 관리, 사운드 및 비주얼 분위기 구성을 모두 담당했습니다.</p>",
        "proj-watchout-resultats": "<p>결과물은 처음부터 끝까지 플레이 가능한 작은 게임입니다: 인트로, 탐험 가능한 세 개의 장면, 힌트 찾기 메커니즘, 타이머가 있는 코드 화면, 그리고 승리 화면과 게임 오버 화면까지 구현했습니다. 이 프로젝트를 통해 Pygame을 이용한 비디오 게임 개발을 경험하고, 멀티미디어 리소스(이미지, 폰트, 음악) 관리 작업을 해볼 수 있었습니다.</p>",
        "proj-voronoi-tagline": "Fortune 알고리즘을 기반으로 Python에서 보로노이 다이어그램을 생성하며, SVG와 PNG로 내보낼 수 있습니다.",
        "proj-voronoi-context": "<p>이 프로젝트는 보로노이 다이어그램을 주제로 한 그룹 학업 프로젝트의 일부입니다. 보로노이 다이어그램은 점들의 집합을 바탕으로 평면을 영역으로 분할하는 데 사용되는 알고리즘 기하학 구조입니다. 저는 프로젝트의 2단계인 생성 알고리즘 구현을 개인적으로 담당했습니다.</p>",
        "proj-voronoi-objectifs": "<p>이 단계의 목표는 다음을 수행할 수 있는 고성능 보로노이 다이어그램 생성기를 구현하는 것이었습니다:</p><ul><li>Fortune 알고리즘(스위프 알고리즘)을 사용하여 점들의 집합으로부터 보로노이 다이어그램 계산하기</li><li>전용 데이터 구조를 사용하여 다이어그램의 셀, 정점, 변을 표현하기</li><li>결과를 이미지(SVG 및 PNG) 형태로 내보내기</li></ul>",
        "proj-voronoi-realisation": "<p>저는 일반화된 클래스 <code>VoronoiGenerator</code>를 상속하는 <code>FortuneAlgorithm</code> 클래스를 구현했으며, 이는 Fortune의 스위프 알고리즘을 구현합니다: 수평 스위프 라인이 평면을 가로지르며 제공된 점들로부터 점진적으로 다이어그램을 구축합니다. 기하학적 요소(점, 변)는 전용 클래스 <code>Point</code>와 <code>Edge</code>로 표현되며, 기하학 유틸리티 함수들은 <code>geometry_utils</code>에 정리되어 있습니다.</p><p>결과를 시각화하기 위해 최종 다이어그램을 <strong>SVG</strong> 및 <strong>PNG</strong> 형식으로 생성할 수 있는 전용 내보내기 모듈을 개발했습니다.</p>",
        "proj-voronoi-role": "<p>프로젝트의 이 단계는 그룹 학업 프로젝트 내에서 개인적으로 수행되었습니다. 저는 프로젝트 1단계에서 마련된 기반을 바탕으로 Fortune 알고리즘과 관련 기하학 및 내보내기 모듈을 설계하고 구현했습니다.</p>",
        "proj-voronoi-resultats": "<p>결과적으로 어떤 점들의 집합으로부터도 올바른 보로노이 다이어그램을 생성할 수 있으며, SVG 또는 PNG로 직접 내보낼 수 있는 생성기를 완성했습니다. 이 프로젝트를 통해 알고리즘 기하학과 복잡한 데이터 구조에 대한 지식을 더욱 심화할 수 있었습니다.</p>"
    }
};

// Met à jour le texte d'un h3 sans supprimer son icône décorative
function setH3Text(h3, text) {
    if (!h3) return;
    const icon = h3.querySelector('i');
    h3.textContent = text;
    if (icon) {
        h3.insertBefore(document.createTextNode(' '), h3.firstChild);
        h3.insertBefore(icon, h3.firstChild);
    }
}

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
    const heroGreeting = document.querySelector('#hero .hero-greeting');
    if (heroGreeting) heroGreeting.textContent = t['hero-greeting'] || heroGreeting.textContent;

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
    if (aboutParas.length > 3) aboutParas[3].textContent = t['about-p4'] || aboutParas[3].textContent;
    
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
        setH3Text(expCategories[0].querySelector('h3'), t['exp-enedis-title']);
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
        setH3Text(expCategories[1].querySelector('h3'), t['exp-carrefour-title']);
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
        setH3Text(expCategories[2].querySelector('h3'), t['exp-babysit-title']);
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
        setH3Text(uniH3, t['edu-uni-title']);
        
        const uniP = eduCategories[0].querySelector('p');
        if (uniP) {
            uniP.innerHTML = '<strong>' + t['edu-uni-date'] + '</strong> — ' + t['edu-uni-degree'];
        }
    }
    
    if (eduCategories.length > 1) {
        const lyceeH3 = eduCategories[1].querySelector('h3');
        setH3Text(lyceeH3, t['edu-lycee-title']);
        
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
    if (skillsH3.length > 0) setH3Text(skillsH3[0], t['skills-prog']);
    if (skillsH3.length > 1) setH3Text(skillsH3[1], t['skills-web']);
    if (skillsH3.length > 2) setH3Text(skillsH3[2], t['skills-sys']);
    if (skillsH3.length > 3) setH3Text(skillsH3[3], t['skills-tools']);
    
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

    // Application générique des traductions via attributs data-i18n
    applyDataI18n(lang);
}

// Applique les traductions sur tous les éléments portant un attribut data-i18n*
function applyDataI18n(lang) {
    const t = translations[lang] || translations.fr;

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (t[key] !== undefined) el.textContent = t[key];
    });

    document.querySelectorAll('[data-i18n-html]').forEach(el => {
        const key = el.dataset.i18nHtml;
        if (t[key] !== undefined) el.innerHTML = t[key];
    });

    document.querySelectorAll('[data-i18n-title]').forEach(el => {
        const key = el.dataset.i18nTitle;
        if (t[key] !== undefined) el.title = t[key];
    });
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
    if (typeof particlesJS === 'undefined' || !document.getElementById('particles-js')) return;
    particlesJS("particles-js", {
      particles: {
        number: { value: 80, density: { enable: true, value_area: 800 } },
        color: { value: "#818cf8" },
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
          color: "#818cf8",
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

/* Carnet de voyage : carte du monde interactive */
document.addEventListener('DOMContentLoaded', function () {
    const worldMap = document.getElementById('world-map');
    if (!worldMap) return;

    const visitedCountries = {
        fr: { flag: '🇫🇷', name: 'France', home: true,
            story: '<p>C\'est ici que j\'habite, entre mes études, mes projets et... mes valises toujours prêtes pour la prochaine destination !</p>',
            photos: [] },
        jp: { flag: '🇯🇵', name: 'Japon',
            story: '<p><em>Brouillon à compléter :</em> ce voyage au Japon s\'est fait dans le cadre d\'un séjour scolaire / linguistique. J\'ai pu découvrir la culture japonaise, son mode de vie et quelques lieux emblématiques.</p><p>À compléter avec les villes visitées, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        kr: { flag: '🇰🇷', name: 'Corée du Sud',
            story: '<p><em>Brouillon à compléter :</em> mon voyage en Corée du Sud s\'est fait dans le cadre d\'un séjour scolaire / linguistique, et c\'est cette expérience qui m\'a donné envie d\'y retourner pour mon PVT.</p><p>À compléter avec les villes visitées, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        kh: { flag: '🇰🇭', name: 'Cambodge',
            story: '<p><em>Brouillon à compléter :</em> ce voyage au Cambodge s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air. J\'ai pu découvrir le pays et sa culture lors d\'un séjour en Asie du Sud-Est.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        vn: { flag: '🇻🇳', name: 'Vietnam',
            story: '<p><em>Brouillon à compléter :</em> ce voyage au Vietnam s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air, lors d\'un séjour en Asie du Sud-Est.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        th: { flag: '🇹🇭', name: 'Thaïlande',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Thaïlande s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air, lors d\'un séjour en Asie du Sud-Est.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        za: { flag: '🇿🇦', name: 'Afrique du Sud',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Afrique du Sud s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air. J\'ai pu découvrir le pays, ses paysages et sa culture.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        hr: { flag: '🇭🇷', name: 'Croatie',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Croatie s\'est fait dans le cadre d\'un séjour scolaire / colonie de vacances. J\'ai pu découvrir le pays, sa côte et sa culture.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        ba: { flag: '🇧🇦', name: 'Bosnie',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Bosnie s\'est fait dans le cadre d\'un séjour scolaire / colonie de vacances.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        fi: { flag: '🇫🇮', name: 'Finlande',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Finlande s\'est fait dans le cadre d\'un séjour scolaire / échange. J\'ai pu découvrir le mode de vie nordique et sa culture.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        de: { flag: '🇩🇪', name: 'Allemagne',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Allemagne s\'est fait dans le cadre d\'un échange scolaire / séjour linguistique.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        pl: { flag: '🇵🇱', name: 'Pologne',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Pologne s\'est fait dans le cadre d\'un séjour scolaire.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        be: { flag: '🇧🇪', name: 'Belgique',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Belgique s\'est fait avec des amis, pour une courte escapade.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        gb: { flag: '🇬🇧', name: 'Angleterre',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Angleterre s\'est fait dans le cadre d\'un séjour scolaire / linguistique.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        ie: { flag: '🇮🇪', name: 'Irlande',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Irlande s\'est fait dans le cadre d\'un séjour scolaire / linguistique.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        us: { flag: '🇺🇸', name: 'États-Unis',
            story: '<p><em>Brouillon à compléter :</em> ce voyage aux États-Unis s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air.</p><p>À compléter avec les villes visitées, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        mx: { flag: '🇲🇽', name: 'Mexique',
            story: '<p><em>Brouillon à compléter :</em> ce voyage au Mexique s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        es: { flag: '🇪🇸', name: 'Espagne',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Espagne s\'est fait avec des amis / mon copain, pour profiter du soleil et de la culture locale.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        cn: { flag: '🇨🇳', name: 'Chine',
            story: '<p><em>Brouillon à compléter :</em> ce voyage en Chine s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        nl: { flag: '🇳🇱', name: 'Pays-Bas',
            story: '<p><em>Brouillon à compléter :</em> ce voyage aux Pays-Bas s\'est fait avec des amis, pour un city-trip.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        sg: { flag: '🇸🇬', name: 'Singapour',
            story: '<p><em>Brouillon à compléter :</em> ce passage par Singapour s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air, lors d\'un séjour en Asie.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        hk: { flag: '🇭🇰', name: 'Hong Kong',
            story: '<p><em>Brouillon à compléter :</em> ce passage par Hong Kong s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air, lors d\'un séjour en Asie.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        re: { flag: '🇷🇪', name: 'La Réunion',
            story: '<p><em>Brouillon à compléter :</em> ce voyage à La Réunion s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air. J\'ai pu découvrir l\'île, ses paysages volcaniques et sa culture créole.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] },
        mu: { flag: '🇲🇺', name: 'Île Maurice',
            story: '<p><em>Brouillon à compléter :</em> ce voyage à l\'Île Maurice s\'est fait en famille, grâce au métier de ma mère, hôtesse de l\'air. J\'ai pu profiter des plages et découvrir la culture locale.</p><p>À compléter avec les lieux visités, les anecdotes et les photos de ce séjour.</p>',
            photos: [] }
    };

    const tooltip = document.createElement('div');
    tooltip.id = 'map-tooltip';
    document.body.appendChild(tooltip);

    function showTooltip(data, event) {
        const lang = localStorage.getItem('selectedLanguage') || 'fr';
        const t = translations[lang] || translations.fr;
        const label = data.home ? t['travel-home'] : t['travel-soon'];
        tooltip.innerHTML = '<span class="travel-flag">' + data.flag + '</span><span>' + data.name + ' — ' + label + '</span>';
        tooltip.classList.add('visible');
        moveTooltip(event);
    }

    function moveTooltip(event) {
        tooltip.style.left = (event.pageX + 15) + 'px';
        tooltip.style.top = (event.pageY + 15) + 'px';
    }

    function hideTooltip() {
        tooltip.classList.remove('visible');
    }

    // Modale "carnet de voyage"
    const travelModal = document.createElement('div');
    travelModal.id = 'travel-modal';
    travelModal.innerHTML =
        '<div class="travel-modal-overlay"></div>' +
        '<div class="travel-modal-card">' +
          '<button class="travel-modal-close" aria-label="Fermer"><i class="fas fa-times"></i></button>' +
          '<div class="travel-modal-header">' +
            '<h3 class="travel-modal-title"></h3>' +
          '</div>' +
          '<div class="travel-modal-body"></div>' +
          '<div class="travel-modal-gallery"></div>' +
        '</div>';
    document.body.appendChild(travelModal);

    function openTravelModal(data) {
        const lang = localStorage.getItem('selectedLanguage') || 'fr';
        const t = translations[lang] || translations.fr;
        travelModal.querySelector('.travel-modal-title').textContent = data.flag + ' ' + data.name;
        travelModal.querySelector('.travel-modal-body').innerHTML = data.story || ('<p>' + t['travel-modal-soon'] + '</p>');
        const gallery = travelModal.querySelector('.travel-modal-gallery');
        gallery.innerHTML = '';
        (data.photos || []).forEach(src => {
            const img = document.createElement('img');
            img.src = src;
            img.alt = data.name;
            img.loading = 'lazy';
            gallery.appendChild(img);
        });
        travelModal.classList.add('visible');
        document.body.classList.add('modal-open');
        hideTooltip();
    }

    function closeTravelModal() {
        travelModal.classList.remove('visible');
        document.body.classList.remove('modal-open');
    }

    travelModal.querySelector('.travel-modal-overlay').addEventListener('click', closeTravelModal);
    travelModal.querySelector('.travel-modal-close').addEventListener('click', closeTravelModal);
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') closeTravelModal();
    });

    worldMap.querySelectorAll('[cc]').forEach(el => {
        const data = visitedCountries[el.getAttribute('cc')];
        if (!data) return;
        el.classList.add('visited');
        if (data.home) el.classList.add('home');
        el.addEventListener('mouseenter', e => showTooltip(data, e));
        el.addEventListener('mousemove', moveTooltip);
        el.addEventListener('mouseleave', hideTooltip);
        el.addEventListener('click', () => openTravelModal(data));
    });

    document.querySelectorAll('.travel-extra-item').forEach(el => {
        const data = visitedCountries[el.dataset.cc] || { flag: el.dataset.flag, name: el.dataset.name };
        el.addEventListener('mouseenter', e => showTooltip(data, e));
        el.addEventListener('mousemove', moveTooltip);
        el.addEventListener('mouseleave', hideTooltip);
        el.addEventListener('click', () => openTravelModal(data));
    });
});
  