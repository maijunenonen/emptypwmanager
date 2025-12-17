import json
import re
import random
import string

# Caesar-salakirjoituksen salaus- ja purkufunktiot
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# Salasanan vahvuuden tarkistusfunktio
def is_strong_password(password):
     """
    Tarkistaa, onko salasana riittävän vahva.
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Salasanan generointifunktio
def generate_password(length):
      """
    Luo satunnaisen vahvan salasanan annetun pituisena.
    """
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return "".join(random.choice(characters) for _ in range(length))


# Alustetaan tyhjät listat
encrypted_passwords = []
websites = []
usernames = []

SHIFT = 3  # Caesar-salauksen siirtoarvo

# Funktio uuden salasanan lisäämiseen
def add_password():
    website = input("Anna verkkosivun nimi: ")
    username = input("Anna käyttäjätunnus: ")

    choice = input("Generoidaanko vahva salasana? (k/e): ").lower()
    if choice == "k":
        length = int(input("Anna salasanan pituus: "))
        password = generate_password(length)
        print(f"Generoitu salasana: {password}")
    else:
        password = input("Anna salasana: ")
        if not is_strong_password(password):
            print("Varoitus: salasana on heikko.")

    encrypted = caesar_encrypt(password, SHIFT)

    websites.append(website)
    usernames.append(username)
    encrypted_passwords.append(encrypted)

    print("Salasana lisätty onnistuneesti!")


# Funktio salasanan hakemiseen
def get_password():
     website = input("Anna verkkosivun nimi: ")

    if website in websites:
        index = websites.index(website)
        username = usernames[index]
        decrypted_password = caesar_decrypt(encrypted_passwords[index], SHIFT)

        print(f"Käyttäjätunnus: {username}")
        print(f"Salasana: {decrypted_password}")
    else:
        print("Verkkosivua ei löytynyt.")

# Funktio salasanojen tallentamiseen
def save_passwords():
    vault = {
        "websites": websites,
        "usernames": usernames,
        "passwords": encrypted_passwords
    }

    with open("vault.txt", "w") as file:
        json.dump(vault, file)

    print("Salasanat tallennettu onnistuneesti!")

# Funktio salasanojen lataamiseen
def load_passwords():
    global websites, usernames, encrypted_passwords

    try:
        with open("vault.txt", "r") as file:
            vault = json.load(file)

        websites = vault["websites"]
        usernames = vault["usernames"]
        encrypted_passwords = vault["passwords"]

    except FileNotFoundError:
        print("Salasanaholvitiedostoa ei löytynyt.")

  # Pääfunktio
def main():
    while True:
        print("\nSalasananhallinnan valikko:")
        print("1. Lisää salasana")
        print("2. Hae salasana")
        print("3. Tallenna salasanat")
        print("4. Lataa salasanat")
        print("5. Lopeta")
    
    choice = input("Valitse toiminto: ")

        if choice == "1":
            add_password()
        elif choice == "2":
            get_password()
        elif choice == "3":
            save_passwords()
        elif choice == "4":
            load_passwords()
            print("Salasanat ladattu onnistuneesti!")
        elif choice == "5":
            print("Ohjelma suljetaan.")
            break
        else:
            print("Virheellinen valinta. Yritä uudelleen.")


# Suorittaa pääfunktion
if __name__ == "__main__":
    main()
