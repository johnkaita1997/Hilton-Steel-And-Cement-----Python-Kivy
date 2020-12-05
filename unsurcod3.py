import datetime
from random import randint

from kivy import Config

Config.set('graphics', 'multisamples', '0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from BaseAdmin.admin import AdminWindow
from BaseLogin.login import LoginWindow
from PointOfSale.pos import PosWindow
from kivy.core.window import Window

# New size
size = (1100, 630)

# Get the actual pos and knowing the old size calcu +late the new one
top = Window.top * Window.size[1] / size[0]
left = Window.left * Window.size[1] / size[0]

# Change the size
Window.size = size

# Fixing pos
Window.top = top
Window.left = left

class MainWindow(BoxLayout):
    admin_widget = AdminWindow()     # An instance of our Pdmin wdindow
    signin_widget = LoginWindow()    # An instance of our sign in window
    pos_widget = PosWindow()         #An instance of the pos window


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from_Company = 'Hilton Steel and Cement'
        address = 'P.O Box 15344'
        city = 'Nakuru'
        tel_no = '0729836000'
        email = 'kaitajohnn@gmail.com'
        date = str(datetime.datetime.today())
        invoiceno =  str(randint(1, 10000))
        header = "                                                      COMPANY INVOICE\n\n"
        clientname = 'Client Name'
        clientmobile = 'Client Mobile'
        left_aligned = header +  "\nCOMPANY: " + from_Company  +  '                                                             DATE: ' + date + '\nINVOICE NO: ' + invoiceno + "\nADDRESS: " + address + "\nCITY :" + city + "\nEMAIL: " + email + "\nTEL NO: " + tel_no + "\nVAT NO: " + " " + "\n\nBILL TO:\n" + clientname + '\nTEL NO: ' + clientmobile + "\n\n\n"

        print(left_aligned)



class WEllIDONTGIVEUP(App):

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    app = WEllIDONTGIVEUP()
    app.run()




