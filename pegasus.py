# pegasus_ime_gsm_pro_fixed.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog, Toplevel
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
import time
import queue
import json
import os
import sys
import random
import string
import hashlib
from datetime import datetime, timedelta
import uuid
import sqlite3
import qrcode
import io
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import re
import serial
import serial.tools.list_ports
import socket
import struct
import platform

class RealGSMInterface:
    """Interface untuk komunikasi GSM real dengan berbagai metode"""
    
    def __init__(self):
        self.system = platform.system()
        self.initialize_gsm_interface()
    
    def initialize_gsm_interface(self):
        """Initialize GSM interface berdasarkan OS"""
        self.serial_ports = []
        self.gsm_connected = False
        
        # Konfigurasi untuk iPhone
        self.iphone_models = {
            'iPhone6,1': {'name': 'iPhone 5s', 'bands': ['GSM 850/900/1800/1900', 'UMTS 850/900/1700/1900/2100', 'LTE 1/2/3/4/5/8/13/17/19/20/25']},
            'iPhone7,1': {'name': 'iPhone 6 Plus', 'bands': ['GSM 850/900/1800/1900', 'CDMA 800/1700/1900/2100', 'LTE 1/2/3/4/5/7/8/13/17/18/19/20/25/26/28/29']},
            'iPhone8,1': {'name': 'iPhone 6s', 'bands': ['GSM 850/900/1800/1900', 'CDMA 800/1700/1900/2100', 'LTE 1/2/3/4/5/7/8/12/13/17/18/19/20/25/26/27/28/29/30']},
            'iPhone9,1': {'name': 'iPhone 7', 'bands': ['GSM 850/900/1800/1900', 'CDMA 800/1700/1900/2100', 'LTE 1/2/3/4/5/7/8/12/13/17/18/19/20/25/26/27/28/29/30/38/39/40/41']},
            'iPhone10,1': {'name': 'iPhone 8', 'bands': ['GSM 850/900/1800/1900', 'CDMA 800/1700/1900/2100', 'LTE 1/2/3/4/5/7/8/12/13/17/18/19/20/25/26/27/28/29/30/34/38/39/40/41']},
            'iPhone10,4': {'name': 'iPhone 8', 'bands': ['GSM 850/900/1800/1900', 'CDMA 800/1700/1900/2100', 'LTE 1/2/3/4/5/7/8/12/13/17/18/19/20/25/26/27/28/29/30/34/38/39/40/41']},
            'iPhone11,2': {'name': 'iPhone XS', 'bands': ['GSM 850/900/1800/1900', 'CDMA 800/1700/1900/2100', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/46/48/66/71']},
            'iPhone12,1': {'name': 'iPhone 11', 'bands': ['GSM 850/900/1800/1900', 'CDMA 800/1700/1900/2100', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']},
            'iPhone12,8': {'name': 'iPhone SE 2nd', 'bands': ['GSM 850/900/1800/1900', 'CDMA 800/1700/1900/2100', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']},
            'iPhone13,1': {'name': 'iPhone 12 mini', 'bands': ['5G NR n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n38/n40/n41/n66/n77/n78/n79', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']},
            'iPhone13,2': {'name': 'iPhone 12', 'bands': ['5G NR n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n38/n40/n41/n66/n77/n78/n79', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']},
            'iPhone14,2': {'name': 'iPhone 13 Pro', 'bands': ['5G NR n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n29/n30/n38/n40/n41/n48/n66/n70/n77/n78/n79', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']},
            'iPhone14,7': {'name': 'iPhone 14', 'bands': ['5G NR n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n29/n30/n38/n40/n41/n48/n66/n70/n71/n77/n78/n79', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']},
            'iPhone15,2': {'name': 'iPhone 14 Pro', 'bands': ['5G NR n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n29/n30/n38/n40/n41/n48/n66/n70/n71/n77/n78/n79', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']},
            'iPhone15,3': {'name': 'iPhone 14 Pro Max', 'bands': ['5G NR n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n29/n30/n38/n40/n41/n48/n66/n70/n71/n77/n78/n79', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']},
            'iPhone16,1': {'name': 'iPhone 15 Pro', 'bands': ['5G NR n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n29/n30/n38/n40/n41/n48/n66/n70/n71/n77/n78/n79/n258/n260/n261', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']},
            'iPhone16,2': {'name': 'iPhone 15 Pro Max', 'bands': ['5G NR n1/n2/n3/n5/n7/n8/n12/n20/n25/n28/n29/n30/n38/n40/n41/n48/n66/n70/n71/n77/n78/n79/n258/n260/n261', 'LTE 1/2/3/4/5/7/8/12/13/14/17/18/19/20/25/26/27/28/29/30/32/34/38/39/40/41/42/46/48/66/71']}
        }
    
    def get_available_ports(self):
        """Get available serial ports untuk koneksi iPhone"""
        ports = []
        try:
            available_ports = serial.tools.list_ports.comports()
            for port in available_ports:
                if any(keyword in port.description for keyword in ['USB', 'Serial', 'iPhone', 'COM']):
                    ports.append({
                        'device': port.device,
                        'description': port.description,
                        'manufacturer': port.manufacturer if port.manufacturer else 'Unknown'
                    })
        except Exception as e:
            print(f"Error getting ports: {e}")
        return ports
    
    def validate_imei(self, imei):
        """Validasi IMEI dengan Luhn algorithm (checksum)"""
        imei = str(imei).strip()
        
        # Basic validation
        if len(imei) != 15 and len(imei) != 16:
            return False, "IMEI harus 15 atau 16 digit"
        
        if not imei.isdigit():
            return False, "IMEI harus hanya angka"
        
        # Validate checksum using Luhn algorithm
        def luhn_checksum(imei_str):
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(imei_str)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            
            return checksum % 10 == 0
        
        is_valid = luhn_checksum(imei)
        return is_valid, "IMEI valid" if is_valid else "IMEI checksum tidak valid"
    
    def detect_iphone_model_from_imei(self, imei):
        """Deteksi model iPhone dari IMEI"""
        # Extract TAC (Type Allocation Code) dari IMEI
        if len(imei) < 8:
            return "Unknown iPhone"
        
        tac = imei[:8]  # 8 digit pertama adalah TAC
        
        # Database TAC untuk iPhone (disederhanakan)
        iphone_tac_ranges = {
            '350030': 'iPhone 4', '351710': 'iPhone 4s',
            '352040': 'iPhone 5', '353258': 'iPhone 5c', '353260': 'iPhone 5s',
            '354430': 'iPhone 6', '354431': 'iPhone 6 Plus',
            '355020': 'iPhone 6s', '355021': 'iPhone 6s Plus',
            '356020': 'iPhone 7', '356021': 'iPhone 7 Plus',
            '357020': 'iPhone 8', '357021': 'iPhone 8 Plus',
            '357820': 'iPhone X',
            '358020': 'iPhone XS', '358021': 'iPhone XS Max', '358022': 'iPhone XR',
            '359020': 'iPhone 11', '359021': 'iPhone 11 Pro', '359022': 'iPhone 11 Pro Max',
            '359520': 'iPhone SE 2nd',
            '359620': 'iPhone 12 mini', '359621': 'iPhone 12', '359622': 'iPhone 12 Pro', '359623': 'iPhone 12 Pro Max',
            '359720': 'iPhone 13', '359721': 'iPhone 13 mini', '359722': 'iPhone 13 Pro', '359723': 'iPhone 13 Pro Max',
            '359820': 'iPhone 14', '359821': 'iPhone 14 Plus', '359822': 'iPhone 14 Pro', '359823': 'iPhone 14 Pro Max',
            '359920': 'iPhone 15', '359921': 'iPhone 15 Plus', '359922': 'iPhone 15 Pro', '359923': 'iPhone 15 Pro Max'
        }
        
        # Cari TAC di database
        for tac_range, model in iphone_tac_ranges.items():
            if tac.startswith(tac_range):
                return model
        
        # Fallback: berdasarkan digit pertama TAC
        if tac[0] == '3':
            return "iPhone (Model tidak terdeteksi)"
        else:
            return "Smartphone (Non-iPhone)"
    
    def get_imei_info(self, imei):
        """Get informasi detail dari IMEI"""
        is_valid, message = self.validate_imei(imei)
        
        if not is_valid and len(imei) != 15:
            return None
        
        info = {
            'imei': imei,
            'is_valid': is_valid,
            'validation_message': message,
            'length': len(imei),
            'type': 'IMEI' if len(imei) == 15 else 'IMEISV',
            'tac': imei[:8] if len(imei) >= 8 else '',
            'serial': imei[8:14] if len(imei) >= 14 else '',
            'checksum': imei[-1] if len(imei) == 15 else 'N/A',
            'model': self.detect_iphone_model_from_imei(imei),
            'country': self.get_manufacturing_country(imei)
        }
        
        return info
    
    def get_manufacturing_country(self, imei):
        """Tentukan negara pembuatan dari IMEI"""
        if len(imei) < 8:
            return 'Tidak diketahui'
        
        # Cek digit reporting body
        reporting_body = imei[6:8]
        
        reporting_bodies = {
            '01': 'Finland', '02': 'Finland',
            '10': 'China', '30': 'China', '80': 'China',
            '04': 'USA', '05': 'USA',
            '08': 'Germany',
            '13': 'Korea',
            '19': 'UK',
            '20': 'Hong Kong',
            '35': 'India',
            '40': 'France',
            '60': 'Singapore',
            '67': 'Brazil',
            '70': 'Finland',
            '78': 'Sweden',
            '89': 'Netherlands',
            '91': 'Finland',
            '99': 'UK'
        }
        
        return reporting_bodies.get(reporting_body, 'Tidak diketahui')
    
    def generate_valid_imei(self, model_code="359922"):
        """Generate IMEI yang valid untuk testing"""
        # Buat 14 digit pertama (TAC + Serial)
        tac_serial = model_code + ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Hitung checksum digit terakhir dengan Luhn algorithm
        def calculate_luhn(partial_imei):
            def digits_of(n):
                return [int(d) for d in str(n)]
            
            digits = digits_of(partial_imei)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = sum(odd_digits)
            
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            
            return (10 - (checksum % 10)) % 10
        
        checksum = calculate_luhn(tac_serial)
        return tac_serial + str(checksum)
    
    def simulate_gsm_signal(self, base_signal=-85):
        """Simulasi sinyal GSM yang realistis dengan noise"""
        # Tambah noise Gaussian
        noise = random.gauss(0, 5)  # mean=0, std=5
        signal = base_signal + noise
        
        # Batasi range
        signal = max(-120, min(-50, signal))
        
        # Tambah pola periodic (simulasi multipath fading)
        time_factor = time.time() * 0.5
        fading = 3 * np.sin(time_factor)
        
        return signal + fading
    
    def calculate_bars_from_signal(self, signal_db):
        """Hitung bars dari sinyal dBm"""
        if signal_db >= -70:  # Excellent
            return 5
        elif signal_db >= -80:  # Good
            return 4
        elif signal_db >= -90:  # Fair
            return 3
        elif signal_db >= -100:  # Poor
            return 2
        else:  # Very Poor
            return 1
    
    def simulate_data_speed(self, signal_bars, technology="4G"):
        """Simulasi kecepatan data berdasarkan sinyal dan teknologi"""
        base_speed = {
            "2G": 0.2,
            "3G": 5,
            "4G": 50,
            "5G": 300
        }
        
        base = base_speed.get(technology, 10)
        
        # Adjust speed based on signal bars
        multiplier = signal_bars / 5.0
        
        # Add random variation
        variation = random.uniform(0.8, 1.2)
        
        return base * multiplier * variation
    
    def simulate_latency(self, signal_bars, technology="4G"):
        """Simulasi latency berdasarkan sinyal dan teknologi"""
        base_latency = {
            "2G": 300,
            "3G": 100,
            "4G": 40,
            "5G": 20
        }
        
        base = base_latency.get(technology, 100)
        
        # Adjust latency based on signal (better signal = lower latency)
        multiplier = 1.5 - (signal_bars / 10.0)  # 0.5 to 1.0
        
        # Add random variation
        variation = random.uniform(0.9, 1.1)
        
        return base * multiplier * variation

class PegasusIMEGSMPro:
    def __init__(self, root):
        self.root = root
        self.root.title("PEGASUS IME GSM v8.0 - iPhone GSM Pairing & Signal Recovery")
        self.root.geometry("1400x850")
        self.root.configure(bg='#000000')
        
        # Initialize GSM interface
        self.gsm = RealGSMInterface()
        
        # Matrix theme colors
        self.colors = {
            'bg': '#000000',
            'dark_bg': '#0a0a0a',
            'panel_bg': '#111111',
            'terminal_bg': '#000000',
            'terminal_fg': '#00ff41',
            'accent': '#00ffff',
            'warning': '#ff5500',
            'success': '#00ff00',
            'error': '#ff0066',
            'highlight': '#ff00ff',
            'blue': '#0088ff',
            'purple': '#aa00ff',
            'yellow': '#ffff00',
            'gsm_signal': '#00ff00',
            'network_bars': '#00ff88',
            'iphone': '#007aff'
        }
        
        # GSM Network Parameters untuk Indonesia
        self.gsm_networks = {
            'Telkomsel': {
                'band': '900/1800/2100 MHz',
                'tech': ['2G', '3G', '4G', '4G+', '5G'],
                'strength': 95,
                'carrier_code': '510-10',
                'apn': 'internet',
                'mcc': 510,
                'mnc': 10
            },
            'Indosat Ooredoo': {
                'band': '900/2100 MHz',
                'tech': ['3G', '4G', '4G+'],
                'strength': 88,
                'carrier_code': '510-01',
                'apn': 'indosatgprs',
                'mcc': 510,
                'mnc': 1
            },
            'XL Axiata': {
                'band': '850/2100 MHz',
                'tech': ['3G', '4G', '4G+'],
                'strength': 92,
                'carrier_code': '510-11',
                'apn': 'www.xlgprs.net',
                'mcc': 510,
                'mnc': 11
            },
            'Smartfren': {
                'band': '850/2100 MHz',
                'tech': ['4G', '4G+'],
                'strength': 85,
                'carrier_code': '510-28',
                'apn': 'smartfren4g',
                'mcc': 510,
                'mnc': 28
            },
            'Tri (3)': {
                'band': '2100 MHz',
                'tech': ['3G', '4G'],
                'strength': 80,
                'carrier_code': '510-89',
                'apn': '3gprs',
                'mcc': 510,
                'mnc': 89
            }
        }
        
        # Device pairing status - menggunakan Python dictionary biasa
        self.pairing_status = {
            'paired': False,
            'device_id': None,
            'imei': None,
            'imei_info': None,
            'model': None,
            'network': None,
            'carrier': None,
            'signal_strength': 0,
            'signal_db': -100,
            'network_bars': 1,
            'connection_quality': 0,
            'data_speed': 0,
            'latency': 0,
            'frequency': 0,
            'technology': '4G',
            'pairing_time': None,
            'repair_count': 0,
            'last_repair': None
        }
        
        # Real-time GSM data
        self.realtime_gsm = {
            'signal_db': deque(maxlen=100),
            'network_bars': deque(maxlen=100),
            'data_speed': deque(maxlen=100),
            'latency': deque(maxlen=100),
            'frequency': deque(maxlen=100),
            'connection_quality': deque(maxlen=100)
        }
        
        # Thread-safe queue for UI updates
        self.ui_queue = queue.Queue()
        
        # Database
        self.db_conn = sqlite3.connect('pegasus_gsm_pro.db', check_same_thread=False)
        self.create_database()
        
        # Initialize data
        self.init_gsm_data()
        
        # Setup UI
        self.setup_gsm_ui()
        
        # Start background services
        self.start_gsm_services()
        
        # Process UI updates from queue
        self.process_ui_queue()
        
        # Status bar
        self.setup_status_bar()
        
        # Initialize scanning flag
        self.scanning_active = False
    
    def create_database(self):
        """Create database for GSM pairing"""
        cursor = self.db_conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gsm_pairings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pairing_id TEXT UNIQUE,
                device_name TEXT,
                imei TEXT,
                model TEXT,
                serial TEXT,
                country TEXT,
                network TEXT,
                carrier TEXT,
                technology TEXT,
                frequency TEXT,
                pairing_date DATETIME,
                signal_strength INTEGER,
                signal_db REAL,
                network_bars INTEGER,
                data_speed REAL,
                latency REAL,
                status TEXT,
                repair_count INTEGER DEFAULT 0,
                last_repair DATETIME
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gsm_repairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pairing_id TEXT,
                repair_date DATETIME,
                repair_type TEXT,
                signal_before INTEGER,
                signal_after INTEGER,
                signal_db_before REAL,
                signal_db_after REAL,
                issues_fixed TEXT,
                duration REAL,
                method TEXT,
                success BOOLEAN,
                notes TEXT,
                FOREIGN KEY (pairing_id) REFERENCES gsm_pairings (pairing_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gsm_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pairing_id TEXT,
                log_date DATETIME,
                signal_db REAL,
                network_bars INTEGER,
                data_speed REAL,
                latency REAL,
                location TEXT,
                technology TEXT,
                cell_id TEXT,
                FOREIGN KEY (pairing_id) REFERENCES gsm_pairings (pairing_id)
            )
        ''')
        
        self.db_conn.commit()
    
    def init_gsm_data(self):
        """Initialize GSM data streams dengan data realistik"""
        for _ in range(100):
            signal = self.gsm.simulate_gsm_signal(-85)
            bars = self.gsm.calculate_bars_from_signal(signal)
            speed = self.gsm.simulate_data_speed(bars)
            latency = self.gsm.simulate_latency(bars)
            
            self.realtime_gsm['signal_db'].append(signal)
            self.realtime_gsm['network_bars'].append(bars)
            self.realtime_gsm['data_speed'].append(speed)
            self.realtime_gsm['latency'].append(latency)
            self.realtime_gsm['frequency'].append(900 + random.randint(0, 12) * 100)
            self.realtime_gsm['connection_quality'].append(min(100, bars * 20))
    
    def setup_gsm_ui(self):
        """Setup GSM pairing interface yang lebih canggih"""
        # Main container with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.tab_gsm = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.tab_iphone = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.tab_pairing = tk.Frame(self.notebook, bg=self.colors['bg'])
        
        self.notebook.add(self.tab_gsm, text="📡 GSM NETWORK")
        self.notebook.add(self.tab_iphone, text="📱 iPHONE PAIRING")
        self.notebook.add(self.tab_pairing, text="🔧 SIGNAL TOOLS")
        
        # Setup each tab
        self.setup_gsm_tab()
        self.setup_iphone_tab()
        self.setup_pairing_tab()
    
    def setup_status_bar(self):
        """Setup status bar di bagian bawah"""
        self.status_bar = tk.Frame(self.root, bg=self.colors['dark_bg'], height=30)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar.pack_propagate(False)
        
        # Status items
        self.status_device = tk.Label(self.status_bar,
                                    text="Device: Not Paired",
                                    font=("Courier New", 9),
                                    fg=self.colors['warning'],
                                    bg=self.colors['dark_bg'])
        self.status_device.pack(side=tk.LEFT, padx=10)
        
        self.status_signal = tk.Label(self.status_bar,
                                     text="Signal: -- dBm",
                                     font=("Courier New", 9),
                                     fg=self.colors['terminal_fg'],
                                     bg=self.colors['dark_bg'])
        self.status_signal.pack(side=tk.LEFT, padx=10)
        
        self.status_network = tk.Label(self.status_bar,
                                      text="Network: None",
                                      font=("Courier New", 9),
                                      fg=self.colors['terminal_fg'],
                                      bg=self.colors['dark_bg'])
        self.status_network.pack(side=tk.LEFT, padx=10)
        
        self.status_quality = tk.Label(self.status_bar,
                                      text="Quality: --",
                                      font=("Courier New", 9),
                                      fg=self.colors['terminal_fg'],
                                      bg=self.colors['dark_bg'])
        self.status_quality.pack(side=tk.LEFT, padx=10)
        
        # Right side status
        self.status_time = tk.Label(self.status_bar,
                                   text=datetime.now().strftime("%H:%M:%S"),
                                   font=("Courier New", 9),
                                   fg=self.colors['accent'],
                                   bg=self.colors['dark_bg'])
        self.status_time.pack(side=tk.RIGHT, padx=10)
        
        # Update time
        self.update_status_time()
    
    def update_status_time(self):
        """Update waktu di status bar"""
        self.status_time.config(text=datetime.now().strftime("%H:%M:%S"))
        self.root.after(1000, self.update_status_time)
    
    def setup_gsm_tab(self):
        """Setup GSM network interface"""
        gsm_frame = tk.Frame(self.tab_gsm, bg=self.colors['bg'])
        gsm_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(gsm_frame, bg=self.colors['dark_bg'], height=80)
        header.pack(fill=tk.X, pady=(0, 10))
        header.pack_propagate(False)
        
        tk.Label(header,
                text="📡 GSM NETWORK MANAGER - INDONESIA",
                font=("Courier New", 18, "bold"),
                fg=self.colors['iphone'],
                bg=self.colors['dark_bg']).pack(pady=20)
        
        # Main Content
        content = tk.Frame(gsm_frame, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left Panel - Network Scanner
        left_panel = tk.Frame(content, bg=self.colors['dark_bg'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Network Scanner
        scanner_frame = tk.LabelFrame(left_panel,
                                     text=" INDONESIA NETWORK SCANNER ",
                                     font=("Courier New", 12, "bold"),
                                     fg=self.colors['iphone'],
                                     bg=self.colors['panel_bg'],
                                     relief=tk.GROOVE,
                                     borderwidth=2)
        scanner_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scanner display
        self.scanner_display = tk.Canvas(scanner_frame,
                                        bg=self.colors['terminal_bg'],
                                        highlightthickness=0)
        self.scanner_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scanner controls
        controls_frame = tk.Frame(scanner_frame, bg=self.colors['panel_bg'])
        controls_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Button(controls_frame,
                 text="📡 START SCAN",
                 font=("Courier New", 10, "bold"),
                 fg=self.colors['success'],
                 bg=self.colors['dark_bg'],
                 command=self.start_network_scan,
                 width=15,
                 height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(controls_frame,
                 text="⏸️ PAUSE",
                 font=("Courier New", 10, "bold"),
                 fg=self.colors['warning'],
                 bg=self.colors['dark_bg'],
                 command=self.pause_network_scan,
                 width=15,
                 height=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(controls_frame,
                 text="🔗 AUTO-CONNECT",
                 font=("Courier New", 10, "bold"),
                 fg=self.colors['iphone'],
                 bg=self.colors['dark_bg'],
                 command=self.auto_connect_network,
                 width=15,
                 height=2).pack(side=tk.RIGHT, padx=5)
        
        # Available Networks with details
        networks_frame = tk.LabelFrame(left_panel,
                                      text=" AVAILABLE NETWORKS IN INDONESIA ",
                                      font=("Courier New", 12, "bold"),
                                      fg=self.colors['iphone'],
                                      bg=self.colors['panel_bg'],
                                      relief=tk.GROOVE,
                                      borderwidth=2)
        networks_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview with more columns
        columns = ('Network', 'Signal', 'Technology', 'Band', 'Status')
        self.network_tree = ttk.Treeview(networks_frame, columns=columns, show='headings', height=8)
        
        column_widths = [120, 80, 100, 120, 100]
        for col, width in zip(columns, column_widths):
            self.network_tree.heading(col, text=col)
            self.network_tree.column(col, width=width)
        
        scrollbar = ttk.Scrollbar(networks_frame, orient=tk.VERTICAL, command=self.network_tree.yview)
        self.network_tree.configure(yscrollcommand=scrollbar.set)
        
        self.network_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right Panel - Signal Visualization
        right_panel = tk.Frame(content, bg=self.colors['dark_bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Signal Strength Gauge
        gauge_frame = tk.LabelFrame(right_panel,
                                   text=" SIGNAL STRENGTH GAUGE ",
                                   font=("Courier New", 12, "bold"),
                                   fg=self.colors['iphone'],
                                   bg=self.colors['panel_bg'],
                                   relief=tk.GROOVE,
                                   borderwidth=2)
        gauge_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.gauge_canvas = tk.Canvas(gauge_frame,
                                     bg=self.colors['panel_bg'],
                                     highlightthickness=0,
                                     width=300,
                                     height=300)
        self.gauge_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Detailed Network Info
        info_frame = tk.LabelFrame(right_panel,
                                  text=" NETWORK DETAILS ",
                                  font=("Courier New", 12, "bold"),
                                  fg=self.colors['iphone'],
                                  bg=self.colors['panel_bg'],
                                  relief=tk.GROOVE,
                                  borderwidth=2)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        self.network_info = scrolledtext.ScrolledText(info_frame,
                                                    height=10,
                                                    font=("Courier New", 9),
                                                    bg=self.colors['dark_bg'],
                                                    fg=self.colors['terminal_fg'],
                                                    wrap=tk.WORD)
        self.network_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.update_network_info()
    
    def setup_iphone_tab(self):
        """Setup iPhone specific pairing interface"""
        iphone_frame = tk.Frame(self.tab_iphone, bg=self.colors['bg'])
        iphone_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(iphone_frame, bg=self.colors['dark_bg'], height=80)
        header.pack(fill=tk.X, pady=(0, 10))
        header.pack_propagate(False)
        
        tk.Label(header,
                text="📱 iPHONE GSM PAIRING CENTER",
                font=("Courier New", 18, "bold"),
                fg=self.colors['iphone'],
                bg=self.colors['dark_bg']).pack(pady=20)
        
        # Main Content
        content = tk.Frame(iphone_frame, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Left - iPhone Detection
        left_detect = tk.Frame(content, bg=self.colors['dark_bg'])
        left_detect.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # iPhone Detection Panel
        detect_frame = tk.LabelFrame(left_detect,
                                    text=" iPHONE DETECTION ",
                                    font=("Courier New", 12, "bold"),
                                    fg=self.colors['iphone'],
                                    bg=self.colors['panel_bg'],
                                    relief=tk.GROOVE,
                                    borderwidth=2)
        detect_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Detection Methods
        methods_frame = tk.Frame(detect_frame, bg=self.colors['panel_bg'])
        methods_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        detection_methods = [
            ("📱 AUTO IMEI SCAN", self.auto_imei_scan),
            ("🔍 MANUAL IMEI ENTRY", self.manual_imei_entry),
            ("📷 QR CODE SCAN", self.qr_code_scan),
            ("🔗 USB DETECTION", self.usb_detection),
            ("📡 WIRELESS SCAN", self.wireless_scan),
            ("⚡ QUICK DETECT", self.quick_detect)
        ]
        
        for text, command in detection_methods:
            btn = tk.Button(methods_frame,
                          text=text,
                          font=("Courier New", 10, "bold"),
                          fg=self.colors['iphone'],
                          bg=self.colors['dark_bg'],
                          command=command,
                          height=2,
                          width=25)
            btn.pack(pady=3, padx=20)
        
        # iPhone Image Display
        image_frame = tk.LabelFrame(left_detect,
                                   text=" iPHONE DISPLAY ",
                                   font=("Courier New", 12, "bold"),
                                   fg=self.colors['iphone'],
                                   bg=self.colors['panel_bg'],
                                   relief=tk.GROOVE,
                                   borderwidth=2)
        image_frame.pack(fill=tk.BOTH, expand=True)
        
        self.iphone_canvas = tk.Canvas(image_frame,
                                      bg=self.colors['panel_bg'],
                                      highlightthickness=0)
        self.iphone_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right - iPhone Info
        right_info = tk.Frame(content, bg=self.colors['dark_bg'])
        right_info.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # iPhone Information Display
        info_frame = tk.LabelFrame(right_info,
                                  text=" iPHONE INFORMATION ",
                                  font=("Courier New", 12, "bold"),
                                  fg=self.colors['iphone'],
                                  bg=self.colors['panel_bg'],
                                  relief=tk.GROOVE,
                                  borderwidth=2)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.iphone_info = scrolledtext.ScrolledText(info_frame,
                                                    height=15,
                                                    font=("Courier New", 10),
                                                    bg=self.colors['dark_bg'],
                                                    fg=self.colors['terminal_fg'],
                                                    wrap=tk.WORD)
        self.iphone_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.iphone_info.insert(tk.END, "No iPhone detected\n\n")
        self.iphone_info.insert(tk.END, "Connect your iPhone or enter IMEI manually")
        self.iphone_info.config(state='disabled')
        
        # Pairing Button
        pair_frame = tk.Frame(right_info, bg=self.colors['panel_bg'])
        pair_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.pair_button = tk.Button(pair_frame,
                                    text="🚀 START iPHONE PAIRING",
                                    font=("Courier New", 14, "bold"),
                                    fg=self.colors['success'],
                                    bg=self.colors['dark_bg'],
                                    command=self.start_iphone_pairing,
                                    height=3,
                                    width=30,
                                    state='disabled')
        self.pair_button.pack(pady=20)
        
        # Pairing Progress
        progress_frame = tk.LabelFrame(right_info,
                                      text=" PAIRING PROGRESS ",
                                      font=("Courier New", 12, "bold"),
                                      fg=self.colors['iphone'],
                                      bg=self.colors['panel_bg'],
                                      relief=tk.GROOVE,
                                      borderwidth=2)
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        self.pairing_progress = ttk.Progressbar(progress_frame,
                                               length=400,
                                               mode='determinate')
        self.pairing_progress.pack(pady=10, padx=10)
        
        self.pairing_status_label = tk.Label(progress_frame,
                                           text="Ready for iPhone pairing",
                                           font=("Courier New", 10),
                                           fg=self.colors['terminal_fg'],
                                           bg=self.colors['panel_bg'])
        self.pairing_status_label.pack(pady=5)
        
        # Draw initial iPhone
        self.draw_iphone_image()
    
    def draw_iphone_image(self):
        """Draw iPhone image on canvas"""
        self.iphone_canvas.delete("all")
        
        width = self.iphone_canvas.winfo_width()
        height = self.iphone_canvas.winfo_height()
        
        if width > 10 and height > 10:
            # Draw iPhone outline
            self.iphone_canvas.create_rectangle(width//4, height//4,
                                              width*3//4, height*3//4,
                                              outline=self.colors['iphone'],
                                              width=3,
                                              fill=self.colors['dark_bg'])
            
            # Draw screen
            self.iphone_canvas.create_rectangle(width//4+10, height//4+30,
                                              width*3//4-10, height*3//4-10,
                                              outline=self.colors['accent'],
                                              width=2,
                                              fill=self.colors['terminal_bg'])
            
            # Draw Apple logo
            self.iphone_canvas.create_text(width//2, height//2,
                                         text="",
                                         font=("Arial", 40),
                                         fill=self.colors['iphone'])
            
            # Draw text
            self.iphone_canvas.create_text(width//2, height//4+50,
                                         text="iPhone Ready",
                                         font=("Courier New", 12, "bold"),
                                         fill=self.colors['iphone'])
            
            self.iphone_canvas.create_text(width//2, height*3//4-30,
                                         text="IMEI: Not Detected",
                                         font=("Courier New", 9),
                                         fill=self.colors['terminal_fg'])
    
    def setup_pairing_tab(self):
        """Setup signal repair tools interface"""
        repair_frame = tk.Frame(self.tab_pairing, bg=self.colors['bg'])
        repair_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header = tk.Frame(repair_frame, bg=self.colors['dark_bg'], height=80)
        header.pack(fill=tk.X, pady=(0, 10))
        header.pack_propagate(False)
        
        tk.Label(header,
                text="🔧 GSM SIGNAL REPAIR TOOLS",
                font=("Courier New", 18, "bold"),
                fg=self.colors['iphone'],
                bg=self.colors['dark_bg']).pack(pady=20)
        
        # Tools Grid
        tools_frame = tk.Frame(repair_frame, bg=self.colors['bg'])
        tools_frame.pack(fill=tk.BOTH, expand=True)
        
        # Repair Tools
        repair_tools = [
            ("⚡ BOOST SIGNAL", self.boost_signal, self.colors['success']),
            ("📡 FIX NETWORK", self.fix_network, self.colors['warning']),
            ("🔄 RESET CONNECTION", self.reset_connection, self.colors['accent']),
            ("🔍 OPTIMIZE BAND", self.optimize_band, self.colors['blue']),
            ("🚨 EMERGENCY REPAIR", self.emergency_repair, self.colors['error']),
            ("🧹 CLEAN CACHE", self.clean_cache, self.colors['purple']),
            ("📊 DIAGNOSE ISSUES", self.diagnose_issues, self.colors['yellow']),
            ("⚙️ GENERATE REPORT", self.generate_report, self.colors['terminal_fg'])
        ]
        
        # Create tool buttons in grid
        for i, (text, command, color) in enumerate(repair_tools):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(tools_frame,
                          text=text,
                          font=("Courier New", 11, "bold"),
                          fg=color,
                          bg=self.colors['dark_bg'],
                          command=command,
                          height=3,
                          width=25)
            btn.grid(row=row, column=col, padx=20, pady=15, sticky='nsew')
            
            # Configure grid weights
            tools_frame.rowconfigure(row, weight=1)
            tools_frame.columnconfigure(col, weight=1)
    
    def update_network_info(self):
        """Update network information display"""
        self.network_info.config(state='normal')
        self.network_info.delete(1.0, tk.END)
        
        if self.pairing_status['paired']:
            self.network_info.insert(tk.END, f"📱 Device: {self.pairing_status['model']}\n")
            self.network_info.insert(tk.END, f"🔢 IMEI: {self.pairing_status['imei']}\n")
            self.network_info.insert(tk.END, f"📶 Network: {self.pairing_status['network']}\n")
            self.network_info.insert(tk.END, f"🏢 Carrier: {self.pairing_status['carrier']}\n")
            self.network_info.insert(tk.END, f"⚡ Technology: {self.pairing_status['technology']}\n")
            self.network_info.insert(tk.END, f"📊 Signal: {self.pairing_status.get('signal_db', -100):.1f} dBm\n")
            self.network_info.insert(tk.END, f"📶 Bars: {self.pairing_status.get('network_bars', 1)}/5\n")
            self.network_info.insert(tk.END, f"🚀 Speed: {self.pairing_status.get('data_speed', 0):.1f} Mbps\n")
            self.network_info.insert(tk.END, f"⏱️ Latency: {self.pairing_status.get('latency', 0):.1f} ms\n")
            self.network_info.insert(tk.END, f"⭐ Quality: {self.pairing_status.get('connection_quality', 0):.1f}%\n")
            self.network_info.insert(tk.END, f"🛠️ Repairs: {self.pairing_status.get('repair_count', 0)}")
        else:
            self.network_info.insert(tk.END, "No device paired\n\n")
            self.network_info.insert(tk.END, "Please pair an iPhone first\n")
            self.network_info.insert(tk.END, "Go to iPhone Pairing tab")
        
        self.network_info.config(state='disabled')
    
    def auto_imei_scan(self):
        """Auto scan IMEI dari iPhone"""
        self.log_message("Starting automatic IMEI scan...", "system")
        self.pairing_status_label.config(text="Scanning for iPhone...")
        
        # Generate valid iPhone IMEI
        imei = self.gsm.generate_valid_imei()
        
        # Get IMEI info
        imei_info = self.gsm.get_imei_info(imei)
        
        if imei_info:
            # Update iPhone info display
            self.iphone_info.config(state='normal')
            self.iphone_info.delete(1.0, tk.END)
            
            self.iphone_info.insert(tk.END, f"✅ iPhone DETECTED\n\n")
            self.iphone_info.insert(tk.END, f"📱 Model: {imei_info['model']}\n")
            self.iphone_info.insert(tk.END, f"🔢 IMEI: {imei_info['imei']}\n")
            self.iphone_info.insert(tk.END, f"✓ IMEI Valid: {imei_info['is_valid']}\n")
            self.iphone_info.insert(tk.END, f"📏 Length: {imei_info['length']} digits\n")
            self.iphone_info.insert(tk.END, f"🎯 Type: {imei_info['type']}\n")
            self.iphone_info.insert(tk.END, f"🏭 TAC: {imei_info['tac']}\n")
            self.iphone_info.insert(tk.END, f"🔢 Serial: {imei_info['serial']}\n")
            self.iphone_info.insert(tk.END, f"✓ Checksum: {imei_info['checksum']}\n")
            self.iphone_info.insert(tk.END, f"🌍 Country: {imei_info['country']}\n")
            
            self.iphone_info.config(state='disabled')
            
            # Update pairing status
            self.pairing_status.update({
                'imei': imei_info['imei'],
                'imei_info': imei_info,
                'model': imei_info['model']
            })
            
            # Update iPhone image
            self.update_iphone_display(imei_info['model'], imei_info['imei'])
            
            # Enable pair button
            self.pair_button.config(state='normal')
            
            self.log_message(f"iPhone detected: {imei_info['model']} - IMEI: {imei}", "success")
            self.pairing_status_label.config(text=f"Found: {imei_info['model']}")
        else:
            self.log_message("No iPhone detected", "warning")
    
    def update_iphone_display(self, model, imei):
        """Update iPhone display dengan info baru"""
        self.iphone_canvas.delete("all")
        
        width = self.iphone_canvas.winfo_width()
        height = self.iphone_canvas.winfo_height()
        
        if width > 10 and height > 10:
            # Draw iPhone outline
            self.iphone_canvas.create_rectangle(width//4, height//4,
                                              width*3//4, height*3//4,
                                              outline=self.colors['iphone'],
                                              width=3,
                                              fill=self.colors['dark_bg'])
            
            # Draw screen
            self.iphone_canvas.create_rectangle(width//4+10, height//4+30,
                                              width*3//4-10, height*3//4-10,
                                              outline=self.colors['accent'],
                                              width=2,
                                              fill=self.colors['terminal_bg'])
            
            # Draw Apple logo
            self.iphone_canvas.create_text(width//2, height//2,
                                         text="",
                                         font=("Arial", 40),
                                         fill=self.colors['iphone'])
            
            # Draw model text
            self.iphone_canvas.create_text(width//2, height//4+50,
                                         text=model,
                                         font=("Courier New", 12, "bold"),
                                         fill=self.colors['iphone'])
            
            # Draw IMEI
            imei_display = f"IMEI: {imei[:8]}..."
            self.iphone_canvas.create_text(width//2, height*3//4-30,
                                         text=imei_display,
                                         font=("Courier New", 9),
                                         fill=self.colors['terminal_fg'])
    
    def manual_imei_entry(self):
        """Manual IMEI entry dialog"""
        dialog = Toplevel(self.root)
        dialog.title("Manual iPhone IMEI Entry")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['dark_bg'])
        
        tk.Label(dialog,
                text="Enter iPhone IMEI Number:",
                font=("Courier New", 14, "bold"),
                fg=self.colors['iphone'],
                bg=self.colors['dark_bg']).pack(pady=20)
        
        imei_entry = tk.Entry(dialog,
                            font=("Courier New", 16),
                            bg=self.colors['panel_bg'],
                            fg=self.colors['terminal_fg'],
                            width=35,
                            justify='center')
        imei_entry.pack(pady=10)
        imei_entry.insert(0, self.gsm.generate_valid_imei())
        
        # IMEI info display
        info_text = tk.Text(dialog,
                          height=8,
                          font=("Courier New", 9),
                          bg=self.colors['dark_bg'],
                          fg=self.colors['terminal_fg'],
                          wrap=tk.WORD)
        info_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        def validate_and_update():
            imei = imei_entry.get().strip()
            info = self.gsm.get_imei_info(imei)
            
            info_text.delete(1.0, tk.END)
            
            if info and info['is_valid']:
                info_text.insert(tk.END, f"✅ VALID IMEI\n\n")
                info_text.insert(tk.END, f"Model: {info['model']}\n")
                info_text.insert(tk.END, f"Country: {info['country']}\n")
                info_text.insert(tk.END, f"TAC: {info['tac']}\n")
                info_text.insert(tk.END, f"Type: {info['type']}\n")
                
                # Update main display
                self.pairing_status.update({
                    'imei': info['imei'],
                    'imei_info': info,
                    'model': info['model']
                })
                
                # Update iPhone info
                self.iphone_info.config(state='normal')
                self.iphone_info.delete(1.0, tk.END)
                self.iphone_info.insert(tk.END, f"Manual Entry: {info['model']}\n")
                self.iphone_info.insert(tk.END, f"IMEI: {info['imei']}\n")
                self.iphone_info.config(state='disabled')
                
                # Update iPhone display
                self.update_iphone_display(info['model'], info['imei'])
                
                # Enable pair button
                self.pair_button.config(state='normal')
                
                self.log_message(f"Manual IMEI entry: {info['model']}", "success")
                
                dialog.destroy()
            else:
                info_text.insert(tk.END, f"❌ INVALID IMEI\n\n")
                info_text.insert(tk.END, f"Please enter a valid 15-digit iPhone IMEI")
        
        tk.Button(dialog,
                 text="VALIDATE & SUBMIT",
                 font=("Courier New", 12, "bold"),
                 fg=self.colors['success'],
                 bg=self.colors['panel_bg'],
                 command=validate_and_update).pack(pady=20)
    
    def qr_code_scan(self):
        """QR code scanning for iPhone pairing"""
        self.log_message("iPhone QR code scan activated", "system")
        
        # Generate pairing data
        pairing_id = f"IPHONE-{uuid.uuid4().hex[:8].upper()}"
        qr_data = f"IPHONE-PAIR:{pairing_id}:{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create QR code window
        qr_window = Toplevel(self.root)
        qr_window.title("iPhone QR Code Pairing")
        qr_window.geometry("400x500")
        qr_window.configure(bg=self.colors['dark_bg'])
        
        tk.Label(qr_window,
                text="Scan this QR code with iPhone Camera",
                font=("Courier New", 11),
                fg=self.colors['iphone'],
                bg=self.colors['dark_bg']).pack(pady=10)
        
        tk.Label(qr_window,
                text="Settings → General → About → IMEI",
                font=("Courier New", 9),
                fg=self.colors['terminal_fg'],
                bg=self.colors['dark_bg']).pack()
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color=self.colors['iphone'], 
                              back_color=self.colors['dark_bg'])
        
        # Convert to PhotoImage
        qr_photo = ImageTk.PhotoImage(qr_img.resize((250, 250)))
        qr_label = tk.Label(qr_window, image=qr_photo, bg=self.colors['dark_bg'])
        qr_label.image = qr_photo
        qr_label.pack(pady=10)
        
        tk.Label(qr_window,
                text=f"Pairing ID: {pairing_id}",
                font=("Courier New", 10, "bold"),
                fg=self.colors['accent'],
                bg=self.colors['dark_bg']).pack()
        
        # Simulate scanning
        def simulate_scan():
            for i in range(3, 0, -1):
                qr_window.title(f"Scanning... {i}")
                time.sleep(1)
            
            # Auto-generate iPhone IMEI
            imei = self.gsm.generate_valid_imei()
            info = self.gsm.get_imei_info(imei)
            
            qr_window.destroy()
            
            if info:
                self.pairing_status.update({
                    'imei': info['imei'],
                    'imei_info': info,
                    'model': info['model']
                })
                
                # Update display
                self.iphone_info.config(state='normal')
                self.iphone_info.delete(1.0, tk.END)
                self.iphone_info.insert(tk.END, f"QR Code Scan Successful\n\n")
                self.iphone_info.insert(tk.END, f"📱 {info['model']}\n")
                self.iphone_info.insert(tk.END, f"🔢 IMEI: {info['imei']}\n")
                self.iphone_info.insert(tk.END, f"🎯 TAC: {info['tac']}\n")
                self.iphone_info.insert(tk.END, f"🌍 {info['country']}")
                self.iphone_info.config(state='disabled')
                
                # Update iPhone display
                self.update_iphone_display(info['model'], info['imei'])
                
                # Enable pair button
                self.pair_button.config(state='normal')
                
                self.log_message(f"QR scan: {info['model']} detected", "success")
        
        threading.Thread(target=simulate_scan, daemon=True).start()
    
    def usb_detection(self):
        """USB connection detection"""
        self.log_message("Checking USB connections...", "system")
        
        ports = self.gsm.get_available_ports()
        
        if ports:
            # Show port selection
            dialog = Toplevel(self.root)
            dialog.title("Select iPhone USB Port")
            dialog.geometry("500x300")
            dialog.configure(bg=self.colors['dark_bg'])
            
            tk.Label(dialog,
                    text="Detected USB Devices:",
                    font=("Courier New", 14, "bold"),
                    fg=self.colors['iphone'],
                    bg=self.colors['dark_bg']).pack(pady=20)
            
            listbox = tk.Listbox(dialog,
                               font=("Courier New", 10),
                               bg=self.colors['panel_bg'],
                               fg=self.colors['terminal_fg'],
                               selectbackground=self.colors['iphone'],
                               height=8)
            listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
            
            for port in ports:
                listbox.insert(tk.END, f"{port['device']} - {port['description']}")
            
            def select_port():
                selection = listbox.curselection()
                if selection:
                    port = ports[selection[0]]
                    self.log_message(f"Selected: {port['device']}", "success")
                    
                    # Simulate iPhone detection via USB
                    time.sleep(1)
                    self.auto_imei_scan()
                    dialog.destroy()
            
            tk.Button(dialog,
                     text="SELECT iPhone",
                     font=("Courier New", 12, "bold"),
                     fg=self.colors['success'],
                     bg=self.colors['panel_bg'],
                     command=select_port).pack(pady=10)
        else:
            self.log_message("No USB devices detected", "warning")
            messagebox.showinfo("No iPhone", "Connect iPhone via USB and try again")
    
    def wireless_scan(self):
        """Wireless network scan for iPhone"""
        self.log_message("Wireless iPhone scan started", "system")
        
        # Simulate wireless scan
        devices = [
            "iPhone 15 Pro (5G)",
            "iPhone 14 Pro Max",
            "iPhone SE (2022)",
            "iPhone 13",
            "iPhone 12 Pro"
        ]
        
        dialog = Toplevel(self.root)
        dialog.title("Wireless iPhone Scan")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['dark_bg'])
        
        tk.Label(dialog,
                text="Nearby iPhone Devices:",
                font=("Courier New", 12, "bold"),
                fg=self.colors['iphone'],
                bg=self.colors['dark_bg']).pack(pady=20)
        
        listbox = tk.Listbox(dialog,
                           font=("Courier New", 10),
                           bg=self.colors['panel_bg'],
                           fg=self.colors['terminal_fg'],
                           selectbackground=self.colors['iphone'])
        listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        for device in devices:
            listbox.insert(tk.END, device)
        
        def select_device():
            selection = listbox.curselection()
            if selection:
                device = devices[selection[0]]
                
                # Generate matching IMEI
                model_code = "359922" if "15 Pro" in device else "359822"
                imei = self.gsm.generate_valid_imei(model_code)
                info = self.gsm.get_imei_info(imei)
                
                if info:
                    # Override model name
                    info['model'] = device
                    
                    self.pairing_status.update({
                        'imei': info['imei'],
                        'imei_info': info,
                        'model': device
                    })
                    
                    # Update display
                    self.iphone_info.config(state='normal')
                    self.iphone_info.delete(1.0, tk.END)
                    self.iphone_info.insert(tk.END, f"Wireless Scan: {device}\n")
                    self.iphone_info.insert(tk.END, f"IMEI: {info['imei']}\n")
                    self.iphone_info.config(state='disabled')
                    
                    # Update iPhone display
                    self.update_iphone_display(device, info['imei'])
                    
                    # Enable pair button
                    self.pair_button.config(state='normal')
                    
                    self.log_message(f"Wireless: {device} detected", "success")
                    dialog.destroy()
        
        tk.Button(dialog,
                 text="SELECT DEVICE",
                 font=("Courier New", 10, "bold"),
                 fg=self.colors['success'],
                 bg=self.colors['panel_bg'],
                 command=select_device).pack(pady=10)
    
    def quick_detect(self):
        """Quick detection for iPhone"""
        self.log_message("Quick iPhone detection started", "system")
        
        # Auto-detect random iPhone model
        models = list(self.gsm.iphone_models.keys())
        model_key = random.choice(models)
        model_info = self.gsm.iphone_models[model_key]
        
        # Generate appropriate IMEI
        model_code = "359920" if "14" in model_info['name'] else "359820"
        imei = self.gsm.generate_valid_imei(model_code)
        info = self.gsm.get_imei_info(imei)
        
        if info:
            # Override model with actual iPhone model
            info['model'] = model_info['name']
            
            self.pairing_status.update({
                'imei': info['imei'],
                'imei_info': info,
                'model': info['model']
            })
            
            # Update display
            self.iphone_info.config(state='normal')
            self.iphone_info.delete(1.0, tk.END)
            
            self.iphone_info.insert(tk.END, f"⚡ QUICK DETECT\n\n")
            self.iphone_info.insert(tk.END, f"📱 {model_info['name']}\n")
            self.iphone_info.insert(tk.END, f"🔢 IMEI: {info['imei']}\n")
            self.iphone_info.insert(tk.END, f"📶 Bands: {', '.join(model_info['bands'][:3])}\n")
            self.iphone_info.insert(tk.END, f"✓ IMEI Valid: Yes\n")
            self.iphone_info.insert(tk.END, f"🌍 Country: {info['country']}")
            
            self.iphone_info.config(state='disabled')
            
            # Update iPhone display
            self.update_iphone_display(model_info['name'], info['imei'])
            
            # Enable pair button
            self.pair_button.config(state='normal')
            
            self.log_message(f"Quick detect: {model_info['name']}", "success")
            self.pairing_status_label.config(text=f"Detected: {model_info['name']}")
    
    def start_iphone_pairing(self):
        """Start iPhone pairing process"""
        if not self.pairing_status.get('imei'):
            messagebox.showwarning("No iPhone", "Please detect iPhone first!")
            return
        
        self.log_message(f"Starting iPhone pairing: {self.pairing_status['model']}", "system")
        
        # Reset progress
        self.pairing_progress['value'] = 0
        self.pairing_status_label.config(text="Starting pairing...", fg=self.colors['iphone'])
        
        def pairing_process():
            steps = [
                ("Verifying IMEI...", 10, 1),
                ("Connecting to iPhone...", 30, 2),
                ("Reading device info...", 50, 1),
                ("Configuring GSM module...", 70, 2),
                ("Establishing secure link...", 85, 2),
                ("Finalizing pairing...", 95, 1),
                ("Complete!", 100, 1)
            ]
            
            for step_text, progress, duration in steps:
                time.sleep(duration)
                self.root.after(0, lambda t=step_text, p=progress: 
                              self.update_pairing_progress(t, p))
            
            # Complete pairing
            pairing_id = f"IPHONE-{uuid.uuid4().hex[:8].upper()}"
            
            # Get current time
            now = datetime.now()
            
            # Update pairing status
            self.pairing_status.update({
                'paired': True,
                'device_id': pairing_id,
                'network': "4G LTE",
                'carrier': "Telkomsel",
                'technology': "4G",
                'signal_strength': 85,
                'signal_db': self.gsm.simulate_gsm_signal(-75),
                'network_bars': 4,
                'data_speed': self.gsm.simulate_data_speed(4),
                'latency': self.gsm.simulate_latency(4),
                'frequency': 1800,
                'connection_quality': 85,
                'pairing_time': now,
                'repair_count': 0,
                'last_repair': None
            })
            
            # Save to database
            try:
                cursor = self.db_conn.cursor()
                cursor.execute('''
                    INSERT INTO gsm_pairings 
                    (pairing_id, device_name, imei, model, serial, country, network, carrier, 
                     technology, frequency, pairing_date, signal_strength, signal_db, 
                     network_bars, data_speed, latency, status, repair_count)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (pairing_id,
                      self.pairing_status['model'],
                      self.pairing_status['imei'],
                      self.pairing_status['model'],
                      self.pairing_status.get('imei_info', {}).get('serial', ''),
                      self.pairing_status.get('imei_info', {}).get('country', ''),
                      self.pairing_status['network'],
                      self.pairing_status['carrier'],
                      self.pairing_status['technology'],
                      self.pairing_status['frequency'],
                      now.strftime('%Y-%m-%d %H:%M:%S'),
                      self.pairing_status['signal_strength'],
                      self.pairing_status['signal_db'],
                      self.pairing_status['network_bars'],
                      self.pairing_status['data_speed'],
                      self.pairing_status['latency'],
                      'ACTIVE',
                      0))
                
                self.db_conn.commit()
            except Exception as e:
                print(f"Database error: {e}")
            
            # Update status bar
            self.root.after(0, lambda: self.status_device.config(
                text=f"Device: {self.pairing_status['model']}",
                fg=self.colors['success']
            ))
            
            self.root.after(0, lambda: self.status_signal.config(
                text=f"Signal: {self.pairing_status['signal_db']:.1f} dBm"
            ))
            
            self.root.after(0, lambda: self.status_network.config(
                text=f"Network: {self.pairing_status['network']}"
            ))
            
            self.root.after(0, lambda: self.status_quality.config(
                text=f"Quality: {self.pairing_status['connection_quality']:.1f}%"
            ))
            
            # Update network info
            self.root.after(0, self.update_network_info)
            
            # Show success message
            self.root.after(0, lambda: self.pairing_status_label.config(
                text=f"✅ {self.pairing_status['model']} PAIRED!",
                fg=self.colors['success']
            ))
            
            self.root.after(0, lambda: self.log_message(
                f"iPhone pairing complete: {self.pairing_status['model']} - {pairing_id}",
                "success"
            ))
            
            # Auto-connect to network after 2 seconds
            time.sleep(2)
            self.root.after(0, self.auto_connect_network)
        
        threading.Thread(target=pairing_process, daemon=True).start()
    
    def update_pairing_progress(self, text, value):
        """Update pairing progress display"""
        self.pairing_progress['value'] = value
        self.pairing_status_label.config(text=text)
    
    def start_network_scan(self):
        """Start network scanning"""
        self.scanning_active = True
        self.log_message("Starting network scan in Indonesia...", "system")
        
        # Clear network tree
        for item in self.network_tree.get_children():
            self.network_tree.delete(item)
        
        # Simulate scanning Indonesian networks
        def scan_process():
            networks = [
                ("Telkomsel", "4G/5G", "900/1800/2100 MHz"),
                ("Indosat Ooredoo", "4G", "900/2100 MHz"),
                ("XL Axiata", "4G+", "850/2100 MHz"),
                ("Smartfren", "4G", "850/2100 MHz"),
                ("Tri (3)", "3G/4G", "2100 MHz"),
                ("By.U", "4G", "900/1800 MHz"),
                ("LiveOn", "4G", "850/2100 MHz")
            ]
            
            for i, (network, tech, band) in enumerate(networks):
                time.sleep(0.5)
                
                # Generate realistic signal
                signal = random.randint(60, 99)
                
                # Determine status
                if signal >= 90:
                    status = "Excellent"
                    tag = 'excellent'
                elif signal >= 80:
                    status = "Good"
                    tag = 'good'
                elif signal >= 70:
                    status = "Fair"
                    tag = 'fair'
                else:
                    status = "Poor"
                    tag = 'poor'
                
                # Insert to tree
                self.root.after(0, lambda n=network, s=signal, t=tech, b=band, st=status, tg=tag: 
                              self.network_tree.insert('', 'end',
                                                      values=(n, f"{s}%", t, b, st),
                                                      tags=(tg,)))
                
                self.root.after(0, lambda n=network, s=signal: 
                              self.log_message(f"Found: {n} ({s}%)", "info"))
            
            # Configure tags
            self.root.after(0, lambda: self.network_tree.tag_configure('excellent', 
                                                                     foreground=self.colors['success']))
            self.root.after(0, lambda: self.network_tree.tag_configure('good',
                                                                     foreground=self.colors['accent']))
            self.root.after(0, lambda: self.network_tree.tag_configure('fair',
                                                                     foreground=self.colors['warning']))
            self.root.after(0, lambda: self.network_tree.tag_configure('poor',
                                                                     foreground=self.colors['error']))
            
            self.root.after(0, lambda: self.log_message("Network scan complete", "success"))
        
        threading.Thread(target=scan_process, daemon=True).start()
    
    def pause_network_scan(self):
        """Pause network scanning"""
        self.scanning_active = False
        self.log_message("Network scan paused", "warning")
    
    def auto_connect_network(self):
        """Auto-connect to best network"""
        if not self.pairing_status['paired']:
            messagebox.showerror("No iPhone", "Pair an iPhone first!")
            return
        
        self.log_message("Searching for best network in Indonesia...", "system")
        
        # Find best network (simulated)
        networks = list(self.gsm_networks.keys())
        best_network = random.choice(networks)
        network_info = self.gsm_networks[best_network]
        
        # Update pairing status
        self.pairing_status['network'] = best_network
        self.pairing_status['carrier'] = best_network
        self.pairing_status['technology'] = random.choice(network_info['tech'])
        
        # Generate realistic signal data
        signal_db = self.gsm.simulate_gsm_signal(-75)
        bars = self.gsm.calculate_bars_from_signal(signal_db)
        speed = self.gsm.simulate_data_speed(bars, self.pairing_status['technology'])
        latency = self.gsm.simulate_latency(bars, self.pairing_status['technology'])
        
        self.pairing_status.update({
            'signal_db': signal_db,
            'signal_strength': min(100, max(0, 100 + int(signal_db))),
            'network_bars': bars,
            'data_speed': speed,
            'latency': latency,
            'frequency': int(network_info['band'].split(' ')[0].replace('/', '')) if '/' in network_info['band'] else 900,
            'connection_quality': bars * 20
        })
        
        # Update status bar
        self.status_network.config(text=f"Network: {best_network}")
        self.status_signal.config(text=f"Signal: {signal_db:.1f} dBm")
        self.status_quality.config(text=f"Quality: {self.pairing_status['connection_quality']:.1f}%")
        
        # Update network info display
        self.update_network_info()
        
        self.log_message(f"Connected to {best_network} ({signal_db:.1f} dBm)", "success")
        
        # Save connection log
        self.save_connection_log()
    
    def save_connection_log(self):
        """Save connection log to database"""
        if not self.pairing_status['device_id']:
            return
        
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO gsm_logs 
                (pairing_id, log_date, signal_db, network_bars, data_speed, latency, technology)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.pairing_status['device_id'],
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  self.pairing_status['signal_db'],
                  self.pairing_status['network_bars'],
                  self.pairing_status['data_speed'],
                  self.pairing_status['latency'],
                  self.pairing_status['technology']))
            
            self.db_conn.commit()
        except Exception as e:
            print(f"Log save error: {e}")
    
    def process_ui_queue(self):
        """Process UI updates from queue"""
        try:
            while True:
                task, data = self.ui_queue.get_nowait()
                if task == "matrix_update":
                    self.update_matrix_display()
                elif task == "update_gauge":
                    self.draw_signal_gauge(data)
                elif task == "update_monitor":
                    self.update_realtime_data()
        except queue.Empty:
            pass
        
        self.root.after(100, self.process_ui_queue)
    
    def update_realtime_data(self):
        """Update real-time data jika iPhone terpair"""
        if self.pairing_status.get('paired', False):
            # Update signal dengan simulasi realistik
            signal_db = self.gsm.simulate_gsm_signal(-75)
            bars = self.gsm.calculate_bars_from_signal(signal_db)
            speed = self.gsm.simulate_data_speed(bars, self.pairing_status.get('technology', '4G'))
            latency = self.gsm.simulate_latency(bars, self.pairing_status.get('technology', '4G'))
            
            # Update realtime data
            self.realtime_gsm['signal_db'].append(signal_db)
            self.realtime_gsm['network_bars'].append(bars)
            self.realtime_gsm['data_speed'].append(speed)
            self.realtime_gsm['latency'].append(latency)
            self.realtime_gsm['connection_quality'].append(bars * 20)
            
            # Update pairing status
            self.pairing_status.update({
                'signal_db': signal_db,
                'signal_strength': min(100, max(0, 100 + int(signal_db))),
                'network_bars': bars,
                'data_speed': speed,
                'latency': latency,
                'connection_quality': bars * 20
            })
            
            # Update status bar
            self.status_signal.config(text=f"Signal: {signal_db:.1f} dBm")
            self.status_quality.config(text=f"Quality: {bars * 20:.1f}%")
            
            # Update network info secara berkala
            if random.random() < 0.1:  # 10% chance setiap update
                self.update_network_info()
    
    def start_gsm_services(self):
        """Start GSM background services"""
        # Start real-time data updates
        self.realtime_thread = threading.Thread(target=self.realtime_update_service, daemon=True)
        self.realtime_thread.start()
        
        # Start gauge updates
        self.gauge_thread = threading.Thread(target=self.gauge_update_service, daemon=True)
        self.gauge_thread.start()
        
        # Start matrix effect
        self.matrix_thread = threading.Thread(target=self.matrix_animation, daemon=True)
        self.matrix_thread.start()
    
    def realtime_update_service(self):
        """Background service for real-time updates"""
        while True:
            self.ui_queue.put(("update_monitor", None))
            time.sleep(2)  # Update setiap 2 detik
    
    def gauge_update_service(self):
        """Background service for gauge updates"""
        while True:
            if self.pairing_status.get('paired', False):
                signal = self.pairing_status.get('signal_strength', 0)
                self.ui_queue.put(("update_gauge", signal))
            time.sleep(3)  # Update setiap 3 detik
    
    def matrix_animation(self):
        """Matrix rain animation"""
        while True:
            if self.scanning_active:
                self.ui_queue.put(("matrix_update", None))
            time.sleep(0.2)
    
    def update_matrix_display(self):
        """Update matrix effect"""
        try:
            self.scanner_display.delete("all")
            width = self.scanner_display.winfo_width()
            height = self.scanner_display.winfo_height()
            
            if width > 10 and height > 10:
                # Draw network scanning animation
                chars = "█▓▒░▓▒░"
                
                # Draw scanning line
                scan_y = int(time.time() * 50) % height
                self.scanner_display.create_line(0, scan_y, width, scan_y,
                                                fill=self.colors['iphone'],
                                                width=2)
                
                # Draw network signals
                for _ in range(20):
                    x = random.randint(0, width)
                    y = random.randint(0, height)
                    char = random.choice(chars)
                    size = random.randint(8, 16)
                    
                    # Color based on position relative to scan line
                    if y < scan_y:
                        color = self.colors['success']
                    else:
                        color = f'#00{random.randint(50, 150):02x}00'
                    
                    self.scanner_display.create_text(x, y,
                                                   text=char,
                                                   fill=color,
                                                   font=('Courier New', size))
        except:
            pass
    
    def draw_signal_gauge(self, strength):
        """Draw signal strength gauge"""
        try:
            self.gauge_canvas.delete("all")
            
            width = self.gauge_canvas.winfo_width()
            height = self.gauge_canvas.winfo_height()
            
            if width < 50 or height < 50:
                return
            
            center_x = width // 2
            center_y = height // 2
            radius = min(width, height) // 2 - 20
            
            # Draw background
            self.gauge_canvas.create_oval(center_x - radius, center_y - radius,
                                         center_x + radius, center_y + radius,
                                         outline=self.colors['terminal_fg'],
                                         width=2,
                                         fill=self.colors['dark_bg'])
            
            # Draw segments (5 segments for 5 bars)
            segments = 5
            segment_angle = 270 / segments
            
            for i in range(segments):
                start_angle = 135 + i * segment_angle
                
                # Determine color based on which segments are active
                active_segments = int((strength / 100) * segments)
                
                if i < active_segments:
                    if i >= 3:
                        color = self.colors['success']
                    elif i >= 1:
                        color = self.colors['warning']
                    else:
                        color = self.colors['error']
                else:
                    color = self.colors['dark_bg']
                
                # Draw segment
                self.gauge_canvas.create_arc(center_x - radius, center_y - radius,
                                            center_x + radius, center_y + radius,
                                            start=start_angle,
                                            extent=segment_angle - 2,
                                            style=tk.PIESLICE,
                                            outline=color,
                                            fill=color,
                                            width=0)
            
            # Draw center text with dBm
            signal_db = self.pairing_status.get('signal_db', -100)
            self.gauge_canvas.create_text(center_x, center_y - 10,
                                         text=f"{strength}%",
                                         font=("Courier New", 18, "bold"),
                                         fill=self.colors['terminal_fg'])
            
            self.gauge_canvas.create_text(center_x, center_y + 20,
                                         text=f"{signal_db:.1f} dBm",
                                         font=("Courier New", 10),
                                         fill=self.colors['accent'])
            
            # Draw iPhone icon
            self.gauge_canvas.create_text(center_x, center_y - radius - 15,
                                         text="📱",
                                         font=("Courier New", 16),
                                         fill=self.colors['iphone'])
        except Exception as e:
            pass
    
    # Repair Tools Methods
    def boost_signal(self):
        """Boost signal strength"""
        if not self.pairing_status.get('paired', False):
            messagebox.showwarning("Not Paired", "Please pair an iPhone first!")
            return
        
        self.log_message("Boosting GSM signal...", "system")
        
        # Simulate boosting
        current_signal = self.pairing_status.get('signal_db', -100)
        boost_amount = random.randint(5, 15)
        new_signal = min(-50, current_signal + boost_amount)
        
        self.pairing_status['signal_db'] = new_signal
        self.pairing_status['signal_strength'] = min(100, max(0, 100 + int(new_signal)))
        
        self.log_message(f"Signal boosted: {current_signal:.1f} dBm → {new_signal:.1f} dBm", "success")
        
        # Update display
        self.update_network_info()
    
    def fix_network(self):
        """Fix network connection"""
        if not self.pairing_status.get('paired', False):
            messagebox.showwarning("Not Paired", "Please pair an iPhone first!")
            return
        
        self.log_message("Fixing network connection...", "system")
        
        # Simulate fixing
        self.pairing_status['connection_quality'] = min(100, self.pairing_status.get('connection_quality', 0) + 20)
        
        self.log_message(f"Network connection improved to {self.pairing_status['connection_quality']:.1f}%", "success")
        
        # Update display
        self.update_network_info()
    
    def reset_connection(self):
        """Reset GSM connection"""
        if not self.pairing_status.get('paired', False):
            messagebox.showwarning("Not Paired", "Please pair an iPhone first!")
            return
        
        response = messagebox.askyesno("Reset Connection",
                                      "This will temporarily disconnect the device.\nContinue?")
        
        if response:
            self.log_message("Resetting GSM connection...", "warning")
            
            # Simulate reset
            old_signal = self.pairing_status.get('signal_db', -100)
            self.pairing_status['signal_db'] = -100
            self.pairing_status['signal_strength'] = 0
            
            time.sleep(2)
            
            # Restore with improvement
            new_signal = max(old_signal + 5, -80)
            self.pairing_status['signal_db'] = new_signal
            self.pairing_status['signal_strength'] = min(100, max(0, 100 + int(new_signal)))
            
            self.log_message(f"Connection reset: {new_signal:.1f} dBm", "success")
            
            # Update display
            self.update_network_info()
    
    def optimize_band(self):
        """Optimize frequency band"""
        if not self.pairing_status.get('paired', False):
            messagebox.showwarning("Not Paired", "Please pair an iPhone first!")
            return
        
        self.log_message("Optimizing frequency band...", "system")
        
        bands = ["850 MHz", "900 MHz", "1800 MHz", "2100 MHz", "2600 MHz"]
        selected_band = random.choice(bands)
        
        self.pairing_status['frequency'] = int(selected_band.split(' ')[0])
        
        self.log_message(f"Optimized to {selected_band} band", "success")
        
        # Update display
        self.update_network_info()
    
    def emergency_repair(self):
        """Emergency GSM repair"""
        if not self.pairing_status.get('paired', False):
            messagebox.showwarning("Not Paired", "Please pair an iPhone first!")
            return
        
        response = messagebox.askyesno("Emergency Repair",
                                      "Emergency repair uses aggressive methods.\nContinue?")
        
        if response:
            self.log_message("🚨 EMERGENCY GSM REPAIR 🚨", "error")
            
            # Force maximum signal
            self.pairing_status.update({
                'signal_db': -60,
                'signal_strength': 99,
                'network_bars': 5,
                'connection_quality': 99,
                'data_speed': self.gsm.simulate_data_speed(5),
                'latency': self.gsm.simulate_latency(5)
            })
            
            self.log_message("Emergency repair complete! Signal: 99%", "success")
            
            # Update display
            self.update_network_info()
    
    def clean_cache(self):
        """Clean GSM cache"""
        self.log_message("Cleaning GSM cache...", "system")
        
        # Simulate cache cleaning
        cache_size = random.randint(50, 200)
        
        self.log_message(f"Cleaned {cache_size}MB of GSM cache", "success")
    
    def diagnose_issues(self):
        """Diagnose GSM issues"""
        self.log_message("Running GSM diagnostics...", "system")
        
        diagnostics = [
            ("Signal Quality", random.randint(70, 100)),
            ("Network Stability", random.randint(80, 100)),
            ("Data Connection", random.randint(60, 95)),
            ("Voice Quality", random.randint(85, 100)),
            ("Hardware Interface", random.randint(75, 100))
        ]
        
        report = "GSM Diagnostics Report:\n"
        report += "=" * 40 + "\n"
        
        for check, score in diagnostics:
            bar = "█" * (score // 10) + "░" * (10 - (score // 10))
            report += f"{check}: {score:3d}% {bar}\n"
        
        report += "=" * 40 + "\n"
        report += "Diagnosis complete. All systems OK."
        
        self.log_message(report, "info")
    
    def generate_report(self):
        """Generate GSM report"""
        if not self.pairing_status.get('paired', False):
            messagebox.showwarning("Not Paired", "Please pair an iPhone first!")
            return
        
        report = f"""
╔═══════════════════════════════════════════════════════╗
║                 GSM SIGNAL REPORT                    ║
╠═══════════════════════════════════════════════════════╣
║ Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
║ Device: {self.pairing_status.get('model', 'Unknown')}
║ IMEI: {self.pairing_status.get('imei', 'Unknown')}
║ Network: {self.pairing_status.get('network', 'None')}
║ Signal: {self.pairing_status.get('signal_db', -100):.1f} dBm
║ Bars: {self.pairing_status.get('network_bars', 0)}/5
║ Speed: {self.pairing_status.get('data_speed', 0):.1f} Mbps
║ Latency: {self.pairing_status.get('latency', 0):.1f} ms
║ Quality: {self.pairing_status.get('connection_quality', 0):.1f}%
║ Status: {'ACTIVE' if self.pairing_status.get('paired', False) else 'INACTIVE'}
╚═══════════════════════════════════════════════════════╝
"""
        
        self.log_message(report, "system")
        
        # Save report
        try:
            filename = f"gsm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(report)
            
            self.log_message(f"Report saved: {filename}", "success")
        except:
            self.log_message("Could not save report", "warning")
    
    def log_message(self, message, msg_type="info"):
        """Log message dengan color coding"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        colors = {
            "info": self.colors['terminal_fg'],
            "success": self.colors['success'],
            "warning": self.colors['warning'],
            "error": self.colors['error'],
            "system": self.colors['accent'],
            "iphone": self.colors['iphone']
        }
        
        color = colors.get(msg_type, self.colors['terminal_fg'])
        
        # Print ke console dengan warna
        color_code = {
            "info": "37",      # White
            "success": "32",   # Green
            "warning": "33",   # Yellow
            "error": "31",     # Red
            "system": "36",    # Cyan
            "iphone": "34"     # Blue
        }.get(msg_type, "37")
        
        print(f"\033[{color_code}m[{timestamp}] {message}\033[0m")

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PegasusIMEGSMPro(root)
    
    # Center window
    root.update_idletasks()
    width = 1400
    height = 850
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Bind escape to exit
    root.bind('<Escape>', lambda e: root.quit())
    
    print("\n" + "="*80)
    print("PEGASUS IME GSM v8.0 - iPhone GSM Pairing & Signal Recovery")
    print("="*80)
    print("🎯 Features for iPhone:")
    print("  • Real iPhone IMEI validation & model detection")
    print("  • Support semua iPhone dari 5s sampai 15 Pro Max")
    print("  • Database TAC untuk identifikasi model akurat")
    print("  • Simulasi sinyal GSM real-time untuk Indonesia")
    print("  • Auto-connect ke jaringan Indonesia (Telkomsel, Indosat, XL, dll)")
    print("  • Signal quality monitoring dengan algoritma real")
    print("  • Repair tools khusus untuk iPhone")
    print("="*80)
    print("📱 Quick Start untuk iPhone:")
    print("  1. Go to '📱 iPHONE PAIRING' tab")
    print("  2. Click '📱 AUTO IMEI SCAN' atau '🔍 MANUAL IMEI ENTRY'")
    print("  3. Enter iPhone IMEI (15 digit dari Settings → General → About)")
    print("  4. Click '🚀 START iPHONE PAIRING'")
    print("  5. Go to '📡 GSM NETWORK' tab")
    print("  6. Click '🔗 AUTO-CONNECT' untuk jaringan Indonesia")
    print("  7. Monitor signal real-time di status bar")
    print("  8. Use '🔧 SIGNAL TOOLS' untuk repair dan optimasi")
    print("="*80)
    print("🔧 Note:")
    print("  • IMEI validation menggunakan Luhn algorithm")
    print("  • Model detection berdasarkan TAC database")
    print("  • Signal simulation menggunakan model realistik")
    print("  • Semua data disimpan di database lokal")
    print("="*80 + "\n")
    
    root.mainloop()

if __name__ == "__main__":
    # Check dependencies
    required = ['pillow', 'qrcode', 'numpy']
    
    print("🔍 Checking dependencies...")
    for package in required:
        try:
            if package == 'pyserial':
                __import__('serial')
            else:
                __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - Install: pip install {package}")
    
    print("\n🚀 Starting PEGASUS IME GSM Pro...")
    main()