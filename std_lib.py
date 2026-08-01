import math
import sys
import datetime

# Казахская стандартная библиотека
KAZAKH_STD_LIB = {
    # Шығару / Ввод-Вывод
    "жаз": print,
    "экранға": print,
    "сұра": input,
    
    # Математика (Математикалық функциялар)
    "тамыр": math.sqrt,
    "дәреже": math.pow,
    "дөңгелекте": round,
    "модуль": abs,
    
    # Жүйелік функциялар / Системное
    "уақыт": lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "тоқта": sys.exit,
    "ұзындығы": len,
    "тип": lambda v: type(v).__name__
}

def execute_builtin(func_name, *args):
    if func_name in KAZAKH_STD_LIB:
        return KAZAKH_STD_LIB[func_name](*args)
    raise NameError(f"Қате: '{func_name}' деген команда стандартты кітапханада табылмады!")