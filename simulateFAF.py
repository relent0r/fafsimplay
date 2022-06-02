from math import nan
from numbers import Number
import re
import threading, subprocess, os, random, time, json, copy, string
class Conditions:
    def greater_than(self,tablein):
        one=tablein[0]
        two=tablein[1]
        return one>two
    def greater_than_ratio(self,tablein):
        one=tablein[0]
        two=tablein[1]
        ratio=tablein[2]
        return one>two*ratio
    def greater_than_amount(self,tablein):
        one=tablein[0]
        two=tablein[1]
        amount=tablein[2]
        return one>two+amount
cond=Conditions()
cwd = os.getcwd()
logDir = cwd+"\\output\\"
resultPath = cwd+"\\results.txt"
with open('simulation.lua','w') as f:
    f.write('')
print(cwd)
JOB_INF=10000000
start = time.time()
toOutput=''
tick=0
uniqueindex=0
demandm=0
demande=0
#global efficiency
efficiency=1
lastefficiency=1
inprogress=[]#0unit,1massdone,2massmax,3bpallocated,4index,5buildername,6isBO
units=[]
inprogressunits=[]
resource=[0,0,0,0,0,0]#0m,1e,2mstore,3estore,4mmax,5emax
bocomplete=False
numInprogress=0
idleengnum=0
maxmexspots=45
unitdb={
    't1eng':[52,260,260,0,0,5,10,0],
    't1pgen':[75,750,125,0,20,0,0,0],
    't1mex':[36,360,60,2,-2,10,0,0],
    't2mex':[900,5400,900,6,-9,15,0,0],
    't3mex':[4600,31625,2875,18,-18,0,0,0],
    't1fac':[240,2100,300,0,0,20,80,0],
    't1hydro':[160,800,400,0,100,0,0,0],
    'command':[0,0,0,1,20,10,650,4000],#0mass, 1energy, 2buildtime,3MassIn,4EnergyIn,5BuildPower,6Massstorage,7Energystorage
}
for item in unitdb:#Go througha and divide incomes by 10
    unitdb[item][3]=unitdb[item][3]/10
    unitdb[item][4]=unitdb[item][4]/10
    unitdb[item][5]=unitdb[item][5]/10
buildpowerdefs={
    't1fac':['t1fac','land',20],#0buildertype,1buildcat,2bp
    't1eng':['t1eng','mobile',5],
    'command':['t1com','mobile',10],
    't1mex':['t1mex','t1mex',10],
    't2mex':['t2mex','t2mex',15],
}
for item in buildpowerdefs:
    buildpowerdefs[item][2]=buildpowerdefs[item][2]/10
bobuilders={
    't1facfirst':[1001,'t1com','mobile','t1fac',1,0,False],
    't1pgenmain':[999,'t1com','mobile','t1pgen',1,0,False],
}
builderlist={
    't1facmain':[999,'t1com','mobile','t1fac',5,0,[
        [cond.greater_than_ratio,'massin','massrequested',0.95],
        [cond.greater_than,1,'idlefactories'],
    ]
    ],
    't1mexmain':[1000,'t1com','mobile','t1mex',JOB_INF,0,[
        [cond.greater_than_ratio,'energyin','energyrequested',1.2],
        [cond.greater_than,'energystored',200],
        [cond.greater_than,'mexspots','mextotal'],
        ]
    ],#0priority,1type,2cat,3whattobuild,4instancelimit,5assigned,6conditions
    't1pgenmain':[999,'t1com','mobile','t1pgen',JOB_INF,0,[
        [cond.greater_than_amount,'energyrequested','energyin',-1000],
        [cond.greater_than_ratio,'energyrequested','energyin',1.5],
    ]
    ],
    't1engmain':[999,'t1fac','land','t1eng',JOB_INF,0,[
        [cond.greater_than_ratio,'massin','massrequested',0.95],
        [cond.greater_than,1,'idleengineers'],
    ]
    ],
    't2mexmain':[999,'t1mex','upgrade','t2mex',JOB_INF,0,[
        [cond.greater_than,1,'t1mexinprogress'],
        [cond.greater_than_ratio,'massin','t2mexinprogress',2],
        [cond.greater_than_amount,'energyin','energyrequested',6],
    ]
    ],
    't3mexmain':[999,'t2mex','upgrade','t3mex',JOB_INF,0,[
        [cond.greater_than,1,'t2mexinprogress'],
        [cond.greater_than_ratio,'massin','t3mexinprogress',3],
        [cond.greater_than_amount,'energyin','energyrequested',10],
    ]
    ],
}
buildpowerlist=[
    #{'command',False},#0unit,1allocated,2build,3requested
]
startlist=[
    'command',
]
def printStatus():
    print('Tick:'+str(tick)+'---------------------------------------------------------------------------')
    print('Income: '+str(round(resource[0]*10,1))+','+str(round(resource[1]*10,1)))
    print('Demand: '+str(round(demandm*10,1))+','+str(round(demande*10,1)))
    print('Storage: '+str(round(resource[2],1))+','+str(round(resource[3],1)))
    print('StorageMax: '+str(round(resource[4],1))+','+str(round(resource[5],1)))
    print('Idle Engineers: '+str(idleengnum))
    print('Idle Factories: '+str(checkIdleNum('t1fac')))
    for unit in unitdb:
        print(unit+' count:'+str(units.count(unit))+'+('+str(inprogressunits.count(unit))+')')
    #print('InProgress:')
    #print(str(inprogressunits))
    #for build in inprogress:
    #    print(str(build))
def checkIdleNum(type):
    idlecount=0
    for unit in buildpowerlist:
        if not unit[1] and unit[0]==type:
            idlecount+=1
    return idlecount
def onCreate(unit,start):
    global efficiency
    global units
    global buildpowerlist
    global buildpowerdefs
    global unitdb
    global resource
    global demandm
    global demande
    units.append(unit)
    if unit in buildpowerdefs:
        buildpowerlist.append([unit,False,None,0])
    resource[0]+=unitdb[unit][3]
    resource[1]+=unitdb[unit][4]
    resource[4]+=unitdb[unit][6]
    resource[5]+=unitdb[unit][7]
    if start=='start':
        resource[2]+=unitdb[unit][6]
        resource[3]+=unitdb[unit][7]
    else:
        inprogressunits.remove(unit)
def onUpgrade(buildpower):
    unit=buildpower[0]
    units.remove(unit)
    buildpowerlist.remove(buildpower)
    resource[0]-=unitdb[unit][3]
    resource[1]-=unitdb[unit][4]
    resource[4]-=unitdb[unit][6]
    resource[5]-=unitdb[unit][7]
def updateResourceIn():
    global resource
    global units
    global unitdb
    global lastefficiency
    for unit in units:
        if unitdb[unit][3]>0 and unit!='command':
            resource[2]+=unitdb[unit][3]*lastefficiency
        else:
            resource[2]+=unitdb[unit][3]
        if unitdb[unit][4]>0:
            resource[3]+=unitdb[unit][4]
def updateDemand():
    global demandm
    global demande
    demandm=0
    demande=0
    for unit in units:
        if unitdb[unit][3]<0:
            demandm-=unitdb[unit][3]
        if unitdb[unit][4]<0:
            demande-=unitdb[unit][4]
    for eng in buildpowerlist:
        build=eng[2]
        if eng[1]:
            request=unitdb[eng[0]][5]/unitdb[build[0]][2]*unitdb[build[0]][0]
            eng[3]=request
            demandm+=request
            demande+=request*unitdb[build[0]][1]/unitdb[build[0]][0]
            #print('request for '+str(eng[0])+' is '+str(request*unitdb[build[0]][1]/unitdb[build[0]][0]))
def updateResourceOut():
    for unit in units:
        if unitdb[unit][3]<0:
            resource[2]-=min(-unitdb[unit][3]*efficiency,resource[2])
        if unitdb[unit][4]<0:
            resource[3]-=min(-unitdb[unit][4]*efficiency,resource[3])
    for eng in buildpowerlist:
        build=eng[2]
        if eng[1]:
            requestm=build[3]/unitdb[build[0]][2]*build[2]
            requeste=requestm*unitdb[build[0]][1]/unitdb[build[0]][0]
            actualm=min(build[2]-build[1],requestm*efficiency)
            actuale=requeste/requestm*actualm
            resource[2]-=min(actualm,resource[2])
            resource[3]-=min(actuale,resource[3])
            build[1]+=min(actualm,resource[2])
def enforceResourceRules():
    if resource[2]>=resource[4]:
        resource[2]=resource[4]
    if resource[3]>=resource[5]:
        resource[3]=resource[5]
def stringToVariable(string):
    global demande
    if string=='energyin':
        return resource[1]
    elif string=='energystored':
        return resource[3]
    elif string=='energyrequested':
        return demande
    elif string=='massin':
        return resource[0]
    elif string=='massrequested':
        return demandm
    elif string=='idleengineers':
        return idleengnum
    elif string=='mexnum':
        return units.count('t1mex')
    elif string=='mexspots':
        return maxmexspots
    elif string=='idlefactories':
        return checkIdleNum('t1fac')
    elif string=='mextotal':
        return units.count('t1mex')+inprogressunits.count('t1mex')+units.count('t2mex')+units.count('t3mex')
    elif string=='t1mexinprogress':
        return inprogressunits.count('t1mex')
    elif string=='t2mexinprogress':
        return inprogressunits.count('t2mex')
    elif string=='t3mexinprogress':
        return inprogressunits.count('t3')
def parseCondition(condition):
    inputs=[]
    for var in condition:
        if isinstance(var,str):
            inputs.append(stringToVariable(var))
        elif isinstance(var,Number):
            inputs.append(var)
    return condition[0](inputs)
def evaluateBuilderCondition(builder):
    global demande
    if not builder[6]:
        return True
    else:
        for condition in builder[6]:
            if not parseCondition(condition):
                #print('condition '+str(condition)+' failed')
                return False
        return True
def viableBuilderCheck(builder,eng):
    if buildpowerdefs[eng[0]][0]==builder[1]:
        return evaluateBuilderCondition(builder)
    if builder[1]=='t1com':
        if buildpowerdefs[eng[0]][0]=='t1eng':
            return evaluateBuilderCondition(builder)
    #print('builder '+str(builder)+' is not '+str(eng))
def allocateBuilders():
    global bocomplete
    global uniqueindex
    global buildpowerlist
    global bobuilders
    global inprogress
    global numInprogress
    if not bocomplete:
        for eng in buildpowerlist:
            if not eng[1]:
                buildselected=False
                #print('grabbing builders at tick '+str(tick))
                #print('builders are '+str(bobuilders))
                for builder in bobuilders:
                    #print('evaluating builder '+str(builder))
                    if bobuilders[builder][5]<bobuilders[builder][4]:
                        if viableBuilderCheck(bobuilders[builder],eng):
                            bobuilders[builder][5]+=1
                            buildselected=True
                            #print('build selected at '+str(tick))
                            eng[1]=True
                            inprogress.append([bobuilders[builder][3],0,unitdb[bobuilders[builder][3]][0],buildpowerdefs[eng[0]][2],uniqueindex,bobuilders[builder],True,builder])
                            inprogressunits.append(bobuilders[builder][3])
                            uniqueindex+=1
                            eng[2]=inprogress[numInprogress]
                            numInprogress+=1
                            break
    else:
        for eng in buildpowerlist:
            if not eng[1]:
                buildselected=False
                #print('grabbing builders at tick '+str(tick))
                #print('builders are '+str(builderlist))
                for builder in builderlist:
                    #print('evaluating builder '+str(builder))
                    if builderlist[builder][5]<builderlist[builder][4]:
                        if viableBuilderCheck(builderlist[builder],eng):
                            if builder=='t2mexmain':
                                print('doing t2mex at tick '+str(tick))
                            if builder=='t3mexmain':
                                print('doing t3mex at tick '+str(tick))
                            builderlist[builder][5]+=1
                            buildselected=True
                            #print('build selected at '+str(tick))
                            eng[1]=True
                            inprogress.append([builderlist[builder][3],0,unitdb[builderlist[builder][3]][0],buildpowerdefs[eng[0]][2],uniqueindex,builderlist[builder],False,builder])
                            inprogressunits.append(builderlist[builder][3])
                            uniqueindex+=1
                            eng[2]=inprogress[numInprogress]
                            numInprogress+=1
                            break
def engDeAllocation(build):
    for eng in buildpowerlist:
        if eng[2]==build:
            #print(eng[2][5][2])
            if eng[2][5][2]=='upgrade':
                print('reached onUpgrade')
                onUpgrade(eng)
            eng[2]=None
            eng[1]=False
            eng[3]=0
def doCompletion():
    global numInprogress
    global bocomplete
    for build in inprogress:
        if build[1]>=build[2]:
            engDeAllocation(build)
            onCreate(build[0],False)
            #print('attempting remove of build '+str(build[4]))
            if build[6]:
                #bobuilders[build[5]]=None
                bobuilders.pop(build[7])
                if len(bobuilders)<1:
                    bocomplete=True
            else:
                builderlist[build[7]][5]-=1
            inprogress.remove(build)
            numInprogress-=1
            #printStatus()
def do_tick():
    global demandm
    global demande
    updateResourceIn()
    global bocomplete
    global efficiency
    global buildpowerlist
    global bobuilders
    global inprogress
    global lastefficiency
    global idleengnum
    allocateBuilders()
    idleengnum=checkIdleNum('t1eng')
    #print('updating demand')
    updateDemand()
    effm=0
    effe=0
    if demandm>0:
        effm=min(resource[2]/demandm,1)
        effe=min(resource[3]/demande,1)
        efficiency=min(effm,effe)
    else:
        efficiency=min(resource[2],1)
        effm=1
        effe=1
    updateResourceOut()
    enforceResourceRules()
    doCompletion()
    # with open('simulation.lua','a') as f:
    #     f.write(data)
    lastefficiency=effe
    global tick
    tick+=1
for unit in startlist:
    onCreate(unit,'start')
try:
    while tick<10*60*45:
        do_tick()
except Exception as e:
    print("Exception: {}".format(e))


for item in resource:
    resource[resource.index(item)]=round(item,1)
print("Time taken: {}s".format(round(time.time()-start)))
print('Seconds simulated: '+str(tick/10))
printStatus()
print('Idle eng: '+str(idleengnum))
print('final builders were '+str(bobuilders)+str(builderlist))