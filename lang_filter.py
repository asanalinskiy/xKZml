import re

# Казахские аффиксы множественного числа и падежей
KAZAKH_SUFFIXES = [
    "лар", "лер", "дар", "дер", "тар", "тер",
    "ның", "нің", "дың", "дің", "тың", "тің",
    "ға", "ге", "қа", "ке",
    "дан", "ден", "тан", "тен", "нан", "нен",
    "мен", "бен", "пен"
]

HARD_VOWELS = set("аоұы")
SOFT_VOWELS = set("әөүіе")

# Белый список разрешенных системных атрибутов
ALLOWED_KAZAKH_ATTRIBS = {
    "атау", "мәні", "шарт", "саны", "орта", "деңгей",
    "тип", "түр", "жол", "уақыт", "қайталау", "параметр"
}

def split_camel_case(text):
    return re.findall(r'[А-ЯӘҒҢӨҰҮҺІа-яәғңөұүһі]+|[a-zA-Z]+', re.sub(r'([a-zа-яәғңөұүһі])([A-ZА-ЯӘҒҢӨҰҮҺІ])', r'\1 \2', text))

def strip_kazakh_suffixes(word):
    word_lower = word.lower()
    for suffix in KAZAKH_SUFFIXES:
        if word_lower.endswith(suffix):
            return word_lower[:-len(suffix)]
    return word_lower

def check_vowel_harmony(root):
    has_hard = any(c in HARD_VOWELS for c in root)
    has_soft = any(c in SOFT_VOWELS for c in root)
    if has_hard and has_soft:
        return False
    return True

def is_kazakh_word(word):
    word_lower = word.lower()

    # 1. Запрет латиницы и сторонних символов
    if not re.match(r'^[а-яәғңөұүһіЁё]+$', word_lower):
        return False, "Тек қазақша кириллицаға рұқсат! (Латиница/араб/эмодзи тыйым салынған)"

    # 2. Отсечение аффиксов и проверка гармонии гласных
    root = strip_kazakh_suffixes(word_lower)
    if not check_vowel_harmony(root):
        return False, f"Үндестік заңы бұзылды: '{root}' қазақ сөзі емес!"

    # 3. Черный список иностранных корней
    banned_roots = ["датабас", "датабейз", "сервер", "принт", "код", "функция", "файл", "скрипт", "нейм", "кондишн"]
    if any(banned in root for banned in banned_roots):
        return False, f"Шетелдік түбір бұғатталды: '{root}'"

    return True, "ОК"

def validate_kazakh_tag(tag_name):
    """Проверка имени тега"""
    words = split_camel_case(tag_name)
    for word in words:
        is_valid, reason = is_kazakh_word(word)
        if not is_valid:
            return False, f"Тег '{tag_name}' ішіндегі '{word}' сөзі қабылданбады: {reason}"
    return True, "ОК"

def validate_kazakh_attribs(attribs, strict_mode=True):
    """🛑 STRICT MODE: Проверка всех атрибутов тега"""
    if not strict_mode:
        return True, "ОК"

    for attr_name, attr_value in attribs.items():
        # 1. Проверяем само название атрибута (например: "атау", "шарт")
        words = split_camel_case(attr_name)
        for word in words:
            is_valid, reason = is_kazakh_word(word)
            if not is_valid:
                return False, f"Атрибут атауы '{attr_name}' бұғатталды: {reason}"

        # 2. Имя атрибута должно быть в казахском контексте или белом списке
        if attr_name.lower() not in ALLOWED_KAZAKH_ATTRIBS:
            # Если это кастомный атрибут, он все равно должен пройти проверку на казахское слово
            is_valid, reason = validate_kazakh_tag(attr_name)
            if not is_valid:
                return False, f"Бейтаныс/орысша атрибут '{attr_name}': {reason}"

    return True, "ОК"