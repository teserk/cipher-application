from .Globals import Alphabet


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