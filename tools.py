import requests
from langchain.tools import tool

@tool
def get_personaje_rick_and_morty(id: int) -> str:
    """
    Devuelve información básica de un personaje de Rick and Morty por ID.
    """
    try:
        url = f"https://rickandmortyapi.com/api/character/{id}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        name = data.get("name", "Desconocido")
        species = data.get("species", "Desconocida")
        status = data.get("status", "Desconocido")
        origin = data.get("origin", {}).get("name", "Desconocido")

        return f"{name} es un {species} que está {status}. Viene de {origin}."
    except Exception:
        return "No se pudo obtener la información del personaje. Intenta con otro ID."

tools = [get_personaje_rick_and_morty]
