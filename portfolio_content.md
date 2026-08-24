# CONTENU COMPLET DU PORTFOLIO — Azeez
> Stack : Django + HTMX | Objectif : décrocher des clients freelance
> À transmettre tel quel à Claude Code pour la génération du projet.

---

## INSTRUCTIONS POUR CLAUDE CODE

Construire un portfolio freelance avec Django (backend) + HTMX (frontend dynamique).
- Pas de framework JS (pas de React, Vue, Next.js)
- HTMX pour les interactions (filtres projets, formulaire contact, onglets)
- TailwindCSS pour le style
- SQLite en développement, PostgreSQL en production
- Déploiement cible : Railway ou Render

---

## STRUCTURE DU PROJET DJANGO

```
portfolio/
├── core/           # Hero, À propos, page d'accueil
├── projects/       # Projets dev + vidéos IA (avec filtre HTMX)
├── services/       # Offres et tarification
├── testimonials/   # Témoignages clients
├── contact/        # Formulaire HTMX (envoi sans rechargement)
├── templates/
│   ├── base.html
│   ├── components/  # partials HTMX (nav, cards, footer)
│   └── pages/
└── static/
    ├── css/
    └── js/          # htmx.min.js uniquement
```

---

## SECTION 1 — HERO

### Titre principal
```
Je crée des applications web performantes
et des vidéos publicitaires IA qui convertissent.
```

### Sous-titre / tagline
```
Développeur Python · Django · FastAPI — 5 ans d'expérience
+ Concepteur de vidéos publicitaires avec les outils IA dernière génération
```

### Description courte (Hero body)
```
Vous avez besoin d'une app web robuste, d'une API sur-mesure
ou d'une vidéo publicitaire percutante générée par IA ?
Je suis le freelance qui réunit les deux — sans que vous ayez
à gérer plusieurs prestataires.
```

### Boutons CTA Hero
- Bouton primaire : `Voir mes projets` → ancre `#projets`
- Bouton secondaire : `Me contacter` → ancre `#contact`

### Métriques clés (bandeau sous le Hero)
| Métrique | Valeur |
|---|---|
| Années d'expérience | 5 ans |
| Projets livrés | 10+ |
| Technologies maîtrisées | 8+ |
| Clients satisfaits | 15+ |

---

## SECTION 2 — PROJETS WEB (Django app: `projects`)

### Modèle de données suggéré
```python
class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Développement web'),
        ('video', 'Vidéo IA publicitaire'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    description = models.TextField()
    problem = models.TextField()       # Problème client résolu
    solution = models.TextField()      # Solution apportée
    result = models.TextField()        # Résultat mesurable
    stack = models.JSONField()         # ["Django", "PostgreSQL", ...]
    live_url = models.URLField(blank=True)
    video_url = models.URLField(blank=True)  # Pour les vidéos IA
    thumbnail = models.ImageField(upload_to='projects/')
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Filtre HTMX (onglets Tous / Dev Web / Vidéo IA)
```html
<!-- Exemple de filtre HTMX -->
<div class="filters">
  <button hx-get="/projects/?category=all"
          hx-target="#projects-grid"
          hx-swap="innerHTML">Tous</button>
  <button hx-get="/projects/?category=web"
          hx-target="#projects-grid"
          hx-swap="innerHTML">Dev Web</button>
  <button hx-get="/projects/?category=video"
          hx-target="#projects-grid"
          hx-swap="innerHTML">Vidéo IA</button>
</div>
<div id="projects-grid">
  {% include "components/projects_grid.html" %}
</div>
```

### Projet 1 — CTAMS
```yaml
title: CTAMS — Système de gestion associative
category: web
url: https://www.ctams.net
description: >
  Plateforme web complète de gestion pour organisations et associations.
  Gestion des membres, des cotisations, des événements et des rapports.
problem: >
  Les associations géraient leurs données sur Excel, sans centralisation
  ni accès multi-utilisateurs, ce qui causait des erreurs et des pertes de données.
solution: >
  Développement d'une application Django full-featured avec authentification
  multi-rôles, tableau de bord en temps réel, gestion des cotisations
  et export de rapports PDF.
result: >
  Adoption par plusieurs associations. Réduction du temps de gestion
  administrative de 60%. Accès centralisé pour tous les membres depuis n'importe quel appareil.
stack:
  - Python
  - Django
  - PostgreSQL
  - Bootstrap
  - JavaScript
```

### Projet 2 — MonApplideGestion (.online)
```yaml
title: MonApplideGestion — Application de gestion PME
category: web
url: https://monapplidegestion.online
description: >
  Application SaaS de gestion commerciale pour PME africaines.
  Gestion des ventes, stocks, clients et facturation.
problem: >
  Les PME locales n'avaient pas accès à des outils de gestion adaptés
  à leur contexte (multi-devises, faible bande passante) et abordables.
solution: >
  Développement d'une app Django légère et responsive, optimisée pour
  les connexions lentes, avec gestion des devis, factures, stocks et clients.
result: >
  Outil utilisé activement par des PME de la région.
  Interface rapide même sur réseau mobile 3G.
stack:
  - Python
  - Django
  - SQLite / PostgreSQL
  - HTMX
  - TailwindCSS
```

### Projet 3 — MonApplideGestion (.net)
```yaml
title: MonApplideGestion — Version entreprise
category: web
url: https://monapplidegestion.net
description: >
  Version étendue de l'application de gestion, avec des fonctionnalités
  avancées pour les entreprises : multi-utilisateurs, rôles, rapports avancés.
problem: >
  Les entreprises plus grandes avaient besoin de plus de contrôle :
  gestion d'équipe, audit trail, et tableaux de bord analytiques.
solution: >
  Extension de l'architecture Django avec API FastAPI pour les modules
  analytiques, système de rôles granulaire, et exports Excel/PDF automatisés.
result: >
  Déployé en production. Architecture scalable prête pour la montée en charge.
stack:
  - Python
  - Django
  - FastAPI
  - PostgreSQL
  - Chart.js
  - HTMX
```

---

## SECTION 3 — PROJETS VIDÉO IA

> **Note pour Claude Code** : Cette section affiche des vidéos embarquées (iframe YouTube/Vimeo).
> Les URLs de vidéos seront renseignées via l'interface d'administration Django.

### Contenu des cards vidéo (template)
Chaque card vidéo affiche :
- Miniature cliquable → ouvre la vidéo en modal HTMX
- Titre du projet
- Secteur (ex: e-commerce, restauration, immobilier…)
- Outils IA utilisés (badges)
- Courte description du brief

### Outils IA à afficher en badges
- Runway ML
- Kling AI
- ElevenLabs
- Sora
- Pika Labs
- Adobe Firefly
- CapCut AI

### Texte d'introduction de la section
```
Je conçois des vidéos publicitaires 100% générées par intelligence artificielle —
de la création des visuels à la voix off, en passant par le montage.
Résultat : des contenus professionnels, livrés rapidement,
à une fraction du coût d'une production traditionnelle.
```

---

## SECTION 4 — SERVICES & TARIFICATION

### Offre 1 — Pack Développement Web
```
Nom : Pack Dev Web
Sous-titre : Une application web sur-mesure, robuste et scalable

Inclus :
- Analyse des besoins et architecture
- Développement Django / FastAPI
- Interface responsive (HTMX + TailwindCSS)
- Connexion base de données (PostgreSQL)
- Déploiement et mise en ligne
- 1 mois de support inclus

Idéal pour : PME, associations, startups qui ont besoin d'un outil métier ou d'une plateforme web.

Délai : 2 à 6 semaines selon complexité
Tarif : À partir de 350 000 FCFA
```

### Offre 2 — Pack Vidéo IA Publicitaire
```
Nom : Pack Vidéo IA
Sous-titre : Une vidéo publicitaire professionnelle générée par IA

Inclus :
- Brief créatif et script
- Génération des visuels IA
- Voix off IA (multilingue possible)
- Montage et sous-titres
- 2 révisions incluses
- Livraison en HD (MP4)

Idéal pour : Lancement de produit, promotion e-commerce, réseaux sociaux, campagne digitale.

Délai : 3 à 7 jours
Tarif : À partir de 75 000 FCFA
```

### Offre 3 — Pack Combo (OFFRE SIGNATURE ⭐)
```
Nom : Pack Combo — Dev + Vidéo IA
Sous-titre : L'offre complète pour lancer votre présence digitale

Inclus :
- Application web ou landing page Django
- 2 vidéos publicitaires IA
- Intégration des vidéos dans le site
- Stratégie de contenu digital incluse
- Déploiement + support 1 mois
- Livraison clé en main

Idéal pour : Entrepreneurs et PME qui veulent lancer un produit avec un site ET du contenu vidéo percutant — sans gérer plusieurs prestataires.

Délai : 3 à 8 semaines
Tarif : À partir de 450 000 FCFA (économie vs offres séparées)

Badge à afficher : ⭐ Offre la plus demandée
```

### Texte sous les offres (réassurance)
```
Tous les projets démarrent par un appel gratuit de 30 minutes
pour cadrer vos besoins. Pas de surprise sur la facturation —
devis détaillé avant tout démarrage. Je réponds sous 24h.
```

---

## SECTION 5 — STACK & COMPÉTENCES

### Colonne 1 — Développement web
| Technologie | Niveau |
|---|---|
| Python | Expert |
| Django | Expert |
| FastAPI | Avancé |
| HTMX | Avancé |
| PostgreSQL | Avancé |
| API REST | Expert |
| TailwindCSS | Intermédiaire |
| Git / GitHub | Avancé |
| Linux / Déploiement | Intermédiaire |

### Colonne 2 — Vidéo & IA
| Outil | Usage |
|---|---|
| Runway ML | Génération vidéo IA |
| Kling AI | Animation et vidéo |
| ElevenLabs | Voix off IA |
| Sora | Génération vidéo |
| Pika Labs | Animation |
| CapCut AI | Montage assisté IA |
| Adobe Firefly | Visuels IA |

### Texte d'introduction de la section
```
5 ans à construire des applications web avec Python et Django,
et une maîtrise des outils IA génératifs les plus récents pour la vidéo.
Deux familles de compétences rares réunies en un seul freelance.
```

---

## SECTION 6 — TÉMOIGNAGES

### Modèle de données
```python
class Testimonial(models.Model):
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=150)  # ex: "Directeur, Entreprise X"
    content = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to='testimonials/', blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### Témoignage placeholder 1
```
Auteur : À renseigner via l'admin Django
Poste : Gérant, PME Abidjan
Texte : "Azeez a livré notre application dans les délais, exactement comme prévu.
Le résultat dépasse nos attentes — notre équipe a adopté l'outil en moins d'une semaine."
```

### Témoignage placeholder 2
```
Auteur : À renseigner via l'admin Django
Poste : Responsable marketing, startup tech
Texte : "La vidéo publicitaire IA qu'il a créée pour notre lancement a généré
un engagement exceptionnel sur nos réseaux. Qualité pro, délai express."
```

### Texte d'introduction de la section
```
Ce que disent ceux qui m'ont fait confiance
```

---

## SECTION 7 — CONTACT

### Formulaire (avec HTMX — envoi sans rechargement)
```html
<!-- Champs du formulaire -->
Prénom & Nom        → CharField
Email               → EmailField
Téléphone           → CharField (optionnel)
Type de besoin      → ChoiceField :
                        - Application web / API
                        - Vidéo publicitaire IA
                        - Pack Combo (Dev + Vidéo)
                        - Autre
Budget estimé       → ChoiceField :
                        - Moins de 100 000 FCFA
                        - 100 000 – 300 000 FCFA
                        - 300 000 – 600 000 FCFA
                        - 600 000 FCFA et plus
Message / Description du projet → TextField

Bouton : "Envoyer ma demande"
```

### Comportement HTMX du formulaire
```python
# Vue Django — réponse partielle après envoi
# hx-post="/contact/"
# hx-target="#contact-form"
# hx-swap="outerHTML"
# → Remplacer le formulaire par un message de succès
```

### Message de succès (partial HTMX)
```
✅ Message envoyé !
Merci [prénom], j'ai bien reçu votre demande.
Je vous réponds dans les 24h pour qu'on échange sur votre projet.
```

### Infos de contact directes
```
Email       : [à renseigner]
WhatsApp    : [à renseigner]
LinkedIn    : [à renseigner]
GitHub      : [à renseigner]
Localisation : Abidjan, Côte d'Ivoire
              (Disponible pour projets remote — monde entier)
```

---

## NAVIGATION

```
Logo / Nom → accueil
Projets    → #projets
Services   → #services
Compétences → #competences
Témoignages → #temoignages
Contact    → #contact (bouton CTA mis en avant)
```

---

## FOOTER

```
© 2025 [Nom] — Développeur Django & Concepteur Vidéo IA
Fait avec Django + HTMX 🇨🇮

Liens :
- LinkedIn
- GitHub
- Email
- Mentions légales (page simple)
```

---

## NOTES TECHNIQUES POUR CLAUDE CODE

1. **Admin Django** : Activer l'admin pour gérer projets, témoignages et messages de contact sans toucher au code.

2. **Envoi d'email** : Configurer `django.core.mail` avec SMTP (Gmail ou SendGrid) pour recevoir les messages du formulaire de contact.

3. **Médias** : Configurer `MEDIA_ROOT` et `MEDIA_URL` pour les images de projets et avatars.

4. **SEO** : Ajouter `<meta>` title/description dynamiques par page via les vues Django.

5. **Performance** :
   - Compresser les images avec Pillow
   - Servir les fichiers statiques avec WhiteNoise
   - Activer le cache Django sur les vues statiques

6. **Variables d'environnement** (.env) :
   ```
   SECRET_KEY=
   DEBUG=False
   DATABASE_URL=
   EMAIL_HOST_USER=
   EMAIL_HOST_PASSWORD=
   ALLOWED_HOSTS=
   ```

7. **Dépendances** (requirements.txt) :
   ```
   django>=4.2
   django-htmx
   whitenoise
   pillow
   python-decouple
   psycopg2-binary
   gunicorn
   ```

8. **Déploiement recommandé** : Railway (support Django natif, PostgreSQL inclus, déploiement via GitHub).
