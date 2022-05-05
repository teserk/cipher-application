from tkinter import *
from tkinter.filedialog import *
import tkinter.messagebox as mb
from abc import ABC, abstractmethod
import random
from PIL import Image, ImageDraw, ImageTk
from collections import Counter
from Globals import Alphabet


class CaesarEncryption:

    def encrypt(self, text, delta):
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


class VigenereEncryption:

    def encrypt(self, text, delta):
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


def LanguageValidation(key):
    if not key:
        return 0
    if key[0] in Alphabet.RU:
        for i in key:
            if i not in Alphabet.RU:
                return 0
    else:
        for i in key:
            if i not in Alphabet.EN:
                return 0
    return 1


class VernamEncryption:

    def encrypt(self, text, delta):
        if len(text) > len(delta):
            raise TypeError
        text, delta = text_to_binary(text), text_to_binary(delta)
        encrypted = []
        for i in range(len(text)):
            encrypted.append(format((int(str(text[i]), 2) ^ int(str(delta[i]), 2)), 'b'))
        encrypted = binary_to_text(encrypted)
        result = ''.join([str(item) for item in encrypted])
        return result


def key_generator_for_vernam(text):
    key = ''
    for i in range(len(text)):
        key += chr(random.randint(1, 1114111))
    return key


def text_to_binary(event):
    return [int(format(ord(elem), 'b')) for elem in event]


def binary_to_text(event):
    return [chr(int(str(elem), 2)) for elem in event]


def steganography_encrypt(text):
    keys = []
    img_to_decode = askopenfile(mode="w", filetypes='.png')
    if img_to_decode is None:
        return

    draw = ImageDraw.Draw(img_to_decode)
    width = img_to_decode.size[0]
    height = img_to_decode.size[1]
    pix = img_to_decode.load()
    for elem in ([ord(elem) for elem in text]):
        key = (random.randint(1, width - 10), random.randint(1, height - 10))
        g, b = pix[key][1:3]
        draw.point(key, (elem, g, b))
        keys.append(key)
    img_to_decode.save('encoded_file.png', "PNG")


def main():
    def encrypt():
        if mode == 0:
            encryption_mode = CaesarEncryption()
            try:
                res = encryption_mode.encrypt(text_input.get("1.0", 'end-1c'), key_input.get("1.0", 'end-1c'))
                result.insert('1.0', res)
            except Exception:
                mb.showerror('Ошибка', 'Ключ для шифра Цезаря должен быть числом')
        if mode == 1:
            encryption_mode = VigenereEncryption()
            if not LanguageValidation(key_input.get('1.0', 'end-1c')):
                mb.showerror("Ошибка", "Ключ для шифра Виженера должен быть словом из мелких букв, \
                 написанных только на кириллице или только на латинице")
                return
            result.delete('1.0', END)
            result.insert('1.0',
                          encryption_mode.encrypt(text_input.get('1.0', 'end-1c'), key_input.get('1.0', 'end-1c')))
        if mode == 2:
            encryption_mode = VernamEncryption()
            result.delete('1.0', END)
            try:
                res = encryption_mode.encrypt(text_input.get('1.0', 'end-1c'), key_input.get('1.0', 'end-1c'))
                result.insert('1.0', res)
            except TypeError:
                mb.showerror("Ошибка", "Длина ключа для шифра Вернама должна быть больше или равна \
                                        длине текста")

    def decrypt():
        if mode == 0:
            encryption_mode = CaesarEncryption()
            if not key_input.get("1.0", 'end-1c').isnumeric():
                mb.showerror("Ошибка", "Ключ для шифра Цезаря должен быть целым числом")
                return
            result.delete('1.0', END)
            result.insert('1.0',
                          encryption_mode.decrypt(text_input.get('1.0', 'end-1c'), int(key_input.get('1.0', 'end-1c'))))
        if mode == 1:
            encryption_mode = VigenereEncryption()
            if not LanguageValidation(key_input.get('1.0', 'end-1c')):
                mb.showerror("Ошибка", "Ключ для шифра Виженера должен быть словом из мелких букв, \
                 написанных только на кириллице или только на латинице")
                return
            result.delete('1.0', END)
            result.insert('1.0',
                          encryption_mode.decrypt(text_input.get('1.0', 'end-1c'), key_input.get('1.0', 'end-1c')))
        if mode == 2:
            encryption_mode = VernamEncryption()
            result.delete('1.0', END)
            try:
                res = encryption_mode.encrypt(text_input.get('1.0', 'end-1c'), key_input.get('1.0', 'end-1c'))
                result.insert('1.0', res)
            except TypeError:
                mb.showerror("Ошибка", "Длина ключа для шифра Вернама должна быть больше или равна \
                                                    длине текста")

    def change_mode():
        nonlocal mode
        mode = (mode + 1) % 3
        mode_button['text'] = 'Режим шифровки: ' + modes[mode]

    def load_file():
        inp = askopenfile(mode="r")
        if inp is None:
            return
        FILE_NAME = inp.name
        data = inp.read()
        text_input.delete('1.0', END)
        text_input.insert('1.0', data)

    def save_file():
        out = asksaveasfile(mode='w', defaultextension='.txt')
        data = result.get('1.0', END)
        try:
            out.write(data.rstrip())
        except Exception:
            mb.showerror(title="Упс!", message="Не смог сохранить результат")

    def brute_force_caesar():
        encryption_mode = CaesarEncryption()
        try:
            res = encryption_mode.BRUTEFORCE(text_input.get("1.0", 'end-1c'))
            result.insert('1.0', res)
        except TypeError:
            mb.showerror('Ошибка', 'что то пошло не так')

    def stega_encrypt():
        ...

    def stega_decrypt():
        ...

    root = Tk()
    root.title("мега крутой шифроватор")
    root.geometry("800x600+200+100")
    Label(root, text="Введите текст для шифровки:  ").grid(row=0, sticky='w')
    Label(root, text="Введите ключ:").grid(row=2, sticky='w')
    Label(root, text="Результат:").grid(row=4, sticky='w')

    f1 = Frame(root)
    f1.grid(row=6, columnspan=3, sticky='nsew')

    text_input = Text(root, width=40, height=3)
    key_input = Text(root, width=40, height=3)
    result = Text(root, width=40, height=3)

    text_input.grid(row=0, column=1, columnspan=3, rowspan=2)
    key_input.grid(row=2, column=1, columnspan=3, rowspan=2)
    result.grid(row=4, column=1, columnspan=3, rowspan=2)

    FILE_NAME = NONE

    mode = 0
    modes = ['Caesar', 'Vigenere', 'Vernam']
    mode_button = Button(f1, text='Режим шифровки: ' + modes[mode], command=change_mode)
    mode_button.pack(side="left")

    encryption_button = Button(f1, text="Шифровать", command=encrypt)
    encryption_button.pack(side="left")

    decryption_button = Button(f1, text="Дешифровать", command=decrypt)
    decryption_button.pack(side="left")

    load_button = Button(f1, text="Загрузить текст", command=load_file)
    load_button.pack(side='left')

    save_button = Button(f1, text="Сохранить результат", command=save_file)
    save_button.pack(side='left')

    caesar_brute_force_button = Button(f1, text="расшифровка Цезаря", command=brute_force_caesar)
    caesar_brute_force_button.pack()

    load_image_button = Button(f1, text="Зашифровать в изображение", command=stega_encrypt)
    load_image_button.pack(side='left')

    decrypt_image_button = Button(f1, text="Расшифровать что-то в сообщении", command=stega_decrypt)

    root.mainloop()


if __name__ == '__main__':
    main()
