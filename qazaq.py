import sys
import os
from parser_xml import parse_qazaq_code
from interpreter import QazaqInterpreter

def run_qs():
    # Проверка аргументов командной строки
    if len(sys.argv) < 2:
        print("\n🇰🇿 XKZML v1.0")
        print("====================================")
        print("Қолдану: python qazaq.py <бағдарлама.xkzml> [--строгий]")
        print("Мысалы:  python qazaq.py бағдарлама.xkzml --строгий\n")
        return

    file_path = sys.argv[1]
    strict_mode = "--строгий" in sys.argv or "--strict" in sys.argv

    # Проверка файла
    if not os.path.exists(file_path):
        print(f"\n❌ [XKZML]: '{file_path}' файлы табылмады!")
        return

    if not file_path.endswith('.qs'):
        print(f"⚠️ [Ескерту]: Файл кеңейтілімі '.xkzml' болуы тиіс!")

    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    try:
        # 1. Парсинг XML + Казахский фильтр (Строгий режим)
        ast_root = parse_qazaq_code(code, strict_mode=strict_mode)
        
        # 2. Выполнение кода
        if ast_root:
            interpreter = QazaqInterpreter()
            interpreter.execute(ast_root)
            
    except Exception as e:
        print(f"⛔ Бағдарлама тоқтатылды: {e}")

if __name__ == "__main__":
    run_qs()
