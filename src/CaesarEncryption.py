from .Globals import Alphabet
from collections import Counter


class CaesarEncryption:
    def encrypt(self, text, delta):
        """
        Зашифровывает сообщение шифром Цезаря
        ---
        params: text, delta
        text : Текст (строка), который надо зашифровать. Если первая буква - символ или буква латиницы,
        то автоматически считает, что текст написан на английском. Иначе - написан на русском.
        delta : целое число, шаг для шифра Цезаря
        """
        if not delta.isnumeric():
            raise TypeError
        delta = int(delta)
        text = text.lower()
        if text[0] in Alphabet.RU:
            cipher_alphabet = Alphabet.RU
        else:
            cipher_alphabet = Alphabet.EN

        encrypted = ''

        for i in range(len(text)):
            if text[i] not in cipher_alphabet:
                encrypted += text[i]
            else:
                char = text[i]
                encrypted += cipher_alphabet[(cipher_alphabet.find(char) + delta) % (len(cipher_alphabet))]
        return encrypted

    def decrypt(self, text, delta):
        """
        Расшифровывает сообщение шифром Цезаря
        ---
        params: text, delta
        text : Текст (строка), который надо расшифровать. Если первая буква - символ или буква латиницы,
        то автоматически считает, что текст написан на английском. Иначе - написан на русском.
        delta : целое число, шаг для шифра Цезаря
        """
        text = text.lower()
        if text[0] in Alphabet.RU:
            cipher_alphabet = Alphabet.RU
        else:
            cipher_alphabet = Alphabet.EN

        decrypted = ''

        for i in range(len(text)):
            if text[i] not in cipher_alphabet:
                decrypted += text[i]
            else:
                char = text[i]
                decrypted += cipher_alphabet[(cipher_alphabet.find(char) - delta) % (len(cipher_alphabet))]
        return decrypted

    def BRUTEFORCE(self, text):  # капсом, потому-что круче
        """
        Расшифровывает текст, зашифрованный шифром Цезаря методом частотного анализа
        ---
        params: text
        text : Текст (строка), который надо зашифровать. Если первая буква - символ или буква латиницы,
        то автоматически считает, что текст написан на английском. Иначе - написан на русском
        """
        text = text.lower()
        if text[0] in Alphabet.RU:
            cipher_alphabet = Alphabet.RU
        else:
            cipher_alphabet = Alphabet.EN

        refactored_text = ''
        for i in text:
            if i in cipher_alphabet:
                refactored_text += i
        ct = Counter(refactored_text)
        most_commons = ct.most_common(1)
        most_frequent = most_commons[0][0]
        delta = cipher_alphabet.index(most_frequent) - cipher_alphabet.index("о")
        return self.decrypt(text, delta)
