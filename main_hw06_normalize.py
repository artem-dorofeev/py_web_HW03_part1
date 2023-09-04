CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
BAD_SYMBOLS = ("*", "!", "#", "$", "%", "+", "-", "=", "&", ",")
TRANS = {}
CYRILLIC = []

for i in CYRILLIC_SYMBOLS:
    CYRILLIC.append(i)

for c, l in zip(CYRILLIC, TRANSLATION):
    TRANS[ord(c)] = l
    # TRANS[ord(c.upper())] = l.upper()

for i in BAD_SYMBOLS:
    TRANS[ord(i)] = "_"


def normalize(name):
    global TRANS
    return name.lower().translate(TRANS)


if __name__ == "__main__":
    print(normalize("****Тестове ПоВідомлеННя -+=&%$#!****"))
