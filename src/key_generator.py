import random


def key_generator_for_vernam(text):
    """
    Генерирует ключ для шифра Вернама
    ---
    params: text
    text : текст. Нужна только его длина
    """
    key = ''
    for i in range(len(text)):
        key += chr(random.randint(1, 1114111))
    return key
