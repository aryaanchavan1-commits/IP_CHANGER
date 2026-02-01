# 🔒 Advanced Automatic IP Changer - Tor IP & Country Changer

A powerful, fully automatic IP changer compatible with **Kali Linux** and **Windows**. This tool automatically configures Tor, changes your IP address and country at specified intervals, and saves all results to a file.

![Version](https://img.shields.io/badge/version-3.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-orange.svg)

## ✨ Features

- 🚀 **Fully Automatic** - Just run and enter values, everything else is automatic
- 🌐 **Auto Tor Setup** - Automatically installs and configures Tor on Linux
- 🌍 **Country Rotation** - Automatically changes to random countries (US, GB, DE, FR, etc.)
- 🔄 **Auto IP Changer** - Changes IP at your specified interval
- ♾️ **Infinite Mode** - Set count to 0 for infinite IP changes
- 📝 **Results Logging** - Saves all IP changes with country info to a file
- 🛡️ **Anti-Detection** - Random User-Agent rotation and header randomization
- 💻 **Terminal Based** - Run directly from command line
- 🖥️ **Cross Platform** - Works on Kali Linux and Windows
- ⌨️ **Interactive Mode** - User-friendly prompts for input

## 📋 Requirements

- Python 3.7 or higher
- Internet connection
- Administrator/root access (for automatic Tor installation on Linux)

## 🚀 Quick Start

### 1. Install Python Dependency
```bash
pip install requests
```

### 2. Run the Tool

Simply run the script and follow the prompts:

```bash
python ip_changer.py
```

The tool will ask for:
- **Time interval** (seconds between IP changes, minimum 10)
- **Number of IP changes** (enter 0 for infinite mode)
- **Output filename** (press Enter for default)

### Alternative: Command Line Arguments

You can also provide arguments directly:

```bash
python ip_changer.py <interval_seconds> <number_of_ips> [output_file]
```

**Examples:**
```bash
# Change IP every 30 seconds, 10 times
python ip_changer.py 30 10

# Change IP every minute, 5 times
python ip_changer.py 60 5

# Infinite mode - change IP every 30 seconds forever
python ip_changer.py 30 0

# Custom output file
python ip_changer.py 30 10 my_results.txt
```

## 📖 Usage Examples

### Interactive Mode (Recommended)

```bash
$ python ip_changer.py

======================================================================
  Advanced Tor IP & Country Changer
======================================================================

Enter time interval in seconds (min 10): 30
Enter number of IP changes (0 = infinite): 0
Enter output filename (press Enter for 'ip_changer_results.txt'): 

    ___  ____  _____    _    _   _ ____  _____ ____  
   ...

Configuration:
  Interval: 30 seconds
  Mode: INFINITE MODE
  Output file: ip_changer_results.txt
  Platform: Linux

[*] Setting up Tor...
[+] Tor is running

[+] Starting IP changer...
[*] Press Ctrl+C to stop

[1] Changing IP... (Infinite mode)
    IP: 185.220.101.42
    Country: Germany (DE)
    City: Berlin
    ISP: Tor Exit Node

[2] Changing IP... (Infinite mode)
    IP: 198.51.100.15
    Country: United States (US)
    City: New York
    ISP: Tor Exit Node
...
```

### Infinite Mode

To run forever (until you press Ctrl+C):

```bash
$ python ip_changer.py
Enter time interval in seconds (min 10): 30
Enter number of IP changes (0 = infinite): 0
```

Or via command line:
```bash
python ip_changer.py 30 0
```

## 🌍 Supported Countries

The tool automatically rotates between these 20 countries:
- 🇺🇸 United States (US)
- 🇬🇧 United Kingdom (GB)
- 🇩🇪 Germany (DE)
- 🇫🇷 France (FR)
- 🇳🇱 Netherlands (NL)
- 🇨🇦 Canada (CA)
- 🇦🇺 Australia (AU)
- 🇯🇵 Japan (JP)
- 🇸🇬 Singapore (SG)
- 🇮🇳 India (IN)
- 🇷🇺 Russia (RU)
- 🇸🇪 Sweden (SE)
- 🇨🇭 Switzerland (CH)
- 🇳🇴 Norway (NO)
- 🇫🇮 Finland (FI)
- 🇩🇰 Denmark (DK)
- 🇵🇱 Poland (PL)
- 🇮🇹 Italy (IT)
- 🇪🇸 Spain (ES)
- 🇧🇷 Brazil (BR)

## 📄 Output File Format

Results are saved in a text file with the following format:

```
2024-01-01 12:00:01 - [1] IP: 185.220.101.42 | Country: Germany (DE) | City: Berlin | ISP: Tor Exit Node
2024-01-01 12:00:31 - [2] IP: 198.51.100.15 | Country: United States (US) | City: New York | ISP: Tor Exit Node
2024-01-01 12:01:02 - [3] IP: 203.0.113.78 | Country: Japan (JP) | City: Tokyo | ISP: Tor Exit Node
...

======================================================================
Session Summary - 2024-01-01 12:05:00
======================================================================
[1] IP: 185.220.101.42 | Country: Germany (DE) | City: Berlin | ISP: Tor Exit Node
[2] IP: 198.51.100.15 | Country: United States (US) | City: New York | ISP: Tor Exit Node
...

Total IP changes: 10
```

## 🖥️ Terminal Output Example

```
======================================================================
  Advanced Tor IP & Country Changer
======================================================================

Enter time interval in seconds (min 10): 30
Enter number of IP changes (0 = infinite): 5
Enter output filename (press Enter for 'ip_changer_results.txt'): 

    ___  ____  _____    _    _   _ ____  _____ ____  
   ...
       Automatic Tor IP & Country Changer v3.1
              by Aryan Chavan
       Compatible with Kali Linux & Windows

Configuration:
  Interval: 30 seconds
  Mode: 5 IP changes
  Output file: ip_changer_results.txt
  Platform: Linux

[*] Setting up Tor...
[+] Tor is running

[+] Starting IP changer...
[*] Press Ctrl+C to stop

[1/5] Changing IP...
    IP: 185.220.101.42
    Country: Germany (DE)
    City: Berlin
    ISP: Tor Exit Node

[2/5] Changing IP...
    IP: 198.51.100.15
    Country: United States (US)
    City: New York
    ISP: Tor Exit Node

...

======================================================================
Completed! 5 IP changes performed.
Results saved to: ip_changer_results.txt
======================================================================
```

## ⚙️ How It Works

1. **User Input**: Asks for interval and number of IP changes (or accepts command line args)
2. **Automatic Tor Setup**: On Linux, automatically installs and configures Tor if not present
3. **Country Selection**: Randomly selects a country from the supported list
4. **Tor Configuration**: Sets Tor to use an exit node from the selected country
5. **IP Change**: Reloads Tor to get a new IP address
6. **Verification**: Retrieves the new IP and geolocation info
7. **Logging**: Saves all information to the output file
8. **Repeat**: Waits for the specified interval and repeats (or runs forever in infinite mode)

## 🔧 Platform-Specific Instructions

### Kali Linux

The tool will automatically:
1. Check if Tor is installed
2. Install Tor if missing (requires sudo)
3. Configure Tor optimally
4. Start the Tor service
5. Change IP and country automatically
6. Save results to file

```bash
# Run with sudo for automatic Tor installation
sudo python ip_changer.py
```

### Windows

1. Download and install [Tor Browser](https://www.torproject.org/download/)
2. Launch Tor Browser
3. Run the tool:

```bash
python ip_changer.py
```

The tool will detect Tor Browser and use it automatically.

## ⚠️ Important Notes

### Requirements
- **Linux**: Run with `sudo` for automatic Tor installation
- **Windows**: Tor Browser must be running before starting the tool
- **Interval**: Minimum 10 seconds between changes (to allow Tor circuits to build)

### Infinite Mode
- Enter `0` when asked for "number of IP changes"
- The tool will run forever until you press **Ctrl+C**
- All IPs are still logged to the output file

### Security
- All traffic is routed through the Tor network
- Random User-Agent headers prevent fingerprinting
- No personal data is collected or transmitted

### Legal
- This tool is for **educational and privacy purposes only**
- Always comply with local laws and regulations
- Do not use for illegal activities

## 🛠️ Troubleshooting

### "Tor setup failed"
- On Linux: Make sure you have sudo privileges
- On Windows: Make sure Tor Browser is running

### "Failed to get IP"
- Check your internet connection
- Increase the interval time (Tor needs time to build circuits)
- Restart Tor and try again

### Permission Denied (Linux)
```bash
sudo python ip_changer.py
```

### Module Not Found
```bash
pip install requests
```

## 📞 Support

**Author**: Aryan Chavan  
**GitHub**: [aryaanchavan1-commits](https://github.com/aryaanchavan1-commits)

---

**⚠️ Disclaimer**: This tool is provided for educational purposes only. Users are responsible for complying with applicable laws and regulations.

**Stay Anonymous! 🔒**
