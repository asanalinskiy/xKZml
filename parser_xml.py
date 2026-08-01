import xml.etree.ElementTree as ET
from lang_filter import validate_kazakh_tag, validate_kazakh_attribs

class QazaqNode:
    def __init__(self, tag, attribs, text, children):
        self.tag = tag.strip()
        self.attribs = attribs
        self.text = text.strip() if text else ""
        self.children = children

def parse_qazaq_code(code_str, strict_mode=True):
    try:
        root = ET.fromstring(code_str)
        return _build_node(root, strict_mode)
    except ET.ParseError as e:
        print(f"\n❌ [ҚазақСкрипт Парсер Қатесі]: XML форматында қате бар: {e}")
        return None

def _build_node(element, strict_mode=True):
    # 1. Проверка названия тега
    is_valid_tag, error_tag = validate_kazakh_tag(element.tag)
    if not is_valid_tag:
        print(f"\n❌ [ҚАРА ТІЗІМ / БАН]: Тег '<{element.tag}>' бұғатталды!")
        print(f"👉 Себебі: {error_tag}\n")
        raise ValueError(f"Қатаң режим қатесі: {error_tag}")

    # 2. 🛑 STRICT MODE: Проверка названий атрибутов
    is_valid_attr, error_attr = validate_kazakh_attribs(element.attrib, strict_mode)
    if not is_valid_attr:
        print(f"\n❌ [ҚАТАҢ РЕЖИМ (STRICT MODE)]: '<{element.tag}>' тегінің атрибуты қабылданбады!")
        print(f"👉 Себебі: {error_attr}\n")
        raise ValueError(f"Атрибут қатесі: {error_attr}")

    children = [_build_node(child, strict_mode) for child in element]
    return QazaqNode(
        tag=element.tag,
        attribs=element.attrib,
        text=element.text,
        children=children
    )