import enum
import time
from simData import unitList

#Easy method for remembering to sleep in ticks vs seconds
global timePerSecond
timePerSecond=10
def dt(t):
    return t/timePerSecond
def tickSleep(ticks):
    time.sleep(dt(ticks/10))

class unitDef:
    def __init__(self, 
    Name='',#Key name = default value
    Type='None',
    #Defense
    Health=0,
    #Cost 
    Mass=0, 
    Energy=0, 
    BuildTime=0,
    #Income
    MassIncome=0, 
    EnergyIncome=0, 
    BuildPower=0, 
    #Storage
    MassStorage=0, 
    EnergyStorage=0, 
    #Categories
    BuildPowerCat='None', 
    BuildCat={'None'},
    Tier=1,
    ):
        #Name
        self.Name=Name
        self.Type=Type
        #Defense
        self.Health=Health
        #Cost
        self.Mass=Mass
        self.Energy=Energy
        self.BuildTime=BuildTime
        #Income
        self.MassIncome=MassIncome
        self.EnergyIncome=EnergyIncome
        self.BuildPower=BuildPower
        #Tick Based Income
        self.TickMass=MassIncome/10
        self.TickEnergy=EnergyIncome/10
        self.TickBuild=BuildPower/10
        #Storage
        self.MassStorage=MassStorage
        self.EnergyStorage=EnergyStorage
        #Category
        self.BuildPowerCat=BuildPowerCat
        self.BuildCat=BuildCat
        self.Tier=Tier

    def __getitem__(self, key): #Allows using item['Key'] notation as you were already doing
        return getattr(self, key)

    def __repr__(self): #Returns the string that occurs when you try to print the object
        return self.Name + ", " + self.Type + ", " + str(self.Tier)

class Unit:
    def __init__(self, bp):
        self.Name = bp.Name
        self.Blueprint = bp
        #Status
        self.Dead=False
        #Defense
        self.MaxHealth = bp.Health
        self.Health = bp.Health
        #Economy
        self.MassIncome = bp.MassIncome
        self.EnergyIncome = bp.EnergyIncome
        self.BuildPower = bp.BuildPower
        #CurrentConsumption
        self.CurrentMassConsumption = 0
        self.CurrentEnergyConsumption = 0
        #Tick Based Income
        self.TickMass = bp.TickMass
        self.TickEnergy = bp.TickEnergy
        self.TickBuild = bp.TickBuild
        #Storage
        self.MassStorage = bp.MassStorage
        self.EnergyStorage = bp.EnergyStorage
        #State
        self.Active = False
        self.Dead = False

    def __getitem__(self, key):#Allowing item['key'] notation...
        return getattr(self, key)

    def Build(self, unit):

        #unitToBuild = unit #No need for creating a unitdef here! just use the unit reference

        massConsumption = unit.Mass / unit.BuildTime * self.TickBuild #If we are doing tenth-second ticks like FAF, we need to use TickBuild for accuracy
        energyConsumption = unit.Energy / unit.BuildTime * self.TickBuild
        print('massConsumption per tick ', massConsumption)

        self.CurrentMassConsumption = massConsumption
        self.CurrentEnergyConsumption = energyConsumption

        timeForBuild = unit.BuildTime / self.TickBuild

        print('time to sleep (ticks)', (timeForBuild))
        tickSleep(timeForBuild)
        
        #Now we create the unit!
        unitToBuild = Unit(unit)

        self.create_consumption_unit(unitToBuild)

        self.CurrentMassConsumption = 0
        self.CurrentEnergyConsumption = 0
        print('we have built a ', unitToBuild.Name)

        return unitToBuild

    def create_consumption_unit(self, unit):
        global consumption
        global unitList
        unit.Active = True
        unitList.append(unit)


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