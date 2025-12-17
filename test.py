import unittest
import os
import json

# Tuodaan testattavat funktiot ja muuttujat
from main import (
    caesar_encrypt,
    caesar_decrypt,
    is_strong_password,
    generate_password,
    save_passwords,
    load_passwords,
    websites,
    usernames,
    encrypted_passwords,
    SHIFT
)

class TestPasswordManager(unittest.TestCase):

    def setUp(self):
        """
        Ajetaan ennen jokaista testiä.
        Tyhjennetään listat ja poistetaan testitiedosto.
        """
        websites.clear()
        usernames.clear()
        encrypted_passwords.clear()

        if os.path.exists("vault.txt"):
            os.remove("vault.txt")

    def test_caesar_encrypt_and_decrypt(self):
        original = "Salasana123!"
        encrypted = caesar_encrypt(original, SHIFT)
        decrypted = caesar_decrypt(encrypted, SHIFT)

        self.assertEqual(original, decrypted)

    def test_strong_password(self):
        strong = "Vahva123!"
        weak = "abc"

        self.assertTrue(is_strong_password(strong))
        self.assertFalse(is_strong_password(weak))

    def test_generate_password_length(self):
        length = 12
        password = generate_password(length)

        self.assertEqual(len(password), length)

    def test_save_and_load_passwords(self):
        # Lisätään testidata
        websites.append("example.com")
        usernames.append("testuser")
        encrypted_passwords.append(caesar_encrypt("Test123!", SHIFT))

        # Tallennetaan
        save_passwords()
        self.assertTrue(os.path.exists("vault.txt"))

        # Tyhjennetään listat
        websites.clear()
        usernames.clear()
        encrypted_passwords.clear()

        # Ladataan
        load_passwords()

        self.assertEqual(websites[0], "example.com")
        self.assertEqual(usernames[0], "testuser")
        decrypted = caesar_decrypt(encrypted_passwords[0], SHIFT)
        self.assertEqual(decrypted, "Test123!")

    def tearDown(self):
        """
        Ajetaan jokaisen testin jälkeen.
        """
        if os.path.exists("vault.txt"):
            os.remove("vault.txt")


if __name__ == "__main__":
    unittest.main()

