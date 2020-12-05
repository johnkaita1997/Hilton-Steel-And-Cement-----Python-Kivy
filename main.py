from kivy import Config
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView

Config.set('graphics', 'multisamples', '0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from BaseAdmin.admin import AdminWindow
from BaseLogin.login import LoginWindow
from PointOfSale.pos import PosWindow
from kivy.core.window import Window
from Control.thecontrol import ControlWindow
from Added.add import AddWindow
from ExtrasView.extras import  ExtrasWindow
from BaseExpenses.expenses import ExpensesWindow


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

class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.3, .3)


class MainWindow(BoxLayout):

    additions_widget = AddWindow()
    admin_widget = AdminWindow()  # An instance of our Pdmin wdindow
    signin_widget = LoginWindow()  # An instance of our sign in window
    pos_widget = PosWindow()  # An instance of the pos window
    control_widget = ControlWindow()
    extras_widget = ExtrasWindow()
    expenses_widget = ExpensesWindow()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_pos.add_widget(self.pos_widget)
        self.ids.scrn_ctrl.add_widget(self.control_widget)
        self.ids.scrn_private_key.add_widget(self.additions_widget)
        self.ids.scrn_extras.add_widget(self.extras_widget)
        self.ids.scrn_Expenses.add_widget(self.expenses_widget)

    def showAlert(self, message):
        self.notify.add_widget(Label(text='[color=#FF0000][b]' + message + '[/b][/color]', markup=True))
        self.notify.open()
        Clock.schedule_once(self.killswitch, 5)

    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()


class MainApp(App):

    def build(self):
        return MainWindow()

if __name__ == '__main__':
    app = MainApp()
    app.run()