import re
from colorama import Fore, Style, init
import requests
import os
import time
import datetime

init(autoreset=True)

def display_banner():
    banner = """
╭─────[By 0xSaikat]──────────────────────────────────╮
│                                                    │           
│       _____ __    _      __    __                  │
│      / ___// /_  (_)__  / /___/ / __               │
│      \__ \\/ __ \\/ / _ \\/ / __  /_/ /_              │
│     ___/ / / / / /  __/ / /_/ /_  __/              │
│    /____/_/ /_/_/\\___/_/\\__,_/ /_/                 │
│                                                    │                                                    
│                                                    │           
╰──────────────────────────────[hackbit.org]─────────╯
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)

def download_rockyou_file():
    url = 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt'
    response = requests.get(url)
    with open('rockyou.txt', 'wb') as file:
        file.write(response.content)

def is_password_in_rockyou(password):
    if not os.path.isfile('rockyou.txt'):
        download_rockyou_file()
    with open('rockyou.txt', 'r', encoding='latin-1') as file:
        for line in file:
            if password == line.strip():
                return True
    return False

def password_strength(password):
    length = len(password)
    complexity = 0
    suggestions = []
    
    if length >= 8:
        complexity += 1
    else:
        suggestions.append("🔸 " + Fore.YELLOW + "Make your password at least 8 characters long.")

    if re.search(r"[a-z]", password):
        complexity += 1
    else:
        suggestions.append("🔸 " + Fore.YELLOW + "Include at least one lowercase letter.")

    if re.search(r"[A-Z]", password):
        complexity += 1
    else:
        suggestions.append("🔸 " + Fore.YELLOW + "Include at least one uppercase letter.")

    if re.search(r"\d", password):
        complexity += 1
    else:
        suggestions.append("🔸 " + Fore.YELLOW + "Include at least one digit.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        complexity += 1
    else:
        suggestions.append("🔸 " + Fore.YELLOW + "Include at least one special character (e.g., !, @, #, $, etc.).")

    if re.search(r"(.)\1{2,}", password):
        complexity -= 1
        suggestions.append("🔸 " + Fore.YELLOW + "Avoid sequences of the same character (e.g., 'aaa').")

    if complexity == 0:
        strength = "Very Weak"
        color = Fore.RED
        emoji = "🔴"
    elif complexity == 1:
        strength = "Weak"
        color = Fore.RED
        emoji = "🟠"
    elif complexity == 2:
        strength = "Moderate"
        color = Fore.YELLOW
        emoji = "🟡"
    elif complexity == 3:
        strength = "Strong"
        color = Fore.GREEN
        emoji = "🟢"
    elif complexity == 4:
        strength = "Very Strong"
        color = Fore.GREEN
        emoji = "🟢"
    else:
        strength = "Excellent"
        color = Fore.CYAN
        emoji = "🔵"
    
    return f"{color}Password Strength: {strength} {emoji}", suggestions, strength

def save_password(password, description=""):
    # Create passwords directory if it doesn't exist
    if not os.path.exists("passwords"):
        os.mkdir("passwords")
    
    # Create date directory
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    date_dir = os.path.join("passwords", today)
    if not os.path.exists(date_dir):
        os.mkdir(date_dir)
    
    # Create a timestamp for the filename
    timestamp = datetime.datetime.now().strftime("%H-%M-%S")
    filename = f"password_{timestamp}.txt"
    file_path = os.path.join(date_dir, filename)
    
    # Save the password with description
    with open(file_path, "w") as file:
        file.write(f"Password: {password}\n")
        if description:
            file.write(f"Description: {description}\n")
        file.write(f"Date saved: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    return file_path

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    display_banner()
    
    linkedin_saikat = "https://www.linkedin.com/in/0xsaikat/"
    hackbit_url = "https://hackbit.org"
    
    link_saikat = f"\033]8;;{linkedin_saikat}\033\\@0xSaikat\033]8;;\033\\"
    link_hackbit = f"\033]8;;{hackbit_url}\033\\hackbit.org\033]8;;\033\\"
    
    while True:
        user_password = input(Fore.GREEN + "🔑 Enter your password to check its strength (or press 'q' to quit): " + Style.RESET_ALL)
        
        if user_password.lower() == 'q':
            print(Fore.CYAN + "Goodbye! 👋")
            break
        
        print()

        if is_password_in_rockyou(user_password):
            print(Fore.RED + "[+] " + Style.RESET_ALL + "Your password is weak and exposed on the internet...!")
            secure_choice = input(Fore.RED + "[+] " + Style.RESET_ALL + "Do you want to secure your password and make it strong (yes/no)? " + Style.RESET_ALL)
            if secure_choice.lower() == 'yes':
                print("\n🔸 Use a mix of uppercase and lowercase letters.")
                print("🔸 Include at least one digit.")
                print("🔸 Add special characters like !, @, #, $, etc.")
                print("🔸 Make your password at least 12 characters long.")
                print("🔸 Avoid using common words or easily guessable information.")
                print("🔸 Avoid using sequences of the same character.\n")
            else:
                print(Fore.CYAN + "Goodbye! 👋")
                break
        else:
            strength, suggestions, strength_level = password_strength(user_password)
            print(Fore.RED + "[+] " + Style.RESET_ALL + "Your password is safe...!")
            print(strength + "\n")
            
            if suggestions:
                print(Fore.RED + "[+] " + Style.RESET_ALL + "Here are some recommendations to make a good password:")
                for suggestion in suggestions:
                    print(suggestion)
            
            if strength_level in ["Strong", "Very Strong", "Excellent"]:
                save_choice = input(Fore.GREEN + "[+] " + Style.RESET_ALL + "Would you like to save this password? (yes/no): " + Style.RESET_ALL)
                if save_choice.lower() == 'yes':
                    description = input(Fore.GREEN + "[+] " + Style.RESET_ALL + "Enter a description for this password: " + Style.RESET_ALL)
                    saved_path = save_password(user_password, description)
                    print(Fore.GREEN + "[+] " + Style.RESET_ALL + f"Password saved to: {saved_path}")
            
            secure_choice = input(Fore.RED + "[+] " + Style.RESET_ALL + "Do you want to make the password more strong (yes/no)? " + Style.RESET_ALL)
            if secure_choice.lower() == 'yes':
                print("\n🔸 Use a mix of uppercase and lowercase letters.")
                print("🔸 Include at least one digit.")
                print("🔸 Add special characters like !, @, #, $, etc.")
                print("🔸 Make your password at least 12 characters long.")
                print("🔸 Avoid using common words or easily guessable information.")
                print("🔸 Avoid using sequences of the same character.\n")
            else:
                print(Fore.CYAN + "Goodbye! 👋")
                break

if __name__ == "__main__":
    main()
