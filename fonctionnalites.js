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
        "about-p1": "Je suis actuellement étudiante en troisième année d'un BUT Informatique, une formation professionnalisante et polyvalente qui me permet d'acquérir des compétences solides dans divers domaines de l'informatique, tels que le développement d'applications web et mobiles, la gestion de bases de données, ou encore l'administration de systèmes et réseaux.",
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
        "lang-fr": "Français : langue maternelle",
        "lang-en": "Anglais : niveau B2",
        "lang-es": "Espagnol : niveau A2",
        "lang-ko": "Coréen : niveau A2",
        "lang-ja": "Japonais : niveau A1",
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
        "future-title": "Bilan & projets d'avenir",
        "future-text": "<p>Court terme : Mon année de BUT3 se termine le 30 juillet 2026, puis je pars le 8 août 2026 en Programme Vacances Travail (PVT) en Corée du Sud, pour un an.</p><p>Moyen terme : L'objectif de cette année de PVT sera avant tout de m'immerger dans le pays : améliorer mon niveau de coréen, m'habituer au mode de vie sur place et découvrir la culture du quotidien, au-delà de mes précédents voyages. À l'issue de ce PVT, je souhaite intégrer un master en cybersécurité à Séoul, sur deux ans.</p><p>Long terme : Ce projet s'inscrit dans la continuité de mon projet personnel et professionnel : mon intérêt pour la cybersécurité, déjà identifié lors de mon stage chez Enedis, et mon attachement à la Corée du Sud depuis mon précédent voyage, se rejoignent dans ce parcours PVT puis master. À l'issue de ce master, j'espère trouver une entreprise sur place pour y travailler durablement.</p>",
        "future-stat-destination-value": "Corée du Sud",
        "future-stat-destination-label": "Destination",
        "future-stat-departure": "Départ en PVT",
        "future-stat-duration": "Durée du PVT",
        "proj-section-context": "Contexte",
        "proj-section-objectifs": "Objectifs",
        "proj-section-realisation": "Réalisation",
        "proj-section-role": "Mon rôle",
        "proj-section-resultats": "Résultats",
        "proj-section-bilan": "Bilan & difficultés",

        // Projet : Calculatrice Java
        "proj-calc-title": "Calculatrice Java",
        "proj-calc-tagline": "Une calculatrice en Java capable d'évaluer et d'afficher des expressions arithmétiques complexes, conçue selon le patron de conception Composite.",
        "proj-calc-context": "<p>Ce projet a été réalisé durant le second semestre de la première année de BUT Informatique, dans le cadre d'une SAÉ en binôme. L'objectif était de découvrir la programmation orientée objet en Java à travers un cas concret : la modélisation et l'évaluation d'expressions mathématiques.</p>",
        "proj-calc-objectifs": "<p>Construire une calculatrice capable de :</p><ul><li>Représenter des expressions mathématiques composées de nombres et d'opérations (addition, soustraction, multiplication, division)</li><li>Afficher ces expressions sous forme textuelle, avec parenthésage automatique</li><li>Calculer récursivement leur résultat</li><li>Gérer proprement les cas d'erreur, comme la division par zéro</li></ul>",
        "proj-calc-realisation": "<p>Nous avons mis en place une architecture orientée objet basée sur le patron de conception Composite :</p><ul><li>Une interface <code>Expression</code>, commune à tous les éléments du calcul</li><li>La classe <code>Nombre</code>, représentant les valeurs terminales (les feuilles de l'arbre d'expression)</li><li>Une classe abstraite <code>Operation</code>, dont héritent <code>Addition</code>, <code>Soustraction</code>, <code>Multiplication</code> et <code>Division</code>, chacune combinant deux sous-expressions</li></ul><p>Chaque expression sait à la fois calculer sa valeur (de manière récursive) et générer sa propre représentation textuelle, par exemple <code>((17 - 2) / (2 + 3)) = 3</code>. La division par zéro est détectée et gérée via une exception dédiée plutôt que de faire planter le programme.</p>",
        "proj-calc-role": "<p>En binôme, j'ai participé à la conception de la hiérarchie de classes <code>Expression</code> / <code>Operation</code> / <code>Nombre</code>, ainsi qu'à l'implémentation de plusieurs opérations et à la gestion des erreurs (division par zéro). Ce projet a été ma première véritable mise en pratique de la programmation orientée objet : héritage, polymorphisme et conception récursive.</p>",
        "proj-calc-resultats": "<p>Le résultat est une calculatrice fonctionnelle capable d'évaluer des expressions imbriquées de complexité arbitraire et d'en afficher une représentation lisible. Ce projet m'a permis de bien comprendre l'intérêt du patron Composite pour modéliser des structures récursives.</p>",
        "proj-calc-bilan": "<p>Étant mon premier vrai projet orienté objet, la principale difficulté a été de bien comprendre comment structurer la hiérarchie de classes avec le patron Composite : faire en sorte que chaque opération (addition, soustraction...) sache à la fois se calculer et s'afficher récursivement, sans dupliquer de code entre les classes. La gestion de la division par zéro a aussi demandé réflexion pour rester propre, via une exception, plutôt que de simplement faire planter le programme.</p><p>Ce projet en binôme m'a permis de vraiment comprendre l'intérêt de l'héritage et du polymorphisme, des notions qui restaient assez abstraites avant de les avoir manipulées sur un cas concret.</p>",

        // Projet : Implémentation d'un besoin client
        "proj-client-title": "Implémentation d'un besoin client",
        "proj-client-tagline": "Détection de communautés dans un réseau d'amitié, modélisé en Python à l'aide de dictionnaires.",
        "proj-client-context": "<p>Cette SAÉ de première année consistait à répondre à un besoin client autour de l'analyse de réseaux sociaux : à partir d'une liste de relations d'amitié, déterminer les groupes de personnes qui se connaissent toutes mutuellement, appelés « communautés ».</p>",
        "proj-client-objectifs": "<p>Le projet, réalisé en binôme, visait à :</p><ul><li>Modéliser un réseau d'amis sous forme de dictionnaire Python (chaque personne associée à la liste de ses amis)</li><li>Construire ce réseau automatiquement à partir d'une liste de paires d'amis</li><li>Identifier les communautés, c'est-à-dire les groupes où chaque membre est ami avec tous les autres membres du groupe</li><li>Valider le fonctionnement du programme à l'aide de tests unitaires</li></ul>",
        "proj-client-realisation": "<p>Nous avons développé une fonction <code>create_network</code> qui construit le réseau d'amitié sous forme de dictionnaire à partir d'une liste de paires (par exemple <code>{\"Alice\": [\"Bob\", \"Dominique\"], ...}</code>), puis un algorithme de détection de communautés qui parcourt ce réseau pour regrouper les personnes mutuellement connectées entre elles.</p><p>L'ensemble du code a été validé par une suite de tests unitaires (<code>test_community_detection.py</code>), couvrant différents cas de figure : réseaux vides, communautés isolées, ou personnes appartenant à plusieurs groupes.</p>",
        "proj-client-role": "<p>En binôme, j'ai travaillé sur la conception des structures de données (dictionnaires représentant le réseau), sur l'algorithme de détection des communautés et sur l'écriture des tests unitaires permettant de vérifier sa robustesse sur différents jeux de données.</p>",
        "proj-client-resultats": "<p>Le programme final identifie correctement les communautés d'un réseau d'amis fourni en entrée, et l'ensemble des tests unitaires passe avec succès. Ce projet a renforcé ma maîtrise des structures de données Python et des bonnes pratiques de test.</p>",
        "proj-client-bilan": "<p>La principale difficulté a été de bien définir ce qu'est une « communauté » et de gérer tous les cas particuliers : personnes isolées, personnes appartenant à plusieurs groupes, ou réseaux vides. Il a fallu plusieurs itérations sur l'algorithme de détection pour qu'il reste correct sur tous ces cas, ce qui nous a poussées à écrire des tests unitaires couvrant chaque situation avant même d'être sûres que l'algorithme final était juste.</p><p>Ce projet m'a appris l'importance d'écrire des tests dès le début pour valider un algorithme au fur et à mesure de ses évolutions, plutôt que de tout vérifier à la fin.</p>",

        // Projet : Jeu du pingouin
        "proj-pingouin-title": "Jeu du pingouin",
        "proj-pingouin-tagline": "Un petit jeu interactif en HTML, CSS et JavaScript : un pingouin qui se déplace pour attraper des poissons.",
        "proj-pingouin-context": "<p>Ce projet est un mini-jeu front-end développé en HTML, CSS et JavaScript, pensé comme un exercice de manipulation du DOM, d'animations et d'événements en temps réel dans le navigateur.</p>",
        "proj-pingouin-objectifs": "<p>L'objectif était de créer un jeu simple mais fonctionnel :</p><ul><li>Un pingouin positionné dans une scène (un bassin), pouvant se déplacer verticalement</li><li>Des poissons apparaissant aléatoirement et traversant l'écran</li><li>Une interaction au clavier fluide et bornée à la zone de jeu</li></ul>",
        "proj-pingouin-realisation": "<p>Le pingouin (représenté par un SVG) se déplace de 30 pixels vers le haut ou vers le bas à chaque pression sur les touches flèches, avec une zone de déplacement limitée pour qu'il reste dans le bassin. En parallèle, un poisson est généré toutes les 500 millisecondes à une hauteur aléatoire, traverse l'écran grâce à une animation CSS, puis est automatiquement retiré du DOM après 2 secondes pour éviter toute accumulation d'éléments.</p>",
        "proj-pingouin-role": "<p>J'ai conçu l'ensemble du jeu : la mise en page de la scène en HTML/CSS, l'intégration des éléments graphiques en SVG (pingouin, poissons, eau), et la logique JavaScript de déplacement, de génération aléatoire et de nettoyage des éléments.</p>",
        "proj-pingouin-resultats": "<p>Le résultat est un mini-jeu fluide et amusant, qui m'a permis de manipuler en profondeur le DOM, les événements clavier, les animations CSS et la gestion du cycle de vie d'éléments générés dynamiquement.</p>",
        "proj-pingouin-bilan": "<p>La principale difficulté a été de gérer le cycle de vie des poissons générés dynamiquement : sans nettoyage, les éléments créés toutes les 500 millisecondes s'accumulaient dans le DOM et finissaient par ralentir la page. Il a aussi fallu ajuster les animations CSS et les déplacements au clavier pour que le jeu reste fluide et que le pingouin ne sorte pas de sa zone de déplacement.</p><p>Ce petit projet m'a permis de vraiment comprendre la manipulation du DOM en temps réel et l'importance de penser à la performance, même sur un projet simple.</p>",

        // Projet : SérendIA
        "proj-serendia-title": "SérendIA",
        "proj-serendia-desc": "Application mobile Flutter de recommandation de voyage, développée en groupe de 7, avec moteur de recommandation vectoriel et mini-jeu de swipe pour affiner les suggestions.",
        "proj-serendia-tagline": "Une application mobile Flutter qui recommande des destinations de voyage personnalisées grâce à un moteur de recommandation basé sur un profil vectoriel.",
        "proj-serendia-context": "<p>SérendIA est une application développée dans le cadre d'une SAÉ de troisième année de BUT, en équipe de 7 personnes. Le projet visait à concevoir une application de recommandation de destinations de voyage, capable de s'adapter aux préférences de chaque utilisateur au fil de ses interactions.</p>",
        "proj-serendia-objectifs": "<p>Le projet s'est déroulé en plusieurs phases :</p><ul><li><strong>Phase 1 — Fondations &amp; données</strong> : mise en place de l'architecture de l'application et préparation des jeux de données de destinations</li><li><strong>Phase 2 — Moteur de recommandation V1</strong> : conception d'un premier algorithme de recommandation basé sur les préférences utilisateur</li><li><strong>Phase 3 — Moteur amélioré &amp; expérience utilisateur</strong> : affinement du moteur de recommandation et amélioration de l'interface et des interactions</li></ul>",
        "proj-serendia-realisation": "<p>Chaque utilisateur est représenté par un <code>UserProfileVector</code>, un vecteur de préférences sur plusieurs axes (Culture, Aventure, Détente, Budget). Les destinations sont comparées à ce profil grâce à une approche de <strong>« Soft Filtering »</strong> : plutôt que d'exclure strictement les destinations qui ne correspondent pas parfaitement au profil, elles sont simplement pénalisées dans le classement, ce qui permet de garder une diversité de suggestions.</p><p>Un <code>UserInteractionService</code> met à jour ce profil en continu à partir des retours de l'utilisateur, notamment via un mini-jeu de swipe permettant de noter cinq destinations proposées. Les données sont stockées localement dans une base <strong>SQLite</strong> (via le package <code>sqflite</code>), et des scripts Python (<code>check_db.py</code>, <code>jsonl_to_csv.py</code>) ont été utilisés pour préparer et vérifier les jeux de données de destinations.</p>",
        "proj-serendia-role": "<p>Au sein de cette équipe de 7, j'ai contribué au développement de l'application Flutter/Dart, notamment sur la logique de profil utilisateur et la préparation des données via les scripts Python, en collaboration étroite avec le reste de l'équipe pour intégrer ces éléments au moteur de recommandation.</p>",
        "proj-serendia-resultats": "<p>Le résultat est une application mobile fonctionnelle, capable de proposer des destinations personnalisées et de faire évoluer ses recommandations au fil des interactions de l'utilisateur. Ce projet m'a permis de travailler sur un développement mobile complet en équipe nombreuse, de la base de données locale jusqu'à l'interface utilisateur.</p>",
        "proj-serendia-bilan-title": "Bilan & difficultés (SAE S5)",
        "proj-serendia-bilan": "<p>Le plus dur dans ce projet n'a pas été la technique, mais le travail à sept : il a fallu se mettre d'accord sur l'utilité réelle de l'application, sur le design, et accepter des compromis pour que le résultat final convienne à tout le monde, ce qui a donné lieu à de grandes discussions, parfois animées. S'ajoutait à ça un problème très concret : nos emplois du temps respectifs ne se recoupaient pas toujours, ce qui rendait difficile de trouver des moments pour avancer ensemble.</p><p>Malgré ça, on a réussi à produire une application dont on est collectivement très fiers. Ce projet, mené sur le premier semestre de troisième année (S5), m'a appris à argumenter mes choix tout en sachant lâcher du lest sur certains points pour faire avancer le collectif, une compétence que je n'aurais pas pu développer sur un projet individuel.</p>",

        // Projet : Vélib'
        "proj-velib-title": "Vélib'",
        "proj-velib-desc": "Refonte complète de l'application Vélib', en groupe de 5, avec l'API officielle Vélib' Métropole : nouveau design et nouvelles fonctionnalités.",
        "proj-velib-tagline": "Une refonte complète de l'application Vélib', avec un nouveau design et de nouvelles fonctionnalités basées sur l'API officielle Vélib' Métropole.",
        "proj-velib-context": "<p>Dans le cadre d'un projet en équipe de 5, nous nous sommes inspirés de l'application officielle Vélib' pour en recréer entièrement notre propre version, en s'appuyant sur les API ouvertes de Vélib' Métropole pour récupérer les données en temps réel des stations.</p>",
        "proj-velib-objectifs": "<p>L'objectif n'était pas de simplement reproduire l'application existante, mais de la repenser :</p><ul><li>Revoir entièrement le design (couleurs, mise en page, expérience utilisateur)</li><li>Ajouter de nouvelles fonctionnalités absentes de l'application originale</li><li>Exploiter les données en temps réel de l'API Vélib' Métropole (disponibilité des vélos mécaniques et électriques, places libres, etc.)</li></ul>",
        "proj-velib-realisation": "<p>Nous avons conçu une nouvelle interface avec une identité visuelle propre, en travaillant sur la palette de couleurs, la lisibilité des informations et la navigation entre les écrans. Côté fonctionnalités, l'application récupère et affiche en temps réel l'état des stations (vélos disponibles, places libres, type de vélo) via l'API Vélib' Métropole, et propose de nouvelles fonctionnalités pensées par l'équipe pour améliorer l'expérience par rapport à l'application existante.</p>",
        "proj-velib-role": "<p>Au sein de cette équipe de 5, j'ai participé à la conception du nouveau design de l'application (charte graphique, écrans) ainsi qu'à l'intégration des données de l'API Vélib' Métropole dans l'interface.</p>",
        "proj-velib-resultats": "<p>Le résultat est une application repensée, à la fois plus agréable à utiliser et enrichie de nouvelles fonctionnalités, tout en s'appuyant sur des données réelles et à jour. Ce projet a été l'occasion de travailler en équipe sur l'ensemble du cycle d'un projet applicatif : conception, design, intégration d'API et développement.</p>",
        "proj-velib-bilan": "<p>La principale difficulté a été de concilier les visions de chacun sur le nouveau design : avec cinq personnes, il a fallu se mettre d'accord sur la charte graphique, l'organisation des écrans et les fonctionnalités à prioriser, ce qui a demandé plusieurs itérations et compromis. Sur la partie technique, l'intégration des données de l'API Vélib' Métropole en temps réel a aussi demandé un travail d'adaptation, notamment pour gérer les cas où certaines stations ne renvoyaient pas toutes les informations attendues.</p><p>Ce projet m'a appris à travailler en équipe sur un projet de design d'interface de bout en bout, et à faire dialoguer une maquette avec des données réelles parfois imprévisibles.</p>",

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
        "proj-watchout-bilan": "<p>La principale difficulté a été de garder une expérience cohérente entre les différentes scènes : il a fallu gérer les transitions, la position des indices cachés dans le décor et le minuteur de l'écran de code sans que le jeu ne devienne trop facile ou trop frustrant. Travailler seul sur tous les aspects (gameplay, graphismes, sons, ambiance) demandait aussi de nombreux allers-retours pour équilibrer l'ambiance horrifique sans que les apparitions ne deviennent répétitives ou prévisibles.</p><p>Ce projet, mon premier jeu complet, m'a appris à découper un développement en petites briques indépendantes (scènes, indices, minuteur, ambiance) pour avancer progressivement plutôt que de tout vouloir faire en même temps.</p>",
        "proj-voronoi-tagline": "Génération de diagrammes de Voronoï en Python à partir de l'algorithme de Fortune, avec export SVG et PNG.",
        "proj-voronoi-context": "<p>Ce projet s'inscrit dans une SAÉ de groupe portant sur les diagrammes de Voronoï, une structure de géométrie algorithmique utilisée pour partitionner un plan en régions à partir d'un ensemble de points. La SAÉ s'est déroulée en trois phases, dont une phase individuelle consacrée à l'utilisation de l'IA pour produire un générateur de diagrammes de Voronoï : c'est cette phase que je détaille ci-dessous.</p>",
        "proj-voronoi-objectifs": "<p>L'objectif de cette phase était d'obtenir, en travaillant avec l'IA DeepSeek, un générateur de diagrammes de Voronoï performant, capable de :</p><ul><li>Calculer un diagramme de Voronoï à partir d'un ensemble de points grâce à l'algorithme de Fortune (algorithme de balayage)</li><li>Représenter les cellules, sommets et arêtes du diagramme à l'aide de structures de données dédiées</li><li>Exporter le résultat sous forme d'image (SVG et PNG)</li></ul>",
        "proj-voronoi-realisation": "<p>En travaillant avec DeepSeek, j'ai obtenu une classe <code>FortuneAlgorithm</code>, héritant d'une classe générique <code>VoronoiGenerator</code>, qui met en œuvre l'algorithme de balayage de Fortune : une ligne de balayage horizontale parcourt le plan et construit progressivement le diagramme à partir des points fournis. Les éléments géométriques (points, arêtes) sont représentés par des classes dédiées <code>Point</code> et <code>Edge</code>, avec des fonctions utilitaires de géométrie regroupées dans <code>geometry_utils</code>.</p><p>Pour visualiser les résultats, des exporteurs dédiés permettent de générer le diagramme final au format SVG et PNG.</p>",
        "proj-voronoi-role": "<p>Cette phase du projet a été réalisée de manière individuelle au sein d'une SAÉ de groupe, en travaillant avec l'IA DeepSeek. Mon rôle a consisté à guider l'IA vers une solution correcte : formuler les demandes, tester le code produit, repérer les cas où le diagramme généré était incorrect, puis itérer avec l'IA jusqu'à obtenir une version fiable de l'algorithme de Fortune et des modules de géométrie et d'export associés, en m'appuyant sur les bases posées lors de la première phase du projet.</p>",
        "proj-voronoi-resultats": "<p>Le résultat est un générateur capable de produire des diagrammes de Voronoï corrects à partir de n'importe quel ensemble de points, exportables directement en SVG ou PNG. Ce projet m'a permis d'approfondir mes connaissances en géométrie algorithmique et en structures de données complexes, tout en prenant du recul sur ce qu'une IA générative comme DeepSeek peut produire (et sur ses limites) face à un même problème résolu « à la main » en phase 1.</p>",
        "proj-voronoi-bilan-title": "Bilan & difficultés (SAE S6)",
        "proj-voronoi-bilan": "<p>La principale difficulté de la phase 2 a été l'algorithme de Fortune lui-même : sa logique générale est simple à comprendre, mais sa mise en œuvre fait apparaître énormément de cas particuliers (points alignés, événements de cercle qui se déclenchent au même moment, cellules ouvertes sur les bords du plan...). Sans ces cas, l'algorithme produit un diagramme qui paraît correct au premier coup d'œil mais qui est en réalité faux ou incomplet sur certaines configurations de points. Avec DeepSeek, j'ai dû reprendre plusieurs fois les fonctions de géométrie pour fiabiliser ces cas limites, en gardant une trace des versions précédentes pour pouvoir comparer les résultats et m'assurer que je ne régressais pas.</p><p>Travailler seule sur cette phase, au sein d'une SAÉ de groupe menée sur le second semestre de troisième année (S6), m'a aussi obligé à être rigoureuse sur les tests : sans relecture immédiate par d'autres personnes, j'ai mis en place des tests unitaires sur les structures géométriques et l'algorithme pour détecter rapidement les régressions de l'IA. La comparaison avec la phase 1 (faite à la main, en équipe) a été révélatrice : DeepSeek allait très vite sur la structure générale du code, mais c'est sur les détails géométriques fins que mon rôle de relecture et de test a fait la différence. Cette double expérience, diagramme à la main, puis diagramme avec IA, a aussi nourri ma réflexion pour la phase 3, sur les conséquences de l'IA pour les personnes qui travaillent avec elle.</p>"
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

// Initialiser la traduction lorsque le DOM est chargé
document.addEventListener('DOMContentLoaded', function() {
    changeLanguage('fr');
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
        fr: { name: 'France', home: true,
            story: '<p>C\'est ici que j\'habite, entre mes études, mes projets et... mes valises toujours prêtes pour la prochaine destination !</p>',
            photos: [] },
        jp: { name: 'Japon',
            story: '<p>Je suis allée au Japon à deux reprises. La première fois, c\'était en 2018, avec ma mère, alors que j\'étais encore assez jeune.</p><p>La seconde fois, en 2025, j\'y suis retournée pendant trois semaines avec mon copain, pour redécouvrir le pays autrement, à deux.</p>',
            photos: [] },
        kr: { name: 'Corée du Sud',
            story: '<p>Juste après mon voyage au Japon, je suis partie 10 jours en Corée du Sud, en 2025, toute seule. Ce voyage a été un vrai déclic : c\'est cette expérience qui m\'a donné envie d\'y retourner, cette fois pour un an, dans le cadre de mon Programme Vacances Travail (PVT).</p><p>Un souvenir marquant : un après-midi près du palais de Gyeongbokgung, où j\'avais loué un hanbok pour la visite. En partant, une famille étrangère m\'a demandé de prendre une photo avec moi, ce qui était assez inattendu et amusant. Mais ce qui m\'a le plus touchée, c\'est qu\'une vieille dame coréenne m\'a arrêtée dans la rue pour me dire que j\'étais jolie : un geste simple mais tellement sincère et chaleureux que ça m\'a vraiment émue.</p><p>Plus tard, en attendant un concert de rue, un vieil homme coréen s\'est assis à côté de moi et a essayé de me parler en coréen. Je ne comprenais rien, et on a tenté de communiquer via une application de traduction, avec beaucoup de bonne volonté et de confusion. Un journaliste qui couvrait le concert a remarqué la scène et est venu m\'aider en anglais : il m\'a expliqué que les personnes âgées coréennes abordent parfois les étrangers avec des questions très directes sur le mariage ou la famille, par simple curiosité culturelle et sans aucune mauvaise intention. Cette explication a complètement changé ma perception de cet échange.</p>',
            photos: [] },
        kh: { name: 'Cambodge',
            story: '<p>Ce voyage au Cambodge s\'est fait dans le cadre d\'une colonie de vacances qui m\'a permis de visiter trois pays d\'Asie du Sud-Est : le Cambodge, le Vietnam et la Thaïlande. J\'y ai rencontré des personnes adorables et j\'ai passé environ trois semaines sur place.</p>',
            photos: [] },
        vn: { name: 'Vietnam',
            story: '<p>Le Vietnam faisait partie d\'un voyage en colonie de vacances qui m\'a permis de visiter trois pays d\'Asie du Sud-Est : le Cambodge, le Vietnam et la Thaïlande. J\'y ai rencontré des personnes adorables et j\'ai passé environ trois semaines sur place.</p>',
            photos: [] },
        th: { name: 'Thaïlande',
            story: '<p>La Thaïlande faisait partie d\'un voyage en colonie de vacances qui m\'a permis de visiter trois pays d\'Asie du Sud-Est : le Cambodge, le Vietnam et la Thaïlande. J\'y ai rencontré des personnes adorables et j\'ai passé environ trois semaines sur place.</p>',
            photos: [] },
        za: { name: 'Afrique du Sud',
            story: '<p>Mon tout premier voyage à l\'étranger ! J\'avais six ans et c\'est ma mère qui m\'y a emmenée. J\'en garde deux souvenirs assez flous mais marquants : avoir joué avec un lionceau dans un enclos rempli de tortues, et avoir été maquillée par des femmes typiques du pays. Une expérience magnifique.</p>',
            photos: [] },
        hr: { name: 'Croatie',
            story: '<p>Une semaine en Croatie avec mon copain, en 2024. Nous avons profité de la côte et du pays, puis avons fait un détour de deux jours en Bosnie.</p>',
            photos: [] },
        ba: { name: 'Bosnie',
            story: '<p>Pendant notre semaine en Croatie en 2024, mon copain et moi avons fait un détour de deux jours en Bosnie pour découvrir le pays.</p>',
            photos: [] },
        fi: { name: 'Finlande',
            story: '<p>Ce voyage en Finlande s\'est fait dans le cadre d\'une colonie de vacances. Au programme : pêche, observation des aurores boréales, construction d\'igloos... et même un « permis » de conduite de rennes obtenu lors d\'une balade tirée par ces animaux !</p>',
            photos: [] },
        de: { name: 'Allemagne',
            story: '<p>J\'ai pu visiter un peu la ville, mais mes voyages en Allemagne sont surtout liés aux parcs d\'attractions : Europa Park, Phantasialand et le parc aquatique Rulantica.</p>',
            photos: [] },
        pl: { name: 'Pologne',
            story: '<p>En janvier 2026, mon copain m\'a fait la surprise d\'une escapade en Pologne, pour découvrir un peu ce pays que je ne connaissais pas encore.</p>',
            photos: [] },
        be: { name: 'Belgique',
            story: '<p>Un peu comme pour la Pologne, mon copain m\'a fait la surprise d\'une escapade en Belgique, en 2025, pour découvrir le pays.</p>',
            photos: [] },
        gb: { name: 'Angleterre',
            story: '<p>Ce voyage en Angleterre s\'est fait dans le cadre d\'une colonie de vacances. Au programme : la visite du musée Harry Potter (Warner Bros. Studio Tour) et quelques-uns des sites touristiques les plus connus du pays.</p>',
            photos: [] },
        ie: { name: 'Irlande',
            story: '<p>Une semaine en Irlande avec mon copain, en 2025, principalement consacrée à la visite touristique du pays.</p>',
            photos: [] },
        us: { name: 'États-Unis',
            story: '<p>Je suis allée aux États-Unis à trois reprises. La première fois, pour le Nouvel An 2014, à New York avec ma mère. La deuxième fois, en colonie de vacances, toujours à New York, où j\'ai pu participer au défilé d\'Halloween déguisée. La troisième fois, encore en colonie de vacances, pour découvrir une grande partie de la côte Ouest : Las Vegas, Los Angeles, San Francisco, ainsi que plusieurs parcs nationaux.</p>',
            photos: [] },
        mx: { name: 'Mexique',
            story: '<p>Je suis allée à Cancún avec ma mère, en 2021 ou 2022, pour quelques jours. Nous avons visité de très beaux parcs naturels et découvert la culture mexicaine.</p>',
            photos: [] },
        es: { name: 'Espagne',
            story: '<p>Je suis allée en Espagne deux ou trois fois : une première fois en colonie de vacances avec une amie d\'enfance, puis deux autres fois avec mes parents et des amis, pour profiter du pays tous ensemble.</p>',
            photos: [] },
        cn: { name: 'Chine',
            story: '<p>Avec ma mère, j\'ai pu découvrir Pékin et Shanghai : marchés, palais et sites touristiques les plus connus étaient au programme.</p>',
            photos: [] },
        nl: { name: 'Pays-Bas',
            story: '<p>Avec ma mère, je suis allée aux Pays-Bas pour rendre visite à une amie qui nous a accueillies. Nous y sommes restées quelques jours pour visiter les environs.</p>',
            photos: [] },
        sg: { name: 'Singapour',
            story: '<p>Avec ma mère, j\'ai passé une petite semaine à Singapour, à découvrir la ville. Je l\'ai trouvée magnifique : très belle, très attirante, avec un environnement tout simplement incroyable. J\'ai adoré cet endroit.</p>',
            photos: [] },
        hk: { name: 'Hong Kong',
            story: '<p>Je suis allée à Hong Kong à deux reprises : une première fois avec ma mère, puis une seconde fois avec mon père. À chaque fois, nous avons visité les sites touristiques les plus connus et découvert la vie sur place.</p>',
            photos: [] },
        re: { name: 'La Réunion',
            story: '<p>Je suis allée à La Réunion avec mon père, pour le mariage d\'amis à lui. C\'était un très joli voyage, et j\'ai hâte de pouvoir y retourner.</p>',
            photos: [] },
        mu: { name: 'Île Maurice',
            story: '<p>J\'ai visité l\'Île Maurice une fois, quand j\'étais très jeune, avec ma mère. Une expérience tout aussi chouette que mes autres voyages.</p>',
            photos: [] }
    };

    const tooltip = document.createElement('div');
    tooltip.id = 'map-tooltip';
    document.body.appendChild(tooltip);

    function showTooltip(data, event) {
        const t = translations.fr;
        const label = data.home ? t['travel-home'] : t['travel-soon'];
        tooltip.innerHTML = '<span>' + data.name + ' — ' + label + '</span>';
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
        const t = translations.fr;
        travelModal.querySelector('.travel-modal-title').textContent = data.name;
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
        const data = visitedCountries[el.dataset.cc] || { name: el.dataset.name };
        el.addEventListener('mouseenter', e => showTooltip(data, e));
        el.addEventListener('mousemove', moveTooltip);
        el.addEventListener('mouseleave', hideTooltip);
        el.addEventListener('click', () => openTravelModal(data));
    });
});
  