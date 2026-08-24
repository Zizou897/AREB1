# Design

## Theme

Sombre premium « atelier nocturne » : fond bleu-noir profond (#07070D → #0A0A0F), surfaces légèrement teintées, lueur violette→cyan réservée aux moments IA (mot-clé du hero, badges outils IA, offre signature). Le reste du site est tenu par la typographie et la grille — la couleur est un événement, pas un fond sonore.

## Color

Stratégie : **Committed** — le bleu-noir porte 90 % de la surface, l'accent dégradé violet→cyan est un marqueur sémantique (= IA / signature), jamais décoratif au hasard.

| Token | Valeur | Usage |
|---|---|---|
| `--bg` | oklch(0.13 0.012 285) ≈ #0A0A12 | fond de page |
| `--bg-deep` | oklch(0.10 0.010 285) ≈ #07070D | bandes alternées, footer |
| `--surface` | oklch(0.17 0.014 285) ≈ #12121C | cards |
| `--surface-2` | oklch(0.21 0.016 285) | hover cards, inputs |
| `--line` | oklch(0.28 0.02 285 / 0.6) | bordures 1px |
| `--ink` | oklch(0.96 0.005 285) ≈ #F2F2F7 | titres |
| `--ink-body` | oklch(0.80 0.01 285) ≈ #C4C4D4 | corps (contraste ≥ 7:1) |
| `--ink-mute` | oklch(0.66 0.015 285) | légendes (≥ 4.5:1) |
| `--violet` | oklch(0.62 0.23 295) ≈ #8B5CF6 | départ dégradé |
| `--cyan` | oklch(0.80 0.14 210) ≈ #22D3EE | fin dégradé |
| `--accent` | var(--cyan) | liens, focus, états actifs |

## Typography

- **Display** : Space Grotesk 500/700 (choix client) — titres, chiffres clés. Letter-spacing ≥ −0.03em, clamp() max 4.5rem.
- **Body** : Inter 400/500 (choix client) — 16px min, line-height 1.65 (fond sombre), max 70ch.
- **Mono** : JetBrains Mono 400 — labels techniques, badges stack, prix. C'est le registre « ingénieur » assumé (portfolio dev = mono légitime).
- Échelle : 13 / 15 / 16 / 18 / 22 / 28 / 36 / clamp(2.4rem→4.5rem).

## Components

- **Nav sticky** : fond `--bg/85` + blur léger uniquement au scroll, lien actif souligné cyan.
- **Cards projet** : screenshot 16:10, zoom 1.04 + overlay au hover, badges stack en mono, bordure `--line` (jamais de side-stripe).
- **Pricing** : 3 cards, Pack Combo avec bordure dégradé (padding-box/border-box) + badge « Offre la plus demandée ».
- **Formulaire** : labels visibles au-dessus, erreurs sous le champ, hauteur inputs ≥ 48px, succès = remplacement HTMX.
- **Boutons** : primaire = dégradé violet→cyan plein, secondaire = ghost bordure `--line`; scale 0.98 au press.

## Motion

- Reveal au scroll via IntersectionObserver : translateY(16px)+fade 500ms ease-out-quart, stagger 60ms dans les grilles. Contenu visible par défaut (JS ajoute la classe de départ) — jamais de section vide sans JS.
- Mot-clé hero : dégradé animé (background-position 6s ease-in-out infinite).
- `prefers-reduced-motion: reduce` → tout en crossfade instantané.
- HTMX swaps : fade 200ms via `.htmx-swapping`.

## Layout

- Container max-w-6xl, gouttières fluides clamp(1rem→3rem).
- Sections : rythme vertical varié (hero plein viewport, métriques serrées, projets généreux).
- Grilles : `repeat(auto-fit, minmax(280px, 1fr))` pour projets/pricing.
- Pas d'eyebrow uppercase répété : les titres de section portent seuls la hiérarchie, ponctués d'un glyphe mono (`//`) propre au registre dev — un seul système, assumé.
