import logging
import threading
import time
from simClasses import unitDef 
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
#    { CHP2001 NOTE: Replacing below with class system- should work somewhat nicer.
#        'Type': 'Engineer',
#        'Tier' : 1,
#        'BuildRate ' : 5,
#        'Health ' : 100
#    },
blueprints = {
    
    't1eng': unitDef(
    Name = 't1eng',
    Health = 100,
    Mass = 52,
    Energy = 260,
    BuildTime = 260,
    BuildPower = 5,
    MassIncome = 0,
    EnergyIncome = 0,
    MassStorage = 10,
    Type = 'Engineer',
    Tier = 1,
    BuildPowerCat = 'structT1',
    BuildCat = {'landT1'}
    ),

    't1pgen':unitDef(
    Name='t1pgen',
    Mass=75,
    Energy=750,
    BuildTime=125,
    EnergyIncome=20,
    Type = 'EnergyProduction',
    Tier = 1,
    BuildCat={'structT1','command'}
    ),

    't1mex':unitDef(
    Name='t1mex',
    Mass=36,
    Energy=360,
    BuildTime=60,
    MassIncome=2,
    EnergyIncome=-2,
    BuildPower=10,
    BuildPowerCat='t2mex',
    Type = 'Extractor',
    Tier = 1,
    BuildCat={'structT1','command'}
    ),

    't2mex':unitDef(
    Name='t2mex',
    Mass=900,
    Energy=5400,
    BuildTime=900,
    MassIncome=6,
    EnergyIncome=-9,
    BuildPower=15,
    BuildPowerCat='t3mex',
    Type = 'Extractor',
    Tier = 2,
    BuildCat={'structT2','t2mex'}
    ),

    't3mex':unitDef(
    Name='t3mex',
    Mass=4600,
    Energy=31625,
    BuildTime=2875,
    MassIncome=18,
    EnergyIncome=-18,
    Type = 'Extractor',
    Tier = 3,
    BuildCat={'structT3','t3mex'}
    ),

    't1fac':unitDef(
    Name='t1fac',
    Mass=240,
    Energy=2100,
    BuildTime=300,
    BuildPower=20,
    MassStorage=80,
    BuildPowerCat='landT1',
    Type = 'Factory',
    Tier = 1,
    BuildCat={'structT1','command'}
    ),

    't1hydro':unitDef(
    Name='t1hydro',
    Mass=160,
    Energy=800,
    BuildTime=400,
    EnergyIncome=100,
    Type = 'Hydro',
    Tier = 1,
    BuildCat={'structT1'}
    ),

    'command':unitDef(
    Name='command',
    MassIncome=1,
    EnergyIncome=20,
    BuildPower=10,
    MassStorage=650,
    EnergyStorage=4000,
    Type = 'ACU',
    Tier = 1,
    BuildPowerCat='command'
    ),

}

unitList = []

def create_consumption_unit(unit):
    global consumption
    unitList.append(unit)

def game_run(name):
    global game_finish
    logging.info("Starting Game")
    create_consumption_unit({
        'Type' : 'Factory',
        'Tier' : 1,
        'Dead' : False,
        'Active' : True
    })
    time.sleep(4)
    logging.info('We have built a factory')
    create_consumption_unit({
        'Type' : 'Extractor',
        'Tier' : 1,
        'Dead' : False,
        'Active' : True
    })
    time.sleep(2)
    logging.info('We have built a mass extractor')
    create_consumption_unit({
        'Type' : 'Extractor',
        'Tier' : 1,
        'Dead' : False,
        'Active' : True
    })
    time.sleep(2)
    logging.info('We have built a mass extractor')
    create_consumption_unit({
        'Type' : 'Hydro',
        'Tier' : 1,
        'Dead' : False,
        'Active' : True
    })
    time.sleep(4)
    logging.info('We have built a hydro')
    create_consumption_unit({
        'Type' : 'Extractor',
        'Tier' : 1,
        'Dead' : False,
        'Active' : True
    })
    time.sleep(2)
    logging.info('We have built a mass extractor')
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