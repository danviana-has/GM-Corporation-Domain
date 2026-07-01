import requests
from bs4 import BeautifulSoup
import json
import os
import re
from urllib.parse import urljoin

# Lista de portais que o seu GM Search vai vasculhar
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
    
    headers = {
        'User-Agent': 'GMBackendBot/1.0 (+https://gmcorporation.com.br)'
    }
    
    print("🤖 Iniciando o Crawler do GM Search...")
    
    for url in SITES_ALVO:
        try:
            print(f"🔗 Rastreando em tempo real: {url}")
            resposta = requests.get(url, headers=headers, timeout=10)
            if resposta.status_code != 200: 
                print(f"⚠️ Ignorando {url} (Status {resposta.status_code})")
                continue
            
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            # --- INDEXADOR DE SITES (TEXTO) ---
            titulo = soup.title.string.strip() if soup.title else url
            
            # Limpa tags que guardam códigos visuais e não conteúdo legível
            for s in soup(["script", "style", "meta", "noscript"]): 
                s.decompose()
                
            texto_limpo = " ".join(soup.get_text().split())
            
            index_cache["paginas"].append({
                "titulo": titulo,
                "url": url,
                "conteudo": texto_limpo[:1000] # Limita os primeiros 1000 caracteres para otimizar o tamanho do JSON
            })
            
            # --- INDEXADOR DE IMAGENS ---
            for img in soup.find_all('img'):
                src = img.get('src')
                alt = img.get('alt', '').strip()
                
                # O robô só armazena a imagem se ela tiver uma descrição (alt) para podermos pesquisar
                if src and alt:
                    # Resolve links relativos (ex: /img/logo.png vira https://site.com/img/logo.png)
                    src_absoluto = urljoin(url, src)
                    
                    index_cache["imagens"].append({
                        "url_imagem": src_absoluto,
                        "url_origem": url,
                        "descricao": alt
                    })
                    
        except Exception as e:
            print(f"❌ Erro ao processar o alvo {url}: {e}")
            
    # --- SALVAMENTO BLINDADO DO INDEXADOR ---
    # os.path.abspath(__file__) descobre a rota exata deste script no Ubuntu do GitHub Actions,
    # contornando de forma limpa o problema do espaço na pasta "GM Search".
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_salvar = os.path.join(diretorio_atual, 'index_cache.json')
    
    with open(caminho_salvar, 'w', encoding='utf-8') as f:
        json.dump(index_cache, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Sucesso! Banco de dados atualizado e indexado em: {caminho_salvar}")

if __name__ == "__main__":
    rodar_crawler()
