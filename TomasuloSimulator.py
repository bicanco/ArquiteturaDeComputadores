class TomasuloSimulator():
    def __init__(self,file):
        print(file)
        f = open(file,'r')
        lines = f.read().splitlines()
        NUnits = int(lines[0])
        lines = lines[1:len(lines)]
        self.Units = []
        for i in range(NUnits):
            aux = []
            for j in lines[i].split(";"):
                k = j.split(",")
                if(len(k) == 1):
                    aux.append([k[0]])
                else:
                    aux.append([k[0],k[1]])
            self.Units.append(aux)
        NInst = int(lines[NUnits])
        lines = lines[NUnits+1:len(lines)]
        self.Instructions = []
        self.Memory = []
        self.Registers = []
        for i in lines:
            aux=i.split(",")
            self.Instructions.append(aux)
        self.preProcessing()
    def preProcessing(self):
#        self.Registers = [["R0",0],["R1",10],["R2",20],["R3",30],["R4",40],["R5",50],["R6",60],["R7",70],["R8",80],["R9",90],["D0",0.0],["D1",10.0],["D2",20.0],["D3",30.0],["D4",40.0],["D5",50.0],["D6",60.0],["D7",70.0],["D8",80.0],["D9",90.0]]
        for inst in self.Instructions:
            aux = inst[0].lower()
            if(aux == "add" or aux == "add.d"):
                self.setRegisterContent(inst[1],self.getRegisterContent(inst[2])+self.getRegisterContent(inst[3]))
            elif(aux == "sub" or aux == "sub.d"):
                self.setRegisterContent(inst[1],self.getRegisterContent(inst[2])-self.getRegisterContent(inst[3]))
            elif(aux == "mult" or aux == "mult.d"):
                self.setRegisterContent(inst[1],self.getRegisterContent(inst[2])*self.getRegisterContent(inst[3]))
            elif(aux == "div"):
                self.setRegisterContent(inst[1],self.getRegisterContent(inst[2])//self.getRegisterContent(inst[3]))
            elif(aux == "div.d"):
                self.setRegisterContent(inst[1],self.getRegisterContent(inst[2])/self.getRegisterContent(inst[3]))
            elif(aux == "lw" or aux == "l.d"):
                self.setRegisterContent(inst[1],self.getMemoryContent(int(inst[2])+self.getRegisterContent(inst[3])))
            elif(aux == "sw" or aux == "s.d"):
                self.setMemoryContent(int(inst[2])+self.getRegisterContent(inst[3]),self.getRegisterContent(inst[1]))
            elif(aux == "jump"):
                continue
            else:
                raise Exception('Invalid Instruction')
        for reg in self.Registers:
            if reg[0][0].lower() == "r":
                reg[1] = int(reg[0][1])*10
            else:
                reg[1] = float(reg[0][1])*10.0
        for mem in self.Memory:
            mem[1] = mem[0]
        self.Registers.sort()
        self.Memory.sort()
    def getRegisterContent(self,reg):
        for i in self.Registers:
            if(i[0].lower() == reg.lower()):
                return i[1]
        if(reg[0].lower() == "r"):
            aux = int(reg[1])*10
        else:
            aux = float(reg[1])*10.0
        self.Registers.append([reg.upper(),aux])
        return aux
    def setRegisterContent(self,reg,content):
        for i in self.Registers:
            if(i[0].lower() == reg.lower()):
                i[1] = content
                return
        if(reg[0].lower() == "r"):
            self.Registers.append([reg.upper(),content])
        else:
            self.Registers.append([reg.upper(),content*1.0])
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
