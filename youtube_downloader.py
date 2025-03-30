import customtkinter as ctk
from PIL import Image
import yt_dlp
import os
from threading import Thread
import re
import subprocess
import sys
import random

class YouTubeDownloader:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("YouTube Downloader")
        self.window.geometry("600x400")
        self.window.configure(fg_color="#2b2b2b")
        
        # Carregar a imagem de fundo
        self.load_background_image()
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Frame principal com transparência
        self.main_frame = ctk.CTkFrame(self.window, fg_color=("#2b2b2b", "#2b2b2b"))
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Frame para o título e a foto de perfil
        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.title_frame.pack(pady=20, fill="x")
        
        # Carrega a imagem do perfil
        self.load_profile_image()
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="YouTube Downloader",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(side="left", padx=10)
        
        # Campo de URL
        self.url_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.url_frame.pack(pady=10, padx=20, fill="x")
        
        self.url_label = ctk.CTkLabel(
            self.url_frame,
            text="URL do Vídeo:",
            font=("Helvetica", 14)
        )
        self.url_label.pack(side="left", padx=10)
        
        self.url_entry = ctk.CTkEntry(
            self.url_frame,
            width=400,
            height=35,
            placeholder_text="Cole a URL do vídeo aqui"
        )
        self.url_entry.pack(side="left", padx=10)
        
        # Botão de download
        self.download_button = ctk.CTkButton(
            self.main_frame,
            text="Baixar Vídeo",
            command=self.start_download,
            width=200,
            height=40
        )
        self.download_button.pack(pady=20)
        
        # Status
        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            font=("Helvetica", 12)
        )
        self.status_label.pack(pady=10)
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.set(0)
        
    def load_background_image(self):
        """Carrega a imagem de fundo e configura como plano de fundo da janela"""
        try:
            # Caminho para a imagem
            image_path = os.path.join(os.getcwd(), "background.jpg")
            
            # Verifica se o arquivo existe
            if not os.path.exists(image_path):
                print("Imagem de fundo não encontrada:", image_path)
                return
                
            # Carrega a imagem usando CTkImage (próprio do CustomTkinter)
            self.bg_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(600, 400)
            )
            
            # Cria um label para exibir a imagem
            self.bg_label = ctk.CTkLabel(
                self.window, 
                image=self.bg_image, 
                text=""
            )
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Envia o label para o fundo
            self.bg_label.lower()
            
            print("Imagem de fundo carregada com sucesso!")
            
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {str(e)}")
    
    def load_profile_image(self):
        """Carrega a imagem de perfil circular"""
        try:
            # Caminho para a imagem
            image_path = os.path.join(os.getcwd(), "perfil.png")
            
            # Verifica se o arquivo existe
            if not os.path.exists(image_path):
                print("Imagem de perfil não encontrada:", image_path)
                return
                
            # Carrega a imagem usando CTkImage (próprio do CustomTkinter)
            self.profile_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(50, 50)  # Tamanho da foto de perfil
            )
            
            # Cria um label para exibir a imagem
            self.profile_label = ctk.CTkLabel(
                self.title_frame, 
                image=self.profile_image, 
                text=""
            )
            self.profile_label.pack(side="right", padx=20)
            
            print("Imagem de perfil carregada com sucesso!")
            
        except Exception as e:
            print(f"Erro ao carregar imagem de perfil: {str(e)}")
    
    def get_random_user_agent(self):
        """Retorna um User-Agent aleatório"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/122.0.0.0 Safari/537.36'
        ]
        return random.choice(user_agents)
        
    def update_status(self, message):
        self.status_label.configure(text=message)
        print(f"Status: {message}")
        
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                total_bytes = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                if total_bytes:
                    downloaded = d.get('downloaded_bytes', 0)
                    progress = downloaded / total_bytes
                    self.progress_bar.set(progress)
                    percent = progress * 100
                    speed = d.get('speed', 0)
                    if speed:
                        speed_mb = speed / 1024 / 1024
                        self.update_status(f"Baixando: {percent:.1f}% ({speed_mb:.1f} MB/s)")
                    else:
                        self.update_status(f"Baixando: {percent:.1f}%")
            except Exception as e:
                print(f"Erro no progresso: {str(e)}")
        elif d['status'] == 'finished':
            self.update_status("Download concluído. Finalizando...")
                
    def download_video(self):
        try:
            url = self.url_entry.get().strip()
            if not url:
                self.update_status("Por favor, insira uma URL válida")
                return
                
            # Remove @ se existir no início da URL
            if url.startswith('@'):
                url = url[1:]
                
            self.update_status("Conectando ao YouTube...")
            
            # Configurações do yt-dlp
            download_path = os.path.join(os.getcwd(), "Downloads")
            os.makedirs(download_path, exist_ok=True)
            
            # User agent aleatório
            user_agent = self.get_random_user_agent()
            
            # Configurações avançadas para contornar restrições
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'noplaylist': True,
                'cookiefile': None,  # Sem cookies salvos
                'nocheckcertificate': True,  # Não verifica certificados SSL
                'ignoreerrors': True,  # Ignora erros
                'no_warnings': False,  # Mostra avisos para debug
                'quiet': False,  # Não silencia saída
                'verbose': True,  # Mostra informações detalhadas
                # Opções para contornar restrições
                'socket_timeout': 30,  # Timeout mais longo
                'retries': 10,  # Mais tentativas
                'fragment_retries': 10,  # Mais tentativas para fragmentos
                'skip_download': False,
                'geo_bypass': True,  # Tenta contornar restrições geográficas
                'geo_bypass_country': 'BR',  # País para bypass
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],  # Tenta simular cliente Android e Web
                        'player_skip': ['js', 'configs', 'webpage']  # Pula verificações problemáticas
                    }
                },
                'http_headers': {
                    'User-Agent': user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Origin': 'https://www.youtube.com',
                    'Referer': 'https://www.youtube.com/'
                }
            }
            
            print(f"Tentando baixar com User-Agent: {user_agent}")
            print(f"URL: {url}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    # Faz o download diretamente
                    info = ydl.extract_info(url, download=True)
                    
                    if info:
                        title = info.get('title', 'Video')
                        self.update_status(f"Download concluído: {title}")
                        self.progress_bar.set(1)
                    else:
                        self.update_status("Erro: Não foi possível obter informações do vídeo")
                except Exception as e:
                    error_msg = str(e)
                    print(f"Erro detalhado: {error_msg}")
                    if "Video unavailable" in error_msg:
                        self.update_status("Erro: Vídeo não disponível (pode ser privado ou ter sido removido)")
                    elif "HTTP Error 400" in error_msg:
                        self.update_status("Erro: Problema ao acessar o vídeo. Tente novamente em alguns minutos.")
                    elif "HTTP Error 403" in error_msg:
                        self.update_status("Erro: Acesso negado. YouTube está bloqueando os downloads.")
                        print("Tente atualizar o yt-dlp para a versão mais recente:")
                        print("pip install -U yt-dlp")
                    else:
                        self.update_status(f"Erro: {error_msg}")
                    self.progress_bar.set(0)
                    
        except Exception as e:
            print(f"Erro geral: {str(e)}")
            self.update_status(f"Erro: {str(e)}")
            self.progress_bar.set(0)
            
    def start_download(self):
        self.progress_bar.set(0)
        self.update_status("Iniciando processo de download...")
        Thread(target=self.download_video).start()
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = YouTubeDownloader()
    app.run() 