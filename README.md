# 🔐 Password Keeper

Password manager with terminal interface and AES-256 encryption. Keeps your passwords safe without the need for an internet connection or cloud services.

> #### This script was created to alleviate the problem of storing and remembering passwords, which the author himself faced.


## ✨ Peculiarities

- **🔒 Strong encryption**: AES-256 with PBKDF2 for key generation
- **🌍 Multilingual**: Russian and English languages supported
- **💾 Local storage**: All data is stored only on your device
- **📋 Convenience**: Automatic copying of passwords to the clipboard
- **🎨 Simple interface**: Convenient terminal menu


## 🚀 Installation

### Requirements
- Python 3.8+
- pip (Python package manager)

### Installing dependencies

```bash
## Clone the repository
git clone https://github.com/zkqw3r/password-keeper.git
cd password-keeper

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

- **pycryptodome** - cryptographic functions

- **stdiomask** - secure password entry with asterisks

- **pyperclip** - working with the clipboard

---

### 🎮 Usage
#### First run

```bash
python password_manager.py
```

When you first launch the program:

- Will prompt you to select a language

- Will ask for a master password

- Will create an encrypted storage

---

### Basic commands

```bash
Select an action:
1 - View passwords
2 - Add password
0 - Exit
```

### Adding a password

- Select **"Add password"**

- Enter the service name (for example, "Google")

- Enter the login

- Specify the password length (minimum 8 characters)

- The password will be automatically generated and copied to the clipboard


## 🔧 Technical details
### Encryption

- **Algorithm**: AES-256-CBC

- **Key derivation**: PBKDF2 with 100,000 iterations

- **Salt**: 32 random bytes

- **IV**: 16 random bytes for each encryption

---

### Data structure
```python
{
    "google.com": {
        "login": "user@gmail.com",
        "password": "aB3!xY7@qW2#zR5$"
    }
}
```

---

### Files

- **vault.enc** - encrypted password storage

- **salt.bin** - salt for key generation

- **locales/** - language files

- **logo.txt** - ASCII art logo

## 🌍 Language support
### Available languages

- **🇷🇺 Русский** (ru.json)

- **🇺🇸 English** (en.json)

#### Adding a new language

- Create a locales/language_code.json file

- Add translations of all keys from en.json

- Update the LANGUAGES dictionary in the code

## ⚠️ Security
### What is protected

- Passwords are encrypted before being written to disk

- The master password is never saved

- Encryption keys are stored in RAM only

### Recommendations

- Use a strong master password (12+ characters)

- Regularly backup vault.enc and salt.bin files

- Do not share these files with anyone

### 📝 To-do list

- [ ] A function that asks for a password once and stores the key
- [ ] A logout function
- [ ] One authentication per session
- [ ] Automatically log out when inactive
- [ ] Something else...