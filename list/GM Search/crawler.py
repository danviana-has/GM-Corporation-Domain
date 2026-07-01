import sys
import os
import json
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
    
    # Inicializa o gerenciador da biblioteca pronta
    try:
        with DDGS() as ddgs:
            # 1. Busca bilhões de páginas web prontas
            print("🌐 Coletando páginas...")
            resultados_web = ddgs.text(termo_busca, max_results=15)
            for item in resultados_web:
                banco_cache["paginas"].append({
                    "titulo": item.get("title", "Sem título"),
                    "url": item.get("href", ""),
                    "conteudo": item.get("body", "Sem resumo disponível.")
                })
                
            # 2. Busca bilhões de imagens prontas
            print("📷 Coletando imagens...")
            resultados_img = ddgs.images(termo_busca, max_results=16)
            for item in resultados_img:
                banco_cache["imagens"].append({
                    "url_imagem": item.get("image", ""),
                    "url_origem": item.get("url", ""),
                    "descricao": item.get("title", termo_busca)
                })
                
    except Exception as e:
        print(f"❌ Erro ao coletar dados da biblioteca: {e}")
        # Garante que o arquivo não quebre caso a biblioteca sofra rate limit
        if not banco_cache["paginas"]:
            banco_cache["paginas"].append({
                "titulo": "Limite temporário atingido",
                "url": "https://duckduckgo.com",
                "conteudo": "O motor recebeu muitas requisições seguidas. Aguarde um instante para rodar a busca novamente."
            })

    # Grava o resultado JSON pronto direto na pasta correta do repositório
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_salvamento = os.path.join(diretorio_atual, 'index_cache.json')
    
    with open(caminho_salvamento, 'w', encoding='utf-8') as f:
        json.dump(banco_cache, f, ensure_ascii=False, indent=2)
        
    print(f"💾 Banco de dados atualizado com sucesso em: {caminho_salvamento}")

if __name__ == "__main__":
    termo = sys.argv[1] if len(sys.argv) > 1 else "Tecnologia"
    rodar_motor_ddg(termo)
