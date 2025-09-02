from google import genai

client = genai.Client(api_key="AIzaSyC6uJPBJuhRK5ook4n04DNPuQk9A6RaaoA")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Je travaille sur une API FastAPI, et je veux que tu sois présent dans cette API. Comment déployer cette API avec ma clé Gemini?"
)
print(response.text)
