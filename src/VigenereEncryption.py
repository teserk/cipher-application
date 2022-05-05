from .Globals import Alphabet


class VigenereEncryption:

    def encrypt(self, text, delta):
        """
        Зашифровывает сообщение шифром Виженера
        ---
        params: text, delta
        text : Текст (строка), который надо зашифровать. Если первая буква - символ или буква латиницы,
        то автоматически считает, что текст написан на английском. Иначе - написан на русском.
        delta : строка, шаг для шифра Виженера
        """
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
                char = cipher_alphabet.index(text[i])
                key = cipher_alphabet.index(delta[i % len(delta)])
                value = (char + key) % len(cipher_alphabet)
                encrypted += cipher_alphabet[value]
        return encrypted

    def decrypt(self, text, delta):
        """
        Расшифровывает сообщение шифром Виженера
        ---
        params: text, delta
        text : Текст (строка), который надо расшифровать. Если первая буква - символ или буква латиницы,
        то автоматически считает, что текст написан на английском. Иначе - написан на русском.
        delta : строка, шаг для шифра Виженера
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
                char = cipher_alphabet.index(text[i])
                key = cipher_alphabet.index(delta[i % len(delta)])
                value = (char - key) % len(cipher_alphabet)
                decrypted += cipher_alphabet[value]
        return decrypted