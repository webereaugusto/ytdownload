import PyInstaller.__main__
import os
import shutil

# Limpa a pasta dist e build se existirem
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

# Lista de arquivos para incluir no executável
additional_files = [
    ("background.jpg", "."),
    ("perfil.png", "."),
    ("README.md", ".")
]

# Converte a lista em formato adequado para o PyInstaller
datas = []
for src, dst in additional_files:
    if os.path.exists(src):
        datas.append((src, dst))

datas_arg = ";".join([f"{src}{os.pathsep}{dst}" for src, dst in datas])

# Configura argumentos do PyInstaller
args = [
    'youtube_downloader.py',               # Script principal
    '--name=YouTube_Downloader',           # Nome do executável
    '--onefile',                           # Cria um único arquivo executável
    '--windowed',                          # Não mostra console ao executar
    '--icon=perfil.png',                   # Ícone do executável (usando a imagem de perfil)
    f'--add-data={datas_arg}',             # Adiciona arquivos de dados
    '--clean',                             # Limpa arquivos temporários
    '--noconsole'                          # Não mostra console (aplicação GUI)
]

# Executa o PyInstaller
PyInstaller.__main__.run(args)

print("Executável criado com sucesso na pasta 'dist'!")
print("Instruções para distribuição:")
print("1. Compartilhe o arquivo 'dist/YouTube_Downloader.exe' com seus amigos")
print("2. Crie uma pasta 'Downloads' no mesmo local do executável (opcional)")
print("3. O programa criará a pasta automaticamente se não existir") 