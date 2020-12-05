from kivy import Config
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView

import overall

Config.set('graphics', 'multisamples', '0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('Control/control.kv')

class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ControlWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.notify = Notify()

    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def showAlert(self, message):
        self.notify.add_widget(Label(text='[color=#FF0000][b]' + message + '[/b][/color]', markup=True))
        self.notify.open()
        Clock.schedule_once(self.killswitch, 5)

    def product_Key_Check(self):
        input = self.ids.enteredproductkey.text.strip()

        if input:

            try:
                #self.users_by_name = overall.db.child("control").order_by_child("key").get().val()
                self.users_by_name = overall.db.child("control").child("asdfasdf").child("key").get().val()
                if self.users_by_name == input:
                    self.parent.parent.current = 'scrn_login'
                else:
                    self.showAlert("Product Not Verified! Login to Firebase Console And Clear Payment Status!!")
            except Exception as message:
                self.showAlert(str(message))

        else:
            self.showAlert("You have to enter all fields")


class ControlApp(App):
    def build(self):
        return ControlWindow()



if __name__ == '__main__':
    app = ControlApp()
    app.run()