# ABD Content Automation — Application Web
# Fichier principal Streamlit — Interface pour Mireille et ses filleuls

import streamlit as st
import os
import json
import datetime
from content_engine import ContentEngine
from image_engine import ImageEngine
from publisher import SocialPublisher

# ═══════════════════════════════════════════════════════════
#  CONFIGURATION DES COULEURS ABD
# ═══════════════════════════════════════════════════════════
VERT_ABD = "#00C853"
VIOLET_ABD = "#6B2FB5"

# Configuration de la page
st.set_page_config(
    page_title="ABD Content Automation",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour les couleurs ABD
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {VIOLET_ABD}, {VERT_ABD});
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {VERT_ABD}, #00E676);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
    }}
    .info-box {{
        background: #f5f5f5;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid {VIOLET_ABD};
        margin: 10px 0;
        color: #1a1a1a;
    }}
    /* Forcer le texte sombre sur les zones claires */
    .stMarkdown, .stText, p, li, td, th {{
        color: #1a1a1a !important;
    }}
    /* Sidebar en fond sombre avec texte clair */
    .css-1d391kg, .css-1e5z2yo, section[data-testid="stSidebar"] {{
        background-color: #1a1a1a;
    }}
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stText {{
        color: #e0e0e0 !important;
    }}
    /* Tableaux lisibles */
    .stTable td, .stTable th {{
        color: #1a1a1a !important;
    }}
    /* Dataframe lisibles */
    .stDataFrame {{
        color: #1a1a1a;
    }}
    /* Zone principale fond clair */
    .stApp {{
        background-color: #ffffff;
    }}
    /* Text areas et inputs */
    .stTextArea, .stTextInput {{
        color: #1a1a1a;
    }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  INITIALISATION DE LA SESSION
# ═══════════════════════════════════════════════════════════

def init_session():
    """Initialise les variables de session"""
    if 'content_engine' not in st.session_state:
        st.session_state.content_engine = None
    if 'image_engine' not in st.session_state:
        st.session_state.image_engine = None
    if 'publisher' not in st.session_state:
        st.session_state.publisher = None
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = None
    if 'config_saved' not in st.session_state:
        st.session_state.config_saved = False

init_session()

# ═══════════════════════════════════════════════════════════
#  EN-TÊTE
# ═══════════════════════════════════════════════════════════

st.markdown("""
<div class="main-header">
    <h1>🚀 ABD Content Automation</h1>
    <p>Académie des Bâtisseurs Digitaux — Système de création de contenu automatique</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  SIDEBAR — CONFIGURATION
# ═══════════════════════════════════════════════════════════

st.sidebar.markdown("## ⚙️ Configuration")

# Onglets de configuration
config_tab = st.sidebar.radio(
    "Étape",
    ["1. Profil", "2. Clés API", "3. Réseaux sociaux", "4. Photo"]
)

# ── ÉTAPE 1 : PROFIL ──
if config_tab == "1. Profil":
    st.sidebar.markdown("### 👤 Votre profil")
    
    prenom = st.sidebar.text_input("Prénom", value="", placeholder="Ex: Mireille")
    nom = st.sidebar.text_input("Nom", value="", placeholder="Ex: Gomont")
    role_abd = st.sidebar.selectbox(
        "Rôle dans ABD",
        ["Membre Niveau 0 (Explorateur)", "Membre Niveau 1 (Bâtisseur)", 
         "Membre Niveau 2 (Créateur)", "Membre Niveau 3 (Leader)",
         "Membre Niveau 4 (Coach)", "Membre Niveau 5 (Mentor)",
         "Leader / Mentrice"]
    )
    bio_courte = st.sidebar.text_area(
        "Bio courte (1 phrase)", 
        value="", 
        placeholder="Ex: Leader digitale et mentrice dans la communauté ABD"
    )
    
    if st.sidebar.button("✅ Sauvegarder le profil"):
        if prenom and nom:
            st.session_state['user_prenom'] = prenom
            st.session_state['user_nom'] = nom
            st.session_state['user_role'] = role_abd
            st.session_state['user_bio'] = bio_courte
            st.sidebar.success("Profil sauvegardé ! Passez à l'étape 2.")
        else:
            st.sidebar.error("Veuillez remplir au moins le prénom et le nom.")

# ── ÉTAPE 2 : CLÉS API ──
elif config_tab == "2. Clés API":
    st.sidebar.markdown("### 🔑 Clé API Google Gemini (GRATUITE)")
    st.sidebar.markdown("""
    <div class="info-box">
    <p><strong>Google Gemini API Key</strong> (OBLIGATOIRE — 100% GRATUIT)</p>
    <p>Obtenez votre clé gratuite sur <a href="https://aistudio.google.com/apikey" target="_blank">aistudio.google.com/apikey</a></p>
    <p>1. Cliquez sur le lien ci-dessus</p>
    <p>2. Connectez-vous avec votre compte Google</p>
    <p>3. Cliquez sur "Create API Key"</p>
    <p>4. Copiez la clé et collez-la ici</p>
    <p>✅ Coût : <strong>0 FCFA — Gratuit</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    gemini_key = st.sidebar.text_input(
        "Google Gemini API Key", 
        type="password",
        placeholder="AIza..."
    )
    
    if st.sidebar.button("✅ Sauvegarder la clé"):
        if gemini_key:
            st.session_state['openai_key'] = gemini_key
            st.sidebar.success("Clé sauvegardée ! Passez à l'étape 3.")
        else:
            st.sidebar.error("La clé Google Gemini est obligatoire.")

# ── ÉTAPE 3 : RÉSEAUX SOCIAUX ──
elif config_tab == "3. Réseaux sociaux":
    st.sidebar.markdown("### 📱 Réseaux sociaux")
    
    st.sidebar.markdown("#### Facebook (optionnel)")
    fb_page_id = st.sidebar.text_input("Facebook Page ID", placeholder="123456789...")
    fb_token = st.sidebar.text_input("Facebook Access Token", type="password", placeholder="EAAG...")
    
    st.sidebar.markdown("#### TikTok (optionnel)")
    tiktok_key = st.sidebar.text_input("TikTok Client Key", placeholder="...")
    tiktok_secret = st.sidebar.text_input("TikTok Client Secret", type="password", placeholder="...")
    
    st.sidebar.markdown("#### WhatsApp (pour notifications de statut)")
    wa_phone_id = st.sidebar.text_input("WhatsApp Phone Number ID", placeholder="...")
    wa_token = st.sidebar.text_input("WhatsApp Access Token", type="password", placeholder="...")
    wa_number = st.sidebar.text_input("Votre numéro WhatsApp", placeholder="2250708667107")
    
    if st.sidebar.button("✅ Sauvegarder les réseaux"):
        st.session_state['fb_page_id'] = fb_page_id
        st.session_state['fb_token'] = fb_token
        st.session_state['tiktok_key'] = tiktok_key
        st.session_state['tiktok_secret'] = tiktok_secret
        st.session_state['wa_phone_id'] = wa_phone_id
        st.session_state['wa_token'] = wa_token
        st.session_state['wa_number'] = wa_number
        st.sidebar.success("Réseaux sauvegardés ! Passez à l'étape 4.")

# ── ÉTAPE 4 : PHOTO ──
elif config_tab == "4. Photo":
    st.sidebar.markdown("### 📸 Votre photo")
    st.sidebar.markdown("""
    <div class="info-box">
    <p>Uploadez une photo de vous (carrée, min 1080x1080).</p>
    <p>Cette photo sera utilisée pour créer des visuels personnalisés.</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_photo = st.sidebar.file_uploader(
        "Choisir une photo",
        type=['jpg', 'jpeg', 'png'],
        help="Format carré recommandé (min 1080x1080)"
    )
    
    if uploaded_photo is not None:
        # Sauvegarder la photo
        photo_dir = "assets"
        os.makedirs(photo_dir, exist_ok=True)
        photo_path = os.path.join(photo_dir, "user_photo.jpg")
        with open(photo_path, "wb") as f:
            f.write(uploaded_photo.getbuffer())
        st.session_state['photo_path'] = photo_path
        st.sidebar.success("Photo sauvegardée ! ✅")
        st.sidebar.image(uploaded_photo, caption="Votre photo", use_column_width=True)
    
    # Logo ABD (optionnel)
    st.sidebar.markdown("#### Logo ABD (optionnel)")
    uploaded_logo = st.sidebar.file_uploader(
        "Logo ABD (optionnel)",
        type=['png', 'jpg'],
        help="Logo de la communauté ABD"
    )
    if uploaded_logo is not None:
        logo_path = os.path.join(photo_dir, "logo_abd.png")
        with open(logo_path, "wb") as f:
            f.write(uploaded_logo.getbuffer())
        st.session_state['logo_path'] = logo_path

# ═══════════════════════════════════════════════════════════
#  VÉRIFICATION DE LA CONFIGURATION
# ═══════════════════════════════════════════════════════════

config_complete = (
    'user_prenom' in st.session_state and
    'openai_key' in st.session_state
)

if not config_complete:
    st.markdown("""
    <div class="info-box">
    <h3>👋 Bienvenue !</h3>
    <p>Pour commencer, configurez votre profil dans la barre latérale (à gauche) :</p>
    <ol>
        <li><strong>Profil</strong> : Votre prénom, nom et rôle</li>
        <li><strong>Clés API</strong> : Votre clé OpenAI (obligatoire)</li>
        <li><strong>Réseaux sociaux</strong> : Vos identifiants Facebook/TikTok/WhatsApp</li>
        <li><strong>Photo</strong> : Uploadez votre photo</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════════════
#  INTERFACE PRINCIPALE
# ═══════════════════════════════════════════════════════════

st.markdown(f"""
<div class="info-box">
<h3>Bonjour {st.session_state['user_prenom']} ! 👋</h3>
<p>Vous êtes connecté(e) en tant que <strong>{st.session_state.get('user_role', 'Membre ABD')}</strong></p>
</div>
""", unsafe_allow_html=True)

# Onglets principaux
tab1, tab2, tab3, tab4 = st.tabs([
    "📅 Calendrier", "✍️ Générer", "📊 Suivi", "⚙️ Paramètres"
])

# ── ONGLET 1 : CALENDRIER ──
with tab1:
    st.markdown("## 📅 Stratégie de contenu hebdomadaire")
    
    st.markdown("""
    | Jour | Matin (Facebook) | Après-midi (TikTok) | Soir (WhatsApp x2) |
    |------|------------------|---------------------|---------------------|
    | **Lundi** | Éducation IA | Tutoriel IA court | Citation · Astuce IA |
    | **Mardi** | Motivation | Story transformation | Message communauté · Conseil santé |
    | **Mercredi** | Communauté | Behind the scenes | Citation · Rappel Challenge |
    | **Jeudi** | Éducation IA | Outil IA du jour | Astuce digitale · Témoignage |
    | **Vendredi** | Challenge & Action | Annonce Challenge | Motivation · CTA communauté |
    | **Samedi** | Santé & Bien-être | Conseil santé | Citation santé · Behind the scenes |
    | **Dimanche** | Réflexion | Récap semaine | Inspiration · Préparation semaine |
    """)
    
    st.markdown("""
    ### Les 5 piliers de contenu
    - **Éducation IA & Digital** (30%) : Tutoriels, astuces, tendances IA
    - **Motivation & Transformation** (25%) : Stories, citations, mentalité
    - **Communauté & Entraide** (20%) : Témoignages, live coaching, entraide
    - **Santé & Bien-être** (15%) : Conseils santé, énergie du bâtisseur
    - **Challenge & Action** (10%) : Annonces Challenge, calls to action
    """)

# ── ONGLET 2 : GÉNÉRER ──
with tab2:
    st.markdown("## ✍️ Générer du contenu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        jour_semaine = st.selectbox(
            "Jour de la semaine",
            ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        )
        
        reseau = st.selectbox(
            "Réseau social",
            ["Facebook", "TikTok", "WhatsApp Statut"]
        )
        
        pilier = st.selectbox(
            "Pilier de contenu",
            ["Éducation IA & Digital", "Motivation & Transformation", 
             "Communauté & Entraide", "Santé & Bien-être", "Challenge & Action",
             "Automatique (selon le calendrier)"]
        )
        
        utiliser_photo = st.checkbox("Inclure ma photo dans le visuel", value=False)
        
        mode_preview = st.checkbox(
            "Mode prévisualisation (sans publier)", 
            value=True,
            help="Cochez pour générer le contenu sans le publier. Décochez pour publier automatiquement."
        )
    
    with col2:
        st.markdown("### Sujet personnalisé (optionnel)")
        sujet_custom = st.text_area(
            "Sujet spécifique",
            placeholder="Laissez vide pour générer automatiquement selon le pilier",
            height=100
        )
        
        st.markdown("### Recherche web")
        faire_recherche = st.checkbox(
            "Rechercher les tendances actuelles sur le web",
            value=True,
            help="Le système va rechercher les sujets tendance avant de générer le contenu"
        )
    
    if st.button("🚀 Générer le contenu", type="primary"):
        if 'openai_key' not in st.session_state:
            st.error("Veuillez configurer votre clé Google Gemini d'abord (Étape 2 dans la sidebar).")
        else:
            with st.spinner("Génération du contenu en cours..."):
                try:
                    # Initialiser le moteur de contenu
                    engine = ContentEngine(
                        api_key=st.session_state['openai_key'],
                        user_prenom=st.session_state['user_prenom'],
                        user_role=st.session_state.get('user_role', 'Membre ABD'),
                        user_bio=st.session_state.get('user_bio', ''),
                    )
                    
                    # Générer le contenu
                    content = engine.generate_content(
                        jour=jour_semaine,
                        reseau=reseau,
                        pilier=pilier,
                        sujet_custom=sujet_custom if sujet_custom else None,
                        faire_recherche=faire_recherche,
                    )
                    
                    st.session_state['generated_content'] = content
                    st.success("Contenu généré avec succès ! ✅")
                    
                except Exception as e:
                    st.error(f"Erreur lors de la génération : {str(e)}")
    
    # Afficher le contenu généré
    if st.session_state['generated_content']:
        content = st.session_state['generated_content']
        
        st.markdown("---")
        st.markdown("## 📝 Contenu généré")
        
        # Texte du post
        st.markdown("### Texte du post")
        st.text_area("Contenu", value=content.get('texte', ''), height=200, key="post_text")
        
        # Hashtags
        if content.get('hashtags'):
            st.markdown("### Hashtags")
            st.code(content['hashtags'])
        
        # Script vidéo (si TikTok)
        if content.get('script_video'):
            st.markdown("### Script vidéo (scènes)")
            for i, scene in enumerate(content['script_video']):
                st.markdown(f"**Scène {i+1}** ({scene.get('duree', '~4 sec')})")
                st.markdown(f"*Visuel :* {scene.get('visuel', '')}")
                st.markdown(f"*Texte à l'écran :* {scene.get('texte_ecran', '')}")
        
        # Image
        if content.get('image_path') and os.path.exists(content['image_path']):
            st.markdown("### Visuel")
            st.image(content['image_path'], use_column_width=True)
        
        # Boutons d'action
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Télécharger le texte
            st.download_button(
                "📥 Télécharger le texte",
                data=content.get('texte', ''),
                file_name=f"post_{jour_semaine}_{reseau}.txt",
                mime="text/plain"
            )
        
        with col2:
            if not mode_preview and content.get('image_path'):
                if st.button("📤 Publier maintenant"):
                    with st.spinner("Publication en cours..."):
                        try:
                            publisher = SocialPublisher(
                                fb_page_id=st.session_state.get('fb_page_id', ''),
                                fb_token=st.session_state.get('fb_token', ''),
                                tiktok_key=st.session_state.get('tiktok_key', ''),
                                tiktok_secret=st.session_state.get('tiktok_secret', ''),
                                wa_phone_id=st.session_state.get('wa_phone_id', ''),
                                wa_token=st.session_state.get('wa_token', ''),
                                wa_number=st.session_state.get('wa_number', ''),
                            )
                            
                            result = publisher.publish(
                                reseau=reseau,
                                texte=content.get('texte', ''),
                                image_path=content.get('image_path', ''),
                                hashtags=content.get('hashtags', ''),
                            )
                            
                            if result.get('success'):
                                st.success(f"Publié sur {reseau} ! ✅")
                                if result.get('url'):
                                    st.markdown(f"[Voir le post]({result['url']})")
                            else:
                                st.error(f"Erreur : {result.get('error', 'Erreur inconnue')}")
                        except Exception as e:
                            st.error(f"Erreur de publication : {str(e)}")
            elif mode_preview:
                st.info("Mode prévisualisation activé — décochez pour publier")
        
        with col3:
            if st.button("💾 Enregistrer dans le suivi"):
                try:
                    from excel_logger import log_to_excel
                    log_to_excel(
                        date=datetime.datetime.now().strftime("%Y-%m-%d"),
                        jour=jour_semaine,
                        reseau=reseau,
                        pilier=pilier,
                        sujet=content.get('sujet', ''),
                        texte=content.get('texte', '')[:200],
                        image_path=content.get('image_path', ''),
                        statut="Généré" if mode_preview else "Publié",
                    )
                    st.success("Enregistré dans le fichier de suivi ! ✅")
                except Exception as e:
                    st.error(f"Erreur : {str(e)}")

# ── ONGLET 3 : SUIVI ──
with tab3:
    st.markdown("## 📊 Suivi des posts")
    
    excel_path = "output/posts_log.xlsx"
    
    if os.path.exists(excel_path):
        try:
            import pandas as pd
            df = pd.read_excel(excel_path)
            st.dataframe(df, use_container_width=True)
            
            # Statistiques
            st.markdown("### Statistiques")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total posts", len(df))
            with col2:
                if 'Statut' in df.columns:
                    publies = len(df[df['Statut'] == 'Publié'])
                    st.metric("Publiés", publies)
            with col3:
                if 'Réseau social' in df.columns:
                    fb_count = len(df[df['Réseau social'] == 'Facebook'])
                    st.metric("Facebook", fb_count)
            with col4:
                if 'Réseau social' in df.columns:
                    tt_count = len(df[df['Réseau social'] == 'TikTok'])
                    st.metric("TikTok", tt_count)
            
            # Télécharger l'Excel
            with open(excel_path, "rb") as f:
                st.download_button(
                    "📥 Télécharger le fichier de suivi",
                    data=f,
                    file_name="posts_log.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {str(e)}")
    else:
        st.info("Aucun post généré pour le moment. Allez dans l'onglet 'Générer' pour créer du contenu.")

# ── ONGLET 4 : PARAMÈTRES ──
with tab4:
    st.markdown("## ⚙️ Paramètres")
    
    st.markdown("### Couleurs ABD")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.color_picker("Vert ABD", value=VERT_ABD)
    with col2:
        st.color_picker("Violet ABD", value=VIOLET_ABD)
    with col3:
        st.color_picker("Blanc", value="#FFFFFF")
    
    st.markdown("### Hashtags par défaut")
    default_hashtags = st.text_area(
        "Hashtags",
        value="#IA #Digital #Entrepreneuriat #Afrique #Transformation #IntelligenceArtificielle #BusinessEnLigne #DéveloppementPersonnel"
    )
    
    st.markdown("### Fréquence de publication")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("Posts Facebook/jour", min_value=0, max_value=5, value=1)
    with col2:
        st.number_input("Posts TikTok/jour", min_value=0, max_value=5, value=1)
    with col3:
        st.number_input("Statuts WhatsApp/jour", min_value=0, max_value=10, value=2)
    
    st.markdown("---")
    st.markdown("### ℹ️ À propos")
    st.markdown("""
    **ABD Content Automation** — Système de création de contenu automatique pour la communauté
    de l'Académie des Bâtisseurs Digitaux.
    
    *Découvrir. Construire. Créer. Diriger. Inspirer.*
    """)
