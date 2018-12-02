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
            self.UnitsState.append(["No","","","","","",""])
        NInst = int(lines[NUnits])
        lines = lines[NUnits+1:len(lines)]
        self.Instructions = []
        self.InstructionsState = []
        self.Memory = []
        self.Registers = []
        self.RegistersState = []
        self.CurrentClock = 0
        for i in lines:
            aux=i.split(",")
            if(len(aux) != 4):
                raise Exception("Invalid Instruction")
            self.Instructions.append(aux)
        self.preProcessing()
    def preProcessing(self):
#        self.Registers = [["R0",0],["R1",10],["R2",20],["R3",30],["R4",40],["R5",50],["R6",60],["R7",70],["R8",80],["R9",90],["D0",0.0],["D1",10.0],["D2",20.0],["D3",30.0],["D4",40.0],["D5",50.0],["D6",60.0],["D7",70.0],["D8",80.0],["D9",90.0]]
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
            elif(aux == "l.d"):
                self.setRegisterContent(inst[1],float(self.getMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])))))
            elif(aux == "sw"):
                self.setMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])),int(self.getRegisterContent(inst[1])))
            elif(aux == "s.d"):
                self.setMemoryContent(int(inst[2])+int(self.getRegisterContent(inst[3])),float(self.getRegisterContent(inst[1])))
            # elif(aux == "jump"):
            #     continue
            else:
                raise Exception("Invalid Instruction")
            self.InstructionsState.append(["","","",""])
        for reg in self.Registers:
            if reg[0][0].lower() == "r":
                reg[1] = int(reg[0][1])*10
            else:
                reg[1] = float(reg[0][1])*10.0
            self.RegistersState.append("")
        for mem in self.Memory:
            mem[1] = mem[0]
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
            # aux.append(self.InstructionsState[i][0])
            # aux.append(self.InstructionsState[i][1])
            # aux.append(self.InstructionsState[i][2])
            # aux.append(self.InstructionsState[i][3])
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
    # def nextStep(self):
    #     self.CurrentClock += 1
    #     self.RegistersState[0] = "oi"
    #     self.Registers[0][1] = 30
    #     self.UnitsState[0][0] = "Yes"
    #     self.Memory[0][1] = 100
    #     self.InstructionsState[0][0] = 10
