import sys
import os
import json
import time
from duckduckgo_search import DDGS

def rodar_motor_ddg(termo_busca):
    if not termo_busca:
        print("⚠️ Nenhum termo de busca fornecido.")
        return

    print(f"🤖 Motor GM Search acionando índice DuckDuckGo para: '{termo_busca}'")
    
    banco_cache = {
        "termo_atual": termo_busca,
        "paginas": [],
        "imagens": []
    }
    
    # 1. COLETA DE PÁGINAS WEB
    try:
        with DDGS() as ddgs:
            print("🌐 Coletando páginas...")
            resultados_web = ddgs.text(termo_busca, max_results=15)
            if resultados_web:
                for item in resultados_web:
                    banco_cache["paginas"].append({
                        "titulo": item.get("title", "Sem título"),
                        "url": item.get("href", ""),
                        "conteudo": item.get("body", "Sem resumo disponível.")
                    })
    except Exception as e:
        print(f"⚠️ Limite de IP na busca Web: {e}")

    # Pausa de segurança de 3 segundos para limpar o tráfego do IP antes de pedir imagens
    time.sleep(3)

    # 2. COLETA DE IMAGENS
    try:
        with DDGS() as ddgs:
            print("📷 Coletando imagens...")
            resultados_img = ddgs.images(termo_busca, max_results=16)
            if resultados_img:
                for item in resultados_img:
                    banco_cache["imagens"].append({
                        "url_imagem": item.get("image", ""),
                        "url_origem": item.get("url", ""),
                        "descricao": item.get("title", termo_busca)
                    })
    except Exception as e:
        print(f"⚠️ Limite de IP na busca de Imagens: {e}")

    # Se o IP do GitHub estiver 100% bloqueado e não trouxer nada, cria um aviso amigável
    if not banco_cache["paginas"] and not banco_cache["imagens"]:
        banco_cache["paginas"].append({
            "titulo": "Servidores do GitHub temporariamente bloqueados pelo DDG",
            "url": "https://duckduckgo.com",
            "conteudo": "O IP compartilhado do GitHub Actions atingiu o limite de requisições do DuckDuckGo neste instante. Aguarde alguns minutos e dispare o Workflow novamente para pegar um IP limpo."
        })

    # Salva o arquivo JSON local na pasta do projeto
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_salvamento = os.path.join(diretorio_atual, 'index_cache.json')
    
    with open(caminho_salvamento, 'w', encoding='utf-8') as f:
        json.dump(banco_cache, f, ensure_ascii=False, indent=2)
        
    print(f"💾 Banco de dados atualizado com sucesso em: {caminho_salvamento}")

if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else "Tecnologia"
    rodar_motor_ddg(termo)
