from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView

import overall

Config.set('graphics', 'resizable', False)

Builder.load_file('BaseLogin/login.kv')

class drop_content(DropDown):
    pass

class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.3, .3)


class LoginWindow(BoxLayout):
    headerlabel = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:

            # A solution for the spinners
            self.locationspinner = []

            drop = drop_content()

            self.variables = []

            self.ulocation = ''
            self.uusername = ''

            self.notify = Notify()
            self.branch = self.ids.branch

            ref = overall.dbs.reference('braches')
            snapshot = ref.order_by_child('name').get()
            name = [value['name'] for value in snapshot.values()]
            newList = name
            self.branch.values = newList

        except Exception as exception:
            self.showAlert(str(exception))


    def show_drop(self):
        self.drop.open

    def Convert(lst):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct

    def showAlert(self, message):
        self.notify.add_widget(Label(text='[color=#FF0000][b]' + message + '[/b][/color]', markup=True))
        self.notify.open()
        Clock.schedule_once(self.killswitch, 5)

    def spinner_selected(self, text):
        self.spinnertext = text
        self.locationspinner.append(text)
        # Add Widgets to
        self.ulocation = self.spinnertext
        overall.location = self.spinnertext
        self.parent.parent.parent.admin_widget.mylocation = str(self.ulocation)
        # Add the active location to the database

    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def login_user(self):

        try:
            if (self.ulocation == ''):
                self.notify.add_widget(Label(text='[color=#FF0000][b]Select location[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:
                theemail = self.ids.email.text.strip()
                thepassword = self.ids.password.text.strip()

                if theemail == '' or thepassword == '':
                    self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
                    self.notify.open()
                    Clock.schedule_once(self.killswitch, 5)

                else:
                    # Get the credential using password
                    ref = overall.dbs.reference("users")
                    snapshot = ref.order_by_child('uid').get()

                    for d in snapshot.values():
                        if thepassword in d.values():

                            operation = overall.db.child("users").child(thepassword).child('designation').get().val()
                            name = overall.db.child("users").child(thepassword).child('name').get().val()

                            if name:
                                self.parent.parent.parent.pos_widget.headerlabel = overall.heading + "                             |                                " + name + "                             "
                                self.parent.parent.parent.pos_widget.reallocation = str(self.ulocation)
                                self.parent.parent.parent.admin_widget.mylocation = str(self.ulocation)
                                self.parent.parent.parent.pos_widget.user = name
                                self.parent.parent.parent.admin_widget.loadEverything()
                                #self.parent.parent.parent.additions_widget.departure()

                                self.ids.email.text = ''
                                self.ids.password.text = ''

                                if operation == 'Administrator':
                                    self.parent.parent.current = 'scrn_admin'
                                elif operation == 'Operator':
                                    self.parent.parent.current = 'scrn_pos'

                                else:
                                    self.notify.add_widget(
                                        Label(text='[color=#FF0000][b]An error occured[/b][/color]', markup=True))
                                    self.notify.open()
                                    Clock.schedule_once(self.killswitch, 5)
                            else:
                                self.showAlert("Does not exist")


                        else:
                           pass

        except Exception as exception:
            self.showAlert(str(exception))


class LogInApp(App):
    def build(self):
        return LoginWindow()


if __name__ == "__main__":
    active_App = LogInApp()
    active_App.run()
