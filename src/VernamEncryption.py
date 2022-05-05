def text_to_binary(text):
    """
    Переводит текст в бинарный вид
    ---
    params: text
    text : текст (Строка)
    """
    return [int(format(ord(elem), 'b')) for elem in text]


def binary_to_text(binary_text):
    """
    Переводит текст в бинарном виде в нормальный вид
    ---
    params: binary_text
    binary_text : текст (строка) в бинарном виде
    """
    return [chr(int(str(elem), 2)) for elem in binary_text]


class VernamEncryption:

    def encrypt(self, text, delta):
        """
        Зашифровывает/расшифровывает сообщение шифром Вернама
        ---
        params: text, delta
        text : Текст (строка), который надо зашифровать/расшифровать.
        delta : ключ для шифра Вернама. Длина должна быть больше, чем длина текста
        """
        if len(text) > len(delta):
            raise TypeError
        text, delta = text_to_binary(text), text_to_binary(delta)
        encrypted = []
        for i in range(len(text)):
            encrypted_char = format((int(str(text[i]), 2) ^ int(str(delta[i]), 2)), 'b')
            encrypted.append(encrypted_char)
        encrypted = binary_to_text(encrypted)
        result = ''.join([str(item) for item in encrypted])
        return result
