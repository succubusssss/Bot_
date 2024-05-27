from modules.parser_input import parser
import modules.messages as msg


def get_subj_list(json_data):
    """Получает список всех предметов из файла JSON
    @json_data - данные, полученные из файла JSON
    """
    list_subj: list = []
    for index, key in enumerate(json_data):
        list_subj.extend(json_data[str(index)]["subject"])
        list_subj.extend(json_data[str(index)]["choice"])
    return list_subj


def data_comp(user_data: dict | str, json_data: dict):
    """Сравнивает данные полученные от пользователя с данными из базы, и отдаёт подходящие специальности
    @user_data - данные, полученные от пользователя
    @json_data - данные загруженные из фала *.json
    """
    # список подходящих специальностей
    suit_spec: list = []
    u_data = user_data

    #получаем список всех предметов из файла JSON для поиска опечаток
    _list: list = get_subj_list(json_data)
    # обрабатываем строку пользователя
    if type(parser(u_data, _list)) == str:
        return parser(user_data, _list)
    else:
        parsed_str: dict = parser(u_data, _list)

    # список предметов, полученный от пользователя
    key_list: list = []

    for key in parsed_str:
        key_list.append(key)

    for index, key in enumerate(json_data):
        subject_list = json_data[str(index)]["subject"]
        choice_subj_list = json_data[str(index)]["choice"]
        score = json_data[str(index)]["score"]
        speciality = json_data[str(index)]["specialty"]

        # совпадение с обязательными предметами
        match_subj = list(set(key_list) & set(subject_list))
        # совпадение с предметами на выбор
        match_choice = list(set(key_list) & set(choice_subj_list))

        # совпавшие предметы
        if len(match_subj) == 2:
            final_list = [*match_subj, *match_choice]
        else:
            final_list = []
        # суммарный балл совпавших предметов
        sum_list = []

        if len(final_list) > 2:
            for val in final_list:
                sum_list.append(parsed_str[val])
            if sum(sum_list) >= score:
                suit_spec.append(speciality)
                print(index, final_list, sum(sum_list), score)

    if not len(suit_spec):
        return "Нет подходящих специальностей"
    # elif typo[0] == 1:
    #     return typo[1]
    else:
        return suit_spec
