import enum
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
        #Tick Based Income
        self.TickMass = bp.TickMass
        self.TickEnergy = bp.TickEnergy
        self.TickBuild = bp.TickBuild
        #Storage
        self.MassStorage = bp.MassStorage
        self.EnergyStorage = bp.EnergyStorage

    def __getitem__(self, key):#Allowing item['key'] notation...
        return getattr(self, key)