# Portfolio — Azeez · Développeur Django & Concepteur Vidéo IA

Portfolio freelance one-page construit avec **Django 5+ / HTMX / TailwindCSS**.
Design sombre premium, filtres de projets sans rechargement, formulaire de
contact asynchrone, admin Django pour tout gérer sans toucher au code.

## Stack

- **Backend** : Django, django-htmx, python-decouple
- **Frontend** : TailwindCSS (CDN), HTMX (vendored dans `static/js/`), vanilla JS (IntersectionObserver)
- **Base de données** : SQLite en dev, PostgreSQL en production (`DATABASE_URL`)
- **Statiques** : WhiteNoise (compression + cache busting en prod)
- **Captures** : Playwright + Pillow (`capture_screenshots.py`)

## Installation locale

```bash
git clone <repo>
cd AREB1
python -m venv .venv
.venv\Scripts\activate        # Windows — source .venv/bin/activate sur Linux/Mac
pip install -r requirements.txt

copy .env.example .env         # puis remplir les valeurs
python manage.py migrate       # crée la base ET pré-remplit les 3 projets + 2 témoignages
python manage.py createsuperuser
python manage.py runserver
```

Le site est sur `http://127.0.0.1:8000/`, l'admin sur `/admin/`.

## Gérer le contenu (admin Django)

| Contenu | Où |
|---|---|
| Projets (dev web & vidéos IA) | Admin → Projets |
| Témoignages | Admin → Témoignages |
| Messages reçus du formulaire | Admin → Messages de contact (lecture seule + case « traité ») |
| Compétences | `core/data.py` (éditorial, versionné dans git) |
| Coordonnées (email, WhatsApp…) | `.env` → `CONTACT_*` |

### Ajouter un projet vidéo IA

1. Admin → Projets → Ajouter
2. Catégorie = « Vidéo IA publicitaire », renseigner **Secteur** (ex. e-commerce)
3. Coller l'URL YouTube/Vimeo dans **URL de la vidéo** (le lien watch classique suffit,
   la conversion en embed est automatique)
4. Uploader une miniature — elle s'affiche dans la grille, la vidéo s'ouvre en modal
5. **Stack / Outils** : liste JSON des outils IA, ex. `["Runway ML", "ElevenLabs"]`

## Recapturer les screenshots des sites

```bash
pip install playwright && playwright install chromium
python capture_screenshots.py
```

Les captures vont dans `static/img/projects/` (PNG + WebP optimisés).
Pour les rebrancher sur les projets existants, mettre à jour la miniature via l'admin.

## Déploiement sur Railway

1. Pousser le repo sur GitHub, puis sur [railway.app](https://railway.app) : **New Project → Deploy from GitHub**
2. Ajouter un service **PostgreSQL** (Railway injecte `DATABASE_URL` automatiquement)
3. Variables d'environnement à définir :
   - `SECRET_KEY` (long et aléatoire), `DEBUG=False`
   - `ALLOWED_HOSTS=votre-domaine.up.railway.app` (puis votre domaine custom)
   - `EMAIL_*` et `CONTACT_*` (voir `.env.example`)
4. Commandes :
   - Build : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start : `python manage.py migrate && gunicorn config.wsgi`
5. Générer un domaine dans Settings → Networking, l'ajouter à `ALLOWED_HOSTS`

Le déploiement Render est identique (Web Service + PostgreSQL, mêmes commandes).

## Structure

```
├── config/          # settings, urls, wsgi
├── core/            # page d'accueil one-page, compétences (core/data.py), mentions légales, 404
├── projects/        # modèle Project + filtre & modal HTMX + seed migration
├── testimonials/    # témoignages + seed migration
├── contact/         # formulaire HTMX + stockage + notification email
├── templates/
│   ├── base.html    # SEO, fonts, tokens Tailwind
│   ├── components/  # navbar, footer, cards, modal, formulaire (partials HTMX)
│   └── pages/       # home, mentions légales
├── static/          # css/custom.css, js/main.js, js/htmx.min.js, img/
└── capture_screenshots.py
```
