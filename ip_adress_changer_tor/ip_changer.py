#!/usr/bin/env python3
"""
Advanced Automatic IP Changer - Tor IP & Country Changer
A powerful, non-trackable IP changer compatible with Kali Linux and Windows
Auto-configures Tor, changes IP and country automatically
Author: Aryan Chavan
Version: 3.1.0
"""

import requests
import time
import os
import random
import sys
import socket
import subprocess
import platform
import json
import logging
import signal
import re
from datetime import datetime
from typing import Optional, Dict, List

# Configuration
CONFIG = {
    'tor_proxy': {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    },
    'tor_proxy_windows': {
        'http': 'socks5h://127.0.0.1:9150',
        'https': 'socks5h://127.0.0.1:9150'
    },
    'tor_control_port': 9051,
    'check_ip_urls': [
        'https://checkip.amazonaws.com',
        'https://api.ipify.org',
        'https://icanhazip.com',
        'https://ident.me',
        'https://ifconfig.me/ip'
    ],
    'ip_info_url': 'https://ipapi.co/{ip}/json/',
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
    ],
    'exit_nodes': {
        'US': 'United States',
        'GB': 'United Kingdom',
        'DE': 'Germany',
        'FR': 'France',
        'NL': 'Netherlands',
        'CA': 'Canada',
        'AU': 'Australia',
        'JP': 'Japan',
        'SG': 'Singapore',
        'IN': 'India',
        'RU': 'Russia',
        'SE': 'Sweden',
        'CH': 'Switzerland',
        'NO': 'Norway',
        'FI': 'Finland',
        'DK': 'Denmark',
        'PL': 'Poland',
        'IT': 'Italy',
        'ES': 'Spain',
        'BR': 'Brazil'
    }
}

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

class IPChanger:
    def __init__(self, interval: int, count: int, output_file: str = "ip_changer_results.txt"):
        self.interval = max(10, interval)  # Minimum 10 seconds
        self.count = count  # 0 means infinite
        self.output_file = output_file
        self.system = platform.system()
        self.session = requests.Session()
        self.running = True
        self.current_proxy = CONFIG['tor_proxy']
        self.results = []
        self.iteration = 0
        
        # Setup logging and signal handlers
        self.setup_logging()
        self.setup_signal_handlers()
        
    def setup_logging(self):
        """Setup logging to file"""
        logging.basicConfig(
            filename=self.output_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n{Colors.WARNING}[!] Stopping IP Changer...{Colors.ENDC}")
        self.running = False
        self.save_results()
        sys.exit(0)
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if self.system == 'Windows' else 'clear')
        
    def print_banner(self):
        """Print ASCII art banner"""
        banner = f"""
{Colors.CYAN}
    ___  ____  _____    _    _   _ ____  _____ ____  
   / _ \\|  _ \\| ____|  / \\  | | | / ___|| ____|  _ \\ 
  | | | | |_) |  _|   / _ \\ | | | \\___ \\|  _| | |_) |
  | |_| |  __/| |___ / ___ \\| |_| |___) | |___|  _ < 
   \\___/|_|   |_____/_/   \\_\\___/|____/|_____|_| \\_\\
{Colors.ENDC}
{Colors.GREEN}       Automatic Tor IP & Country Changer v3.1{Colors.ENDC}
{Colors.YELLOW}              by Aryan Chavan{Colors.ENDC}
{Colors.MAGENTA}       Compatible with Kali Linux & Windows{Colors.ENDC}
        """
        print(banner)
        
    def install_tor_linux(self) -> bool:
        """Automatically install Tor on Linux"""
        print(f"{Colors.YELLOW}[*] Installing Tor...{Colors.ENDC}")
        try:
            # Update package list
            subprocess.run(['sudo', 'apt', 'update'], capture_output=True, timeout=60)
            # Install Tor
            result = subprocess.run(['sudo', 'apt', 'install', '-y', 'tor'], 
                                  capture_output=True, timeout=120)
            if result.returncode == 0:
                print(f"{Colors.GREEN}[+] Tor installed successfully{Colors.ENDC}")
                return True
            else:
                print(f"{Colors.FAIL}[!] Failed to install Tor{Colors.ENDC}")
                return False
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error installing Tor: {e}{Colors.ENDC}")
            return False
            
    def configure_tor(self) -> bool:
        """Configure Tor with optimal settings"""
        print(f"{Colors.YELLOW}[*] Configuring Tor...{Colors.ENDC}")
        
        torrc_content = """# Tor configuration for IP Changer
SocksPort 9050
ControlPort 9051
CookieAuthentication 0
MaxCircuitDirtiness 10
NewCircuitPeriod 15
UseEntryGuards 1
SafeLogging 0
Log notice stdout
DisableDebuggerAttachment 1
ClientOnly 1
"""
        try:
            # Write config
            with open('/tmp/torrc_temp', 'w') as f:
                f.write(torrc_content)
            
            # Copy to system location
            subprocess.run(['sudo', 'cp', '/tmp/torrc_temp', '/etc/tor/torrc'], 
                         capture_output=True)
            subprocess.run(['sudo', 'chmod', '644', '/etc/tor/torrc'], 
                         capture_output=True)
            print(f"{Colors.GREEN}[+] Tor configured{Colors.ENDC}")
            return True
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error configuring Tor: {e}{Colors.ENDC}")
            return False
            
    def start_tor_linux(self) -> bool:
        """Start Tor service on Linux"""
        print(f"{Colors.YELLOW}[*] Starting Tor service...{Colors.ENDC}")
        try:
            # Try systemctl
            result = subprocess.run(['sudo', 'systemctl', 'start', 'tor'], 
                                  capture_output=True, timeout=10)
            if result.returncode == 0:
                time.sleep(3)
                return True
                
            # Try service command
            result = subprocess.run(['sudo', 'service', 'tor', 'start'], 
                                  capture_output=True, timeout=10)
            if result.returncode == 0:
                time.sleep(3)
                return True
                
            return False
        except Exception as e:
            print(f"{Colors.FAIL}[!] Error starting Tor: {e}{Colors.ENDC}")
            return False
            
    def check_tor_running(self) -> bool:
        """Check if Tor SOCKS proxy is accessible"""
        ports_to_check = [9050, 9150]  # 9050 for Linux, 9150 for Tor Browser on Windows
        
        for port in ports_to_check:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                
                if result == 0:
                    # Update proxy config based on working port
                    if port == 9150:
                        self.current_proxy = CONFIG['tor_proxy_windows']
                    else:
                        self.current_proxy = CONFIG['tor_proxy']
                    return True
            except:
                pass
        return False
        
    def setup_tor(self) -> bool:
        """Automatically setup and start Tor"""
        print(f"{Colors.CYAN}[*] Setting up Tor...{Colors.ENDC}")
        
        # Check if Tor is already running
        if self.check_tor_running():
            print(f"{Colors.GREEN}[+] Tor is already running{Colors.ENDC}")
            return True
            
        if self.system == 'Linux':
            # Check if Tor is installed
            tor_installed = subprocess.run(['which', 'tor'], capture_output=True).returncode == 0
            
            if not tor_installed:
                if not self.install_tor_linux():
                    return False
                    
            # Configure Tor
            self.configure_tor()
            
            # Start Tor
            if self.start_tor_linux():
                # Wait for Tor to be ready
                for i in range(10):
                    if self.check_tor_running():
                        print(f"{Colors.GREEN}[+] Tor is running{Colors.ENDC}")
                        return True
                    time.sleep(1)
                    
            print(f"{Colors.FAIL}[!] Could not start Tor{Colors.ENDC}")
            return False
            
        elif self.system == 'Windows':
            print(f"{Colors.WARNING}[!] On Windows, please ensure Tor Browser is running{Colors.ENDC}")
            print(f"{Colors.CYAN}[i] Tor Browser provides SOCKS proxy on port 9150{Colors.ENDC}")
            print(f"{Colors.YELLOW}[*] Waiting for Tor Browser...{Colors.ENDC}")
            
            # Wait for Tor Browser
            for i in range(30):
                if self.check_tor_running():
                    print(f"{Colors.GREEN}[+] Tor Browser detected{Colors.ENDC}")
                    return True
                time.sleep(1)
                
            print(f"{Colors.FAIL}[!] Tor Browser not detected{Colors.ENDC}")
            return False
            
        return False
        
    def get_random_user_agent(self) -> str:
        """Get random user agent"""
        return random.choice(CONFIG['user_agents'])
        
    def get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with randomization"""
        return {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
    def get_current_ip(self, retries: int = 3) -> Optional[str]:
        """Get current public IP through Tor"""
        for _ in range(retries):
            try:
                url = random.choice(CONFIG['check_ip_urls'])
                response = self.session.get(
                    url, 
                    proxies=self.current_proxy, 
                    headers=self.get_headers(),
                    timeout=15
                )
                if response.status_code == 200:
                    return response.text.strip()
            except Exception as e:
                self.logger.error(f"Failed to get IP: {e}")
                time.sleep(2)
        return None
        
    def get_ip_info(self, ip: str) -> Dict:
        """Get detailed IP information"""
        try:
            url = CONFIG['ip_info_url'].format(ip=ip)
            response = self.session.get(url, proxies=self.current_proxy, 
                                      headers=self.get_headers(), timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            self.logger.error(f"Failed to get IP info: {e}")
        return {}
        
    def change_tor_identity(self) -> bool:
        """Change Tor identity to get new IP"""
        try:
            if self.system == 'Linux':
                # Try to reload Tor to get new identity
                subprocess.run(['sudo', 'systemctl', 'reload', 'tor'], 
                             capture_output=True, timeout=10)
                subprocess.run(['sudo', 'killall', '-HUP', 'tor'], 
                             capture_output=True, timeout=5)
            else:
                # On Windows, we can't easily signal Tor Browser
                # Just wait for circuit to expire
                pass
                
            time.sleep(5)
            return True
        except Exception as e:
            self.logger.error(f"Failed to change identity: {e}")
            return False
            
    def set_exit_node(self, country_code: str) -> bool:
        """Set specific exit node country"""
        if self.system != 'Linux':
            return False
            
        try:
            # Create temporary torrc with exit node
            config = f"""
SocksPort 9050
ControlPort 9051
CookieAuthentication 0
ExitNodes {{{country_code}}}
StrictNodes 1
"""
            with open('/tmp/torrc_temp', 'w') as f:
                f.write(config)
                
            subprocess.run(['sudo', 'cp', '/tmp/torrc_temp', '/etc/tor/torrc'], 
                         capture_output=True)
            subprocess.run(['sudo', 'systemctl', 'reload', 'tor'], 
                         capture_output=True, timeout=10)
            time.sleep(5)
            return True
        except Exception as e:
            self.logger.error(f"Failed to set exit node: {e}")
            return False
            
    def reset_exit_node(self):
        """Reset exit node to random"""
        if self.system == 'Linux':
            self.configure_tor()
            subprocess.run(['sudo', 'systemctl', 'reload', 'tor'], 
                         capture_output=True, timeout=10)
            time.sleep(5)
            
    def save_results(self):
        """Save results to file"""
        with open(self.output_file, 'a') as f:
            f.write("\n" + "="*70 + "\n")
            f.write(f"Session Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*70 + "\n")
            for result in self.results:
                f.write(f"{result}\n")
            f.write(f"\nTotal IP changes: {len(self.results)}\n")
            
    def display_progress(self):
        """Display current progress"""
        if self.count == 0:
            print(f"{Colors.CYAN}[{self.iteration}] Changing IP... (Infinite mode){Colors.ENDC}")
        else:
            print(f"{Colors.CYAN}[{self.iteration}/{self.count}] Changing IP...{Colors.ENDC}")
            
    def run(self):
        """Main execution"""
        self.clear_screen()
        self.print_banner()
        
        # Display mode
        if self.count == 0:
            mode_str = f"{Colors.MAGENTA}INFINITE MODE{Colors.ENDC}"
        else:
            mode_str = f"{self.count} IP changes"
            
        print(f"{Colors.CYAN}Configuration:{Colors.ENDC}")
        print(f"  Interval: {self.interval} seconds")
        print(f"  Mode: {mode_str}")
        print(f"  Output file: {self.output_file}")
        print(f"  Platform: {self.system}\n")
        
        # Setup Tor
        if not self.setup_tor():
            print(f"{Colors.FAIL}[!] Tor setup failed. Exiting.{Colors.ENDC}")
            return
            
        print(f"\n{Colors.GREEN}[+] Starting IP changer...{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] Press Ctrl+C to stop\n{Colors.ENDC}")
        
        # Get list of countries
        countries = list(CONFIG['exit_nodes'].keys())
        
        while self.running:
            self.iteration += 1
            
            # Check if we've reached the count (if not infinite)
            if self.count > 0 and self.iteration > self.count:
                break
                
            self.display_progress()
            
            # Select random country
            country = random.choice(countries)
            country_name = CONFIG['exit_nodes'][country]
            
            # Set exit node (Linux only)
            if self.system == 'Linux':
                self.set_exit_node(country)
            else:
                # On Windows, just wait for natural circuit rotation
                time.sleep(3)
                
            # Change identity
            self.change_tor_identity()
            
            # Get new IP
            new_ip = self.get_current_ip()
            
            if new_ip:
                # Get IP info
                info = self.get_ip_info(new_ip)
                actual_country = info.get('country_code', 'Unknown')
                actual_country_name = info.get('country_name', 'Unknown')
                city = info.get('city', 'Unknown')
                isp = info.get('org', 'Unknown')
                
                # Display result
                print(f"{Colors.GREEN}    IP: {new_ip}{Colors.ENDC}")
                print(f"{Colors.GREEN}    Country: {actual_country_name} ({actual_country}){Colors.ENDC}")
                print(f"{Colors.GREEN}    City: {city}{Colors.ENDC}")
                print(f"{Colors.GREEN}    ISP: {isp}{Colors.ENDC}")
                print()
                
                # Log result
                result_str = (f"[{self.iteration}] IP: {new_ip} | "
                            f"Country: {actual_country_name} ({actual_country}) | "
                            f"City: {city} | ISP: {isp}")
                self.results.append(result_str)
                self.logger.info(result_str)
            else:
                error_msg = f"[{self.iteration}] Failed to get IP"
                print(f"{Colors.FAIL}    {error_msg}{Colors.ENDC}")
                self.results.append(error_msg)
                self.logger.error(error_msg)
                
            # Wait for next change
            if self.running:
                # Add random jitter to interval
                sleep_time = self.interval + random.randint(-3, 5)
                sleep_time = max(5, sleep_time)
                time.sleep(sleep_time)
                
        # Reset exit node
        self.reset_exit_node()
        
        # Save results
        self.save_results()
        
        # Print summary
        print(f"\n{Colors.CYAN}{'='*70}{Colors.ENDC}")
        if self.count == 0:
            print(f"{Colors.GREEN}Stopped! {len(self.results)} IP changes performed.{Colors.ENDC}")
        else:
            print(f"{Colors.GREEN}Completed! {len(self.results)} IP changes performed.{Colors.ENDC}")
        print(f"{Colors.GREEN}Results saved to: {self.output_file}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")

def get_user_input():
    """Get user input for interval and count"""
    print(f"{Colors.CYAN}\n{'='*70}{Colors.ENDC}")
    print(f"{Colors.GREEN}  Advanced Tor IP & Country Changer{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    # Get interval
    while True:
        try:
            interval_input = input(f"{Colors.YELLOW}Enter time interval in seconds (min 10): {Colors.ENDC}")
            interval = int(interval_input)
            if interval < 10:
                print(f"{Colors.FAIL}[!] Interval must be at least 10 seconds{Colors.ENDC}")
                continue
            break
        except ValueError:
            print(f"{Colors.FAIL}[!] Please enter a valid number{Colors.ENDC}")
    
    # Get count
    while True:
        try:
            count_input = input(f"{Colors.YELLOW}Enter number of IP changes (0 = infinite): {Colors.ENDC}")
            count = int(count_input)
            if count < 0:
                print(f"{Colors.FAIL}[!] Please enter 0 or a positive number{Colors.ENDC}")
                continue
            break
        except ValueError:
            print(f"{Colors.FAIL}[!] Please enter a valid number{Colors.ENDC}")
    
    # Get output file (optional)
    output_default = "ip_changer_results.txt"
    output_input = input(f"{Colors.YELLOW}Enter output filename (press Enter for '{output_default}'): {Colors.ENDC}").strip()
    output_file = output_input if output_input else output_default
    
    return interval, count, output_file

def main():
    # Check if command line arguments provided
    if len(sys.argv) >= 3:
        # Command line mode
        try:
            interval = int(sys.argv[1])
            count = int(sys.argv[2])
            output_file = sys.argv[3] if len(sys.argv) > 3 else "ip_changer_results.txt"
            
            if interval < 10:
                print(f"{Colors.FAIL}[!] Interval must be at least 10 seconds{Colors.ENDC}")
                sys.exit(1)
        except ValueError:
            print(f"{Colors.FAIL}[!] Invalid arguments. Usage: python ip_changer.py <interval> <count> [output_file]{Colors.ENDC}")
            sys.exit(1)
    else:
        # Interactive mode
        interval, count, output_file = get_user_input()
    
    # Create and run IP changer
    changer = IPChanger(interval, count, output_file)
    changer.run()

if __name__ == "__main__":
    main()
