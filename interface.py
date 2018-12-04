import wx #wxPython lybrary
import os
import sys
import TomasuloSimulator as tss

class MainWindow(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.initialized = False

        #Menu Bar creation
        menu = wx.Menu()
        loadFile = wx.MenuItem(menu,-1,text="Load File",helpString="Load File")
        menu.Append(loadFile)
        exit = wx.MenuItem(menu,-1,text="Exit",helpString="Exit")
        menu.Append(exit)
        menuBar = wx.MenuBar()
        menuBar.Append(menu,"File")
        parent.SetMenuBar(menuBar)
        parent.Bind(wx.EVT_MENU,self.loadFile,loadFile)
        parent.Bind(wx.EVT_MENU,self.exit,exit)
        parent.CreateStatusBar()

        #Current Clock text creation
        self.clockLabel = wx.StaticText(self,label="Current Clock:",pos=(10,10))
        self.clock = wx.StaticText(self,label="",pos=(110,10))

        #Instructions' State table creation
        self.table1Title = wx.StaticText(self,label="Instructions' State",pos=(50,140))
        self.table1 = wx.ListCtrl(self,name="instructions'State",style=wx.LC_REPORT,pos=(50,160),size=(400,150))
        self.table1.AppendColumn("Instruction")
        self.table1.AppendColumn("IF")
        self.table1.AppendColumn("EX start")
        self.table1.AppendColumn("EX end")
        self.table1.AppendColumn("WB")

        #Registers' State table creation
        self.table2Title = wx.StaticText(self,label="Registers' State",pos=(450,30))
        self.table2 = wx.ListCtrl(self,name="registers'State",style=wx.LC_REPORT,pos=(450,50),size=(300,85))
        self.table2.AppendColumn("Registers")
        self.table2.Append(["Content"])
        self.table2.Append(["Qi"])

        #Functional Units table creation
        self.table3Title = wx.StaticText(self,label="Functional Units",pos=(50,330))
        self.table3 = wx.ListCtrl(self,name="functional Units",style=wx.LC_REPORT,pos=(50,350),size=(640,150))
        self.table3.AppendColumn("UF")
        self.table3.AppendColumn("Busy")
        self.table3.AppendColumn("Op")
        self.table3.AppendColumn("Vj")
        self.table3.AppendColumn("Vk")
        self.table3.AppendColumn("Qj")
        self.table3.AppendColumn("Qk")
        self.table3.AppendColumn("A")

        #Main Memory table creation
        self.table4Title = wx.StaticText(self,label="Main Memory",pos=(50,30))
        self.table4 = wx.ListCtrl(self,name="main Memory",style=wx.LC_REPORT,pos=(50,50),size=(300,70))
        self.table4.AppendColumn("Memory Address")
        self.table4.Append(["Content"])

        #next button creation
        nextButton = wx.Button(self,label="Next",pos=(50,530))
        parent.Bind(wx.EVT_BUTTON,self.update,nextButton)
        #previous button creation
        previousButton = wx.Button(self,label="Previous",pos=(150,530))
        parent.Bind(wx.EVT_BUTTON,self.outdate,previousButton)
    def loadFile(self,event):
        #load file dialog creation
        chooseFile = wx.FileDialog(self)
        if chooseFile.ShowModal() == wx.ID_OK:
            try:
                #if the file is in the right format, the simulation is initialized
                self.simulator = tss.TomasuloSimulator(os.path.join(chooseFile.GetDirectory(),chooseFile.GetFilename()))
                self.initialized = True
                #The tables are initialized with the starting State of the simulator
                self.startTables()
            except ValueError:
                #if the file is the worng format a error message is shown
                message = wx.MessageDialog(self,"Invalid Value")
                message.ShowModal()
            except Exception as e:
                message = wx.MessageDialog(self,str(e))
                message.ShowModal()
    def exit(self,event):
        #closing aplication function
        sys.exit()
    def startTables(self):
        #CurrentClock text initialization
        self.clock.SetLabel("0")
        #initialization of the tables
        #Instructions' State table initialization
        list = self.simulator.getInicialInstructions()
        self.table1.DeleteAllItems()
        for i in list:
            self.table1.Append(i)
        #Registers' State table initialization
        list = self.simulator.getInicialRegisters()
        self.table2.ClearAll()
        self.table2.AppendColumn("Registers")
        for i in list:
            self.table2.AppendColumn(i)
        list = self.simulator.getRegisters()
        self.table2.Append(["Content"]+list[0])
        self.table2.Append(["Qi"]+list[1])
        #Functional Units table initialization
        list = self.simulator.getInicialUnits()
        self.table3.DeleteAllItems()
        for i in list:
            self.table3.Append(i)
        #Main Memory table initialization
        list = self.simulator.getInicialMemory()
        self.table4.ClearAll()
        self.table4.AppendColumn("Memory Address")
        for i in list:
            self.table4.AppendColumn(str(i))
        list = self.simulator.getMemory()
        self.table4.Append(["Content"]+list)
    def outdate(self,event):
        if(self.initialized):
            try:
                #if possible to go back in the simulation the tables are updated
                self.simulator.simulateTo(self.simulator.getCurrentClock())
                self.clock.SetLabel(str(self.simulator.getCurrentClock()))
                self.updateTables()
            except Exception as e:
                #otherwise a message is displayed
                message = wx.MessageDialog(self,str(e))
                message.ShowModal()
    def update(self,event):
        if(self.initialized):
            try:
                #if possible to go forward in the simulation the tables are updated
                self.simulator.simulate()
                self.clock.SetLabel(str(self.simulator.getCurrentClock()))
                self.updateTables()
            except Exception as e:
                #otherwise a message is displayed
                message = wx.MessageDialog(self,str(e))
                message.ShowModal()
    def updateTables(self):
        #update of the tables
        #Instructions' State table update
        list = self.simulator.getInstructions()
        for i in range(len(list)):
            for j in range(4):
                self.table1.SetItem(i,j+1,str(list[i][j]))
        #Registers' State table update
        list = self.simulator.getRegisters()
        for i in range(len(list)):
            for j in range(len(list[i])):
                self.table2.SetItem(i,j+1,str(list[i][j]))
        #Functional Units table update
        list = self.simulator.getUnits()
        for i in range(len(list)):
            for j in range(7):
                self.table3.SetItem(i,j+1,str(list[i][j]))
        #Main Memory table update
        list = self.simulator.getMemory()
        for i in range(len(list)):
            self.table4.SetItem(0,i+1,str(list[i]))
if __name__ == "__main__":
    #aplication window creation
    app = wx.App(True)
    frame = wx.Frame(None,title="Tomasulo's algorithm simulator",size=(800,640))
    MainWindow(frame)
    frame.Show()
    app.MainLoop()
