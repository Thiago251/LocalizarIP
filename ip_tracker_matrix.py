#!/usr/bin/env python3
"""
Localizador de IP - Estilo Matrix
Desenvolvido por Thiago Oliveira
Versão Python com Interface Gráfica
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import requests
import platform
import socket
import re
import json
from datetime import datetime
import threading
import time
import sys

class MatrixIPTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("IP Tracker ")
        self.root.geometry("900x700")
        self.root.configure(bg='#000000')
        self.root.resizable(True, True)
        
        # Variáveis
        self.output_text = []
        self.is_tracking = False
        
        # Configurar interface
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface gráfica no estilo Matrix"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#000000')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="═══ IP TRACKER  ═══",
            font=('Courier', 16, 'bold'),
            fg='#00FF00',
            bg='#000000'
        )
        title_label.pack(pady=(0, 10))
        
        # Subtítulo
        subtitle_label = tk.Label(
            main_frame,
            text="Desenvolvido por Thiago Oliveira",
            font=('Courier', 10),
            fg='#00AA00',
            bg='#000000'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame de opções
        options_frame = tk.Frame(main_frame, bg='#000000')
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Label de opção
        option_label = tk.Label(
            options_frame,
            text="Escolha uma opção:",
            font=('Courier', 11, 'bold'),
            fg='#00FF00',
            bg='#000000'
        )
        option_label.pack(anchor=tk.W)
        
        # Radio buttons
        self.option_var = tk.IntVar(value=1)
        
        radio1 = tk.Radiobutton(
            options_frame,
            text="1 - Rastrear meu IP atual",
            variable=self.option_var,
            value=1,
            font=('Courier', 10),
            fg='#00FF00',
            bg='#000000',
            selectcolor='#003300',
            activebackground='#000000',
            activeforeground='#00FF00',
            command=self.toggle_ip_entry
        )
        radio1.pack(anchor=tk.W, padx=20)
        
        radio2 = tk.Radiobutton(
            options_frame,
            text="2 - Rastrear um IP específico",
            variable=self.option_var,
            value=2,
            font=('Courier', 10),
            fg='#00FF00',
            bg='#000000',
            selectcolor='#003300',
            activebackground='#000000',
            activeforeground='#00FF00',
            command=self.toggle_ip_entry
        )
        radio2.pack(anchor=tk.W, padx=20)
        
        # Frame de entrada de IP
        ip_frame = tk.Frame(main_frame, bg='#000000')
        ip_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.ip_label = tk.Label(
            ip_frame,
            text="Digite o IP:",
            font=('Courier', 10),
            fg='#00FF00',
            bg='#000000'
        )
        self.ip_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.ip_entry = tk.Entry(
            ip_frame,
            font=('Courier', 10),
            fg='#00FF00',
            bg='#000000',
            insertbackground='#00FF00',
            disabledbackground='#000000',
            disabledforeground='#004400',
            width=20,
            relief=tk.SUNKEN,
            bd=2,
            state='disabled'
        )
        self.ip_entry.pack(side=tk.LEFT)
        
        self.ip_label.config(fg='#004400')
        
        # Botão de rastrear
        self.track_button = tk.Button(
            main_frame,
            text="▶ INICIAR RASTREAMENTO",
            font=('Courier', 11, 'bold'),
            fg='#000000',
            bg='#00FF00',
            activebackground='#00AA00',
            activeforeground='#000000',
            command=self.start_tracking,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3
        )
        self.track_button.pack(pady=15)
        
        # Área de texto para output
        self.text_area = scrolledtext.ScrolledText(
            main_frame,
            font=('Courier', 9),
            fg='#00FF00',
            bg='#000000',
            insertbackground='#00FF00',
            wrap=tk.WORD,
            height=25,
            state='disabled'
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=(10, 10))
        
        # Frame de botões inferiores
        bottom_frame = tk.Frame(main_frame, bg='#000000')
        bottom_frame.pack(fill=tk.X)
        
        # Botão de exportar
        self.export_button = tk.Button(
            bottom_frame,
            text="💾 EXPORTAR PARA TXT",
            font=('Courier', 10, 'bold'),
            fg='#000000',
            bg='#00AA00',
            activebackground='#008800',
            activeforeground='#000000',
            command=self.export_to_txt,
            cursor='hand2',
            state='disabled'
        )
        self.export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão de limpar
        clear_button = tk.Button(
            bottom_frame,
            text="🗑 LIMPAR",
            font=('Courier', 10, 'bold'),
            fg='#000000',
            bg='#00AA00',
            activebackground='#008800',
            activeforeground='#000000',
            command=self.clear_output,
            cursor='hand2'
        )
        clear_button.pack(side=tk.LEFT)
        
    def toggle_ip_entry(self):
        """Habilita/desabilita entrada de IP baseado na opção selecionada"""
        if self.option_var.get() == 2:
            self.ip_entry.config(
                state='normal',
                bg='#001100',
                relief=tk.SUNKEN
            )
            self.ip_label.config(fg='#00FF00')
            self.ip_entry.focus_set()
        else:
            self.ip_entry.config(
                state='disabled',
                bg='#000000',
                relief=tk.FLAT
            )
            self.ip_label.config(fg='#004400')
            self.ip_entry.delete(0, tk.END)
            
    def print_matrix(self, text, color='#00FF00', delay=0.01):
        """Imprime texto com efeito Matrix (caractere por caractere)"""
        self.text_area.config(state='normal')
        
        for char in text:
            self.text_area.insert(tk.END, char, color)
            self.text_area.see(tk.END)
            self.text_area.update()
            time.sleep(delay)
        
        self.text_area.insert(tk.END, '\n')
        self.text_area.config(state='disabled')
        self.output_text.append(text)
        
    def print_fast(self, text, color='#00FF00'):
        """Imprime texto instantaneamente"""
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, text + '\n', color)
        self.text_area.see(tk.END)
        self.text_area.config(state='disabled')
        self.output_text.append(text)
        
    def clear_output(self):
        """Limpa a área de texto"""
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state='disabled')
        self.output_text = []
        self.export_button.config(state='disabled')
        
    def validate_ip(self, ip):
        """Valida formato de endereço IP"""
        pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return re.match(pattern, ip) is not None
    
    def get_local_info(self):
        """Obtém informações do sistema local"""
        self.print_matrix("═" * 60, delay=0.005)
        self.print_matrix("   LOCALIZADOR DE IP - MATRIX STYLE", delay=0.02)
        self.print_matrix("   Desenvolvido por Thiago Oliveira", delay=0.02)
        self.print_matrix("═" * 60, delay=0.005)
        self.print_fast("")
        
        self.print_matrix("[INFO LOCAL DO SISTEMA]", color='#FFFF00', delay=0.01)
        
        try:
            hostname = socket.gethostname()
            system = platform.system()
            release = platform.release()
            version = platform.version()
            machine = platform.machine()
            processor = platform.processor()
            
            self.print_fast(f"Nome do Computador: {hostname}")
            self.print_fast(f"Sistema Operacional: {system}")
            self.print_fast(f"Versão: {release}")
            self.print_fast(f"Build: {version}")
            self.print_fast(f"Arquitetura: {machine}")
            self.print_fast(f"Processador: {processor}")
            self.print_fast("")
            
        except Exception as e:
            self.print_fast(f"[ERRO] Não foi possível obter informações locais: {e}", color='#FF0000')
            self.print_fast("")
    
    def get_public_ip(self):
        """Obtém o IP público do usuário"""
        self.print_matrix("[OBTENDO IP PÚBLICO...]", color='#FFFF00', delay=0.01)
        
        apis = [
            ("https://api.ipify.org?format=json", "ip"),
            ("https://api.my-ip.io/ip.json", "ip"),
            ("https://ipapi.co/json/", "ip"),
        ]
        
        for api_url, key in apis:
            try:
                self.print_fast(f"→ Tentando API: {api_url.split('/')[2]}...")
                response = requests.get(api_url, timeout=5)
                response.raise_for_status()
                
                if key:
                    data = response.json()
                    ip = data.get(key)
                else:
                    ip = response.text.strip()
                
                if ip and self.validate_ip(ip):
                    self.print_fast(f"✓ IP Público obtido: {ip}", color='#00FF00')
                    self.print_fast("")
                    return ip
                    
            except Exception as e:
                self.print_fast(f"✗ Falha: {str(e)}", color='#FF6600')
                continue
        
        self.print_fast("[ERRO] Não foi possível obter o IP público.", color='#FF0000')
        return None
    
    def get_geolocation(self, ip):
        """Obtém informações de geolocalização do IP"""
        self.print_matrix("[RASTREANDO GEOLOCALIZAÇÃO...]", color='#FFFF00', delay=0.01)
        self.print_fast(f"→ Alvo: {ip}")
        self.print_fast("")
        
        # Lista de APIs para tentar (6 APIs robustas)
        apis = [
            {
                'name': 'ipapi.co',
                'url': f'https://ipapi.co/{ip}/json/',
                'parser': self.parse_ipapi_co
            },
            {
                'name': 'ipwhois.app',
                'url': f'http://ipwhois.app/json/{ip}',
                'parser': self.parse_ipwhois
            },
            {
                'name': 'ipinfo.io',
                'url': f'https://ipinfo.io/{ip}/json',
                'parser': self.parse_ipinfo
            },
            {
                'name': 'freeipapi.com',
                'url': f'https://freeipapi.com/api/json/{ip}',
                'parser': self.parse_freeipapi
            },
            {
                'name': 'ip2location.io',
                'url': f'https://api.ip2location.io/?ip={ip}',
                'parser': self.parse_ip2location
            }
        ]
        
        for api in apis:
            try:
                self.print_fast(f"→ Consultando API: {api['name']}...")
                response = requests.get(api['url'], timeout=10)
                response.raise_for_status()
                data = response.json()
                
                # Verificar se há erro na resposta
                if 'error' in data or data.get('status') == 'fail':
                    error_msg = data.get('reason', data.get('message', 'Erro desconhecido'))
                    self.print_fast(f"✗ API retornou erro: {error_msg}", color='#FF6600')
                    continue
                
                self.print_fast(f"✓ Dados obtidos com sucesso!", color='#00FF00')
                self.print_fast("")
                
                # Parse dos dados
                api['parser'](data)
                return True
                
            except requests.exceptions.Timeout:
                self.print_fast(f"✗ Timeout ao consultar {api['name']}", color='#FF6600')
            except requests.exceptions.RequestException as e:
                self.print_fast(f"✗ Erro de conexão com {api['name']}: {str(e)}", color='#FF6600')
            except Exception as e:
                self.print_fast(f"✗ Erro ao processar dados de {api['name']}: {str(e)}", color='#FF6600')
        
        self.print_fast("")
        self.print_fast("[ERRO] Não foi possível obter informações de geolocalização.", color='#FF0000')
        return False
    
    def parse_ipapi_co(self, data):
        """Parse dos dados da API ipapi.co"""
        self.print_matrix("═" * 60, delay=0.005)
        self.print_matrix("[INFORMAÇÕES DE GEOLOCALIZAÇÃO]", color='#00FFFF', delay=0.01)
        self.print_matrix("═" * 60, delay=0.005)
        
        fields = [
            ('IP', 'ip'),
            ('Versão IP', 'version'),
            ('Cidade', 'city'),
            ('Região', 'region'),
            ('País', 'country_name'),
            ('Código do País', 'country_code'),
            ('Continente', 'continent_code'),
            ('Latitude', 'latitude'),
            ('Longitude', 'longitude'),
            ('CEP/Código Postal', 'postal'),
            ('Timezone', 'timezone'),
            ('UTC Offset', 'utc_offset'),
            ('Código de Área', 'country_calling_code'),
            ('Moeda', 'currency'),
            ('Idiomas', 'languages'),
            ('ASN', 'asn'),
            ('Organização/ISP', 'org'),
        ]
        
        for label, key in fields:
            value = data.get(key, 'N/A')
            if value and value != 'N/A':
                self.print_fast(f"{label}: {value}")
        
        # Link do Google Maps
        lat = data.get('latitude')
        lon = data.get('longitude')
        if lat and lon:
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            self.print_fast("")
            self.print_fast(f"📍 Google Maps: {maps_url}", color='#FF00FF')
    
    def parse_ip_api_com(self, data):
        """Parse dos dados da API ip-api.com"""
        self.print_matrix("═" * 60, delay=0.005)
        self.print_matrix("[INFORMAÇÕES DE GEOLOCALIZAÇÃO]", color='#00FFFF', delay=0.01)
        self.print_matrix("═" * 60, delay=0.005)
        
        fields = [
            ('IP', 'query'),
            ('Cidade', 'city'),
            ('Região', 'regionName'),
            ('País', 'country'),
            ('Código do País', 'countryCode'),
            ('Continente', 'continent_name'),
            ('Latitude', 'lat'),
            ('Longitude', 'lon'),
            ('CEP', 'zip'),
            ('Tipo', 'type'),
        ]
        
        for label, key in fields:
            value = data.get(key, 'N/A')
            if value and value != 'N/A':
                self.print_fast(f"{label}: {value}")
        
        # Link do Google Maps
        lat = data.get('lat')
        lon = data.get('lon')
        if lat and lon:
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            self.print_fast("")
            self.print_fast(f"📍 Google Maps: {maps_url}", color='#FF00FF')
    
    def parse_ipwhois(self, data):
        """Parse dos dados da API ipwhois.app"""
        self.print_matrix("═" * 60, delay=0.005)
        self.print_matrix("[INFORMAÇÕES DE GEOLOCALIZAÇÃO]", color='#00FFFF', delay=0.01)
        self.print_matrix("═" * 60, delay=0.005)
        
        fields = [
            ('IP', 'ip'),
            ('Cidade', 'city'),
            ('Região', 'region'),
            ('País', 'country'),
            ('Código do País', 'country_code'),
            ('Continente', 'continent'),
            ('Latitude', 'latitude'),
            ('Longitude', 'longitude'),
            ('Timezone', 'timezone'),
            ('ISP', 'isp'),
            ('Organização', 'org'),
            ('ASN', 'asn'),
        ]
        
        for label, key in fields:
            value = data.get(key, 'N/A')
            if value and value != 'N/A':
                self.print_fast(f"{label}: {value}")
        
        # Link do Google Maps
        lat = data.get('latitude')
        lon = data.get('longitude')
        if lat and lon:
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            self.print_fast("")
            self.print_fast(f"📍 Google Maps: {maps_url}", color='#FF00FF')
    
    def parse_ipinfo(self, data):
        """Parse dos dados da API ipinfo.io"""
        self.print_matrix("═" * 60, delay=0.005)
        self.print_matrix("[INFORMAÇÕES DE GEOLOCALIZAÇÃO]", color='#00FFFF', delay=0.01)
        self.print_matrix("═" * 60, delay=0.005)
        
        # ipinfo.io retorna localização como "City, Region"
        loc = data.get('loc', '').split(',')
        lat = loc[0] if len(loc) > 0 else 'N/A'
        lon = loc[1] if len(loc) > 1 else 'N/A'
        
        fields = [
            ('IP', 'ip'),
            ('Cidade', 'city'),
            ('Região', 'region'),
            ('País', 'country'),
            ('Latitude', lat),
            ('Longitude', lon),
            ('CEP', 'postal'),
            ('Timezone', 'timezone'),
            ('Organização/ISP', 'org'),
        ]
        
        for label, value in fields:
            if isinstance(value, str) and value in data:
                value = data.get(value, 'N/A')
            if value and value != 'N/A':
                self.print_fast(f"{label}: {value}")
        
        # Link do Google Maps
        if lat != 'N/A' and lon != 'N/A':
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            self.print_fast("")
            self.print_fast(f"📍 Google Maps: {maps_url}", color='#FF00FF')
    
    def parse_freeipapi(self, data):
        """Parse dos dados da API freeipapi.com"""
        self.print_matrix("═" * 60, delay=0.005)
        self.print_matrix("[INFORMAÇÕES DE GEOLOCALIZAÇÃO]", color='#00FFFF', delay=0.01)
        self.print_matrix("═" * 60, delay=0.005)
        
        fields = [
            ('IP', 'ipAddress'),
            ('Versão IP', 'ipVersion'),
            ('Cidade', 'cityName'),
            ('Região', 'regionName'),
            ('País', 'countryName'),
            ('Código do País', 'countryCode'),
            ('Continente', 'continent'),
            ('Latitude', 'latitude'),
            ('Longitude', 'longitude'),
            ('CEP', 'zipCode'),
            ('Timezone', 'timeZone'),
            ('Moeda', 'currency'),
            ('Idioma', 'language'),
        ]
        
        for label, key in fields:
            value = data.get(key, 'N/A')
            if value and value != 'N/A':
                self.print_fast(f"{label}: {value}")
        
        # Link do Google Maps
        lat = data.get('latitude')
        lon = data.get('longitude')
        if lat and lon:
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            self.print_fast("")
            self.print_fast(f"📍 Google Maps: {maps_url}", color='#FF00FF')
    
    def parse_ip2location(self, data):
        """Parse dos dados da API ip2location.io"""
        self.print_matrix("═" * 60, delay=0.005)
        self.print_matrix("[INFORMAÇÕES DE GEOLOCALIZAÇÃO]", color='#00FFFF', delay=0.01)
        self.print_matrix("═" * 60, delay=0.005)
        
        fields = [
            ('IP', 'ip'),
            ('Cidade', 'city_name'),
            ('Região', 'region_name'),
            ('País', 'country_name'),
            ('Código do País', 'country_code'),
            ('Latitude', 'latitude'),
            ('Longitude', 'longitude'),
            ('CEP', 'zip_code'),
            ('Timezone', 'time_zone'),
            ('ISP', 'isp'),
            ('Domínio', 'domain'),
            ('ASN', 'asn'),
            ('AS', 'as'),
        ]
        
        for label, key in fields:
            value = data.get(key, 'N/A')
            if value and value != 'N/A':
                self.print_fast(f"{label}: {value}")
        
        # Link do Google Maps
        lat = data.get('latitude')
        lon = data.get('longitude')
        if lat and lon:
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            self.print_fast("")
            self.print_fast(f"📍 Google Maps: {maps_url}", color='#FF00FF')
    
    def track_ip_thread(self, ip=None):
        """Thread para rastrear IP sem bloquear a interface"""
        try:
            # Informações locais
            self.get_local_info()
            
            # Obter IP
            if ip is None:
                ip = self.get_public_ip()
                if not ip:
                    self.is_tracking = False
                    self.track_button.config(state='normal', text="▶ INICIAR RASTREAMENTO")
                    return
            else:
                self.print_matrix("[IP ESPECÍFICO INFORMADO]", color='#FFFF00', delay=0.01)
                self.print_fast(f"IP: {ip}")
                self.print_fast("")
            
            # Geolocalização
            success = self.get_geolocation(ip)
            
            # Finalização
            self.print_fast("")
            self.print_matrix("═" * 60, delay=0.005)
            if success:
                self.print_matrix("✓ RASTREAMENTO CONCLUÍDO COM SUCESSO!", color='#00FF00', delay=0.02)
            else:
                self.print_matrix("⚠ RASTREAMENTO CONCLUÍDO COM ERROS", color='#FFFF00', delay=0.02)
            self.print_matrix("═" * 60, delay=0.005)
            self.print_fast("")
            self.print_fast(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            self.print_fast("Desenvolvido por: Thiago Oliveira")
            
            # Habilitar botão de exportar
            self.export_button.config(state='normal')
            
        except Exception as e:
            self.print_fast("")
            self.print_fast(f"[ERRO CRÍTICO] {str(e)}", color='#FF0000')
            
        finally:
            self.is_tracking = False
            self.track_button.config(state='normal', text="▶ INICIAR RASTREAMENTO")
    
    def start_tracking(self):
        """Inicia o rastreamento de IP"""
        if self.is_tracking:
            return
        
        # Limpar output anterior
        self.clear_output()
        
        # Verificar opção selecionada
        if self.option_var.get() == 2:
            ip = self.ip_entry.get().strip()
            if not ip:
                messagebox.showerror("Erro", "Por favor, digite um endereço IP!")
                return
            if not self.validate_ip(ip):
                messagebox.showerror("Erro", "Endereço IP inválido!\nFormato correto: xxx.xxx.xxx.xxx")
                return
        else:
            ip = None
        
        # Desabilitar botão
        self.is_tracking = True
        self.track_button.config(state='disabled', text="⏳ RASTREANDO...")
        
        # Iniciar thread
        thread = threading.Thread(target=self.track_ip_thread, args=(ip,), daemon=True)
        thread.start()
    
    def export_to_txt(self):
        """Exporta os resultados para arquivo TXT"""
        if not self.output_text:
            messagebox.showwarning("Aviso", "Não há dados para exportar!")
            return
        
        # Diálogo para salvar arquivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"rastreamento_ip_{timestamp}.txt"
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os Arquivos", "*.*")],
            initialfile=default_filename
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.output_text))
                
                messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso!\n\n{filepath}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{str(e)}")

def main():
    """Função principal"""
    root = tk.Tk()
    app = MatrixIPTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
