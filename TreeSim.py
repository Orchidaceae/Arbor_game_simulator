import xlsxwriter
import random

#Seed phase constants
SEED_WATERBUFFER_MAX = 20
SEED_SUNBUFFER_MAX = 40
SEED_HEALTHBUFFER_MAX = 1 #must be larger than zero
SEED_WATER_NEED = 24
SEED_SUN_NEED = 48
SEED_SUN_INTAKE = 2
SEED_WATER_INTAKE = 2

#Sprout phase constants
SPROUT_WATERBUFFER_MAX = 114
SPROUT_SUNBUFFER_MAX = 182
SPROUT_HEALTHBUFFER_MAX = 3
SPROUT_WATER_NEED = 120
SPROUT_SUN_NEED = 192
SPROUT_SUN_INTAKE = 2
SPROUT_WATER_INTAKE = 2

#Sapling phase constants
SAPLING_WATERBUFFER_MAX = 472
SAPLING_SUNBUFFER_MAX = 708
SAPLING_HEALTHBUFFER_MAX = 10
SAPLING_WATER_NEED = 480
SAPLING_SUN_NEED = 720
SAPLING_SUN_INTAKE = 2
SAPLING_WATER_INTAKE = 2

#Grown tree phase constants
GROWN_TREE_WATERBUFFER_MAX = 950
GROWN_TREE_SUNBUFFER_MAX = 1186
GROWN_TREE_HEALTHBUFFER_MAX = 23
GROWN_TREE_WATER_NEED = 960
GROWN_TREE_SUN_NEED = 1200
GROWN_TREE_SUN_INTAKE = 2
GROWN_TREE_WATER_INTAKE = 2

#keep track of day
DAY = 0

#total distance
TOTAL_DIST = 0

##class Phase(Enum):
##    SEED = 1
##    SPROUT = 2
##    SAPLING = 3
##    GROWN_TREE = 4

##class Weather(Enum):
##                SUN = 1
##                CLOUDY = 2
##                RAIN = 3

## Create spreadsheet
workbook = xlsxwriter.Workbook('TreeSim.xlsx')
worksheet = workbook.add_worksheet()
labels = ["day", "distance", "total distance", "weather", "phase", "WB-level", "SB-level", "HB-level"]

#keep track of which colon to write to
COL = 1

def createRowLables(row):
    for item in labels:
        worksheet.write(row, 0, item)
        row += 1

def generateRandomWeather():
                weather = random.randint(1,3)
                if  weather == 1:
                                return "SUN"
                elif weather == 2:
                                return "CLOUDY"
                elif weather == 3:
                                return "RAIN"

def generateRandomKm():
                return random.randint(0, 7)

class Tree(object):
    """docstring for ."""
    class Buffer(object):
        """docstring for ."""
        
        def __init__(self, bufferMax):
            self.max = bufferMax
            self.value = bufferMax

        def setMax(self, newMax):
            self.max = newMax

        def setValue(self, newValue):
            self.value = newValue

        def getValue(self):
            return self.value

        def incrValue(self, incrBy):
            if self.value + incrBy < self.max:
                self.value += incrBy
            else:
                self.value = self.max

        def decrValue(self, decrBy):
            if self.value - decrBy > 0:
                self.value -= decrBy
            else:
                self.value = 0
                
    def __init__(self):
        self.treePhase = "SEED"
        self.waterBuffer = self.Buffer(SEED_WATERBUFFER_MAX)
        self.sunBuffer = self.Buffer(SEED_SUNBUFFER_MAX)
        self.healthBuffer = self.Buffer(SEED_HEALTHBUFFER_MAX)

    def getWaterLevel(self):
        return self.waterBuffer.value

    def getSunLevel(self):
        return self.sunBuffer.value

    def getHealth(self):
        return self.healthBuffer.value

    def getPhase(self):
        return self.treePhase

    def changeWaterBuffer(self, increase, amount):
        if increase:
            self.waterBuffer.incrValue(amount)
        else:
            self.waterBuffer.decrValue(amount)

    def changeSunBuffer(self, increase, amount):
        if increase:
            self.sunBuffer.incrValue(amount)
        else:
            self.sunBuffer.decrValue(amount)

    def changeHealthBuffer(self, increase, amount):
        if increase:
            self.healthBuffer.incrValue(amount)
        else:
            self.healthBuffer.decrValue(amount)

    def changePhase(self):
        if self.treePhase == "SEED":
            self.treePhase = "SPROUT";
            self.waterBuffer.setMax(SPROUT_WATERBUFFER_MAX)
            self.waterBuffer.setValue(SPROUT_WATERBUFFER_MAX)
            self.sunBuffer.setMax(SPROUT_SUNBUFFER_MAX)
            self.sunBuffer.setValue(SPROUT_SUNBUFFER_MAX)
            self.healthBuffer.setMax(SPROUT_HEALTHBUFFER_MAX)
            self.healthBuffer.setValue(SPROUT_HEALTHBUFFER_MAX)
        elif self.treePhase == "SPROUT":
            self.treePhase = "SAPLING"
            self.waterBuffer.setMax(SAPLING_WATERBUFFER_MAX)
            self.waterBuffer.setValue(SAPLING_WATERBUFFER_MAX)
            self.sunBuffer.setMax(SAPLING_SUNBUFFER_MAX)
            self.sunBuffer.setValue(SAPLING_SUNBUFFER_MAX)
            self.healthBuffer.setMax(SAPLING_HEALTHBUFFER_MAX)
            self.healthBuffer.setValue(SAPLING_HEALTHBUFFER_MAX)
        elif self.treePhase == "SAPLING":
            self.treePhase = "GROWN_TREE"
            self.waterBuffer.setMax(GROWN_TREE_WATERBUFFER_MAX)
            self.waterBuffer.setValue(GROWN_TREE_WATERBUFFER_MAX)
            self.sunBuffer.setMax(GROWN_TREE_SUNBUFFER_MAX)
            self.sunBuffer.setValue(GROWN_TREE_SUNBUFFER_MAX)
            self.healthBuffer.setMax(GROWN_TREE_HEALTHBUFFER_MAX)
            self.healthBuffer.setValue(GROWN_TREE_HEALTHBUFFER_MAX)

def intake(tree, dist, weather):
    phase = tree.treePhase
    if weather == "SUN":
        if phase == "SEED":
            x = SEED_SUN_INTAKE
        elif phase == "SAPLING":
            x = SAPLING_SUN_INTAKE
        elif phase == "SPROUT":
            x = SPROUT_SUN_INTAKE
        elif phase == "GROWN_TREE":
            x = GROWN_TREE_SUN_INTAKE
        amount = x * dist
        tree.changeSunBuffer(1, amount)
    elif weather == "RAIN":
        if phase == "SEED":
            x = SEED_WATER_INTAKE
        elif phase == "SAPLING":
            x = SAPLING_WATER_INTAKE
        elif phase == "SPROUT":
            x = SPROUT_WATER_INTAKE
        elif phase == "GROWN_TREE":
            x = GROWN_TREE_WATER_INTAKE
        amount = x * dist
        tree.changeWaterBuffer(1, amount)        

def needs(tree):
    phase = tree.treePhase
    if phase == "SEED":
        tree.changeWaterBuffer(0, SEED_WATER_NEED)
        tree.changeSunBuffer(0, SEED_SUN_NEED)
    elif phase == "SAPLING":
        tree.changeWaterBuffer(0, SAPLING_WATER_NEED)
        tree.changeSunBuffer(0, SAPLING_SUN_NEED)
    elif phase == "SPROUT":
        tree.changeWaterBuffer(0, SPROUT_WATER_NEED)
        tree.changeSunBuffer(0, SPROUT_SUN_NEED)
    elif phase == "GROWN_TREE":
        tree.changeWaterBuffer(0, GROWN_TREE_WATER_NEED)
        tree.changeSunBuffer(0, GROWN_TREE_SUN_NEED)   
    
def checkPhase(tree):
    phase = tree.treePhase
    global TOTAL_DIST

    if TOTAL_DIST >= 7 and TOTAL_DIST < 20 and phase != "SPROUT":
        tree.changePhase()
    elif TOTAL_DIST >= 20 and TOTAL_DIST < 50 and phase != "SAPLING":
        tree.changePhase()
    elif TOTAL_DIST >= 50 and phase != "GROWN_TREE":
        tree.changePhase()
            
def init(tree):
    global COL
    global TOTAL_DIST

    createRowLables(0)

    #day zero (start stats)
    row = 0
    data = [DAY, "-", TOTAL_DIST, "-", tree.getPhase(), tree.getWaterLevel(), tree.getSunLevel(), tree.getHealth()]
    colonWrite(data, COL)
    COL += 1
    

def colonWrite(data, colon):
    row = 0
    for item in data:
        worksheet.write(row, colon, item)
        row += 1
    print("writes to spreadsheet")

def simStart(tree):
    global DAY
    global TOTAL_DIST
    global COL

    print("banan")
    DAY += 1
    data = [DAY]

    walked = generateRandomKm()
    print("walked %d" % walked)
    TOTAL_DIST += walked
    data = data + [walked, TOTAL_DIST]

    weather = generateRandomWeather()
    data = data + [weather]

    #check phase
    checkPhase(tree)
    data = data + [tree.treePhase]

    #Needs
    needs(tree)

    #intake
    intake(tree, walked, weather)

    #if any buffer's level is at zero, the tree's health will take damage by 1hp
    if tree.waterBuffer.getValue() == 0:
        tree.changeHealthBuffer(0, 1)
        
    if tree.sunBuffer.getValue() == 0:
        tree.changeHealthBuffer(0, 1)

    data = data + [tree.waterBuffer.getValue(), tree.sunBuffer.getValue(), tree.healthBuffer.getValue()]

    print(data)
    
    colonWrite(data, COL)
    COL += 1

    if tree.healthBuffer.getValue() == 0:
        return  ## tree is dead, end simulation

    simStart(tree) ## continue loop simulation


    
    

def main():
    global COL
    global DAY
    for x in range (0, 10):
        tree = Tree()
        
        init(tree)
        print("initialized")
        simStart(tree)
        print("simulation finnished")
        COL += 1
        DAY = 0
        TOTAL_DIST = 0
        
    workbook.close()
    
main()

print("hello world")
