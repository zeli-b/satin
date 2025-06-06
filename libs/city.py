from json import dump, load

FILENAME = "res/city.json"

try:
    with open(FILENAME, "r") as file:
        cities = load(file)
except:
    cities = dict()


def create_city(name, owner):
    cities[name] = [owner, 0, 0]
    save()


def get_owner_account(name):
    if name not in cities:
        return
    return cities.get(name)[0]


def get_area(name):
    if name not in cities:
        return
    return cities.get(name)[1]


def get_population(name):
    if name not in cities:
        return
    return cities.get(name)[2]


def set_area(name, area):
    if name not in cities:
        return
    cities[name][1] = area
    save()


def set_population(name, population):
    if name not in cities:
        return
    cities[name][2] = population
    save()


def is_city(name):
    return name in cities


def save():
    with open(FILENAME, "w") as file:
        dump(cities, file)
