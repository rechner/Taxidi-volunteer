#from wxPython.wx import * 
import wx
import sha 

class LoginDialog(wx.Dialog): 
    def __init__(self, parent, id=-1, title="Login", 
                 pos=wx.DefaultPosition, 
                 size=wx.Size(250, 150)): 
        wx.Dialog.__init__(self, parent, id, title, pos, size) 
        wx.StaticText(self, -1, 'Please type your user name and password.', 
                     wxPoint(15, 5)) 
        wx.StaticText(self, -1, 'User name: ', wx.Point(20, 30)) 
        wx.StaticText(self, -1, 'Password: ', wx.Point(20, 55)) 
        self.nameBox = wx.TextCtrl(self, -1, '', wx.Point(80,30), 
                                  wx.Size(120, -1)) 
        self.passwordBox = wx.TextCtrl(self, -1, '', wx.Point(80,55), 
                                 wx.Size(120, -1), style=wx.TE_PASSWORD) 
        wx.Button(self, wx.ID_OK,     ' OK ', wx.Point(35, 90), 
                 wx.DefaultSize).SetDefault() 
        wx.Button(self, wxID_CANCEL, ' Cancel ', wx.Point(135, 90), 
                 wx.DefaultSize) 

    def GetUser(self): 
        val = self.ShowModal() 
        if val == wxID_OK: 
            username = self.nameBox.GetValue() 
            h = sha.new(self.passwordBox.GetValue()) 
            password = h.hexdigest() 
            return [username, password] 
        else: 
            return None 

class testLogin(wx.Frame): 
    def OnInit(self): 
        main = wx.Frame(None, -1, 'Main Frame') 
        main.Show(true) 
        self.SetTopWindow(main) 
        login = LoginDialog(main) 
        user = login.GetUser() 
        print user 
        return true 

app = wx.PySimpleApp()
window = testLogin()
app.MainLoop()

