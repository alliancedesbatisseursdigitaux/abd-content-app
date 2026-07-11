# image_engine.py — Génération et montage d'images ABD
# Module pour créer des visuels avec la photo de l'utilisateur

from PIL import Image, ImageDraw, ImageFont
import os

# Couleurs ABD
VERT_ABD = (0, 200, 83)
VIOLET_ABD = (107, 47, 181)
BLANC = (255, 255, 255)
NOIR = (10, 10, 10)

class ImageEngine:
    """Générateur d'images pour ABD avec photo utilisateur"""
    
    def __init__(self, photo_path=None, logo_path=None):
        self.photo_path = photo_path
        self.logo_path = logo_path
    
    def create_quote_image(self, texte, auteur=None, format="carre"):
        """Crée une image citation avec fond ABD"""
        width, height = (1080, 1080) if format == "carre" else (1080, 1920)
        
        # Créer le fond avec dégradé violet vers vert
        img = Image.new('RGB', (width, height), NOIR)
        draw = ImageDraw.Draw(img)
        
        # Dégradé simple
        for y in range(height):
            ratio = y / height
            r = int(VIOLET_ABD[0] * (1 - ratio) + VERT_ABD[0] * ratio)
            g = int(VIOLET_ABD[1] * (1 - ratio) + VERT_ABD[1] * ratio)
            b = int(VIOLET_ABD[2] * (1 - ratio) + VERT_ABD[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Ajouter la photo de l'utilisateur si disponible
        if self.photo_path and os.path.exists(self.photo_path):
            try:
                photo = Image.open(self.photo_path)
                photo_size = 300 if format == "carre" else 400
                photo = photo.resize((photo_size, photo_size), Image.Resampling.LANCZOS)
                
                # Créer un masque circulaire
                mask = Image.new('L', (photo_size, photo_size), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse([0, 0, photo_size, photo_size], fill=255)
                
                # Position de la photo
                photo_x = (width - photo_size) // 2
                photo_y = 100 if format == "carre" else 150
                img.paste(photo, (photo_x, photo_y), mask)
            except Exception as e:
                print(f"Erreur photo : {e}")
        
        # Ajouter le texte
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
        
        # Centrer le texte
        text_y = 500 if format == "carre" else 700
        lines = self._wrap_text(texte, font_large, width - 100, draw)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, text_y), line, fill=BLANC, font=font_large)
            text_y += 60
        
        # Ajouter l'auteur
        if auteur:
            bbox = draw.textbbox((0, 0), f"— {auteur}", font=font_medium)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, text_y + 30), f"— {auteur}", fill=BLANC, font=font_medium)
        
        # Ajouter le logo ABD si disponible
        if self.logo_path and os.path.exists(self.logo_path):
            try:
                logo = Image.open(self.logo_path)
                logo = logo.resize((100, 100), Image.Resampling.LANCZOS)
                img.paste(logo, (width - 120, height - 120))
            except:
                pass
        
        # Sauvegarder
        os.makedirs("output/images", exist_ok=True)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"output/images/quote_{timestamp}.png"
        img.save(path)
        return path
    
    def create_statut_image(self, texte, format="vertical"):
        """Crée une image pour statut WhatsApp"""
        return self.create_quote_image(texte, format="vertical")
    
    def _wrap_text(self, text, font, max_width, draw):
        """Découpe le texte en lignes pour tenir dans la largeur"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
