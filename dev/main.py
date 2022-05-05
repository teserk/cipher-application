from tkinter import END, Tk, Label, Frame, Text, Button, NONE
from tkinter.filedialog import askopenfile, asksaveasfile
import tkinter.messagebox as mb
from pathlib import Path
import random
from src.Globals import Alphabet
from src.CaesarEncryption import CaesarEncryption
from src.VernamEncryption import VernamEncryption
from src.VigenereEncryption import VigenereEncryption
from src.steganography import steganography_decrypt, steganography_encrypt


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


def LanguageValidation(key):
    """
    Проверяет ключ для шифра Виженера
    ---
    params: key
    key : ключ, который надо проверить
    """
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


def main():
    def encrypt():
        """
        Кнопка, которая считывает мод шифровки и по данному моду производит шифровку
        читает с text_input текст для шифровки и с key_input ключ для шифровки
        """
        if mode == 0:
            encryption_mode = CaesarEncryption()
            try:
                res = encryption_mode.encrypt(text_input.get("1.0", 'end-1c'), key_input.get("1.0", 'end-1c'))
                result.insert('1.0', res)
            except TypeError:
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
        """
        Кнопка, которая считывает мод расшифровки и по данному моду производит расшифровку
        читает с text_input текст для расшифровки и с key_input ключ для расшифровки
        """
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
        """
        Кнопка, меняющая режим шифровки
        """
        nonlocal mode
        mode = (mode + 1) % 3
        mode_button['text'] = 'Режим шифровки: ' + modes[mode]

    def load_file():
        """
        Кнопка, считывающая файл для шифровки
        """
        inp = askopenfile(mode="r")
        if inp is None:
            return
        data = inp.read()
        text_input.delete('1.0', END)
        text_input.insert('1.0', data)

    def save_file():
        """
        Кнопка, сохраняющая расшифрованный текст
        """
        out = asksaveasfile(mode='w', defaultextension='.txt')
        data = result.get('1.0', END)
        try:
            out.write(data.rstrip())
        except Exception:
            mb.showerror(title="Упс!", message="Не смог сохранить результат")

    def brute_force_caesar():
        """
        Кнопка, которая расшифровывает текст, зашифрованный шифром Цезаря, методом частотного анализа
        """
        encryption_mode = CaesarEncryption()
        try:
            res = encryption_mode.BRUTEFORCE(text_input.get("1.0", 'end-1c'))
            result.insert('1.0', res)
        except TypeError:
            mb.showerror('Ошибка', 'что то пошло не так')

    def stega_encrypt():
        """
        Кнопка, отвечающая за шифровку Стеганографии
        """
        img_to_decode = askopenfile(mode="w")
        if img_to_decode is None:
            return
        text_to_encode = text_input.get('1.0', 'end-1c')
        path_to_img = Path(img_to_decode.name)
        keys = steganography_encrypt(path_to_img, text_to_encode)
        mb.showinfo('Успешно!', 'Картинка сохранена с названием encoded_file.png')
        key_input.insert('1.0', keys)

    def stega_decrypt():
        """
        Кнопка, отвечающая за расшифровку Стеганографии
        """
        img_to_decode = askopenfile(mode="w", filetypes='.png')
        if img_to_decode is None:
            return
        path_to_img = Path(img_to_decode.name)
        keys = key_input.get('1.0', 'end-1c')
        decoded_text = steganography_decrypt(path_to_img, keys)
        text_input.delete('1.0', END)
        text_input.insert('1.0', 'end-1c')

    root = Tk()
    root.title("мега крутой шифроватор")
    root.geometry("1200x600+200+100")
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

    encrypt_image_button = Button(f1, text="Стеганография - зашифровка", command=stega_encrypt)
    decrypt_image_button = Button(f1, text="Стеганография - расшифровка", command=stega_decrypt)
    encrypt_image_button.pack()
    decrypt_image_button.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
