import os
import datetime
import requests

# 1. Funzione per cercare le notizie di oggi sull'Inter
def cerca_notizie():
    url = "https://google.serper.dev/search"
    payload = {"q": "Inter FC ultime notizie calciomercato", "tbm": "nws", "gl": "it", "hl": "it"}
    headers = {"X-API-KEY": os.environ.get("SERPER_API_KEY")}
    try:
        response = requests.post(url, json=payload, headers=headers)
        risultati = response.json().get('news', [])
        testo_notizie = ""
        for n in risultati[:5]: # Prende le prime 5 notizie
            testo_notizie += f"- {n['title']}: {n['snippet']}\n"
        return testo_notizie
    except:
        return "Nessuna nuova notizia trovata oggi."

# 2. Funzione per far scrivere l'articolo a OpenAI
def chiedi_a_openai(notizie):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    prompt = f"Sei un giornalista tifoso dell'Inter. Scrivi un articolo di blog appassionante e ben formattato in italiano basandoti su queste notizie del giorno:\n\n{notizie}\n\nUsa i titoli in Markdown (##) per separare le notizie."
    
    data = {
        "model": "gpt-4o-mini", # Modello economico e veloce
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()['choices'][0]['message']['content']

# 3. Esecuzione del processo
notizie_del_giorno = cerca_notizie()
articolo_finale = chiedi_a_openai(notizie_del_giorno)

# 4. Salva l'articolo con la data di oggi
oggi = datetime.date.today().strftime("%Y-%m-%d")
nome_file = f"_posts/{oggi}-notizie-inter.md"

os.makedirs("_posts", exist_ok=True)
with open(nome_file, "w", encoding="utf-8") as f:
    f.write(f"---\nlayout: post\ntitle: 'Notizie Inter del {oggi}'\ndate: {oggi}\n---\n\n")
    f.write(articolo_finale)

print("Articolo creato!")
