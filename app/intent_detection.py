from google import genai
from dotenv import load_dotenv
import os

class IntentDetection:
    intentions = []
    def __init__(self):
        load_dotenv()
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY"),
        )
        self.intentions = {"Problème de Configuration de Telephone pour accès a Internet":"Reponse 1",
                      "Demande de Codes Courts (Ne Connait Pas Son Numéro, Consultation Crédit Voix Et Data etc... )":"Reponse 2",
                      "Demandes liées au compte My Xtremnet (Création, Réinitialisation…)":"Reponse 3",
                      "SIM Inactive/Invalide/Résiliée":"Reponse 4",
                      "Demande liées à la non détection automatique du réseau en zone de roaming":"Reponse 5",
                      "Demande d'infos sur les Nouveaux Produits( Recharge En Ligne,  Crédit Communication, Coût des Appels, Appareils/Accessoires Défectueux,  Etc":"Reponse 6",
                      "Autres (Listing, Probléme de Site Web/ Data Center, Messagerie, Etc…)":"Reponse 7",
                      "Demande de solde":"Reponse 7"}

    def generate_response(self, message: str) -> str:
        """
        Donne l'intention détectée dans le message.
        """
        text = ""
        text += "Voici les intentions possibles : \n"
        text += "\n".join(self.intentions.keys())
        text += "\n\nVoici le message : \n"
        text += message
        text += "\n\nQuelle est l'intention du message ? Si aucune n'est compatible, renvoie \"Aucune\"\n"
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=text
        )
        return response.text if response.text else "Aucune réponse générée."