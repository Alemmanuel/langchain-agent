import requests

def rick_and_morty_tool(id: str) -> str:
    if not id.strip().isdigit():
        return "❌ Debes proporcionar un ID numérico del personaje."

    url = f"https://rickandmortyapi.com/api/character/{id}"
    response = requests.get(url)
    if response.status_code != 200:
        return "❌ No se encontró ese personaje."

    data = response.json()
    return (
        f"{data['name']} es un {data['species']} que está {data['status']}. "
        f"Viene de {data['origin']['name']}."
    )

def saludar(nombre: str) -> str:
    if not nombre.strip():
        return "❌ Debes escribir un nombre."
    return f"¡Hola, {nombre}! ¿Cómo estás?"
