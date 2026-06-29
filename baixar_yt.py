from yt_dlp import YoutubeDL
import os
import json
from datetime import datetime

HISTORICO_ARQUIVO = "historico_downloads.json"
COOKIES_ARQUIVO = "cookies.txt"


def carregar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        try:
            with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []


def salvar_historico(item):
    historico = carregar_historico()
    historico.append(item)
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)


def mostrar_historico():
    historico = carregar_historico()
    if not historico:
        print("Nenhum download registrado ainda.")
        return

    print("\n" + "=" * 60)
    print("📜 HISTÓRICO DE DOWNLOADS")
    print("=" * 60)
    for i, item in enumerate(historico[-10:], 1):  # Últimos 10
        data = item.get("data", "---")
        titulo = item.get("titulo", "Sem título")
        tipo = item.get("tipo", "Vídeo")
        print(f"{i:2d}. [{data}] {tipo} - {titulo[:60]}")
    print("=" * 60)


def menu():
    print("\n" + "=" * 55)
    print("🎥 YOUTUBE DOWNLOADER - yt-dlp")
    print("=" * 55)
    print("1. Baixar Vídeo (melhor qualidade)")
    print("2. Baixar Apenas Áudio (MP3)")
    print("3. Baixar em Qualidade Específica")
    print("4. Baixar Playlist")
    print("5. Baixar Múltiplos Links")
    print("6. Ver Histórico de Downloads")
    print("7. Usar Cookies (para vídeos restritos)")
    print("8. Mudar Pasta de Download")
    print("0. Sair")
    print("=" * 55)


def main():
    pasta_download = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Downloads")
    usar_cookies = False

    if not os.path.exists(pasta_download):
        os.makedirs(pasta_download)

    while True:
        menu()
        escolha = input("\nEscolha uma opção (0-8): ").strip()

        if escolha == "0":
            print("👋 Até mais!")
            break

        elif escolha == "6":
            mostrar_historico()
            input("\nPressione ENTER para continuar...")
            continue

        elif escolha == "7":
            usar_cookies = not usar_cookies
            if usar_cookies and os.path.exists(COOKIES_ARQUIVO):
                print(f"✅ Cookies carregados de '{COOKIES_ARQUIVO}'")
            elif usar_cookies:
                print(
                    f"⚠️ Arquivo '{COOKIES_ARQUIVO}' não encontrado. Exporte seus cookies do navegador."
                )
            else:
                print("✅ Cookies desativados.")
            input("\nPressione ENTER...")
            continue

        # Configurações básicas
        if escolha == "1":
            formato = "bestvideo+bestaudio/best"
            tipo = "Vídeo"
        elif escolha == "2":
            formato = "bestaudio/best"
            tipo = "Áudio MP3"
        elif escolha == "3":
            q = input("Qualidade (720/1080/1440/2160): ").strip()
            altura = q if q in ["720", "1080", "1440", "2160"] else "1080"
            formato = f"best[height<={altura}]/best"
            tipo = f"Vídeo {altura}p"
        elif escolha in ["4", "5"]:
            formato = "bestvideo+bestaudio/best"
            tipo = "Playlist" if escolha == "4" else "Múltiplos Links"
        else:
            print("❌ Opção inválida!")
            continue

        # Coleta de links
        print(f"\n📋 Modo: {tipo}")
        urls = []
        print("Cole o(s) link(s) (um por linha). Digite 'pronto' quando terminar:")
        while True:
            link = input().strip()
            if link.lower() == "pronto":
                break
            if link:
                urls.append(link)

        if not urls:
            print("Nenhum link informado!")
            continue

        # Configuração do yt-dlp
        opcoes = {
            "outtmpl": f"{pasta_download}/%(title)s.%(ext)s",
            "merge_output_format": "mp4",
            "progress_hooks": [
                lambda d: (
                    print(f"  {d.get('status', '')} - {d.get('_percent_str', '')}")
                    if d.get("status") == "downloading"
                    else None
                )
            ],
            "ignoreerrors": True,
        }

        if formato:
            opcoes["format"] = formato
        if escolha == "2":  # Áudio MP3
            opcoes["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]
        if usar_cookies and os.path.exists(COOKIES_ARQUIVO):
            opcoes["cookiefile"] = COOKIES_ARQUIVO

        print(f"\n🔄 Iniciando download de {len(urls)} item(s)...\n")

        try:
            with YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(
                    urls[0], download=False
                )  # Pega info do primeiro
                titulo = (
                    info.get("title", "Desconhecido")
                    if len(urls) == 1
                    else f"{len(urls)} itens"
                )

                ydl.download(urls)

                # Salva no histórico
                historico_item = {
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "titulo": titulo,
                    "tipo": tipo,
                    "urls": urls,
                }
                salvar_historico(historico_item)

            print("\n✅ Download finalizado com sucesso!")

        except Exception as e:
            print(f"\n❌ Erro durante o download: {e}")

        input("\nPressione ENTER para voltar ao menu...")


if __name__ == "__main__":
    print("🚀 Iniciando YouTube Downloader...")
    main()
