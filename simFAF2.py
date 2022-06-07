import logging
import threading
import time
from simClasses import unitDef, Unit, blueprints
from simData import unitList


consumption = {
    "mass" : 0,
    "energy" : 0
}
generation = {
    "mass" : 0,
    "energy" : 0
}
current = {
    "mass" : 0,
    "energy" : 0
}
total = {
    "mass" : 0,
    "energy" : 0
}
game_finish = False

def create_consumption_unit(unit):
    global consumption
    unitList.append(unit)

def game_run(name):
    global game_finish
    logging.info("Starting Game")
    create_consumption_unit({
        'Type' : 'ACU',
        'Tier' : 1,
        'Dead' : False,
        'Active' : True
    })
    acuBP = unitDef(blueprints['command'])
    acuUnit = Unit(acuBP.Name)
    logging.info('We have an ACU')
    acuUnit.Build(blueprints['t1fac'])
    acuUnit.Build(blueprints['t1mex'])
    acuUnit.Build(blueprints['t1mex'])
    acuUnit.Build(blueprints['t1mex'])
    acuUnit.Build(blueprints['t1hydro'])
    acuUnit.Build(blueprints['t1mex'])

    time.sleep(10)
    logging.info('Mass Income at end of game %s', current["mass"])
    logging.info('Energy Income at end of game %s', current["energy"])
    logging.info('Mass Total %s', total["mass"])
    logging.info('Energy Total %s', total["energy"])
    game_finish = True
    logging.info("Finishing Game")


def economy_thread(name):
    global game_finish
    global generation
    global consumption
    global current
    global total

    while game_finish == False:
        current['mass'] = 0
        current['mass'] = 0
        generation['mass'] = 0
        consumption['mass'] = 0
        generation['energy'] = 0
        consumption['energy'] = 0

        for v in unitList:
            if v['Active']:
                unitResource = next((x for x in blueprints.values() if v["Type"] == x["Type"] and v["Tier"] == x["Tier"]), None)
                if unitResource:
                    if hasattr(unitResource, 'MassIncome'):
                        generation["mass"] += unitResource.MassIncome
                    if hasattr(unitResource, 'EnergyIncome'):
                        generation["energy"] += unitResource.EnergyIncome
        current["mass"] = generation['mass'] - consumption['mass']
        current["energy"] = generation['energy'] - consumption['energy']
        total["mass"] += current["mass"]
        total["energy"] += current["energy"]

        time.sleep(1)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : Creating Game threads")
    x = threading.Thread(target=economy_thread, args=(1,))
    y = threading.Thread(target=game_run, args=(1,))
    x.start()
    y.start()
    logging.info("Main    : Game threads created")