import wx as wx
import os as os

class MainWindow(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.initialized = False

        #Menu Bar
        menu = wx.Menu()
        loadFile = wx.MenuItem(menu,-1,text="Load File",helpString="teste")
        menu.Append(loadFile)
        exit = wx.MenuItem(menu,-1,text="Exit",helpString="test")
        menu.Append(exit)
        menuBar = wx.MenuBar()
        menuBar.Append(menu,"File")
        parent.SetMenuBar(menuBar)
        parent.Bind(wx.EVT_MENU,self.loadFile,loadFile)
        parent.Bind(wx.EVT_MENU,self.exit,exit)
        parent.CreateStatusBar()

        #current clock
        self.clockLabel = wx.StaticText(self,label="Current Clock:",pos=(10,10))
        self.clock = wx.StaticText(self,label="",pos=(110,10))

        #Instructions' State table
        self.table1Title = wx.StaticText(self,label="Instructions' State",pos=(50,140))
        self.table1 = wx.ListCtrl(self,name="instructions'State",style=wx.LC_REPORT,pos=(50,160),size=(320,150))
        self.table1.AppendColumn("IF")
        self.table1.AppendColumn("EX start")
        self.table1.AppendColumn("EX end")
        self.table1.AppendColumn("WB")

        #Registers' State table
        self.table2Title = wx.StaticText(self,label="Registers' State",pos=(450,30))
        self.table2 = wx.ListCtrl(self,name="registers'State",style=wx.LC_REPORT,pos=(450,50),size=(300,70))
        self.table2.AppendColumn("Registers")
        self.table2.Append(["Qi"])

        #Functional Units table
        self.table3Title = wx.StaticText(self,label="Functional Units",pos=(50,330))
        self.table3 = wx.ListCtrl(self,name="functional Units",style=wx.LC_REPORT,pos=(50,350),size=(640,150))
        self.table3.AppendColumn("UF")
        self.table3.AppendColumn("Busy")
        self.table3.AppendColumn("Op")
        self.table3.AppendColumn("Qj")
        self.table3.AppendColumn("Qk")
        self.table3.AppendColumn("Vj")
        self.table3.AppendColumn("Vk")
        self.table3.AppendColumn("A")

        #Main Memory table
        self.table4Title = wx.StaticText(self,label="Main Memory",pos=(50,30))
        self.table4 = wx.ListCtrl(self,name="main Memory",style=wx.LC_REPORT,pos=(50,50),size=(300,70))
        self.table4.AppendColumn("Memory Address")
        self.table4.Append(["Content"])

        #next button
        nextButton = wx.Button(self,label="Next",pos=(50,530))
        parent.Bind(wx.EVT_BUTTON,self.update,nextButton)
    def loadFile(self,event):
        chooseFile = wx.FileDialog(self)
        if chooseFile.ShowModal() == wx.ID_OK:
            #self.simulator = TSsimulator(os.path.join(chooseFile.GetDirectory,chooseFile.GetFilename()))
            self.initialized = True
            self.startTables()
        chooseFile.Destroy()
    def exit(self,event):
        exit()
    def startTables(self):
        self.clock.SetLabel("0")
        #list = self.simulator.instructions()
        self.table1.DeleteAllItems()
        list = [[0,0,0,0]]
        for i in list:
            self.table1.Append(i)
        #list = self.simulator.register()
        self.table2.ClearAll()
        self.table2.AppendColumn("Registers")
        list =[""]
        for i in list:
            self.table2.AppendColumn(i)
        #list = self.simulator.registerStates()
        list = [0]
        list = ["Qi"]+list
        self.table2.Append(list)
        #list = self.simulator.units()
        self.table3.DeleteAllItems()
        list = [[0,0,0,0,0,0,0,0]]
        for i in list:
            self.table3.Append(i)
        #list = self.simulator.memory()
        self.table4.ClearAll()
        self.table4.AppendColumn("Memory Address")
        list = [""]
        for i in list:
            self.table4.AppendColumn(i)
        #list = self.simulator.memoryStates()
        list = ["Content"]+list
        self.table4.Append(list)
    def update(self,event):
        if(self.initialized):
            #self.simulator.nextStep()
            #self.clock.SetLabel(str(self.simulator.currentClock()))
            #list = self.simulator.instructions()
            list = [[0,1,2,3]]
            for i in range(len(list)):
                for j in range(4):
                    self.table1.SetItem(i,j,str(list[i][j]))
            #list = self.simulator.registerStates()
            list = [0]
            for i in range(len(list)):
                self.table2.SetItem(0,i+1,str(list[i]))
            #list = self.simulator.units()
            list = [[0,1,2,3,4,5,6,7]]
            for i in range(len(list)):
                for j in range(8):
                    self.table3.SetItem(i,j,str(list[i][j]))
            #list = self.simulator.memoryStates()
            list = [0]
            for i in range(len(list)):
                self.table4.SetItem(0,i+1,str(list[i]))

app = wx.App(True)
frame = wx.Frame(None,title="Tomasulo's algorithm simulator",size=(800,640))
panel = MainWindow(frame)
frame.Show()
app.MainLoop()
