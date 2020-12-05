from kivy.app import App
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class MessageBox(Popup):

    def popup_dismiss(self):
        self.dismiss()


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """
    selected_value = StringProperty('')
    btn_info = ListProperty(['Button 0 Text', 'Button 1 Text', 'Button 2 Text'])


class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """
    index = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_press(self):
        self.parent.selected_value = 'Selected: {}'.format(self.parent.btn_info[int(self.text)])

    def on_release(self):
        MessageBox().open()


class HoldWindow(RecycleView):
    rv_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(HoldWindow, self).__init__(**kwargs)


class Holder(App):
    title = "RecycleView Button Popup Demo"
    def build(self):
        return HoldWindow()


if __name__ == "__main__":
    Holder().run()