# 🎥 YT Downloader

Downloader simples e poderoso de vídeos do YouTube feito em Python.

## Como instalar

1. Baixe este repositório (Code → Download ZIP)
2. Extraia a pasta
3. Abra o terminal dentro da pasta do projeto e rode:

```bash
pip install -r requirements.txt
```

## Executar o programa:

Rode:

```bash
python yt_downloader.py
```

## Como usar Cookies (para vídeos com restrição de idade, +18, privados, etc)

### Alguns vídeos não baixam normalmente porque exigem login. Para resolver isso:

1. Instale a extensão

```bash
Get cookies.txt LOCALLY
```

ou baixe direto por [aqui](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
no Chrome.

2. Acesse o YouTube logado na sua conta.

3. Clique no ícone da extensão e selecione Export.

4. Salve o arquivo como cookies.txt na mesma pasta do programa.

5. No menu do programa, escolha a opção 7 para ativar os cookies.

**Para baixar vídeos normais não precisa fazer nada com cookies**

---

## Instalação do FFmpeg (necessário para unir vídeo e áudio)

Para baixar vídeos na melhor qualidade, o programa utiliza o FFmpeg para unir o vídeo e o áudio em um único arquivo.

### Instalação (Windows)

Abra o PowerShell e execute:

```powershell
winget install Gyan.FFmpeg
```

Após a instalação, feche e abra novamente o terminal.

Para verificar se a instalação foi concluída corretamente, execute:

```powershell
ffmpeg -version
```

Se aparecer a versão do FFmpeg, está tudo pronto.

> **Sem o FFmpeg**, vídeos baixados na melhor qualidade poderão ser salvos em dois arquivos separados (um de vídeo e outro de áudio), em vez de um único arquivo `.mp4`.
