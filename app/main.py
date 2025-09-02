from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .types import Data, RawData
from .intent_detection import IntentDetection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_response(source: str, data: Data):
    """
    Génère une réponse automatique en fonction de la source et des données de la réclamation.
    """
    message = data.message
    user = data.user
    username = "client "+user.username

    # Logique de base pour personnaliser la réponse
    # Pour une version plus avancée, on pourrait ici intégrer de l'analyse de sentiment
    # ou un moteur de traitement du langage naturel (NLP).

    response_text = f"Bonjour {username}, \n\n"
    response_text += "Nous avons bien reçu votre message et nous vous remercions de nous avoir contactés. \n"

    special_cases = False
    detection = IntentDetection()
    intentions = detection.intentions
    responses = []
    intent = detection.generate_response(message)
    # if ("solde" in message.lower() or "credit" in message.lower() or "crédit" in message.lower()) and ("consulter" in message.lower() or "connaitre" in message.lower()):
    #     response_text += "Le code pour consulter votre solde est *825*3*2*1*1#. \n"
    #     special_cases = True
    # if "numéro" in message.lower() and ("consulter" in message.lower() or "connaitre" in message.lower()):
    #     special_cases = True
    #     response_text += "Pour connaître votre numéro, tapez le *825*3*3#. \n"
    # if "sim" in message.lower() and ("inactive" in message.lower() or "invalide" in message.lower() or "résilié" in message.lower()):
    #     special_cases = True
    #     reponse_text += "Votre carte SIM a été résiliée, veuillez vous rapprocher d'une agence CAMTEL pour une prise en charge."
    # if "xtremnet" in message.lower():
    #     special_cases = True
    #     if "creer" in message.lower() or "creation" in message.lower():
    #         reponse_text = "Voici la procédure de création d'un compte My Xtremnet."
    #     if "reinitiali" in message.lower() or "réinitiali" in message.lower():
    #         reponse_text = "Voici la procédure de réinitialisation de votre compte My Xtremnet."
    # if "roaming" in message.lower() and ("detect" in message.lower() or "détect" in message.lower()):
    #     special_cases = True
    #     reponse_text = "Vous n'arrivez pas à accéder au réseau dans une zone en roaming. Ce n'est pas grave, voici la procédure à suivre pour vous connecter."
    # if "site" in message.lower() and "web" in message.lower():
    #     special_cases = True
    #     reponse_text += "Le site web de CAMTEL est le https://camtel.cm. Nous resolvons tout bug pouvant nuire à votre confort."
    
    # if not special_cases:
    #     response_text += "Un membre de notre équipe support va examiner votre réclamation et vous apportera une réponse personnalisée sous 24 heures. \n"
    intent_response = intentions[intent] if intentions.keys().__contains__(intent.strip()) else "Un membre de notre équipe support va examiner votre réclamation et vous apportera une réponse personnalisée sous 24 heures."
    print(f"La reponse à l'intention {intent} est : {intent_response}")
    response_text += f"Nous avons détecté l'intention suivante : {intent.strip()}. \n" if intent.lower() != "aucune" else "Aucune intention détectée. \n"
    response_text += "\nCordialement, \nL'équipe de support"

    # Personnalisation supplémentaire en fonction de la source
    if source in ["instagram_comment", "facebook_comment"]:
        response_text = f"@{user.username} " + "Nous avons bien pris en compte votre commentaire. Nous vous avons envoyé un message privé pour discuter plus en détail. "
    
    return response_text

@app.post("/api/reclamation", summary="Response to claim")
async def handle_reclamation(request: RawData):
    try:
        if not request or not request.source or not request.data:
            raise HTTPException(status_code=400, detail="Requête invalide. Les champs 'source' et 'data' sont requis.")
        
        source = request.source
        data = request.data
        print(f'Données reçues: {data}')

        allowed_sources = ["website", "instagram_comment", "facebook_comment", "instagram_inbox", "facebook_inbox"]
        if source not in allowed_sources:
            raise HTTPException(status_code=400, detail=f"Source '{source}' non valide.")

        response = generate_response(source, data)

        return {
            "response_text": response
        }
    except Exception as e:
        print(f'Une erreur est survenue: {e}')