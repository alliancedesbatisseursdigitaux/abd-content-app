# content_engine.py — Moteur de création de contenu ABD
# Ce module contient les prompts système cachés derrière l'interface

from openai import OpenAI
import json
import os
import requests
from datetime import datetime

class ContentEngine:
    """Moteur de création de contenu pour ABD"""
    
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
        """Initialise le moteur de contenu"""
        self.client = OpenAI(api_key=api_key)
        self.user_prenom = user_prenom
        self.user_role = user_role
        self.user_bio = user_bio
    
    def research_trends(self):
        """Recherche les tendances actuelles sur le web"""
        try:
            # Utiliser GPT-4o pour identifier les tendances
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu es un analyste de tendances. Réponds en JSON."},
                    {"role": "user", "content": """Identifie 5 sujets tendance actuels pour créer du contenu 
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
                    
                    Réponds en JSON avec une liste 'tendances'."""}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result.get('tendances', [])
            
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
            format_prompt = f"""Crée un post Facebook de 100-200 mots.
            Structure : accroche > corps > call to action doux > hashtags.
            Inclure 5-8 hashtags pertinents.
            Le post doit être authentique, chaleureux, et apporter de la valeur."""
            
        elif reseau == "TikTok":
            format_prompt = f"""Crée un script vidéo TikTok de 15-30 secondes.
            Découpe en 3-5 scènes avec pour chaque : durée, description visuelle, texte à l'écran.
            Inclure une caption courte avec 3-5 hashtags.
            Le hook (3 premières secondes) doit capter l'attention immédiatement."""
            
        elif reseau == "WhatsApp Statut":
            format_prompt = f"""Crée un statut WhatsApp : 1-2 phrases maximum + suggestion d'image.
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
        
        Réponds en JSON avec ce format :
        {{
            "texte": "le texte du post",
            "hashtags": "les hashtags",
            "sujet": "le sujet généré",
            "image_prompt": "un prompt pour générer l'image avec DALL-E (en anglais, format 1080x1080 ou 1080x1920)",
            "script_video": [{{"duree": "~4 sec", "visuel": "description", "texte_ecran": "texte"}}] (si TikTok, sinon null)
        }}"""
        
        # Appel à l'API OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        content = json.loads(response.choices[0].message.content)
        
        # Générer l'image si un prompt est fourni
        if content.get('image_prompt'):
            try:
                image_path = self._generate_image(content['image_prompt'], reseau)
                content['image_path'] = image_path
            except Exception as e:
                print(f"Erreur génération image : {e}")
                content['image_path'] = None
        
        return content
    
    def _generate_image(self, prompt, reseau):
        """Génère une image avec DALL-E"""
        # Déterminer la taille selon le réseau
        if reseau == "TikTok" or reseau == "WhatsApp Statut":
            size = "1024x1792"  # Vertical
        else:
            size = "1024x1024"  # Carré
        
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        
        # Télécharger l'image
        os.makedirs("output/images", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"output/images/post_{timestamp}.png"
        
        img_response = requests.get(image_url)
        with open(image_path, 'wb') as f:
            f.write(img_response.content)
        
        return image_path
