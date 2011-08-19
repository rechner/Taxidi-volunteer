from wxPython.wx import * 
import sha 

class LoginDialog(wxDialog): 
    def __init__(self, parent, id=-1, title="Login", 
                 pos=wxDefaultPosition, 
                 size=wxSize(250, 150)): 
        wxDialog.__init__(self, parent, id, title, pos, size) 
        wxStaticText(self, -1, 'Please type your user name and password.', 
                     wxPoint(15, 5)) 
        wxStaticText(self, -1, 'User name: ', wxPoint(20, 30)) 
        wxStaticText(self, -1, 'Password: ', wxPoint(20, 55)) 
        self.nameBox = wxTextCtrl(self, -1, '', wxPoint(80,30), 
                                  wxSize(120, -1)) 
        self.passwordBox = wxTextCtrl(self, -1, '', wxPoint(80,55), 
                                 wxSize(120, -1), style=wxTE_PASSWORD) 
        wxButton(self, wxID_OK,     ' OK ', wxPoint(35, 90), 
                 wxDefaultSize).SetDefault() 
        wxButton(self, wxID_CANCEL, ' Cancel ', wxPoint(135, 90), 
                 wxDefaultSize) 

    def GetUser(self): 
        val = self.ShowModal() 
        if val == wxID_OK: 
            username = self.nameBox.GetValue() 
            h = sha.new(self.passwordBox.GetValue()) 
            password = h.hexdigest() 
            return [username, password] 
        else: 
            return None 

class testLogin(wxApp): 
    def OnInit(self): 
        main = wxFrame(None, -1, 'Main Frame') 
        main.Show(true) 
        self.SetTopWindow(main) 
        login = LoginDialog(main) 
        user = login.GetUser() 
        print user 
        return true 

app = testLogin(0) 
app.MainLoop() 
