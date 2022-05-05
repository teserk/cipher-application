import random
from PIL import Image, ImageDraw
from re import findall


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


def steganography_encrypt(path_to_img, text):
    """
    Стеганография, шифрует в изображении текст, и сохраняет его в виде encoded_file.png
    ---
    params: path_to_img, text
    path_to_img : путь к исходному изображению
    text : текст, который надо зашифровать
    """
    keys = ''

    img = Image.open(path_to_img)
    draw = ImageDraw.Draw(img)
    width = img.size[0]
    height = img.size[1]
    pix = img.load()
    for elem in ([ord(elem) for elem in text]):
        key = (random.randint(1, width - 10), random.randint(1, height - 10))
        g, b = pix[key][1:3]
        draw.point(key, (elem, g, b))
        keys += key
    img.save('encoded_file.png', "PNG")
    return keys


def steganography_decrypt(path_to_img, key):
    """
    Стеганография, расшифровывает в изображении текст, и возвращает его
    ---
    params: path_to_img, key
    path_to_img : путь к исходному изображению
    key : ключ для расшифровки
    """
    a = []
    keys = []
    img = Image.open(path_to_img)
    pix = img.load()
    y = str([line.strip() for line in key])
    for i in range(len(findall(r'\((\d+),', y))):
        keys.append((int(findall(r'\((\d+),', y)[i]), int(findall(r',\s(\d+)\)', y)[i])))
    for key in keys:
        a.append(pix[tuple(key)][0])
    return ''.join([chr(elem) for elem in a])