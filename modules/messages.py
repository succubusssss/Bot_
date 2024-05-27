from modules.parser_excel import parser_excel

example: str = f"Пример: физика 80, русский язык 90, математика 77"


def answer(string: str):
    match string:
        case "/start":
            return f'Введите данные в формате "предмет пробел оценка". Несколько предметов разделяйте запятой.\n\n{example}'
        case "/help":
            return (
                f"По вопросам жалоб и предложений просьба писать в аккаунт: @ArikMoroz"
            )
        case "/data_update":
            return parser_excel("./data/specialties.xlsx", "./data/spec.json")
        case _:
            return (
                "Вы проходите на следующие специальности:\n\n{}".format(
                    "\n\n ".join(string)
                )
                if type(string) == list
                else string
            )


def error(val: list):
    if type(val[1]) == int:

        def info():
            if val[0].isdigit():
                return f'Вы не ввели название предмета для балла "{val[0]}"'
            elif not len(val[0]):
                return f"Обнаружен пустой запрос"
            elif not val[0].isdigit():
                return f'Вы не ввели балл для предмета "{val[0]}"'
            else:
                return val

        return (
            f"Ошибка!\nНесоответствие шаблону. {info()} (позиция {val[1]})\n\n{example}"
        )

    elif "typo" in val[1]:
        return f'Ошибка!\nНе найдено в базе: "{val[0]}"\n\n{example}\nВведите данные повторно.'
    else:
        return f"Неизвестная ошибка\n\n{example}"
