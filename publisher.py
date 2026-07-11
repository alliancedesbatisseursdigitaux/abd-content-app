# publisher.py — Publication sur les réseaux sociaux
# Module pour publier automatiquement sur Facebook, TikTok et WhatsApp

import requests
import json
import os

class SocialPublisher:
    """Gestionnaire de publication sur les réseaux sociaux"""
    
    def __init__(self, fb_page_id=None, fb_token=None, tiktok_key=None, 
                 tiktok_secret=None, wa_phone_id=None, wa_token=None, wa_number=None):
        self.fb_page_id = fb_page_id
        self.fb_token = fb_token
        self.tiktok_key = tiktok_key
        self.tiktok_secret = tiktok_secret
        self.wa_phone_id = wa_phone_id
        self.wa_token = wa_token
        self.wa_number = wa_number
    
    def publish(self, reseau, texte, image_path=None, hashtags=None):
        """Publie sur le réseau social spécifié"""
        if reseau == "Facebook":
            return self._publish_facebook(texte, image_path, hashtags)
        elif reseau == "TikTok":
            return self._publish_tiktok(texte, image_path, hashtags)
        elif reseau == "WhatsApp Statut":
            return self._notify_whatsapp(texte, image_path)
        else:
            return {"success": False, "error": f"Réseau {reseau} non supporté"}
    
    def _publish_facebook(self, texte, image_path=None, hashtags=None):
        """Publie sur Facebook Page"""
        if not self.fb_page_id or not self.fb_token:
            return {"success": False, "error": "Facebook non configuré. Ajoutez Page ID et Access Token."}
        
        try:
            url = f"https://graph.facebook.com/v18.0/{self.fb_page_id}/feed"
            
            # Combiner texte et hashtags
            full_text = texte
            if hashtags:
                full_text += f"\n\n{hashtags}"
            
            data = {
                "message": full_text,
                "access_token": self.fb_token
            }
            
            # Si image, publier avec photo
            if image_path and os.path.exists(image_path):
                url = f"https://graph.facebook.com/v18.0/{self.fb_page_id}/photos"
                data["caption"] = full_text
                # Upload de l'image
                with open(image_path, 'rb') as img:
                    files = {'source': img}
                    response = requests.post(url, data=data, files=files)
            else:
                response = requests.post(url, data=data)
            
            result = response.json()
            
            if 'id' in result:
                post_id = result['id']
                return {
                    "success": True,
                    "post_id": post_id,
                    "url": f"https://facebook.com/{post_id}"
                }
            else:
                return {"success": False, "error": json.dumps(result)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _publish_tiktok(self, texte, image_path=None, hashtags=None):
        """Publie sur TikTok (via Content Posting API)"""
        if not self.tiktok_key or not self.tiktok_secret:
            return {"success": False, "error": "TikTok non configuré. Ajoutez Client Key et Secret."}
        
        # Note: TikTok Content Posting API nécessite une vidéo, pas une image
        # Pour une implémentation complète, il faut convertir les images en vidéo
        # ou utiliser les scripts vidéo générés
        
        try:
            # Étape 1: Obtenir le token d'accès
            token_url = "https://open.tiktokapis.com/v2/oauth/token/"
            token_data = {
                "client_key": self.tiktok_key,
                "client_secret": self.tiktok_secret,
                "grant_type": "client_credentials"
            }
            token_response = requests.post(token_url, data=token_data)
            token_result = token_response.json()
            
            if 'access_token' not in token_result:
                return {"success": False, "error": "Impossible d'obtenir le token TikTok"}
            
            access_token = token_result['access_token']
            
            # Pour une publication complète, il faut :
            # 1. Initialiser l'upload (POST /v2/post/publish/video/init/)
            # 2. Uploader la vidéo
            # 3. Finaliser la publication
            
            # Cette implémentation est simplifiée — pour une version complète,
            # il faut implémenter le flow d'upload TikTok complet
            
            return {
                "success": False, 
                "error": "Publication TikTok nécessite une vidéo. Utilisez le script vidéo généré pour créer la vidéo dans CapCut, puis publiez manuellement."
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _notify_whatsapp(self, texte, image_path=None):
        """Envoie une notification WhatsApp avec le contenu du statut à poster manuellement"""
        if not self.wa_phone_id or not self.wa_token:
            return {"success": False, "error": "WhatsApp non configuré."}
        
        try:
            url = f"https://graph.facebook.com/v18.0/{self.wa_phone_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.wa_token}",
                "Content-Type": "application/json"
            }
            
            # Message texte
            message_text = f"📱 *Statut WhatsApp du jour*\n\n{texte}\n\n_Poste ce statut manuellement sur WhatsApp !_"
            
            data = {
                "messaging_product": "whatsapp",
                "to": self.wa_number,
                "type": "text",
                "text": {"body": message_text}
            }
            
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            if 'messages' in result:
                return {"success": True, "message": "Notification WhatsApp envoyée. Postez le statut manuellement."}
            else:
                return {"success": False, "error": json.dumps(result)}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
