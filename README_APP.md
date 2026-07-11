# README — ABD Content Automation App
## Application Web pour Mireille et ses filleuls

---

## POUR MIREILLE (VOUS) — DÉPLOIEMENT INITIAL

### Étape 1 : Créer un compte Streamlit Cloud (gratuit)
1. Aller sur https://share.streamlit.io
2. Créer un compte avec GitHub
3. Créer un nouveau repository GitHub (ex: `abd-content-app`)
4. Uploader tous les fichiers du projet dans ce repository

### Étape 2 : Déployer l'app
1. Sur Streamlit Cloud, cliquer sur "New app"
2. Sélectionner votre repository `abd-content-app`
3. Choisir le fichier principal : `app.py`
4. Cliquer sur "Deploy"
5. Streamlit Cloud va installer les dépendances automatiquement

### Étape 3 : Récupérer le lien
- Une fois déployée, vous obtenez un lien comme :
  `https://votre-nom-abd-content-app.streamlit.app`
- C'est CE lien que vous partagez à vos filleuls

### Étape 4 : Configurer les secrets (pour vous)
- Sur Streamlit Cloud, aller dans Settings → Secrets
- Ajouter votre clé OpenAI :
```toml
[secrets]
OPENAI_API_KEY = "sk-votre-cle-ici"
```
- Vos filleuls n'auront PAS accès à ces secrets

---

## POUR VOS FILLEULS — UTILISATION

### Ce que vos filleuls voient :
1. Ils ouvrent le lien dans leur navigateur (Chrome, Safari, etc.)
2. Ils voient un formulaire avec 4 étapes :
   - **Étape 1** : Leur prénom, nom, rôle dans ABD
   - **Étape 2** : Leur clé API OpenAI (obligatoire)
   - **Étape 3** : Leurs identifiants Facebook/TikTok/WhatsApp (optionnel)
   - **Étape 4** : Upload de leur photo
3. Ils cliquent sur "Générer le contenu"
4. Le système génère le texte + l'image automatiquement
5. Ils peuvent prévisualiser, télécharger, ou publier directement

### Ce que vos filleuls NE voient PAS :
- ❌ Le code Python
- ❌ Les prompts système (cachés dans content_engine.py)
- ❌ Vos secrets et clés API
- ❌ La structure technique du projet

### Ce que vos filleuls doivent avoir :
- Une clé API OpenAI (obligatoire — ~10-20$/mois)
- Une photo d'eux-mêmes (optionnel mais recommandé)
- Des identifiants Facebook/TikTok/WhatsApp (optionnel pour publication auto)

---

## FONCTIONNALITÉS DE L'APP

### Onglet "Calendrier"
- Vue d'ensemble de la stratégie de contenu hebdomadaire
- Les 5 piliers de contenu ABD
- Répartition par jour et par réseau social

### Onglet "Générer"
- Choisir le jour, le réseau social et le pilier
- Option de recherche web de tendances
- Génération automatique du texte + image
- Prévisualisation avant publication
- Publication directe sur Facebook (si configuré)
- Notification WhatsApp pour statut (à poster manuellement)
- Enregistrement dans le fichier de suivi Excel

### Onglet "Suivi"
- Tableau de bord de tous les posts générés
- Statistiques (total, publiés, par réseau)
- Téléchargement du fichier Excel

### Onglet "Paramètres"
- Couleurs ABD
- Hashtags par défaut
- Fréquence de publication

---

## DÉPANNAGE

| Problème | Solution |
|----------|----------|
| L'app ne se charge pas | Vérifier que le repository GitHub est public |
| "Erreur OpenAI" | Vérifier la clé API OpenAI |
| "Image non générée" | Vérifier le crédit OpenAI (DALL-E) |
| "Facebook non configuré" | Remplir Page ID et Access Token dans l'étape 3 |
| L'app est lente | Normal — la génération d'images prend 10-20 secondes |

---

## COÛTS

| Service | Coût |
|---------|------|
| Streamlit Cloud | Gratuit (1 app publique) |
| OpenAI API | ~10-20$/mois par utilisateur |
| Facebook Graph API | Gratuit |
| TikTok API | Gratuit |
| WhatsApp Cloud API | Gratuit |
| **Total par filleul** | **10-20$/mois** |

---

## FICHIERS DU PROJET

| Fichier | Rôle | Visible par filleuls ? |
|---------|------|----------------------|
| `app.py` | Interface principale | Non (derrière l'app) |
| `content_engine.py` | Moteur de contenu + prompts | Non (derrière l'app) |
| `image_engine.py` | Génération d'images | Non (derrière l'app) |
| `publisher.py` | Publication réseaux sociaux | Non (derrière l'app) |
| `excel_logger.py` | Suivi Excel | Non (derrière l'app) |
| `requirements_app.txt` | Dépendances | Non (installé automatiquement) |

---

*ABD Content Automation — Académie des Bâtisseurs Digitaux*
*Découvrir. Construire. Créer. Diriger. Inspirer.*
