# content_engine.py — Moteur de création de contenu ABD
# Version Gemini (Google AI Studio — API gratuite)
# Ce module contient les prompts système cachés derrière l'interface

import google.generativeai as genai
import json
import os
import requests
from datetime import datetime

class ContentEngine:
    """Moteur de création de contenu pour ABD avec Google Gemini"""
    
    # Prompt système caché — les filleuls ne voient jamais ce prompt
    SYSTEM_PROMPT = """Tu es un expert en création de contenu pour la communauté ABD (Académie des Bâtisseurs Digitaux).
    
    CONTEXTE ABD :
    ABD est une communauté qui aide les personnes fatiguées de leur situation financière à créer une source de revenu
    par le digital et l'IA. ABD s'appuie sur une entreprise partenaire YUPI Global (compléments alimentaires de santé)
    comme moteur économique. Le système ABD donne à ses membres des outils IA (Agents IA, tunnels de vente, branding)
    pour éviter le démarchage traditionnel. C'est un business clé en main propulsé par l'IA.
    
    CIBLE :
    - Âge : 22-45 ans, Afrique francophone
    - Profil : salarié fatigué, chômeur motivé, étudiant ambitieux, entrepreneur qui stagne
    - Douleur : situation financière difficile, peur du MLM traditionnel, manque de compétences
    - Désir : système clé en main, sans gros budget, sans démarcher
    
    RÈGLES STRICTES :
    - JAMAIS promettre des revenus ou des résultats garantis
    - JAMAIS mentionner "MLM" ou "marketing de réseau" directement dans les posts sociaux
    - JAMAIS faire du démarchage agressif
    - JAMAIS utiliser un ton "gourou" ou "get rich quick"
    - Toujours utiliser le tutoiement
    - Ton : chaleureux, authentique, motivant, pas vendeur
    - Couleurs ABD : VERT (#00C853), BLANC, VIOLET (#6B2FB5)
    
    LES 5 PILIERS DE CONTENU :
    1. Éducation IA & Digital (30%) : Tutoriels, astuces, tendances IA
    2. Motivation & Transformation (25%) : Stories, citations, mentalité entrepreneur
    3. Communauté & Entraide (20%) : Témoignages, live coaching, entraide
    4. Santé & Bien-être (15%) : Conseils santé, énergie du bâtisseur
    5. Challenge & Action (10%) : Annonces Challenge 5 jours, CTA doux
    
    L'HISTOIRE DE KOFFI (à utiliser comme inspiration) :
    Koffi avait 32 ans. Salarié. Fatigué. Il n'y connaissait rien au digital ni à l'IA.
    Il a démarré avec le Challenge gratuit. En 5 jours, il a mis en place son système.
    Aujourd'hui, Koffi est un leader digital. Il forme d'autres personnes.
    
    LE CHALLENGE 5 JOURS :
    - Jour 0 : Bienvenue & Motivation
    - Jour 1 : Boîte à outils
    - Jour 2 : Tunnel de vente Santé
    - Jour 3 : Branding, photoshoot IA, réseaux sociaux
    - Jour 4 : Agent IA et closing WhatsApp
    - Jour 5 : 1er post sur Facebook
    """
    
    def __init__(self, api_key, user_prenom, user_role, user_bio):
        """Initialise le moteur de contenu avec Gemini"""
        genai.configure(api_key=api_key)
        self.user_prenom = user_prenom
        self.user_role = user_role
        self.user_bio = user_bio
        self.model_name = self._find_available_model()
    
    def _find_available_model(self):
        """Trouve un modèle Gemini disponible"""
        models_to_try = [
            'gemini-2.0-flash',
            'gemini-2.0-flash-lite',
            'gemini-1.5-flash',
            'gemini-1.5-flash-8b',
            'gemini-1.5-pro',
        ]
        try:
            available = [m.name for m in genai.list_models()]
            for model in models_to_try:
                full_name = f'models/{model}'
                if full_name in available:
                    return model
            # Si aucun trouvé, retourner le premier de la liste
            return models_to_try[0]
        except:
            return models_to_try[0]
    
    def research_trends(self):
        """Recherche les tendances actuelles sur le web"""
        try:
            model = genai.GenerativeModel(self.model_name)
            
            prompt = """Identifie 5 sujets tendance actuels pour créer du contenu 
            sur les réseaux sociaux en Afrique francophone autour de ces thématiques :
            1. Intelligence Artificielle et outils IA
            2. Entrepreneuriat en ligne et digital
            3. Développement personnel et motivation
            4. Santé et bien-être
            5. Communauté et entraide
            
            Pour chaque sujet, donne :
            - sujet : le sujet en 1 phrase
            - angle : l'angle de contenu suggéré
            - format_recommande : Facebook / TikTok / WhatsApp
            
            Réponds en JSON avec une liste 'tendances'."""
            
            response = model.generate_content(prompt)
            text = response.text
            
            # Essayer de parser le JSON
            try:
                # Trouver le JSON dans la réponse
                start = text.find('{')
                end = text.rfind('}') + 1
                if start != -1 and end != -1:
                    json_str = text[start:end]
                    result = json.loads(json_str)
                    return result.get('tendances', [])
            except:
                pass
            
            return []
            
        except Exception as e:
            print(f"Erreur recherche tendances : {e}")
            return []
    
    def generate_content(self, jour, reseau, pilier, sujet_custom=None, faire_recherche=True):
        """Génère le contenu pour un post"""
        
        # Recherche de tendances si demandé
        tendances = []
        if faire_recherche:
            tendances = self.research_trends()
        
        # Construire le prompt utilisateur
        if sujet_custom:
            sujet = sujet_custom
        else:
            # Déterminer le sujet selon le pilier et le jour
            sujets_par_pilier = {
                "Éducation IA & Digital": [
                    "3 façons d'utiliser ChatGPT pour ton business (même si tu débutes)",
                    "Comment l'IA crée ton contenu en 2 minutes",
                    "L'IA en Afrique : les opportunités que personne ne voit",
                    "Comment automatiser ton WhatsApp avec l'IA",
                    "Outil IA gratuit du jour",
                ],
                "Motivation & Transformation": [
                    "Chaque leader a commencé quelque part. Et toi ?",
                    "L'histoire de Koffi : de salarié à leader digital",
                    "Tu n'as pas besoin d'argent pour commencer. Tu as besoin de décider.",
                    "Le plus gros risque, c'est de ne rien risquer.",
                ],
                "Communauté & Entraide": [
                    "Seul, tu vas vite. Ensemble, tu vas loin.",
                    "Voici ce qui se passe dans notre communauté quand tu poses une question.",
                    "Live coaching : rejoins-nous pour apprendre ensemble",
                    "Behind the scenes : une journée dans la communauté",
                ],
                "Santé & Bien-être": [
                    "Un entrepreneur en bonne santé vaut 10 entrepreneurs épuisés",
                    "3 habitudes santé pour garder l'énergie de bâtisseur",
                    "Pourquoi la santé est le 1er investissement de ton business",
                    "Le lien entre énergie physique et performance digitale",
                ],
                "Challenge & Action": [
                    "5 jours. 1 système. 1er post. Tu es prêt ?",
                    "Le Challenge est gratuit. La seule chose qu'on demande, c'est ton action.",
                    "Rejoins la communauté et démarre ton Challenge aujourd'hui.",
                    "Jour X du Challenge : voici ce que ça donne.",
                ],
            }
            
            sujets = sujets_par_pilier.get(pilier, sujets_par_pilier["Éducation IA & Digital"])
            # Choisir un sujet basé sur le jour de la semaine
            jour_index = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"].index(jour)
            sujet = sujets[jour_index % len(sujets)]
        
        # Adapter le prompt selon le réseau social
        if reseau == "Facebook":
            format_prompt = """Crée un post Facebook de 100-200 mots.
            Structure : accroche > corps > call to action doux > hashtags.
            Inclure 5-8 hashtags pertinents.
            Le post doit être authentique, chaleureux, et apporter de la valeur."""
            
        elif reseau == "TikTok":
            format_prompt = """Crée un script vidéo TikTok de 15-30 secondes.
            Découpe en 3-5 scènes avec pour chaque : durée, description visuelle, texte à l'écran.
            Inclure une caption courte avec 3-5 hashtags.
            Le hook (3 premières secondes) doit capter l'attention immédiatement."""
            
        elif reseau == "WhatsApp Statut":
            format_prompt = """Crée un statut WhatsApp : 1-2 phrases maximum + suggestion d'image.
            Le ton doit être plus personnel et direct que Facebook/TikTok.
            Format court et impactant."""
        
        # Prompt complet
        user_prompt = f"""Crée du contenu pour le réseau : {reseau}
        Jour : {jour}
        Pilier : {pilier}
        Sujet : {sujet}
        
        Utilisateur : {self.user_prenom}, {self.user_role}
        Bio : {self.user_bio}
        
        {format_prompt}
        
        Réponds en JSON avec ce format exact :
        {{
            "texte": "le texte du post",
            "hashtags": "les hashtags",
            "sujet": "le sujet généré",
            "image_prompt": "un prompt pour générer l'image (en anglais, décris une image moderne avec couleurs vert #00C853 et violet #6B2FB5, contexte africain, format carré ou vertical)",
            "script_video": [{{"duree": "~4 sec", "visuel": "description", "texte_ecran": "texte"}}]
        }}
        
        Si ce n'est pas pour TikTok, mets "script_video" à null."""
        
        # Appel à l'API Gemini
        model = genai.GenerativeModel(self.model_name)
        full_prompt = self.SYSTEM_PROMPT + "\n\n" + user_prompt
        response = model.generate_content(full_prompt)
        
        text = response.text
        
        # Parser le JSON
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = text[start:end]
                content = json.loads(json_str)
            else:
                # Si pas de JSON, créer un contenu basique
                content = {
                    "texte": text,
                    "hashtags": "#IA #Digital #Entrepreneuriat #Afrique",
                    "sujet": sujet,
                    "image_prompt": None,
                    "script_video": None
                }
        except:
            content = {
                "texte": text,
                "hashtags": "#IA #Digital #Entrepreneuriat #Afrique",
                "sujet": sujet,
                "image_prompt": None,
                "script_video": None
            }
        
        # Générer l'image si un prompt est fourni
        if content.get('image_prompt'):
            try:
                image_path = self._generate_image(content['image_prompt'], reseau)
                content['image_path'] = image_path
            except Exception as e:
                print(f"Erreur génération image : {e}")
                content['image_path'] = None
        else:
            content['image_path'] = None
        
        return content
    
    def _generate_image(self, prompt, reseau):
        """Génère une image avec Gemini (Imagen)"""
        try:
            # Utiliser le modèle Imagen de Google pour générer des images
            # Note: Si Imagen n'est pas disponible, on utilise un fallback
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Demander à Gemini de créer une description d'image détaillée
            # puis utiliser l'API d'images de Google
            image_prompt_enhanced = f"""Generate a detailed image description for: {prompt}
            The image should be modern, with green (#00C853) and purple (#6B2FB5) colors, 
            African context, professional social media style."""
            
            # Essayer de générer une image avec Gemini
            try:
                # Utiliser le modèle disponible
                response = model.generate_content([image_prompt_enhanced])
                # Si Gemini ne peut pas générer d'image directement, on utilise un fallback
            except:
                pass
            
            # Fallback: Créer une image avec Pillow (image_engine)
            from image_engine import ImageEngine
            engine = ImageEngine(
                photo_path="assets/user_photo.jpg" if os.path.exists("assets/user_photo.jpg") else None,
                logo_path="assets/logo_abd.png" if os.path.exists("assets/logo_abd.png") else None
            )
            
            # Déterminer le format
            format_type = "vertical" if reseau in ["TikTok", "WhatsApp Statut"] else "carre"
            
            # Extraire un texte court du prompt pour l'image
            short_text = prompt[:100] if len(prompt) > 100 else prompt
            image_path = engine.create_quote_image(short_text, format=format_type)
            
            return image_path
            
        except Exception as e:
            print(f"Erreur génération image : {e}")
            # Dernier fallback: créer une image simple
            from image_engine import ImageEngine
            engine = ImageEngine()
            format_type = "vertical" if reseau in ["TikTok", "WhatsApp Statut"] else "carre"
            return engine.create_quote_image("ABD - Académie des Bâtisseurs Digitaux", format=format_type)
