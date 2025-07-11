import requests
from langchain.tools import tool

@tool
def get_character_by_id(id: int) -> str:
    """
    Devuelve nombre, especie y estado de un personaje de Rick and Morty por ID.
    """
    try:
        res = requests.get(f"https://rickandmortyapi.com/api/character/{id}")
        res.raise_for_status()
        data = res.json()
        name = data.get("name", "Desconocido")
        species = data.get("species", "Desconocido")
        status = data.get("status", "Desconocido")
        origin = data.get("origin", {}).get("name", "Desconocida")
        return f"{name} es un {species} que está {status}. Viene de {origin}."
    except Exception:
        return "❌ No se pudo obtener información del personaje."
