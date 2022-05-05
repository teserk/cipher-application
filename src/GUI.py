from tkinter import Tk, Label, Frame, Text, Button
import tkinter.messagebox as mb
import random
from pathlib import Path
from src.CaesarEncryption import CaesarEncryption
from src.VernamEncryption import VernamEncryption
from src.VigenereEncryption import VigenereEncryption
from src.steganography import steganography_decrypt, steganography_encrypt
from src.key_generator import key_generator_for_vernam
from src.languageValidation import LanguageValidation
from tkinter import END
from tkinter.filedialog import askopenfile, asksaveasfile


class UserInterface(Tk):
    def __init__(self, title):
        Tk.__init__(self)
        self.geometry("1200x600+200+100")
        self.title(title)
        self.build()

    def build(self):
        Label(self, text="Введите текст для шифровки:  ").grid(row=0, sticky='w')
        Label(self, text="Введите ключ:").grid(row=2, sticky='w')
        Label(self, text="Результат:").grid(row=4, sticky='w')

        f1 = Frame(self)
        f1.grid(row=6, columnspan=3, sticky='nsew')

        self.text_input = Text(self, width=40, height=3)
        self.key_input = Text(self, width=40, height=3)
        self.result = Text(self, width=40, height=3)

        self.text_input.grid(row=0, column=1, columnspan=3, rowspan=2)
        self.key_input.grid(row=2, column=1, columnspan=3, rowspan=2)
        self.result.grid(row=4, column=1, columnspan=3, rowspan=2)

        self.mode = 0
        self.modes = ['Caesar', 'Vigenere', 'Vernam']
        self.mode_button = Button(f1, text='Режим шифровки: ' + self.modes[self.mode], command=self.change_mode)
        self.mode_button.pack(side="left")

        self.encryption_button = Button(f1, text="Шифровать", command=self.encrypt)
        self.encryption_button.pack(side="left")

        self.decryption_button = Button(f1, text="Дешифровать", command=self.decrypt)
        self.decryption_button.pack(side="left")

        self.load_button = Button(f1, text="Загрузить текст", command=self.load_file)
        self.load_button.pack(side='left')

        self.save_button = Button(f1, text="Сохранить результат", command=self.save_file)
        self.save_button.pack(side='left')

        self.caesar_brute_force_button = Button(f1, text="расшифровка Цезаря", command=self.brute_force_caesar)
        self.caesar_brute_force_button.pack()

        self.encrypt_image_button = Button(f1, text="Стеганография - зашифровка", command=self.stega_encrypt)
        self.decrypt_image_button = Button(f1, text="Стеганография - расшифровка", command=self.stega_decrypt)
        self.encrypt_image_button.pack()
        self.decrypt_image_button.pack()

    def encrypt(self):
        """
        Кнопка, которая считывает мод шифровки и по данному моду производит шифровку
        читает с self.text_input текст для шифровки и с self.key_input ключ для шифровки
        """
        if self.mode == 0:
            encryption_mode = CaesarEncryption()
            try:
                res = encryption_mode.encrypt(self.text_input.get("1.0", 'end-1c'), self.key_input.get("1.0", 'end-1c'))
                self.result.insert('1.0', res)
            except TypeError:
                mb.showerror('Ошибка', 'Ключ для шифра Цезаря должен быть числом')
        if self.mode == 1:
            encryption_mode = VigenereEncryption()
            if not LanguageValidation(self.key_input.get('1.0', 'end-1c')):
                mb.showerror("Ошибка", "Ключ для шифра Виженера должен быть словом из мелких букв, \
                 написанных только на кириллице или только на латинице")
                return
            self.result.delete('1.0', END)
            self.result.insert('1.0',
                               encryption_mode.encrypt(self.text_input.get('1.0', 'end-1c'),
                                                       self.key_input.get('1.0', 'end-1c')))
        if self.mode == 2:
            encryption_mode = VernamEncryption()
            self.result.delete('1.0', END)
            try:
                res = encryption_mode.encrypt(self.text_input.get('1.0', 'end-1c'), self.key_input.get('1.0', 'end-1c'))
                self.result.insert('1.0', res)
            except TypeError:
                mb.showerror("Ошибка", "Длина ключа для шифра Вернама должна быть больше или равна \
                                        длине текста")

    def decrypt(self):
        """
        Кнопка, которая считывает мод расшифровки и по данному моду производит расшифровку
        читает с self.text_input текст для расшифровки и с self.key_input ключ для расшифровки
        """
        if self.mode == 0:
            encryption_mode = CaesarEncryption()
            if not self.key_input.get("1.0", 'end-1c').isnumeric():
                mb.showerror("Ошибка", "Ключ для шифра Цезаря должен быть целым числом")
                return
            self.result.delete('1.0', END)
            self.result.insert('1.0',
                               encryption_mode.decrypt(self.text_input.get('1.0', 'end-1c'),
                                                       int(self.key_input.get('1.0', 'end-1c'))))
        if self.mode == 1:
            encryption_mode = VigenereEncryption()
            if not LanguageValidation(self.key_input.get('1.0', 'end-1c')):
                mb.showerror("Ошибка", "Ключ для шифра Виженера должен быть словом из мелких букв, \
                 написанных только на кириллице или только на латинице")
                return
            self.result.delete('1.0', END)
            self.result.insert('1.0',
                               encryption_mode.decrypt(self.text_input.get('1.0', 'end-1c'),
                                                       self.key_input.get('1.0', 'end-1c')))
        if self.mode == 2:
            encryption_mode = VernamEncryption()
            self.result.delete('1.0', END)
            try:
                res = encryption_mode.encrypt(self.text_input.get('1.0', 'end-1c'), self.key_input.get('1.0', 'end-1c'))
                self.result.insert('1.0', res)
            except TypeError:
                mb.showerror("Ошибка", "Длина ключа для шифра Вернама должна быть больше или равна \
                                                    длине текста")

    def change_mode(self):
        """
        Кнопка, меняющая режим шифровки
        """
        self.mode = (self.mode + 1) % 3
        self.mode_button['text'] = 'Режим шифровки: ' + self.modes[self.mode]

    def load_file(self):
        """
        Кнопка, считывающая файл для шифровки
        """
        inp = askopenfile(mode="r")
        if inp is None:
            return
        data = inp.read()
        self.text_input.delete('1.0', END)
        self.text_input.insert('1.0', data)

    def save_file(self):
        """
        Кнопка, сохраняющая расшифрованный текст
        """
        out = asksaveasfile(mode='w', defaultextension='.txt')
        data = self.result.get('1.0', END)
        try:
            out.write(data.rstrip())
        except Exception:
            mb.showerror(title="Упс!", message="Не смог сохранить результат")

    def brute_force_caesar(self):
        """
        Кнопка, которая расшифровывает текст, зашифрованный шифром Цезаря, методом частотного анализа
        """
        encryption_mode = CaesarEncryption()
        try:
            res = encryption_mode.BRUTEFORCE(self.text_input.get("1.0", 'end-1c'))
            self.result.insert('1.0', res)
        except TypeError:
            mb.showerror('Ошибка', 'что то пошло не так')

    def stega_encrypt(self):
        """
        Кнопка, отвечающая за шифровку Стеганографии
        """
        img_to_decode = askopenfile(mode="w")
        if img_to_decode is None:
            return
        text_to_encode = self.text_input.get('1.0', 'end-1c')
        path_to_img = Path(img_to_decode.name)
        keys = steganography_encrypt(path_to_img, text_to_encode)
        mb.showinfo('Успешно!', 'Картинка сохранена с названием encoded_file.png')
        self.key_input.insert('1.0', keys)

    def stega_decrypt(self):
        """
        Кнопка, отвечающая за расшифровку Стеганографии
        """
        img_to_decode = askopenfile(mode="w", filetypes='.png')
        if img_to_decode is None:
            return
        path_to_img = Path(img_to_decode.name)
        keys = self.key_input.get('1.0', 'end-1c')
        decoded_text = steganography_decrypt(path_to_img, keys)
        self.text_input.delete('1.0', END)
        self.text_input.insert('1.0', 'end-1c')
