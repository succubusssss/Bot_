from json import load, dumps
from pandas import read_excel


with open("./data/spec.json", "r", encoding="utf-8") as file:
    json_data = load(file)
data = read_excel("./data/specialties.xlsx")
