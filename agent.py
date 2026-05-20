import os
import datetime
import requests
from duckduckgo_search import DDGS

# 1. Ricerca GRATUITA tramite DuckDuckGo
def cerca_notizie():
    try:
        print("Cerco notizie su DuckDuckGo...")
        risultati = DDGS().news(keywords="Inter FC ultime notizie", max_results=5)
        testo_notizie = ""
        for n in risultati:
            testo_notizie += f"- {n['title']}: {n['body']}\n"

        if not testo_notizie:
            return "Nessuna notizia rilevante trovata oggi."
        return testo_notizie
    except Exception as e:
        print(f"Errore nella ricerca: {e}")
        return "Nessuna notizia trovata a causa di un errore."

# 2. Generazione AI GRATUITA tramite Groq (Modello Llama 3)
def chiedi_a_groq(notizie):
    url = "https://api.groq.com/openai/v1/chat/completions"
    chiave = os.environ.get('GROQ_API_KEY')

    if not chiave:
        print("❌ ERRORE: La chiave GROQ_API_KEY non è stata trovata nei Secrets di GitHub!")
        exit(1)

    headers = {
        "Authorization": f"Bearer {chiave}",
        "Content-Type": "application/json"
    }

    prompt = f"Sei un giornalista tifoso dell'Inter. Scrivi un articolo di blog appassionante e ben formattato in italiano basandoti su queste notizie del giorno:\n\n{notizie}\n\nUsa i titoli in Markdown (##) per separare le notizie. Non inserire convenevoli, scrivi solo l'articolo."

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}]
    }

    print("Elaborazione dell'articolo con l'AI in corso...")
    response = requests.post(url, json=data, headers=headers)
    risposta_json = response.json()

    if 'choices' not in risposta_json:
        print("❌ ERRORE DA GROQ:")
        print(risposta_json)
        exit(1)

    return risposta_json['choices'][0]['message']['content']

# 3. Esecuzione del processo
notizie_del_giorno = cerca_notizie()
articolo_finale = chiedi_a_groq(notizie_del_giorno)

# 4. Salvataggio dell'articolo
oggi = datetime.date.today().strftime("%Y-%m-%d")
nome_file = f"_posts/{oggi}-notizie-inter.md"

os.makedirs("_posts", exist_ok=True)
with open(nome_file, "w", encoding="utf-8") as f:
    f.write(f"---\nlayout: post\ntitle: 'Notizie Inter del {oggi}'\ndate: {oggi}\n---\n\n")
    f.write(articolo_finale)

print("✅ Articolo creato:", nome_file)

