from json import dump, load

FILENAME = "res/city.json"

try:
    with open(FILENAME, "r") as file:
        data = load(file)
    cities = data["cities"]
    areas = data["areas"]
except:
    cities = dict()
    areas = dict()


def create_city(name, owner):
    cities[name] = [owner, 0, 0, 0.5, 0]
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


def get_dominance(name):
    if name not in cities:
        return
    return cities.get(name)[3]


def get_management(name):
    if name not in cities:
        return
    return cities.get(name)[4]


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


def set_dominance(name, dominance):
    if name not in cities:
        return
    cities[name][3] = min(max(dominance, 0), 1)
    save()


def set_management(name, management):
    if name not in cities:
        return
    cities[name][4] = management
    save()


def is_city(name):
    return name in cities


def set_account_area(account, area):
    area[account] = area
    save()


def get_account_area(account):
    return area.get(account, 0)


def get_city_names():
    return cities.keys()


def save():
    with open(FILENAME, "w") as file:
        dump({
            "cities": cities,
            "areas": areas,
        }, file)
