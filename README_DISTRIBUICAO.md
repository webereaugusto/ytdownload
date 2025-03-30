# Guia de Distribuição - YouTube Downloader

Este documento explica como criar um executável do YouTube Downloader e distribuí-lo para outras pessoas.

## Criando o executável

### Passo 1: Instalar as dependências necessárias

```bash
pip install -r requirements_exe.txt
```

### Passo 2: Gerar o executável

Execute o script de build:

```bash
python build_exe.py
```

O executável será criado na pasta `dist` com o nome `YouTube_Downloader.exe`.

## Distribuindo o executável

### Método 1: Distribuição básica

Simplesmente compartilhe o arquivo `YouTube_Downloader.exe` com seus amigos. Eles podem:

1. Baixar o arquivo
2. Criar uma pasta em qualquer lugar no computador
3. Mover o arquivo para esta pasta
4. Clicar duas vezes para executar

O programa criará automaticamente uma pasta "Downloads" no mesmo diretório onde o executável está para salvar os vídeos baixados.

### Método 2: Criando um instalador (opcional)

Para uma experiência mais profissional, você pode criar um instalador usando ferramentas como:

- [Inno Setup](https://jrsoftware.org/isinfo.php) (Gratuito)
- [NSIS](https://nsis.sourceforge.io/Main_Page) (Gratuito)

### Método 3: Compactando o executável

Você também pode comprimir o executável em um arquivo zip ou rar:

1. Crie uma pasta chamada "YouTube Downloader"
2. Coloque o arquivo `YouTube_Downloader.exe` nesta pasta
3. Adicione um arquivo README.txt com instruções simples
4. Compacte a pasta em um arquivo .zip
5. Compartilhe este arquivo .zip

## Notas importantes sobre a distribuição

- **Tamanho do arquivo**: O executável pode ser grande (50-100 MB) porque inclui Python e todas as bibliotecas necessárias
- **Antivírus**: Alguns antivírus podem dar um falso positivo. Isso acontece com aplicativos PyInstaller porque eles são empacotados de forma semelhante a alguns malwares. Se necessário, instrua seus amigos a adicionarem o aplicativo como exceção no antivírus.
- **Windows Defender**: Para evitar o alerta do Windows SmartScreen, considere assinar digitalmente o executável (porém isso requer um certificado pago)

## Compatibilidade

- O executável funcionará apenas em **Windows**
- Foi testado em Windows 10/11
- Não requer direitos de administrador para executar
- Não requer qualquer instalação 