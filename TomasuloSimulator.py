class TomasuloSimulator():
    def __init__(self,file):
        f = open(file,'r')
        lines = f.read().splitlines()
        NUnits = int(lines[0])
        lines = lines[1:len(lines)]
        self.Units = []
        self.UnitsState = []
        for i in range(NUnits):
            aux = []
            for j in lines[i].split(";"):
                k = j.split(",")
                if(len(k) == 1):
                    aux.append([k[0]])
                else:
                    aux.append([k[0],k[1]])
            self.Units.append(aux)
        lines = lines[NUnits:len(lines)]
        self.Instructions = []
        self.InstructionsState = []
        self.Memory = []
        self.Registers = []
        self.RegistersState = []
        for i in lines:
            aux=i.split(",")
            if(len(aux) != 4):
                raise Exception("Invalid Instruction")
            self.Instructions.append(aux)
        self.preProcessing()
    def preProcessing(self):
        for inst in self.Instructions:
            aux = inst[0].lower()
            if(aux == "add"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))+int(self.getRegisterContent(inst[3])))
            elif(aux == "add.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))+float(self.getRegisterContent(inst[3])))
            elif(aux == "addi"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))+int(inst[3]))
            elif(aux == "addi.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))+float(inst[3]))
            elif(aux == "sub"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))-int(self.getRegisterContent(inst[3])))
            elif(aux == "sub.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))-float(self.getRegisterContent(inst[3])))
            elif(aux == "subi"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))-int(inst[3]))
            elif(aux == "subi.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))-float(inst[3]))
            elif(aux == "mult"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))*int(self.getRegisterContent(inst[3])))
            elif(aux == "mult.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))*float(self.getRegisterContent(inst[3])))
            elif(aux == "multi"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))*int(inst[3]))
            elif(aux == "multi.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))*float(inst[3]))
            elif(aux == "div"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))//int(self.getRegisterContent(inst[3])))
            elif(aux == "div.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))/float(self.getRegisterContent(inst[3])))
            elif(aux == "divi"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))//int(inst[3]))
            elif(aux == "divi.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))/float(inst[3]))
            elif(aux == "lw"):
                self.setRegisterContent(inst[1],int(self.getMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])))))
            elif(aux == "ld.d"):
                self.setRegisterContent(inst[1],float(self.getMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])))))
            elif(aux == "sw"):
                self.setMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])),int(self.getRegisterContent(inst[1])))
            elif(aux == "sd.d"):
                self.setMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])),float(self.getRegisterContent(inst[1])))
            else:
                raise Exception("Invalid Instruction")
            flag = True
            for unit in self.Units:
                for i in range(1,len(unit)):
                    if(unit[i][0].lower() == aux):
                        flag = False
                        break
                if(not flag):
                    break
            if(flag):
                raise Exception("Functional Unit Missing")
        self.clean()
        self.Registers.sort()
        self.Memory.sort()
    def getRegisterContent(self,reg):
        for i in self.Registers:
            if(i[0] == reg.upper()):
                return i[1]
        type = reg[0].lower()
        if(type == "r"):
            aux = int(reg[1])*10
        elif(type == "d"):
            aux = float(int(reg[1]))*10.0
        else:
            raise Exception("Invalid Register")
        self.Registers.append([reg.upper(),aux])
        return aux
    def setRegisterContent(self,reg,content):
        for i in self.Registers:
            if(i[0] == reg.upper()):
                i[1] = content
                return
        type = reg[0].lower()
        if(type == "r"):
            self.Registers.append([reg.upper(),content])
        elif(type == "d"):
            self.Registers.append([reg.upper(),content*1.0])
        else:
            raise Exception("Invalid Register")
    def getRegisterState(self,reg):
        for regs in range(len(self.Registers)):
            if(self.Registers[regs][0] == reg.upper()):
                return self.RegistersState[regs]
    def setRegisterState(self,reg,state):
        for regs in range(len(self.Registers)):
            if(self.Registers[regs][0] == reg.upper()):
                self.RegistersState[regs] = state
                return
    def getMemoryContent(self,address):
        for i in self.Memory:
            if(i[0] == address):
                return i[1]
        self.Memory.append([address,address])
        return address
    def setMemoryContent(self,address,content):
        for i in self.Memory:
            if(i[0] == address):
                i[1] = content
                return
        self.Memory.append([address,content])
        return
    def getCurrentClock(self):
        return self.CurrentClock
    def getInicialInstructions(self):
        list = []
        for i in range(len(self.Instructions)):
            aux = [self.Instructions[i][0]+","+self.Instructions[i][1]+","+self.Instructions[i][2]+","+self.Instructions[i][3]]
            aux += self.InstructionsState[i]
            list.append(aux)
        return list
    def getInstructions(self):
        return self.InstructionsState
    def getInicialRegisters(self):
        list = []
        for i in self.Registers:
            list.append(i[0])
        return list
    def getRegisters(self):
        list = []
        for i in self.Registers:
            list.append(i[1])
        return list,self.RegistersState
    def getInicialUnits(self):
        list = []
        for i in range(len(self.Units)):
            list.append(self.Units[i][0]+self.UnitsState[i])
        return list
    def getUnits(self):
        return self.UnitsState
    def getLatency(self,unit,op):
        for ops in self.Units[unit]:
            if(op == ops[0].lower()):
                return int(ops[1])
    def getInicialMemory(self):
        list = []
        for i in self.Memory:
            list.append(i[0])
        return list
    def getMemory(self):
        list = []
        for i in self.Memory:
            list.append(i[1])
        return list
    def dispacth(self,unit,inst):
        self.InstructionsState[inst][0] = self.CurrentClock
        aux = self.Instructions[inst][0].lower()
        self.UnitsState[unit][0] = "Yes"
        self.UnitsState[unit][1] = aux
        if(aux == "lw" or aux == "ld.d"):
            state = self.getRegisterState(self.Instructions[inst][3])
            if(state == ""):
                self.UnitsState[unit][2] = self.getRegisterContent(self.Instructions[inst][3])
                self.UnitsState[unit][4] = "-"
            else:
                self.UnitsState[unit][2] = "-"
                self.UnitsState[unit][4] = state
            self.UnitsState[unit][3] = "-"
            self.UnitsState[unit][5] = "-"
            self.UnitsState[unit][6] = int(self.Instructions[inst][2])
            self.setRegisterState(self.Instructions[inst][1],self.Units[unit][0][0])
        elif(aux == "sw" or aux == "sd.d"):
            state = self.getRegisterState(self.Instructions[inst][1])
            if(state == ""):
                self.UnitsState[unit][2] = self.getRegisterContent(self.Instructions[inst][1])
                self.UnitsState[unit][4] = "-"
            else:
                self.UnitsState[unit][2] = "-"
                self.UnitsState[unit][4] = state
            state = self.getRegisterState(self.Instructions[inst][3])
            if(state == ""):
                self.UnitsState[unit][3] = self.getRegisterContent(self.Instructions[inst][3])
                self.UnitsState[unit][5] = "-"
            else:
                self.UnitsState[unit][3] = "-"
                self.UnitsState[unit][5] = state
            self.UnitsState[unit][6] = int(self.Instructions[inst][2])
        else:
            state = self.getRegisterState(self.Instructions[inst][2])
            if(state == ""):
                self.UnitsState[unit][2] = self.getRegisterContent(self.Instructions[inst][2])
                self.UnitsState[unit][4] = "-"
            else:
                self.UnitsState[unit][2] = "-"
                self.UnitsState[unit][4] = state
            if(aux == "add" or aux =="add.d" or aux == "sub" or aux == "sub.d" or aux == "mult" or aux == "mult.d" or aux == "div" or aux == "div.d"):
                state = self.getRegisterState(self.Instructions[inst][3])
                if(state == ""):
                    self.UnitsState[unit][3] = self.getRegisterContent(self.Instructions[inst][3])
                    self.UnitsState[unit][5] = "-"
                else:
                    self.UnitsState[unit][3] = "-"
                    self.UnitsState[unit][5] = state
            elif(aux == "addi" or aux == "subi" or aux == "multi" or aux == "divi"):
                self.UnitsState[unit][3] = int(self.Instructions[inst][3])
                self.UnitsState[unit][5] = "-"
            else:
                self.UnitsState[unit][3] = float(self.Instructions[inst][3])
                self.UnitsState[unit][5] = "-"
            self.setRegisterState(self.Instructions[inst][1],self.Units[unit][0][0])
    def writeBack(self,unit,value):
        self.UnitsState[unit][0] = "No"
        self.UnitsState[unit][1] = ""
        self.UnitsState[unit][2] = ""
        self.UnitsState[unit][3] = ""
        self.UnitsState[unit][4] = ""
        self.UnitsState[unit][5] = ""
        self.UnitsState[unit][6] = ""
        if(value == None):
            return
        for reg in range(len(self.RegistersState)):
            if(self.Units[unit][0][0] == self.RegistersState[reg]):
                self.RegistersState[reg] = ""
                self.Registers[reg][1] = value
        for uni in self.UnitsState:
            if(uni[4] == self.Units[unit][0][0]):
                uni[2] = value
                uni[4] = "-"
            if(uni[5] == self.Units[unit][0][0]):
                uni[3] = value
                uni[5] = "-"
    def simulate(self):
        if(self.ended == len(self.Instructions)):
            raise Exception("Already at end")
        flag = False
        writeBacksToBeDone = []
        finished = 0
        for inst in range(len(self.Instructions)):
            if(self.InstructionsState[inst][0] == ""):
                if(self.NextInstruction == inst):
                    for unit in range(len(self.Units)):
                        for i in range(1,len(self.Units[unit])):
                            if(self.Units[unit][i][0].lower() == self.Instructions[inst][0].lower() and self.UnitsState[unit][0] == "No"):
                                flag = True
                                self.Instructions[inst].append(unit)
                                break
                        if(flag):
                            self.dispacth(unit,inst)
                            break
            elif(self.InstructionsState[inst][1] == ""):
                aux = self.Instructions[inst][4]
                if(self.UnitsState[aux][4] == self.UnitsState[aux][5] == "-"):
                    self.InstructionsState[inst][1] = self.CurrentClock
                    i = self.Instructions[inst][0].lower()
                    if(i == "sw" or i=="sd.d"):
                        self.UnitsState[aux][6] += int(self.UnitsState[aux][3])
                    elif(i == "lw" or i =="ld.d"):
                        self.UnitsState[aux][6] += int(self.UnitsState[aux][2])
                    if(self.getLatency(aux,self.Units[aux][1][0]) == 1):
                        self.InstructionsState[inst][2] = self.CurrentClock
            elif(self.InstructionsState[inst][2] == ""):
                aux = self.Instructions[inst][4]
                if(self.InstructionsState[inst][1]-1+self.getLatency(aux,self.Units[aux][1][0]) == self.CurrentClock):
                    self.InstructionsState[inst][2] = self.CurrentClock
            elif(self.InstructionsState[inst][3] == ""):
                aux = self.Instructions[inst][4]
                writeBacksToBeDone.append([aux,self.execute(inst,self.UnitsState[aux][2],self.UnitsState[aux][3],self.UnitsState[aux][6])])
                #self.writeBack(aux,self.execute(inst,self.UnitsState[aux][2],self.UnitsState[aux][3],self.UnitsState[aux][6]))
                #unitsToRelease.append(aux)
                self.InstructionsState[inst][3] = self.CurrentClock
                self.ended += 1
        if(flag):
            self.NextInstruction += 1
        for i in writeBacksToBeDone:
            self.writeBack(i[0],i[1])
        self.CurrentClock += 1
    def simulateTo(self,target):
        if target <= 0:
            raise Exception("Already at start")
        self.clean()
        for i in range(target-1):
            self.simulate()
    def clean(self):
        self.ended = 0
        self.NextInstruction = 0
        self.CurrentClock = 0
        self.UnitsState.clear()
        self.InstructionsState.clear()
        self.RegistersState.clear()
        for i in self.Units:
            self.UnitsState.append(["No","","","","","",""])
        for i in self.Instructions:
            self.InstructionsState.append(["","","",""])
        for reg in self.Registers:
            if reg[0][0].lower() == "r":
                reg[1] = int(reg[0][1])*10
            else:
                reg[1] = float(int(reg[0][1]))*10.0
            self.RegistersState.append("")
        for mem in self.Memory:
            mem[1] = mem[0]
    def execute(self,inst,value1,value2,value3):
        aux = self.Instructions[inst][0].lower()
        if(aux == "add" or aux == "add.d" or aux == "addi" or aux == "addi.d"):
            return value1 + value2
        elif(aux == "sub" or aux == "sub.d" or aux == "subi" or aux == "subi.d"):
            return value1 - value2
        elif(aux == "mult" or aux == "mult.d" or aux == "multi" or aux == "multi.d"):
            return value1 * value2
        elif(aux == "div" or aux == "divi"):
            return value1//value2
        elif(aux == "div.d" or aux == "divi.d"):
            return value1/value2
        elif(aux == "lw" or aux == "ld.d"):
            return self.getMemoryContent(value3)
        elif(aux == "sw" or aux == "sd.d"):
            self.setMemoryContent(value3,value1)
