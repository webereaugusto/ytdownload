import customtkinter as ctk
from PIL import Image, ImageTk
import yt_dlp
import os
from threading import Thread
import re
import subprocess
import sys

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
        self.main_frame = ctk.CTkFrame(self.window, fg_color=("rgba(43, 43, 43, 0.7)"))
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="YouTube Downloader",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=20)
        
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
                
            # Carrega a imagem usando PIL
            bg_image = Image.open(image_path)
            
            # Redimensiona a imagem para o tamanho da janela
            bg_image = bg_image.resize((600, 400), Image.LANCZOS)
            
            # Converte para formato compatível com tkinter
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            # Cria um label para exibir a imagem
            self.bg_label = ctk.CTkLabel(self.window, image=self.bg_photo, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
            # Envia o label para o fundo
            self.bg_label.lower()
            
            print("Imagem de fundo carregada com sucesso!")
            
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {str(e)}")
        
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
            
            # Configurações MUITO SIMPLES que devem funcionar para todos os vídeos
            ydl_opts = {
                # Usando o formato mais básico e compatível possível
                'format': 'best[ext=mp4]/best',  # Tenta o melhor formato mp4, ou qualquer formato se mp4 não estiver disponível
                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'noplaylist': True
            }
            
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
                        self.update_status("Erro: Acesso negado. Tente novamente mais tarde")
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