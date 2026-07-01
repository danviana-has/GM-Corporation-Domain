import requests
from bs4 import BeautifulSoup
import json
import os
import re

# Lista de sites e portais que o seu GM Search vai indexar
SITES_ALVO = [
    "https://www.python.org",
    "https://news.ycombinator.com",
    "https://en.wikipedia.org/wiki/Main_Page"
]

def rodar_crawler():
    index_cache = {
        "paginas": [],
        "imagens": []
    }
    
    headers = {'User-Agent': 'GMSearchBot/1.0 (+https://gmcorporation.com.br)'}
    
    print("🤖 Iniciando o Crawler do GM Search...")
    
    for url in SITES_ALVO:
        try:
            print(f"🔗 Rastreando: {url}")
            resposta = requests.get(url, headers=headers, timeout=10)
            if resposta.status_code != 200: continue
            
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            # --- INDEXADOR DE PÁGINAS ---
            titulo = soup.title.string.strip() if soup.title else url
            for s in soup(["script", "style"]): s.decompose() # limpa o HTML
            texto_limpo = " ".join(soup.get_text().split())
            
            index_cache["paginas"].append({
                "titulo": titulo,
                "url": url,
                "conteudo": texto_limpo[:1000] # Guarda os primeiros 1000 caracteres para busca
            })
            
            # --- INDEXADOR DE IMAGENS ---
            for img in soup.find_all('img'):
                src = img.get('src')
                alt = img.get('alt', '').strip()
                if src and alt: # Só indexa se tiver texto alternativo para poder buscar
                    # Corrige links relativos
                    if src.startswith('/'):
                        from urllib.parse import urljoin
                        src = urljoin(url, src)
                    
                    index_cache["imagens"].append({
                        "url_imagem": src,
                        "url_origem": url,
                        "descricao": alt
                    })
                    
        except Exception as e:
            print(f"❌ Erro ao rastrear {url}: {e}")
            
    # Salva o banco de dados (Cache) em formato JSON
    caminho_salvar = os.path.join(os.path.dirname(__file__), 'index_cache.json')
    with open(caminho_salvar, 'w', encoding='utf-8') as f:
        json.dump(index_cache, f, ensure_ascii=False, indent=2)
    
    print("💾 Indexação concluída! Cache salvo com sucesso.")

if __name__ == "__main__":
    rodar_crawler()
