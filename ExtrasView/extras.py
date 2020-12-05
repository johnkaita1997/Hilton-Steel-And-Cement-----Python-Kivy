from kivy.config import Config
import pandas as pd

Config.set('graphics', 'resizable', False)
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

import webbrowser
import datetime
import tempfile

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView

import overall

Builder.load_file('ExtrasView/extras.kv')


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton2(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv = None

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton2, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton2, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        self.index = index
        self.rv = rv

    def on_press(self):
       pass

    def get_row_range(self, index: int, num_cols: int) -> range:
        # index - index, which you want the row of
        # num_cols - number of columns in your table
        row = int(index / num_cols)  # the row you want
        return range(row * num_cols, (row + 1) * num_cols)  # the range which that index lies

    def update_changes(self, obj_text):
        # ALERT DIALOG IN  PYTHO
        hello = ExtrasWindow()
        # Example usage of querying the index '10'
        clicked_index = self.index  # in the event handler get which index was clicked
        num_cols = 4  # your example has 9 columns

        # List
        thelist = []

        for i in self.get_row_range(clicked_index, num_cols):
            thelist.append(self.rv.data[i]["text"])

        date = thelist[0]
        tittle = thelist[1]
        description = thelist[2]
        url = thelist[3]

        hello.openurl(url)




class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.5, .5)


class ExtrasWindow(BoxLayout):
    data_items = ListProperty([])
    mylocation = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            self.notify = Notify()
            self.blob_value = None
            self.active = None
            self.prodactive = None
            self.today = datetime.datetime.today()
            self.filename = tempfile.mktemp(".txt")

            self.loadspinnerssec()
            self.loadtheinitiatorsec()

            self.dated_already = []

            self.fectchall()
            self.notify = Notify()
        except Exception as exception:
            self.showAlert(str(exception))



    def root_Go_back(self):
        try:
            self.parent.parent.current = 'scrn_admin'
        except Exception as exception:
            self.showAlert(str(exception))



    def export_dated(self):
        if not self.dated_already:
            self.showAlert("Reenter the search dates")
        else:
            try:
                additions = self.dated_already
                data = pd.DataFrame(additions)
                datatoExcel = pd.ExcelWriter("C:\CocabTechSolutionsPos\Dated_Extras_Search.xlsx",
                                             engine='xlsxwriter')
                data.to_excel(datatoExcel, sheet_name='Sheet1')
                datatoExcel.save()
            except Exception as exception:
                self.showAlert(str(exception))


    def dated_Search(self):

        try:

            print("Dated Search")

            beginday = self.ids.sdaysec.text.strip()
            beginmonth = self.ids.smonthsec.text.strip()
            beginyear = self.ids.syearsec.text.strip()

            endday = self.ids.edaysec.text.strip()
            endmonth = self.ids.emonthsec.text.strip()
            endyear = self.ids.eyearsec.text.strip()

            mindate = beginyear + "-" + beginmonth + "-" + beginday
            maxdate = endyear + "-" + endmonth + "-" + endday

            datte = {}
            datte['mindate'] = mindate
            datte['maxdate'] = maxdate

            try:
                editedmindate = datetime.datetime.strptime(mindate, '%Y-%m-%d')
                editedmaxdate = datetime.datetime.strptime(maxdate, '%Y-%m-%d')

                the_total_search = []

                path = overall.dbs.reference("specialhistory")
                snapshot = path.order_by_child('date').get()

                thelist = []
                second_list = []

                if snapshot:
                    for sale in snapshot.values():
                        thedate = sale['date']
                        editeddate = datetime.datetime.strptime(thedate, '%Y-%m-%d')

                        line_format = '%s : %s'
                        john = "\n".join([line_format % (key, str(value)) for key, value in sale.items()])

                        if editeddate <= editedmaxdate and editeddate >= editedmindate:
                            thelist.append(john)
                            second_list.append(sale)
                            print("Found one....")

                    self.data_items = []
                    self.data_items = thelist
                    self.dated_already = second_list


                else:
                    self.Alert('Could not find data')

            except Exception as exception:
                self.showAlert(str(exception))
        except Exception as exception:
            self.showAlert(str(exception))




    def export_all_additions(self):

        try:
            ref = overall.dbs.reference('specialhistory')
            snapshot = ref.get()

            if snapshot:
                for value in snapshot.values():
                    line_format = '%s : %s'
                    john = "\n".join([line_format % (key, str(value)) for key, value in value.items()])

                    self.data_items = []
                    self.data_items.append(john)

                additions = snapshot.values()
                data = pd.DataFrame(additions)
                datatoExcel = pd.ExcelWriter("C:\CocabTechSolutionsPos\Extras_All.xlsx", engine='xlsxwriter')
                data.to_excel(datatoExcel, sheet_name='Sheet1')
                datatoExcel.save()


            else:
                self.showAlert("No data is available")
        except Exception as exception:
            self.showAlert(str(exception))
        else:
            self.showAlert("Operation was successful")



    def openurl(self, text):
        return webbrowser.open(text)


    def search_Description(self):

        try:
            inp_description = self.ids.thedescription.text.strip()
            list = []

            if not inp_description:
                self.showAlert("Enter the tittle")
            else:

                ref = overall.dbs.reference('links')
                snapshot = ref.get()

                if not snapshot:
                    self.showAlert("No data")
                else:
                    for value in snapshot.values():
                        date = value['date']
                        description = value['description']
                        title = value['title']
                        url = value['url']

                        if inp_description in description:

                            oldurl = url
                            newurl = ""
                            for i, letter in enumerate(oldurl):
                                if i % 20 == 0:
                                    newurl += '\n'
                                newurl += letter

                            # this is just because at the beginning too a `\n` character gets added
                            newurl = newurl[1:]

                            print(newurl)

                            list.append((date, title, description, newurl))

                            self.data_items = []

                            # create data_items
                            for row in list:
                                for col in row:  self.data_items.append(col)

        except Exception as exception:
            self.showAlert(str(exception))


    def search_Id(self):
        try:
            inp_idnuimber = self.ids.theidnumber.text.strip()
            thelist = []

            if not inp_idnuimber:
                self.showAlert("Enter the Id Number")
            else:

                ref = overall.dbs.reference('specialhistory')
                snapshot = ref.order_by_child('idnumber').equal_to(inp_idnuimber).get()

            if snapshot:
                for value in snapshot.values():
                    line_format = '%s : %s'
                    john = "\n".join([line_format % (key, str(value)) for key, value in value.items()])

                    thelist.append(john)

                self.data_items = []
                self.data_items = thelist

            else:
                self.showAlert("No data is available")

            self.ids.theidnumber.text = ''

        except Exception as exception:
            self.showAlert(str(exception))



    def fectchall(self):
        try:
            the_total_search = []
            ref = overall.dbs.reference('specialhistory')
            snapshot = ref.get()

            thelist = []

            if snapshot:
                for value in snapshot.values():
                    line_format = '%s : %s'
                    john = "\n".join([line_format % (key, str(value)) for key, value in value.items()])

                    thelist.append(john)

                self.data_items = []
                self.data_items = thelist

            else:
                self.showAlert("No data is available")

        except Exception as exception:
            self.showAlert(str(exception))


    def loadtheinitiatorsec(self):

        try:
            self.sgdaysec = '0'
            self.sgmonthsec = '0'
            self.sgyearsec = '0'

            self.egdaysec = '0'
            self.egmonthsec = '0'
            self.egyearsec = '0'

        except Exception as exception:
            self.showAlert(str(exception))



    def loadspinnerssec(self):

        try:
            # Prepare the spinners
            self.sdaysec = self.ids.sdaysec
            self.sdaysec.values = [str(x) for x in range(32)]
            self.sdaysec.bind(text=self.sssdaysec)

            self.smonthsec = self.ids.smonthsec
            self.smonthsec.values = [str(x) for x in range(13)]
            self.smonthsec.bind(text=self.sssmonthsec)

            self.syearsec = self.ids.syearsec
            self.syearsec.values = [str(x) for x in range(2020, 2030)]
            self.syearsec.bind(text=self.sssyearsec)

            # Prepare the spinners
            self.edaysec = self.ids.edaysec
            self.edaysec.values = [str(x) for x in range(32)]
            self.edaysec.bind(text=self.eeedaysec)

            self.emonthsec = self.ids.emonthsec
            self.emonthsec.values = [str(x) for x in range(13)]
            self.emonthsec.bind(text=self.eeemonthsec)

            self.eyearsec = self.ids.eyearsec
            self.eyearsec.values = [str(x) for x in range(2020, 2030)]
            self.eyearsec.bind(text=self.eeeyearsec)
        except Exception as exception:
            self.showAlert(str(exception))




    def sssdaysec(self, spinner, text):

        try:
            self.sgdaysec = text
        except Exception as exception:
            self.showAlert(str(exception))



    def sssmonthsec(self, spinner, text):
        try:
            self.sgmonthsec = text

        except Exception as exception:
            self.showAlert(str(exception))


    def sssyearsec(self, spinner, text):
        try:
            self.sgyearsec = text
        except Exception as exception:
            self.showAlert(str(exception))

    def eeedaysec(self, spinner, text):
        try:
            self.egdaysec = text
        except Exception as exception:
            self.showAlert(str(exception))


    def eeemonthsec(self, spinner, text):
        try:
            self.egmonthsec = text
        except Exception as exception:
            self.showAlert(str(exception))

    def eeeyearsec(self, spinner, text):
        try:
            self.egyearsec = text
        except Exception as exception:
            self.showAlert(str(exception))




    def showAlert(self, message):
        self.notify.add_widget(Label(text='[color=#FF0000][b]' + message + '[/b][/color]', markup=True))
        self.notify.open()
        Clock.schedule_once(self.killswitch, 5)


    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()


class AddApp(App):
    def build(self):
        return ExtrasWindow()


if __name__ == "__main__":
    active_App = AddApp()
    active_App.run()
