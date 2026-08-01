from std_lib import KAZAKH_STD_LIB, execute_builtin

class Environment:
    """Контекст переменных и функций (Scope)"""
    def __init__(self, parent=None):
        self.vars = {}
        self.funcs = {}
        self.parent = parent

    def get_var(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get_var(name)
        return None

    def set_var(self, name, val):
        self.vars[name] = val

class QazaqInterpreter:
    def __init__(self):
        self.global_env = Environment()

    def eval_expr(self, expr, env):
        """Вычисление строк, чисел и переменных"""
        if not expr:
            return None
        expr = expr.strip()
        
        # Переменная
        if expr.startswith("$"):
            var_name = expr[1:]
            val = env.get_var(var_name)
            return val if val is not None else f"[Айнымалы ${var_name} табылмады]"
            
        # Числа
        if expr.isdigit():
            return int(expr)
        try:
            return float(expr)
        except ValueError:
            pass
            
        # Строка
        return expr

    def execute(self, node, env=None):
        if env is None:
            env = self.global_env

        tag = node.tag

        # 1. Главный контейнер скрипта
        if tag in ["қазақскрипт", "qazaqscript", "бағдарлама"]:
            for child in node.children:
                self.execute(child, env)
            return

        # 2. Создание переменной <айнымалы атау="x">10</айнымалы>
        elif tag in ["айнымалы", "сан", "мәтін"]:
            var_name = node.attribs.get("атау") or node.attribs.get("name")
            raw_val = node.text or node.attribs.get("мәні")
            val = self.eval_expr(raw_val, env)
            if var_name:
                env.set_var(var_name, val)

        # 3. Условие <егер шарт="$x > 5"> ... </егер>
        elif tag in ["егер", "if"]:
            condition = node.attribs.get("шарт", "")
            # Простейший парсинг условий
            parts = condition.split()
            if len(parts) == 3:
                left = self.eval_expr(parts[0], env)
                op = parts[1]
                right = self.eval_expr(parts[2], env)
                
                res = False
                if op == ">": res = float(left) > float(right)
                elif op == "<": res = float(left) < float(right)
                elif op == "==": res = str(left) == str(right)
                
                if res:
                    for child in node.children:
                        self.execute(child, env)

        # 4. Цикл <қайтала саны="5"> ... </қайтала>
        elif tag in ["қайтала", "цикл"]:
            count = int(self.eval_expr(node.attribs.get("саны", "1"), env))
            for _ in range(count):
                for child in node.children:
                    self.execute(child, env)

        # 5. Печать / Вывод на экран
        elif tag in ["жаз", "экранға", "басып_шығар"]:
            msg = self.eval_expr(node.text or node.attribs.get("мәні"), env)
            print(msg)

        # 6. Вызов стандартных функций библиотеки
        elif tag in KAZAKH_STD_LIB:
            arg = self.eval_expr(node.text or node.attribs.get("мәні"), env)
            res = execute_builtin(tag, arg) if arg is not None else execute_builtin(tag)
            if res is not None:
                print(res)

        # 7. Пользовательские динамические теги (Бесконечность XML!)
        else:
            print(f"┌─ [Тег/Модуль: <{tag}>]")
            if node.text:
                print(f"│  Мәтін: {node.text}")
            for child in node.children:
                self.execute(child, env)
            print(f"└─ [Конец <{tag}>]")