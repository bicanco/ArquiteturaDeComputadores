#class for simulating Tomasulo's Algorithm
class TomasuloSimulator():
    def __init__(self,file):
        #reding the file
        f = open(file,'r')
        lines = f.read().splitlines()
        #reading the number of functional units
        NUnits = int(lines[0])
        lines = lines[1:len(lines)]
        #reading the functional units
        self.Units = []
        self.UnitsState = []
        for i in range(NUnits):
            aux = []
            unit = lines[i].split(";")
            if unit[1] == "":
                raise Exception("Functional Unit without operations")
            aux.append(unit[0])
            for j in range(1,len(unit)):
                k = unit[j].split(",")
                #checking for wrong format input
                if(len(k) == 2):
                    if(k[1] == ""):
                        raise Exception("Missing Latency")
                    op = k[0].lower()
                    #checking for valid operations
                    if(op != "add" and op != "add.d" and op != "addi" and op != "addi.d" and op != "sub" and op != "sub.d" and op != "subi" and op != "subi.d" and op != "mult" and op != "mult.d" and op != "multi" and op != "multi.d" and op != "div" and op != "divi" and op != "div.d" and op != "divi.d" and op != "lw" and op != "ld.d" and op != "sw" and op != "sd.d"):
                        raise Exception("Invalid Operation")
                    aux.append([k[0],int(k[1])])
                    if(int(k[1]) <= 0):
                        raise Exception("Invalid Latency")
                else:
                    raise Exception("Invalid Functional Unit Format")
            self.Units.append(aux)
        #reading the instructions
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
        #pre-processing to find which registers and memory adresses are being used
        self.preProcessing()
        #closing file
        f.close()
    def preProcessing(self):
        #for each instruction the operation is executed to find which registers and memory adresses are being used
        #the instructions format is also checked
        for inst in self.Instructions:
            aux = inst[0].lower()
            if(aux == "add"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))+int(self.getRegisterContent(inst[3])))
                if(inst[1][0].upper() == "D" or inst[2][0].upper() == "D" or inst[3][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "add.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))+float(self.getRegisterContent(inst[3])))
                if(inst[1][0].upper() == "R" or inst[2][0].upper() == "R" or inst[3][0].upper() == "R"):
                    raise Exception("Wrong format instruction")
            elif(aux == "addi"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))+int(inst[3]))
                if(inst[1][0].upper() == "D" or inst[2][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "addi.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))+float(inst[3]))
                if(inst[1][0].upper() == "R" or inst[2][0].upper() == "R"):
                    raise Exception("Wrong format instruction")
            elif(aux == "sub"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))-int(self.getRegisterContent(inst[3])))
                if(inst[1][0].upper() == "D" or inst[2][0].upper() == "D" or inst[3][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "sub.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))-float(self.getRegisterContent(inst[3])))
                if(inst[1][0].upper() == "R" or inst[2][0].upper() == "R" or inst[3][0].upper() == "R"):
                    raise Exception("Wrong format instruction")
            elif(aux == "subi"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))-int(inst[3]))
                if(inst[1][0].upper() == "D" or inst[2][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "subi.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))-float(inst[3]))
                if(inst[1][0].upper() == "R" or inst[2][0].upper() == "R"):
                    raise Exception("Wrong format instruction")
            elif(aux == "mult"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))*int(self.getRegisterContent(inst[3])))
                if(inst[1][0].upper() == "D" or inst[2][0].upper() == "D" or inst[3][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "mult.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))*float(self.getRegisterContent(inst[3])))
                if(inst[1][0].upper() == "R" or inst[2][0].upper() == "R" or inst[3][0].upper() == "R"):
                    raise Exception("Wrong format instruction")
            elif(aux == "multi"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))*int(inst[3]))
                if(inst[1][0].upper() == "D" or inst[2][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "multi.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))*float(inst[3]))
                if(inst[1][0].upper() == "R" or inst[2][0].upper() == "R"):
                    raise Exception("Wrong format instruction")
            elif(aux == "div"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))//int(self.getRegisterContent(inst[3])))
                if(inst[1][0].upper() == "D" or inst[2][0].upper() == "D" or inst[3][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "div.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))/float(self.getRegisterContent(inst[3])))
                if(inst[1][0].upper() == "R" or inst[2][0].upper() == "R" or inst[3][0].upper() == "R"):
                    raise Exception("Wrong format instruction")
            elif(aux == "divi"):
                self.setRegisterContent(inst[1],int(self.getRegisterContent(inst[2]))//int(inst[3]))
                if(inst[1][0].upper() == "D" or inst[2][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "divi.d"):
                self.setRegisterContent(inst[1],float(self.getRegisterContent(inst[2]))/float(inst[3]))
                if(inst[1][0].upper() == "R" or inst[2][0].upper() == "R"):
                    raise Exception("Wrong format instruction")
            elif(aux == "lw"):
                self.setRegisterContent(inst[1],int(self.getMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])))))
                if(inst[1][0].upper() == "D" or inst[3][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "ld.d"):
                self.setRegisterContent(inst[1],float(self.getMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])))))
                if(inst[1][0].upper() == "R" or inst[3][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "sw"):
                self.setMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])),int(self.getRegisterContent(inst[1])))
                if(inst[1][0].upper() == "D" or inst[3][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            elif(aux == "sd.d"):
                self.setMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])),float(self.getRegisterContent(inst[1])))
                if(inst[1][0].upper() == "R" or inst[3][0].upper() == "D"):
                    raise Exception("Wrong format instruction")
            else:
                #checking for valid instructions
                raise Exception("Invalid Instruction")
            flag = True
            #checking for instruction without coresponding functional unit
            for unit in self.Units:
                for i in range(1,len(unit)):
                    if(unit[i][0].lower() == aux):
                        flag = False
                        break
                if(not flag):
                    break
            if(flag):
                raise Exception("Functional Unit Missing")
        #initializing lists
        self.clean()
        self.Registers.sort()
        self.Memory.sort()
    def getRegisterContent(self,reg):
        #getting resgister content
        for i in self.Registers:
            if(i[0] == reg.upper()):
                return i[1]
        #if not previously used the register is initialized
        type = reg[0].lower()
        if(type == "r"):
            aux = int(reg[1:len(reg)])*10
        elif(type == "d"):
            aux = float(int(reg[1:len(reg)]))*10.0
        else:
            raise Exception("Invalid Register")
        self.Registers.append([reg.upper(),aux])
        return aux
    def setRegisterContent(self,reg,content):
        #setting resgister content
        for i in self.Registers:
            if(i[0] == reg.upper()):
                i[1] = content
                return
        #if not previously used the register is initialized
        type = reg[0].lower()
        if(type == "r"):
            self.Registers.append([reg.upper(),content])
        elif(type == "d"):
            self.Registers.append([reg.upper(),content*1.0])
        else:
            raise Exception("Invalid Register")
    def getRegisterState(self,reg):
        #getting resgister state
        for regs in range(len(self.Registers)):
            if(self.Registers[regs][0] == reg.upper()):
                return self.RegistersState[regs]
    def setRegisterState(self,reg,state):
        #setting resgister state
        for regs in range(len(self.Registers)):
            if(self.Registers[regs][0] == reg.upper()):
                self.RegistersState[regs] = state
                return
    def getMemoryContent(self,address):
        #getting memory content
        for i in self.Memory:
            if(i[0] == address):
                return i[1]
        #if not previously used the adress is initialized
        self.Memory.append([address,address])
        return address
    def setMemoryContent(self,address,content):
        #setting memory content
        for i in self.Memory:
            if(i[0] == address):
                i[1] = content
                return
        #if not previously used the adress is initialized
        self.Memory.append([address,content])
        return
    def getCurrentClock(self):
        #getting current clock
        return self.CurrentClock
    def getInicialInstructions(self):
        #getting initial instruction table
        list = []
        for i in range(len(self.Instructions)):
            aux = [self.Instructions[i][0]+","+self.Instructions[i][1]+","+self.Instructions[i][2]+","+self.Instructions[i][3]]
            aux += self.InstructionsState[i]
            list.append(aux)
        return list
    def getInstructions(self):
        #getting instructions' state
        return self.InstructionsState
    def getInicialRegisters(self):
        #getting initial registers table
        list = []
        for i in self.Registers:
            list.append(i[0])
        return list
    def getRegisters(self):
        #getting registers' state
        list = []
        for i in self.Registers:
            list.append(i[1])
        return list,self.RegistersState
    def getInicialUnits(self):
        #getting initial units table
        list = []
        for i in range(len(self.Units)):
            list.append([self.Units[i][0]]+self.UnitsState[i])
        return list
    def getUnits(self):
        #getting Units' state
        return self.UnitsState
    def getLatency(self,unit,op):
        #getting latency of operation in specific unit
        for ops in self.Units[unit]:
            if(op == ops[0].lower()):
                return ops[1]
    def getInicialMemory(self):
        #getting initial memory table
        list = []
        for i in self.Memory:
            list.append(i[0])
        return list
    def getMemory(self):
        #getting memory contents
        list = []
        for i in self.Memory:
            list.append(i[1])
        return list
    def dispacth(self,unit,inst):
        #dispacthing instuction to designated unit
        self.InstructionsState[inst][0] = self.CurrentClock
        aux = self.Instructions[inst][0].lower()
        self.UnitsState[unit][0] = "Yes"
        self.UnitsState[unit][1] = aux
        #handling load instructions
        if(aux == "lw" or aux == "ld.d"):
            #setting Vj,Qj fields
            state = self.getRegisterState(self.Instructions[inst][3])
            if(state == ""):
                self.UnitsState[unit][2] = self.getRegisterContent(self.Instructions[inst][3])
                self.UnitsState[unit][4] = "-"
            else:
                self.UnitsState[unit][2] = "-"
                self.UnitsState[unit][4] = state
            self.UnitsState[unit][3] = "-"
            self.UnitsState[unit][5] = "-"
            #setting adress and register state
            self.UnitsState[unit][6] = int(self.Instructions[inst][2])
            self.setRegisterState(self.Instructions[inst][1],self.Units[unit][0])
        #handling store instructions
        elif(aux == "sw" or aux == "sd.d"):
            #setting Vj,Vk,Qj,Qk fields
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
            #setting adress
            self.UnitsState[unit][6] = int(self.Instructions[inst][2])
        #handling the remaining instructions
        else:
            #setting Vj,Vk,Qj,Qk fields
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
            #setting register state
            self.setRegisterState(self.Instructions[inst][1],self.Units[unit][0])
    def writeBack(self,unit,value):
        #freeing unit
        self.UnitsState[unit][0] = "No"
        self.UnitsState[unit][1] = ""
        self.UnitsState[unit][2] = ""
        self.UnitsState[unit][3] = ""
        self.UnitsState[unit][4] = ""
        self.UnitsState[unit][5] = ""
        self.UnitsState[unit][6] = ""
        if(value == None):
            return
        #updating units and registers values when needed
        for reg in range(len(self.RegistersState)):
            if(self.Units[unit][0] == self.RegistersState[reg]):
                self.RegistersState[reg] = ""
                self.Registers[reg][1] = value
        for uni in self.UnitsState:
            if(uni[4] == self.Units[unit][0]):
                uni[2] = value
                uni[4] = "-"
            if(uni[5] == self.Units[unit][0]):
                uni[3] = value
                uni[5] = "-"
    def simulate(self):
        #simulation of Tomasulo's Algorithm until all the instructions have been executed
        if(self.ended == len(self.Instructions)):
            raise Exception("Already at end")
        flag = False
        writeBacksToBeDone = []
        finished = 0
        for inst in range(len(self.Instructions)):
            #dispacthing instructions
            if(self.InstructionsState[inst][0] == ""):
                if(self.NextInstruction == inst):
                    for unit in range(len(self.Units)):
                        #checking available functional units
                        for i in range(1,len(self.Units[unit])):
                            if(self.Units[unit][i][0].lower() == self.Instructions[inst][0].lower() and self.UnitsState[unit][0] == "No"):
                                flag = True
                                self.Instructions[inst].append(unit)
                                break
                        if(flag):
                            self.dispacth(unit,inst)
                            break
            #starting instructions execution
            elif(self.InstructionsState[inst][1] == ""):
                aux = self.Instructions[inst][4]
                if(self.UnitsState[aux][4] == self.UnitsState[aux][5] == "-"):
                    self.InstructionsState[inst][1] = self.CurrentClock
                    i = self.Instructions[inst][0].lower()
                    #calculating adress
                    if(i == "sw" or i=="sd.d"):
                        self.UnitsState[aux][6] += int(self.UnitsState[aux][3])
                    elif(i == "lw" or i =="ld.d"):
                        self.UnitsState[aux][6] += int(self.UnitsState[aux][2])
                    #checking if instruction starts and ends in the same clock cicle
                    if(self.getLatency(aux,self.Units[aux][1][0]) == 1):
                        self.InstructionsState[inst][2] = self.CurrentClock
            #ending instructions execution
            elif(self.InstructionsState[inst][2] == ""):
                aux = self.Instructions[inst][4]
                #checking if instruction has ended
                if(self.InstructionsState[inst][1]-1+self.getLatency(aux,self.Units[aux][1][0]) == self.CurrentClock):
                    self.InstructionsState[inst][2] = self.CurrentClock
            #wrinting results of operations where they are needed
            elif(self.InstructionsState[inst][3] == ""):
                #marking unit to be freed in the end of the clock cicle and updating number of finished instructions
                aux = self.Instructions[inst][4]
                writeBacksToBeDone.append([aux,self.execute(inst,self.UnitsState[aux][2],self.UnitsState[aux][3],self.UnitsState[aux][6])])
                self.InstructionsState[inst][3] = self.CurrentClock
                self.ended += 1
        if(flag):
            #updating next instruction to dispatch
            self.NextInstruction += 1
        for i in writeBacksToBeDone:
            #executing writeBacks marked to be done
            self.writeBack(i[0],i[1])
        #updating clock cicle
        self.CurrentClock += 1
    def simulateTo(self,target):
        #simulation from begining to previous step from target
        if target <= 0:
            raise Exception("Already at start")
        #cleaning simulation tables
        self.clean()
        for i in range(target-1):
            self.simulate()
    def clean(self):
        #setting initial values of all lists used in simulation for the file used to initialize simulation
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
                reg[1] = int(reg[0][1:len(reg[0])])*10
            else:
                reg[1] = float(int(reg[0][1:len(reg[0])]))*10.0
            self.RegistersState.append("")
        for mem in self.Memory:
            mem[1] = mem[0]
    def execute(self,inst,value1,value2,value3):
        #execution of operation
        aux = self.Instructions[inst][0].lower()
        if(aux == "add" or aux == "addi"):
            return int(value1 + value2)
        elif(aux == "add.d" or aux == "addi.d"):
            return float(value1 + value2)
        elif(aux == "sub" or aux == "subi"):
            return int(value1 - value2)
        elif(aux == "sub.d" or aux == "subi.d"):
            return float(value1 - value2)
        elif(aux == "mult" or aux == "multi"):
            return int(value1 * value2)
        elif(aux == "mult.d" or aux == "multi.d"):
            return float(value1 * value2)
        elif(aux == "div" or aux == "divi"):
            return int(value1//value2)
        elif(aux == "div.d" or aux == "divi.d"):
            return float(value1/value2)
        elif(aux == "lw"):
            return int(self.getMemoryContent(int(value3)))
        elif(aux == "ld.d"):
            return float(self.getMemoryContent(int(value3)))
        elif(aux == "sw"):
            self.setMemoryContent(int(value3),int(value1))
        elif(aux == "sd.d"):
            self.setMemoryContent(int(value3),float(value1))
