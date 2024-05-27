from re import match, sub
import modules.messages as msg


def parser(string: str, subj_list: list = [], ind: int = 0):
    """Преобразование строки в словарь:\n
    \"string, string, ..." -> {string: int, string: int, ...}
    """

    def typo_search(user_word, subj_list):
        if not user_word in subj_list:
            return 1
        return 0

    # Подчищаем строку от лишних пробелов и переводим в нижний регистр
    def pars_func(string: str):
        _match = string.groups()
        if _match[0]:
            return r","
        elif _match[1]:
            return r" "

    parsed_str: str = (
        sub(r"(\s*,\s*)|(\s+)", pars_func, string).strip().lower().split(",")
    )
    err: list = []

    ####
    def list_for_dict(string: str):
        nonlocal ind
        ind += 1
        # проверка на соответсвие шаблону "предмет балл"
        _search: str = match(r"^(?:\w+\s*)+\s\d+$", string)
        if _search:
            # Если проверка пройдена, создаём список ['предмет', балл]
            _list: list = sub(r"\s(?=(\d+$))", r"_", string).split("_")
            typo = typo_search(_list[0], subj_list)
            if not typo:
                return [_list[0], int(_list[1])]
            else:
                return err.extend([_list[0], "typo"])
        else:
            return err.extend([string, ind])

    try:
        return dict(map(list_for_dict, parsed_str))
    except:
        return msg.error(err)
