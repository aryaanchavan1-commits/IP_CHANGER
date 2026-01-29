import requests 
import time
import os
import random 

TOR_PROXY = {
    "http": 'socks5h://127.0.0.1:9050',
    "https": 'socks5h://127.0.0.1:9050'
}

MESSAGES ={
    'en':{
        'welcome': "Welcome to the automatic IP Changer! -- by aryan chavan",
        'interval_prompt': "Enter time interval in seconds (e.g. 30): ",
        'count_prompt': "Enter how many times to change IP (0 = infinite): ",
        'invalid_number': "Invalid number entered.",
        'infinite_mode': "Starting infinite mode. Press Ctrl+C to stop.",
        'changing_ip': "[+] Reloading Tor service...",
        'ip_output': "New IP address: ",
        'error': "Failed to get IP: "
    },
    'mr':{
        'welcome': "स्वागत आहे ऑटोमॅटिक IP चेंजरमध्ये! -- आर्यन चव्हाण द्वारा",
        'interval_prompt': "सेकंदांमध्ये वेळ अंतर प्रविष्ट करा (उदा. 30): ",
        'count_prompt': "IP किती वेळा बदलायचा आहे ते प्रविष्ट करा (0 = अनंत): ",
        'invalid_number': "अवैध संख्या प्रविष्ट केली.",
        'infinite_mode': "अनंत मोड सुरू करत आहे. थांबवण्यासाठी Ctrl+C दाबा.",
        'changing_ip': "[+] टॉर सेवा रीलोड करत आहे...",
        'ip_output': "नवीन IP पत्ता: ",
        'error': "IP मिळवण्यात अयशस्वी: "
    }
}
def colorize(text, color_code):
    return f"{color_code}{text}\033[0m"

def get_ip(lang):
    try:
        response = requests.get('https://checkip.amazonaws.com', proxies=TOR_PROXY, timeout=10)
        return response.text.strip()
    except Exception as e:
        return f"{MESSAGES[lang]['error']} {e}"
    
def change_tor_ip(lang):
    print(MESSAGES[lang]['changing_ip'])
    os.system("sudo systemctl reload tor")
    time.sleep(5)

def print_ascii_art():
    os.system("clear")
    ascii_art = """

                            
 ___________ ______            __________ 
  |        | |     |   \     / |         | |\     | 
  |        | |     |    \   /  |         | | \    |
  |        | |_____|     \ /   |         | |  \   |
  |________| |      \     |    |_________| |   \  |
  |        | |       \    |    |         | |    \ |
  |        | |        \   |    |         | |     \|   .py
             
  
                
"""

    print(ascii_art)

def main():
    print_ascii_art()


    lang = input("Choose language (en/tr): ").lower()
    if lang not in MESSAGES:
        print("Unsupported language. Default: en")
        lang = 'en'

    print(MESSAGES[lang]['welcome'])

    try:
        interval = int(input(MESSAGES[lang]['interval_prompt']))
        count = int(input(MESSAGES[lang]['count_prompt']))
    except ValueError:
        print(MESSAGES[lang]['invalid_number'])
        return 
    
    if count == 0:
        print(MESSAGES[lang]['infinite_mode'])  #forever
        while True:
            change_tor_ip(lang)
            print(MESSAGES[lang]['ip_output'], get_ip(lang))  #visible output
            time.sleep(random.randint(interval - 5, interval + 5))  
    else:
        for i in range(count):
            change_tor_ip(lang)
            new_ip = get_ip(lang)
            print(f"[{i+1}/{count}] {MESSAGES[lang]['ip_output']}{colorize(new_ip, '\033[92m')}")
            time.sleep(interval)

if __name__ == "__main__":
    main()  
