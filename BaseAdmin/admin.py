import datetime
import os
import tempfile
from random import randint

import texttable as tt
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

import overall

Config.set('graphics', 'resizable', False)
from kivy.lang import Builder
from utils.usersrecycler import DataTable
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup
import pandas as pd
from tkinter.filedialog import askopenfilename
from tkinter import Tk


Builder.load_file('BaseAdmin/admin.kv')


class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton3(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv = None

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton3, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton3, self).on_touch_down(touch):
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


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    rv = None

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        self.index = index
        self.rv = rv

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def get_row_range(self, index: int, num_cols: int) -> range:
        # index - index, which you want the row of
        # num_cols - number of columns in your table
        row = int(index / num_cols)  # the row you want
        return range(row * num_cols, (row + 1) * num_cols)  # the range which that index lies

    def update_changes(self, txt, spinnerinput, obj_text):
        # ALERT DIALOG IN  PYTHO
        hello = AdminWindow()
        # Example usage of querying the index '10'
        clicked_index = self.index  # in the event handler get which index was clicked
        num_cols = 7  # your example has 9 columns

        # List
        thelist = []

        for i in self.get_row_range(clicked_index, num_cols):
            thelist.append(self.rv.data[i]["text"])

        name = thelist[0]
        category = thelist[1]
        stock = thelist[2]
        available = thelist[3]
        buyingprice = thelist[4]
        sellingprice = thelist[5]
        code = thelist[6]

        try:

            got_Stock = stock
            new_Stock = float(got_Stock) + float(txt)

            datte = {}
            datte['stock'] = new_Stock

            overall.dbs.reference('mycharacter').child(code).update(datte)

        except Exception as erro:
            hello.showAlert(str(erro))

        else:
            hello.showAlert("Operation successsful")



class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.3, .3)


class AdminWindow(BoxLayout):
    data_items = ListProperty([])
    data_items_sec = ListProperty([])
    mylocation = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.notify = Notify()
        self.blob_value = None
        self.active = None
        self.prodactive = None
        self.today = datetime.datetime.today()
        self.filename = tempfile.mktemp(".txt")

        self.notify = Notify()


    def endakwaExpenses(self):
        try:
            self.parent.parent.current = 'scrn_Expenses'
        except Exception as exception:
            self.showAlert(str(exception))


    def go_To_Expenses(self):
        try:
            self.parent.parent.current = 'scrn_Expenses'
        except Exception as exception:
            self.showAlert(str(exception))


    def view_Extras(self):
        self.go_To_Expenses()

    def view_additions(self):
        try:
            self.parent.parent.current = 'scrn_private_key'
        except Exception as exception:
            self.showAlert(str(exception))


    def save_extras(self):

        try:
            target = self.ids.addition_fields
            target.clear_widgets()

            self.numberplate_extras = TextInput(hint_text='Number Plate Extras', multiline=False,
                                                write_tab=False)
            self.empty_extras = TextInput(hint_text='Empty', input_filter='float', multiline=False, write_tab=False)
            self.firstweight_extras = TextInput(hint_text='1st Weight Extras', input_filter='float', multiline=False,
                                                write_tab=False)
            self.second_weight_extras = TextInput(hint_text='2nd Weight Extras', input_filter='float', multiline=False,
                                                  write_tab=False)
            self.customer_extras = TextInput(hint_text='Customer Extras', multiline=False, write_tab=False)
            self.the_id_number = TextInput(hint_text='Id Number', multiline=False, write_tab=False)

            try:
                self.crud_submit_Button = Button(text='Save Extras Entry', on_release=lambda x: self.add_new_extras(

                    self.numberplate_extras.text.strip(),
                    self.empty_extras.text.strip(),
                    self.firstweight_extras.text.strip(),
                    self.second_weight_extras.text.strip(),
                    str(float(self.firstweight_extras.text.strip()) - float(self.second_weight_extras.text.strip())),
                    str(float(self.firstweight_extras.text.strip()) - float(self.empty_extras.text.strip())),
                    self.customer_extras.text.strip(),
                    self.the_id_number.text.strip()))

            except Exception as exception:
                self.showAlert(str(exception))

            self.empty_label_extras_d = Label()

            path = overall.dbs.reference('mycharacter')
            theshotsec = path.get()
            subcategories = [value['name'] for value in theshotsec.values()]

            self.spinner_goods_extras = Spinner(text='Select Goods', values=subcategories)
            self.quantity_extras = TextInput(hint_text='Quantity', input_filter='float', multiline=False,
                                             write_tab=False)
            self.idinput_extras = TextInput(hint_text='Id Number', input_filter='float', multiline=False,
                                            write_tab=False)

            self.crud_push_Button_d = Button(text='Register Extras Good', on_release=lambda x: self.push_new_entries(
                self.spinner_goods_extras.text.strip(),
                self.quantity_extras.text.strip(),
                self.idinput_extras.text.strip()
            ))

            target.add_widget(self.numberplate_extras)
            target.add_widget(self.empty_extras)
            target.add_widget(self.firstweight_extras)
            target.add_widget(self.second_weight_extras)
            target.add_widget(self.customer_extras)
            target.add_widget(self.the_id_number)
            target.add_widget(self.crud_submit_Button)

            target.add_widget(self.empty_label_extras_d)

            goods_target_extras = BoxLayout(orientation='horizontal', height=35, spacing=20)
            goods_target_extras.clear_widgets()
            goods_target_extras.add_widget(self.spinner_goods_extras)
            goods_target_extras.add_widget(self.quantity_extras)
            goods_target_extras.add_widget(self.idinput_extras)
            goods_target_extras.add_widget(self.crud_push_Button_d)

            target.add_widget(goods_target_extras)

            self.actual_push = Button(text='Complete Extras Operation', on_release=lambda x: self.extra_push(
                self.idinput_extras.text.strip()
            ))

            target.add_widget(Label())
            target.add_widget(self.actual_push)




        except Exception as exception:
            self.showAlert(str(exception))


    def extra_push(self, idnumber):
        ref = overall.dbs.reference('special')
        snapshot = ref.order_by_child('idnumber').equal_to(idnumber + "\uf8ff").get() or ref.order_by_child(
            'idnumber').equal_to(idnumber.capitalize()).get()

        if snapshot:
            for key in snapshot.keys():
                # Add the value to it (Update) Zodiac is Zodiac is
                try:
                    path = overall.dbs.reference("special").child(key)
                    snapshot = path.get()

                    if snapshot:
                        overall.dbs.reference("specialhistory").push(snapshot)
                    # Load the values and get all the data from it

                    else:
                        self.showAlert("Couldn't complete operation")


                except Exception as exception:
                    self.showAlert(str(exception))

                else:
                    self.showAlert("Operation Complete")
                    self.idinput_extras.text = ''

        else:
            self.showAlert("Error! Ensure you enter correct id")


    def push_new_entries(self, spiinner_items, quantity, idnumber):

        theid = idnumber

        if not theid or not quantity:
            self.showAlert("Enter all fields")
        else:

            ref = overall.dbs.reference('special')
            snapshot = ref.order_by_child('idnumber').equal_to(theid + "\uf8ff").get() or ref.order_by_child(
                'idnumber').equal_to(theid.capitalize()).get()

            if snapshot:
                for key in snapshot.keys():
                    # Add the value to it (Update) Zodiac is Zodiac is
                    datte = {}
                    datte[spiinner_items] = quantity

                    try:
                        overall.dbs.reference("special").child(key).update(datte)

                    except Exception as exception:
                        self.showAlert(str(exception))
                    else:
                        self.showAlert("Operation was successful")


            else:
                self.showAlert("Error! Ensure you enter correct id")

            self.quantity_extras.text = ''
            self.idinput_extras.text = ''


    def add_new_extras(self,  numberplate, empty,  firstweight, secondweight, thirdweight, netweight, customername, idnumber):
        if not numberplate or not empty or not firstweight or not secondweight or not thirdweight or not netweight or not customername or not idnumber:

            if not numberplate:
                self.showAlert("Numberplate Missing")
            if not empty:
                self.showAlert("Empty Missing")
            if not firstweight:
                self.showAlert("First Weight missing")
            if not secondweight:
                self.showAlert("Second Weight Missing")
            if not thirdweight:
                self.showAlert("Third Weight Missing")
            if not netweight:
                self.showAlert("Net Weight Missing")
            if not customername:
                self.showAlert("Customer  Name missing")
            if not idnumber:
                self.showAlert("Id Number Missing")

        else:
            datte = {}
            datte["date"] = overall.today
            datte["Numberplate"] = numberplate
            datte["Empty"] = empty
            datte["Firstweight"] = firstweight
            datte["Secondweight"] = secondweight
            datte["Thirdweight"] = thirdweight
            datte["Netweight"] = netweight
            datte["Customername"] = customername
            datte["idnumber"] = idnumber

            try:
                overall.db.child("special").push(datte)
            except Exception as exception:
                self.showAlert(str(exception))
            else:
                self.showAlert("Operation was successful")

                self.numberplate_extras.text = ''
                self.empty_extras.text = ''
                self.firstweight_extras.text = ''
                self.second_weight_extras.text = ''
                self.customer_extras.text = ''
                self.the_id_number.text = ''


    def push_departure_Goods(self, spinner_goods, quantity, idnumber):

        theid = idnumber

        if not theid or not quantity:
            self.showAlert("Enter all fields")
        else:

            ref = overall.dbs.reference('additions')
            snapshot = ref.order_by_child('Didnumber').equal_to(theid + "\uf8ff").get() or ref.order_by_child(
                'Didnumber').equal_to(theid.capitalize()).get()

            if snapshot:
                for key in snapshot.keys():
                    #Add the value to it (Update) Zodiac is Zodiac is
                    datte = {}
                    datte[spinner_goods] = quantity

                    try:
                        overall.dbs.reference("additions").child(key).update(datte)

                    except Exception as exception:
                        self.showAlert(str(exception))
                    else:
                        self.showAlert("Operation was successful")


            else:
                self.showAlert("Error! Ensure you enter correct id")

            self.idinput.text = ''
            self.quantity.text = ''



    def arrival(self):
        try:
            target = self.ids.addition_fields
            target.clear_widgets()

            self.date_a = TextInput(hint_text='YYYY-MM-DD', multiline=False, write_tab=False)
            self.empty_a = TextInput(hint_text='Arrival Empty', input_filter='float', multiline=False, write_tab=False)
            self.full_a = TextInput(hint_text='Arrival Full', input_filter='float', multiline=False, write_tab=False)
            self.waste_a = TextInput(hint_text='Arrival Waste', input_filter='float', multiline=False, write_tab=False)
            self.sellingprice_a = TextInput(hint_text='Arrival Selling Price', input_filter='float', multiline=False,
                                            write_tab=False)
            self.total_sales_a = TextInput(hint_text='Total Sales', input_filter='float', multiline=False,
                                           write_tab=False)
            self.idnumber_a = TextInput(hint_text='Id Number', input_filter='float', multiline=False, write_tab=False)

            crud_submit = Button(text='Save Arrival Entry', on_release=lambda x: self.add_arrival_Entry(
                # Add the date here
                # Also add purchsases total methematically
                self.date_a.text.strip(),
                self.full_a.text.strip(),
                self.empty_a.text.strip(),
                str(float(self.full_a.text.strip()) - float(self.empty_a.text.strip())),
                self.waste_a.text.strip(),
                str(float(self.full_a.text.strip()) - float(self.empty_a.text.strip()) - float(
                    self.waste_a.text.strip())),
                self.sellingprice_a.text.strip(),
                str((float(self.full_a.text.strip()) - float(self.empty_a.text.strip()) - float(
                    self.waste_a.text.strip())) * float(self.sellingprice_a.text.strip())),
                self.idnumber_a.text.strip()))

            target.add_widget(self.date_a)
            target.add_widget(self.full_a)
            target.add_widget(self.empty_a)
            target.add_widget(self.waste_a)
            target.add_widget(self.sellingprice_a)
            target.add_widget(self.idnumber_a)
            target.add_widget(crud_submit)

        except Exception as exception:
            self.showAlert(str(exception))


    def add_arrival_Entry(self, arrival_date, arrival_full, arrival_empty, arrival_original_netweight, arrival_waste, arrival_new_net_weight, arrival_sellingprice, arrival_total_sales, arrival_idnumber):

        if not arrival_date or not arrival_full or not arrival_empty or not arrival_original_netweight or not arrival_waste or not arrival_new_net_weight or not arrival_sellingprice or not arrival_total_sales or not arrival_idnumber:
            self.showAlert("Enter all the fields")
        else:
            ref = overall.dbs.reference('additions')
            snapshot = ref.order_by_child('Didnumber').equal_to(arrival_idnumber + "\uf8ff").get() or ref.order_by_child(
                'Didnumber').equal_to(arrival_idnumber.capitalize()).get()

            if snapshot:
                for key in snapshot.keys():
                    # Add the value to it (Update) Zodiac is Zodiac is
                    datte = {}
                    datte['A-Date'] = arrival_date
                    datte['A-Full'] = str(arrival_full)
                    datte['A-Empty'] = str(arrival_empty)
                    datte['A-Origal-Weight'] = str(arrival_original_netweight)
                    datte['A-Waste'] = str(arrival_waste)
                    datte['A-Newweight'] = str(arrival_new_net_weight)
                    datte['A-Sellingprice'] = arrival_sellingprice
                    datte['A-Total-Sales'] = arrival_total_sales

                    try:
                        overall.dbs.reference("additions").child(key).update(datte)
                        path = overall.dbs.reference("additions").child(key)
                        snapshot = path.get()

                        if snapshot:
                            overall.dbs.reference("additionshistory").push(snapshot)
                        #Load the values and get all the data from it


                    except Exception as exception:
                        self.showAlert(str(exception))

                    else:
                        self.date_a.text = ''
                        self.empty_a.text = ''
                        self.full_a.text = ''
                        self.waste_a.text = ''
                        self.sellingprice_a.text = ''
                        self.idnumber_a.text = ''

            else:
                self.showAlert("Error! Ensure you enter correct id")


    def departure(self):

        target = self.ids.addition_fields
        target.clear_widgets()

        self.empty_d = TextInput(hint_text='D.empty', multiline=False,write_tab=False)
        self.full_d = TextInput(hint_text='D.full',  input_filter='float', multiline=False, write_tab=False)
        self.company_d = TextInput(hint_text='Company',  multiline=False, write_tab=False)
        self.location_d = TextInput(hint_text='Location', multiline=False, write_tab=False)
        self.vehicle_d = TextInput(hint_text='Vehicle Number Plate ', multiline=False, write_tab=False)
        self.buyingprice_d  = TextInput(hint_text='Buying Price', input_filter='float', multiline=False, write_tab=False)
        self.idnumber_d = TextInput(hint_text='Id Number', input_filter='float', multiline=False, write_tab=False)


        crud_submit = Button(text='Save Departure Entry', on_release=lambda x: self.add_departure_Entry(
                                 overall.today.strip(),
                                 self.empty_d.text.strip(),
                                 self.full_d.text.strip(),
                                 self.company_d.text.strip(),
                                 self.location_d.text.strip(),
                                 self.vehicle_d.text.strip(),
                                 self.buyingprice_d.text.strip(),
                                 self.idnumber_d.text.strip()))

        self.empty_label_extras_d = Label()

        path = overall.dbs.reference('mycharacter')
        theshotsec = path.get()
        subcategories = [value['name'] for value in theshotsec.values()]

        self.spinner_goods = Spinner(text='Select Goods', values = subcategories)
        self.quantity = TextInput(hint_text='Quantity', input_filter='float', multiline=False,write_tab=False)
        self.idinput = TextInput(hint_text='Id Number', input_filter='float', multiline=False,write_tab=False)
        self.crud_push_Button_d = Button(text='Register This Good',on_release=lambda x: self.push_departure_Goods(
            self.spinner_goods.text.strip(),
            self.quantity.text.strip(),
            self.idinput.text.strip()
        ))

        target.add_widget(self.empty_d)
        target.add_widget(self.full_d)
        target.add_widget(self.company_d)
        target.add_widget(self.location_d)
        target.add_widget(self.vehicle_d)
        target.add_widget(self.buyingprice_d)
        target.add_widget(self.idnumber_d)
        target.add_widget(crud_submit)
        target.add_widget(self.empty_label_extras_d)

        goods_target = BoxLayout(orientation = 'horizontal', height = 35, spacing = 20)
        goods_target.clear_widgets()
        goods_target.add_widget(self.spinner_goods)
        goods_target.add_widget(self.quantity)
        goods_target.add_widget(self.idinput)
        goods_target.add_widget(self.crud_push_Button_d)

        target.add_widget(goods_target)


    def add_departure_Entry(self, ddate, demptyweight, dfullweight, dcompany, dlocation, dvehicle, dbuyingprice, didnumber):

        if not ddate or not demptyweight or not dfullweight or not dcompany or not dlocation or not dvehicle or not dbuyingprice or not didnumber:
            self.showAlert("Enter all the fields")
        else:

            load = float(dfullweight) - float(demptyweight)

            datte = {}
            datte["date"] = ddate
            datte["DEmpty"] = demptyweight
            datte["DFull"] = dfullweight
            datte["DLoad"] = str(load)
            datte["Company"] = dcompany
            datte["Location"] = dlocation
            datte["Vehicle"] = dvehicle
            datte["Dbuyingprice"] = dbuyingprice
            datte["Didnumber"] = didnumber
            datte["DTotalPurchases"] = (load * float (dbuyingprice))

            try:
                overall.db.child("additions").push(datte)
            except Exception as exception:
                self.showAlert(str(exception))
            else:
                self.showAlert("Operation was successful")


            self.empty_d.text = ''
            self.full_d.text = ''
            self.company_d.text = ''
            self.location_d.text = ''
            self.vehicle_d.text = ''
            self.buyingprice_d.text = ''
            self.idnumber_d.text = ''


    def validate_Item(self, name):
        path = overall.dbs.reference("products")
        snapshot = path.order_by_child('name').get()

        names = [value['name'] for value in snapshot.values()]
        if name in names:
            self.showAlert("Name already exists\nUse a different name")
            pass


    def load_negative_money(self):
        try:

            date = []
            name = []
            amount = []
            idnumber = []
            mode = []
            bank = []

            path = overall.dbs.reference("transactions")
            snapshot = path.get()
            self.overalldata = snapshot.values()

            for transaction in snapshot.values():

                balance = transaction['amount']

                if float(balance) < 0:
                    retrieve_date = transaction['date']
                    date.append(retrieve_date)

                    retrieve_name = transaction['name']
                    name.append(retrieve_name)

                    retrieve_amount = transaction['amount']
                    amount.append(retrieve_amount)

                    retrieve_idnumber = transaction['idnumber']
                    idnumber.append(retrieve_idnumber)

                    retrieve_mode = transaction['mode']
                    mode.append(retrieve_mode)

                    retrieve_bank = transaction['bank']
                    bank.append(retrieve_bank)

            transaction = dict()
            transaction['Date'] = {}
            transaction['Name'] = {}
            transaction['Amount'] = {}
            transaction['IdNumber'] = {}
            transaction['Mode'] = {}
            transaction['Bank'] = {}

            users_length = len(date)
            idx = 0
            while idx < users_length:
                transaction['Date'][idx] = date[idx]
                transaction['Name'][idx] = name[idx]
                transaction['Amount'][idx] = amount[idx]
                transaction['IdNumber'][idx] = idnumber[idx]
                transaction['Mode'][idx] = mode[idx]
                transaction['Bank'][idx] = bank[idx]

                idx += 1

            transactioncontents = self.ids.scrn_display_all_client_statuses
            transactioncontents.clear_widgets()
            thetransaction = transaction
            transactiontable = DataTable(thetransaction)
            transactioncontents.add_widget(transactiontable)

            self.active = transaction

        except Exception as exception:
            self.showAlert(str(exception))


    def findsalesDeni(self):

        try:
            date = []
            amount = []
            payment = []
            served = []
            location = []
            confirmationcode = []
            customerpay = []
            heybalance = []

            path = overall.dbs.reference("sales")
            theshot = path.order_by_child('balance')

            snapshot = theshot.get()
            self.overalldata = snapshot.values()

            for value in snapshot.values():

                balance = value['balance']

                if float(balance) < 0:

                    damount = value['amount']
                    amount.append(damount)

                    dpayment = value['payment']
                    payment.append(dpayment)

                    dserved = value['served']
                    served.append(dserved)

                    dlocation = value['location']
                    location.append(dlocation)

                    dconfirmationcode = value['confirmationcode']
                    confirmationcode.append(dconfirmationcode)

                    dcustomerpay = value['customerpay']
                    customerpay.append(dcustomerpay)

                    jbalance = value['balance']
                    heybalance.append(jbalance)

                    ddate = value['date']
                    date.append(ddate)


            _sales = dict()
            _sales['Date'] = {}
            _sales['Amount'] = {}
            _sales['Payment'] = {}
            _sales['Served'] = {}
            _sales['Location'] = {}
            _sales['Code'] = {}
            _sales['Customerpay'] = {}
            _sales['Balance'] = {}

            users_length = len(date)
            idx = 0
            while idx < users_length:
                _sales['Date'][idx] = date[idx]
                _sales['Amount'][idx] = amount[idx]
                _sales['Payment'][idx] = payment[idx]
                _sales['Served'][idx] = served[idx]
                _sales['Location'][idx] = location[idx]
                _sales['Code'][idx] = confirmationcode[idx]
                _sales['Customerpay'][idx] = customerpay[idx]
                _sales['Balance'][idx] = heybalance[idx]

                idx += 1

            salesContents = self.ids.display_sales
            salesContents.clear_widgets()
            sales = _sales
            salestable = DataTable(sales)
            salesContents.add_widget(salestable)

        except Exception as exception:
            self.showAlert(str(exception))


    def export_Products_Today(self):
        # ALERT DIALOG IN  PYTHON
        if self.prodactive:
            try:
                data = self.prodactive

                df = pd.DataFrame(data=data)
                df = (df.T)

                datatoExcel = pd.ExcelWriter("C:\CocabTechSolutionsPos\Incoming_Products.xlsx", engine='xlsxwriter')
                df.to_excel(datatoExcel, sheet_name='Sheet1')
                datatoExcel.save()


            except:
                self.showAlert("An error occured")
            else:
                self.showAlert("Operation was successful")

        else:
            self.showAlert("Reenter the dates first")


    def dated_product_search(self):

        try:
            beginday = self.ids.sdaythird.text.strip()
            beginmonth = self.ids.smonththird.text.strip()
            beginyear = self.ids.syearthird.text.strip()

            endday = self.ids.edaythird.text.strip()
            endmonth = self.ids.emonththird.text.strip()
            endyear = self.ids.eyearthird.text.strip()

            mindate = beginyear + "-" + beginmonth + "-" + beginday
            maxdate = endyear + "-" + endmonth + "-" + endday

            datte = {}
            datte['mindate'] = mindate
            datte['maxdate'] = maxdate

            editedmindate = datetime.datetime.strptime(mindate, '%Y-%m-%d')
            editedmaxdate = datetime.datetime.strptime(maxdate, '%Y-%m-%d')

            path = overall.dbs.reference('products')
            theshot = path.get()

            list = []
            thedic = {}

            for value in theshot.values():

                date = value['date']
                editeddate = datetime.datetime.strptime(date, '%Y-%m-%d')

                if editeddate >= editedmindate and editeddate <= editedmaxdate:
                    name = value['name']
                    code = value['code']
                    buyingprice = value['buyingprice']
                    sellingprice = value['sellingprice']
                    category = value['category']
                    date = value['date']
                    total = value['total']
                    stock = value['stock']
                    subcategory = value['subcategory']

                    list.append((name, code, buyingprice, sellingprice, category, date, total, stock, subcategory))

            self.data_items_sec = []
            # create data_items
            for row in list:
                for col in row: self.data_items_sec.append(col)

            self.prodactive = list


        except Exception as exception:
            self.showAlert(str(exception))
        else:
            #self.showAlert("Operation was successful")
            pass



    def add_edit_inventory_fields(self):
            target = self.ids.ops_fields_pfinal
            target.clear_widgets()

            self.studpidbuyingprice = TextInput(hint_text='Selling Price', input_filter = 'float', multiline=False, write_tab=False)
            self.stupidsellingprice = TextInput(hint_text='Buying Price', input_filter = 'float',  multiline=False, write_tab=False)
            self.stupidproductcode = TextInput(hint_text='Prod code', multiline=False, write_tab=False)

            crud_submit = Button(text='Edit SubCat', size_hint_x=None, width=100,
                                 on_release=lambda x: self.add_edit_inventory_fields_real(self.studpidbuyingprice.text.strip(),
                                                                                    self.stupidsellingprice.text.strip(),
                                                                                          self.stupidproductcode.text.strip()))

            target.add_widget(self.studpidbuyingprice)
            target.add_widget(self.stupidsellingprice)
            target.add_widget(self.stupidproductcode)
            target.add_widget(crud_submit)


    def add_edit_inventory_fields_real(self, sellingprice, buyingprice, thecode):

        try:
            datte = {}
            datte["sellingprice"] = sellingprice
            datte["buyingprice"] = buyingprice

            if sellingprice == '' or buyingprice == '' or thecode == '' or thecode.isalnum() == False:
                self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:

                overall.dbs.reference("mycharacter").child(thecode).update(datte)

                self.studpidbuyingprice.text = ''
                self.stupidsellingprice.text = ''
                self.stupidproductcode.text = ''

        except Exception as exception:
              self.showAlert(str(exception))
        else:
            self.showAlert("Operation was successful")


    def add_product_sub_category_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        path = overall.dbs.reference('categorylist')
        theshotsec = path.get()
        maincategories = [value['name'] for value in theshotsec.values()]

        self.studpidbuyingprice = TextInput(hint_text='Buying Price', input_filter = 'float',  multiline=False, write_tab=False)
        self.stupidsellingprice = TextInput(hint_text='Selling Price', input_filter = 'float', multiline=False, write_tab=False)
        self.stupidcode = TextInput(hint_text='Product Code', multiline=False, write_tab=False)
        self.stupidname = TextInput(hint_text='Category Name', multiline=False, write_tab=False)
        self.stupidmaincategory = Spinner(text='Main Cat',  values = maincategories)
        self.stupidstock = "0.0"
        self.stupidavialabilitiy = 'Available'


        crud_submit = Button(text='Add Sub', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_product_sub_category(self.studpidbuyingprice.text.strip(), self.stupidsellingprice.text.strip(),
                                                                            self.stupidcode.text.strip(),
                                                                            self.stupidname.text.strip(),
                                                                            self.stupidmaincategory.text.strip(),
                                                                            self.stupidstock,
                                                                            self.stupidavialabilitiy, ))

        target.add_widget(self.studpidbuyingprice)
        target.add_widget(self.stupidsellingprice)
        #target.add_widget(self.stupidcode)
        target.add_widget(self.stupidname)
        target.add_widget(self.stupidmaincategory)
        target.add_widget(crud_submit)



    def add_product_sub_category(self, buyingprice, sellingprice, code, name, maincategory, stock, availability):

        datte = {}
        name = name.replace(" ","-")
        datte["code"] = name.capitalize()
        datte["name"] = name.capitalize()
        datte["buyingprice"] = buyingprice.capitalize()
        datte["sellingprice"] = sellingprice.capitalize()
        datte["maincategory"] = maincategory.capitalize()
        datte["stock"] = stock.capitalize()
        datte["available"] = "Available".capitalize()

        if  name == '' or buyingprice == '' or sellingprice == '' or maincategory == '' or stock == '' or availability == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 5)
        else:
            try:

                overall.db.child("mycharacter").child(name.capitalize()).set(datte)

            except Exception as exception:
                self.showAlert(str(exception))
            else:
                self.showAlert("Operation was successful")

                self.studpidbuyingprice.text = ''
                self.stupidsellingprice.text = ''
                self.stupidcode.text = ''
                self.stupidname.text  = ''


    def export_result(self):
        try:
            if self.active:
                sales = self.active
                data = pd.DataFrame(sales)
                datatoExcel = pd.ExcelWriter("C:\CocabTechSolutionsPos\Standalone.xlsx", engine='xlsxwriter')
                data.to_excel(datatoExcel, sheet_name='Sheet1')
                datatoExcel.save()
            else:
                self.showAlert("No data to export")

        except Exception as exception:
            self.showAlert(str(exception))
        else:
            self.showAlert("Operation was successful")



    def periodicsearch_All(self):
        try:

            path = overall.dbs.reference("history")
            snapshot = path.get()

            if snapshot:
                date = []
                name = []
                amount = []
                idnumber = []
                mode = []
                bank = []
                description = []
                previous = []

                for transaction in snapshot.values():
                    retrieve_date = transaction['date']
                    date.append(retrieve_date)

                    retrieve_name = transaction['name']
                    name.append(retrieve_name)

                    retrieve_amount = transaction['amount']
                    amount.append(retrieve_amount)

                    retrieve_idnumber = transaction['idnumber']
                    idnumber.append(retrieve_idnumber)

                    retrieve_mode = transaction['mode']
                    mode.append(retrieve_mode)

                    retrieve_bank = transaction['bank']
                    bank.append(retrieve_bank)

                    retrieve_description = transaction['description']
                    description.append(retrieve_description)

                    retrieve_previoius = transaction['previous']
                    previous.append(retrieve_previoius)

                transaction = dict()
                transaction['Date'] = {}
                transaction['Name'] = {}
                transaction['Amount'] = {}
                transaction['IdNumber'] = {}
                transaction['Mode'] = {}
                transaction['Bank'] = {}
                transaction['Description'] = {}
                transaction['Previous'] = {}

                users_length = len(date)
                idx = 0
                while idx < users_length:
                    transaction['Date'][idx] = date[idx]
                    transaction['Name'][idx] = name[idx]
                    transaction['Amount'][idx] = amount[idx]
                    transaction['IdNumber'][idx] = idnumber[idx]
                    transaction['Mode'][idx] = mode[idx]
                    transaction['Bank'][idx] = bank[idx]
                    transaction['Description'][idx] = description[idx]
                    transaction['Previous'][idx] = previous[idx]

                    idx += 1

                transactioncontents = self.ids.scrn_display_all_client_statuses
                transactioncontents.clear_widgets()
                thetransaction = transaction
                transactiontable = DataTable(thetransaction)
                transactioncontents.add_widget(transactiontable)

                self.active = transaction

                self.ids.looking_for_client.text = ''

            else:
                self.showAlert("No data avaialable")


        except Exception as ex:
            self.showAlert(str(ex))

    def periodicsearch_Advanced(self):
        identity_of_client = self.ids.looking_for_client.text

        if identity_of_client:
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

                path = overall.dbs.reference("history")
                snapshot = path.order_by_child('date').get()

                date = []
                name = []
                amount = []
                idnumber = []
                mode = []
                bank = []
                description = []
                previous = []

                for transaction in snapshot.values():
                    date = transaction['date']
                    uid = transaction['idnumber']
                    editeddate = datetime.datetime.strptime(date, '%Y-%m-%d')

                    if editeddate <= editedmindate and editeddate >= editedmaxdate and uid == identity_of_client:

                        retrieve_date = transaction[0]
                        date.append(retrieve_date)

                        retrieve_name = transaction[1]
                        name.append(retrieve_name)

                        retrieve_amount = transaction[2]
                        amount.append(retrieve_amount)

                        retrieve_idnumber = transaction[3]
                        idnumber.append(retrieve_idnumber)

                        retrieve_mode = transaction[4]
                        mode.append(retrieve_mode)

                        retrieve_bank = transaction[5]
                        bank.append(retrieve_bank)

                        retrieve_description = transaction[6]
                        description.append(retrieve_description)

                        retrieve_previoius = transaction[7]
                        previous.append(retrieve_previoius)

                    transaction = dict()
                    transaction['Date'] = {}
                    transaction['Name'] = {}
                    transaction['Amount'] = {}
                    transaction['IdNumber'] = {}
                    transaction['Mode'] = {}
                    transaction['Bank'] = {}
                    transaction['Description'] = {}
                    transaction['Previous'] = {}

                    users_length = len(date)
                    idx = 0
                    while idx < users_length:
                        transaction['Date'][idx] = date[idx]
                        transaction['Name'][idx] = name[idx]
                        transaction['Amount'][idx] = amount[idx]
                        transaction['IdNumber'][idx] = idnumber[idx]
                        transaction['Mode'][idx] = mode[idx]
                        transaction['Bank'][idx] = bank[idx]
                        transaction['Description'][idx] = description[idx]
                        transaction['Previous'][idx] = previous[idx]

                        idx += 1

                    transactioncontents = self.ids.scrn_display_all_client_statuses
                    transactioncontents.clear_widgets()
                    thetransaction = transaction
                    transactiontable = DataTable(thetransaction)
                    transactioncontents.add_widget(transactiontable)

                    self.active = transaction

                    self.ids.looking_for_client.text = ''


            except Exception as exception:
                self.showAlert(str(exception))
        else:
            self.showAlert("Enter Client ID first")
            self.displayall_active_standalone_clients()
            self.ids.looking_for_client.text = ''



    def periodicsearch_Normal(self):
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

            path = overall.dbs.reference("transactions")
            snapshot = path.order_by_child('date').get()

            if snapshot:
                date = []
                name = []
                amount = []
                idnumber = []
                mode = []
                bank = []

                for transaction in snapshot.values():

                    thedate = transaction['date']
                    editeddate = datetime.datetime.strptime(thedate, '%Y-%m-%d')

                    if editeddate <= editedmaxdate and editeddate >= editedmindate:

                        retrieve_date = transaction['date']
                        date.append(retrieve_date)

                        retrieve_name = transaction['name']
                        name.append(retrieve_name)

                        retrieve_amount = transaction['amount']
                        amount.append(retrieve_amount)

                        retrieve_idnumber = transaction['idnumber']
                        idnumber.append(retrieve_idnumber)

                        retrieve_mode = transaction['mode']
                        mode.append(retrieve_mode)

                        retrieve_bank = transaction['bank']
                        bank.append(retrieve_bank)

                transaction = dict()
                transaction['Date'] = {}
                transaction['Name'] = {}
                transaction['Amount'] = {}
                transaction['IdNumber'] = {}
                transaction['Mode'] = {}
                transaction['Bank'] = {}

                users_length = len(date)
                idx = 0
                while idx < users_length:
                    transaction['Date'][idx] = date[idx]
                    transaction['Name'][idx] = name[idx]
                    transaction['Amount'][idx] = amount[idx]
                    transaction['IdNumber'][idx] = idnumber[idx]
                    transaction['Mode'][idx] = mode[idx]
                    transaction['Bank'][idx] = bank[idx]

                    idx += 1

                transactioncontents = self.ids.scrn_display_all_client_statuses
                transactioncontents.clear_widgets()
                thetransaction = transaction
                transactiontable = DataTable(thetransaction)
                transactioncontents.add_widget(transactiontable)

                self.active = transaction

            else:
                self.showAlert("No data avaialable")


        except Exception as exception:
            self.showAlert(str(exception))

    def client_Search(self):
        identity_of_client = self.ids.looking_for_client.text.strip()
        if identity_of_client:
            #Search for this client
            try:

                path = overall.dbs.reference("history")
                theshot = path.order_by_child('idnumber').equal_to(identity_of_client).get()
                snapshot = theshot

                if snapshot:
                    date = []
                    name = []
                    amount = []
                    idnumber = []
                    mode = []
                    bank = []
                    description = []
                    previous = []

                    for transaction in snapshot.values():
                        retrieve_date = transaction['date']
                        date.append(retrieve_date)

                        retrieve_name = transaction['name']
                        name.append(retrieve_name)

                        retrieve_amount = transaction['amount']
                        amount.append(retrieve_amount)

                        retrieve_idnumber = transaction['idnumber']
                        idnumber.append(retrieve_idnumber)

                        retrieve_mode = transaction['mode']
                        mode.append(retrieve_mode)

                        retrieve_bank = transaction['bank']
                        bank.append(retrieve_bank)

                        retrieve_description = transaction['description']
                        description.append(retrieve_description)

                        retrieve_previoius = transaction['previous']
                        previous.append(retrieve_previoius)

                    transaction = dict()
                    transaction['Date'] = {}
                    transaction['Name'] = {}
                    transaction['Amount'] = {}
                    transaction['IdNumber'] = {}
                    transaction['Mode'] = {}
                    transaction['Bank'] = {}
                    transaction['Description'] = {}
                    transaction['Previous'] = {}

                    users_length = len(date)
                    idx = 0
                    while idx < users_length:
                        transaction['Date'][idx] = date[idx]
                        transaction['Name'][idx] = name[idx]
                        transaction['Amount'][idx] = amount[idx]
                        transaction['IdNumber'][idx] = idnumber[idx]
                        transaction['Mode'][idx] = mode[idx]
                        transaction['Bank'][idx] = bank[idx]
                        transaction['Description'][idx] = description[idx]
                        transaction['Previous'][idx] = previous[idx]

                        idx += 1

                    transactioncontents = self.ids.scrn_display_all_client_statuses
                    transactioncontents.clear_widgets()
                    thetransaction = transaction
                    transactiontable = DataTable(thetransaction)
                    transactioncontents.add_widget(transactiontable)

                    self.active = transaction

                    self.ids.looking_for_client.text = ''

                else:
                    self.showAlert("No such client")
                    self.ids.looking_for_client.text = ''
            except Exception as exception:
                self.showAlert(str(exception))
            else:
               #self.showAlert("Operation was successful")
                pass

        else:
            self.showAlert("Enter Client Id first")
            self.displayall_active_standalone_clients()
            self.ids.looking_for_client.text = ''


    def displayall_active_standalone_clients(self):
        try:
            # insert intio the database

            path = overall.dbs.reference("transactions")
            snapshot = path.get()

            date = []
            name = []
            amount = []
            idnumber = []
            mode = []
            bank = []

            for transaction in snapshot.values():
                retrieve_date = transaction['date']
                date.append(retrieve_date)

                retrieve_name = transaction['name']
                name.append(retrieve_name)

                retrieve_amount = transaction['amount']
                amount.append(retrieve_amount)

                retrieve_idnumber = transaction['idnumber']
                idnumber.append(retrieve_idnumber)

                retrieve_mode = transaction['mode']
                mode.append(retrieve_mode)

                retrieve_bank = transaction['bank']
                bank.append(retrieve_bank)

            transaction = dict()
            transaction['Date'] = {}
            transaction['Name'] = {}
            transaction['Amount'] = {}
            transaction['IdNumber'] = {}
            transaction['Mode'] = {}
            transaction['Bank'] = {}

            users_length = len(date)
            idx = 0
            while idx < users_length:
                transaction['Date'][idx] = date[idx]
                transaction['Name'][idx] = name[idx]
                transaction['Amount'][idx] = amount[idx]
                transaction['IdNumber'][idx] = idnumber[idx]
                transaction['Mode'][idx] = mode[idx]
                transaction['Bank'][idx] = bank[idx]

                idx += 1

            transactioncontents = self.ids.scrn_display_all_client_statuses
            transactioncontents.clear_widgets()
            thetransaction = transaction
            transactiontable = DataTable(thetransaction)
            transactioncontents.add_widget(transactiontable)

            self.active = transaction
        except Exception as exception:
            self.showAlert(str(exception))


    def add_money_fields(self):
        target = self.ids.ops_fields_standalone
        target.clear_widgets()
        self.hereamount = TextInput(hint_text='Amount', input_filter = 'float', multiline=False, write_tab=False)
        self.hereidnumber = TextInput(hint_text='Id No', input_filter = 'float', multiline=False, write_tab=False)
        self.herename = TextInput(hint_text='C.Name', multiline=False, write_tab=False)
        self.bank = TextInput(hint_text='Bank', multiline=False, write_tab=False)
        # Load the values from the database
        self.here_category = Spinner(text='Transaction', values=('Out', 'In'))
        crud_submit = Button(text='Record', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_money_entry(self.hereamount.text.strip(),
                                                                       self.hereidnumber.text.strip(),
                                                                       self.herename.text.strip(),
                                                                       self.here_category.text.strip(),
                                                                       self.bank.text.strip()))

        target.add_widget(self.hereamount)
        target.add_widget(self.hereidnumber)
        target.add_widget(self.herename)
        target.add_widget(self.bank)
        target.add_widget(self.here_category)
        target.add_widget(crud_submit)



    def add_money_entry(self, hereamount, hereidnumber, herename, herecategory, bankname):
        try:
            today = datetime.datetime.today()
            # Inssert into the database
            datte = {}
            datte["amount"] = hereamount
            datte["idnumber"] = hereidnumber
            datte["name"] = herename
            datte["mode"] = herecategory
            datte["date"] = str(today.date())
            datte["bank"] = bankname

            if hereamount == '' or hereidnumber == '' or herename == '' or herecategory == '' or bankname == '':
                self.showAlert("All fields are required")
            else:

                path = overall.dbs.reference("transactions")
                snapshot = path.child(hereidnumber).get()

                if snapshot:
                    if herecategory == 'Out':
                        old_amount = snapshot['amount']

                        new_amount = float(old_amount) + float(hereamount)

                        datte['amount'] = str(new_amount)
                        datte['bank'] = bankname

                        dattesec = {}
                        dattesec['amount'] = str(new_amount)
                        dattesec['bank'] = bankname

                        overall.dbs.reference("transactions").child(hereidnumber).update(dattesec)

                        datte["previous"] = old_amount
                        datte["description"] = "Cash out"
                        self.insert(datte)
                        self.displayall_active_standalone_clients()

                    else:
                        # Get what he has and subtract what he was given that is saved int he app
                        customer_was_given = snapshot['amount']
                        customerbrought = hereamount
                        theresult = float(customer_was_given) - float(customerbrought)

                        if float(customerbrought) > float(customer_was_given):
                            # Once it is paid remove the negative and add the value back
                            customer_Anatudai = float(customer_was_given) - float(customerbrought)
                            # Try to add to character this new stock

                            # SEARCH IF EXISTS
                            overall.dbs.reference("transactions").child(hereidnumber).update({
                                'amount': str(customer_Anatudai)
                            })

                            datte["previous"] = customer_was_given
                            datte["description"] = "Cah In More"
                            self.insert(datte)


                        elif float(customerbrought) < float(customer_was_given):
                            # Let that balance be the new acount #Pushed as the new amount to the customer
                            inaanza_next_round = theresult - float(customer_was_given)
                            # Try to add to character this new stock

                            # SEARCH IF EXISTS
                            overall.dbs.reference("transactions").child(hereidnumber).update({
                                'amount': str(theresult)
                            })

                            datte["previous"] = customer_was_given
                            datte["description"] = "Cash In Less"
                            self.insert(datte)


                        elif float(customerbrought) == float(customer_was_given):
                            # Return to zero now

                            # SEARCH IF EXISTS
                            overall.dbs.reference("transactions").child(hereidnumber).update({
                                'amount': str(0.00)
                            })

                            # Get what he has and subtract what he was given that is saved int he app
                            customer_was_given = snapshot['amount']
                            datte["previous"] = customer_was_given
                            datte["description"] = "Cash In Equal"
                            self.insert(datte)


                else:
                    # IT IS THE FIRST TIME
                    datte = {}
                    datte["amount"] = hereamount
                    datte["idnumber"] = hereidnumber
                    datte["name"] = herename
                    datte["mode"] = herecategory
                    datte["date"] = str(today.date())
                    datte["bank"] = bankname

                    try:
                        overall.db.child("transactions").child(hereidnumber).set(datte)
                        # Get what he has and subtract what he was given that is saved int he app
                        datte["previous"] = hereamount
                        datte["description"] = "Cash In Equal"
                        self.insert(datte)

                    except Exception as ex:
                        self.showAlert(str(ex))

            self.hereamount.text = ''
            self.hereidnumber.text = ''
            self.herename.text = ''
            self.bank.text = ''
        except Exception as exception:
            self.showAlert(str(exception))



    def insert(self, datte):
        try:
            strName = str(datetime.datetime.now().timestamp()).replace('.', '-')
            overall.db.child("history").child(strName).set(datte)
            self.displayall_active_standalone_clients()
        except Exception as exception:
            self.showAlert(str(exception))
        else:
            self.showAlert("Operation was successful")


    def fetchInvoice(self):
        target = self.ids.ops_fields_invoice
        target.clear_widgets()

        self.uclientcode = TextInput(hint_text='clientcode', multiline=False, write_tab=False)
        self.ucompanyname = TextInput(hint_text='TO: Name', multiline=False, write_tab=False)
        self.ucompanymobile = TextInput(hint_text='TO: Mobile', input_filter = 'float', multiline=False, write_tab=False)
        crud_submit = Button(text='Print Invoice', size_hint_x=None, width=100,
                             on_release=lambda x: self.actualInvoice(self.ucompanyname.text.strip(), self.ucompanymobile.text.strip(),
                                                                     self.uclientcode.text.strip()))

        #target.add_widget(self.uclientcode)
        target.add_widget(self.ucompanyname)
        target.add_widget(self.ucompanymobile)
        target.add_widget(crud_submit)

    def actualInvoice(self, mcompanyname, mcompanymobile, mclientcode):
        try:
            if mcompanyname == '' or mcompanymobile == '':
                self.showAlert("Enter all fields")
            else:
                try:
                    confirmedname = mcompanyname
                    confirmedmobile = mcompanymobile
                    confirmedclientcode = mclientcode

                    beginday = self.sgday
                    beginmonth = self.sgmonth
                    beginyear = self.sgyear

                    endday = self.egday
                    endmonth = self.egmonth
                    endyear = self.egyear

                    mindate = beginyear + "-" + beginmonth + "-" + beginday
                    maxdate = endyear + "-" + endmonth + "-" + endday

                    datte = {}
                    datte['mindate'] = mindate
                    datte['maxdate'] = maxdate

                    editedmindate = datetime.datetime.strptime(mindate, '%Y-%m-%d')
                    editedmaxdate = datetime.datetime.strptime(maxdate, '%Y-%m-%d')

                    date = []
                    amount = []
                    payment = []
                    served = []
                    location = []
                    confirmationcode = []
                    customerpay = []
                    balance = []

                    the_total_search = []

                    path = overall.dbs.reference("sales")
                    snapshot = path.order_by_child('date').get()

                    if snapshot:
                        for sale in snapshot.values():
                            thedate = sale['date']
                            editeddate = datetime.datetime.strptime(thedate, '%Y-%m-%d')

                            if editeddate <= editedmaxdate and editeddate >= editedmindate:
                                retrieve_date = sale['date']
                                date.append(retrieve_date)

                                retrieve_amount = sale['amount']
                                amount.append(retrieve_amount)
                                the_total_search.append(float(retrieve_amount))

                                retrieve_payment = sale['payment']
                                payment.append(retrieve_payment)

                                retrieve_served = sale['served']
                                served.append(retrieve_served)

                                retrieve_location = sale['location']
                                location.append(retrieve_location)

                                retrieve_confirmationcode = sale['confirmationcode']
                                confirmationcode.append(retrieve_confirmationcode)

                                retrieve_customerpay = sale['customerpay']
                                customerpay.append(retrieve_customerpay)

                                retrieve_balance = sale['balance']
                                balance.append(retrieve_balance)

                        total = str(sum(the_total_search))

                        _sales = dict()
                        _sales['Date'] = {}
                        _sales['Amount'] = {}
                        _sales['Payment'] = {}
                        _sales['Served'] = {}
                        _sales['Code'] = {}
                        _sales['Customerpay'] = {}
                        _sales['Balance'] = {}

                        users_length = len(date)
                        idx = 0
                        while idx < users_length:
                            _sales['Date'][idx] = date[idx]
                            _sales['Amount'][idx] = amount[idx]
                            _sales['Payment'][idx] = payment[idx]
                            _sales['Served'][idx] = served[idx]
                            _sales['Code'][idx] = confirmationcode[idx]
                            _sales['Customerpay'][idx] = customerpay[idx]
                            _sales['Balance'][idx] = balance[idx]

                            idx += 1

                        # Change the text values
                        self.ids.total_sales_select.text = "TOT KES:" + " " + total

                        target = self.ids.ops_fields_invoice
                        target.clear_widgets()

                        # Change Screen
                        content = self.ids.display_sales
                        content.clear_widgets()
                        salestable = DataTable(_sales)
                        content.add_widget(salestable)

                        self.uclientcode.text = ''
                        self.ucompanyname.text = ''
                        self.ucompanymobile.text = ''

                        from_Company = 'Hilton Steel and Cement'
                        address = 'P.O Box 3404-20100'
                        city = 'Nakuru'
                        tel_no = '0727441192'
                        email = 'Hiltonltd@yandex.com '
                        date = str(datetime.datetime.today())
                        invoiceno = str(randint(1, 10000))
                        header = "                                     COMPANY INVOICE\n\n\n\n"
                        clientname = confirmedname
                        clientmobile = confirmedmobile

                        tab = tt.Texttable()
                        headings = ['Date', 'Amount', 'Payment', 'Served', 'Location', 'Code', 'Customerpay',
                                    'Main Balance']
                        tab.header(headings)
                        #
                        # dated = []
                        # amount = []
                        # payment = []
                        # served = []
                        # location = []
                        # code = []
                        # customerpay = []
                        # mainbalance = []
                        #
                        # dated.append(_sales['Date'][0])
                        # amount.append(_sales['Amount'][0])
                        # payment.append(_sales['Payment'][0])
                        # served.append(_sales['Served'][0])
                        # location.append(_sales['Location'][0])
                        # code.append(_sales['Code'][0])
                        # customerpay.append(_sales['Customerpay'][0])
                        # mainbalance.append(_sales['Balance'][0])
                        #
                        # for row in zip(dated, amount, payment, served, location, code, customerpay, mainbalance):
                        #     tab.add_row(row)
                        #
                        # s = tab.draw()

                        thedata = pd.DataFrame(_sales)

                        ending = "SUB TOTALS:       KES " + total + "\nVAT(14%):         KES " + str(
                            str(int((float(total)) * 0.14)) + ".0" + "\nINVOICE TOTALS:   KES " + str(
                                (float(total)) - (int((float(total)) * 0.14))))
                        left_aligned = header + "\nCOMPANY: " + from_Company + '                                    DATE: ' + date + '\n                                                                    INVOICE NO: ' + invoiceno + "\nADDRESS: " + address + "\nCITY :" + city + "\nEMAIL: " + email + "\nTEL NO: " + tel_no + "\nVAT NO: " + " " + "\n\n\n\nBILL TO:" + clientname + '\nTEL NO: ' + clientmobile + "\n\n\n"
                        all = left_aligned + str(thedata) + "\n\n\n\n\n" + ending

                        try:
                            text_file = open("C:\CocabTechSolutionsPos\Exported_Invoice.txt", "w")
                            text_file.write("Purchase Amount: %s" % all)
                            text_file.close()

                            # pdf = fpdf.FPDF(format='letter')
                            # pdf.add_page()
                            # pdf.set_xy(0, 0)
                            # pdf.set_font("Arial", size=12)
                            # pdf.write(5, all)
                            # pdf.ln()
                            # pdf.output("C:/CocabTechSolutionsPos/Sales/sample.pdf")
                            # # os.startfile("C:/Users/John/Desktop/PDF/sample.pdf", "print")
                            # webbrowser.open('C:/CocabTechSolutionsPos/Sales/sample.pdf')

                        except Exception as exception:
                            self.showAlert(str(exception))
                        else:
                            self.showAlert("Invoice Export was successful")


                    else:
                        self.showAlert("No records")

                except Exception as exception:
                    self.showAlert(str(exception))

        except Exception as exception:
            self.showAlert(str(exception))


    def remove_branch_fields(self):
        target = self.ids.ops_fields_branches
        target.clear_widgets()
        self.brachnamed = TextInput(hint_text='Brach Name')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_branch(self.brachnamed.text.strip()))

        target.add_widget(self.brachnamed)
        target.add_widget(crud_submit)

    def remove_branch(self, branch):
        try:
            if branch == '' or branch:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Enter Brach Name[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:

                # ALERT DIALOG IN  PYTHON
                try:
                    overall.db.child("braches").child(branch).remove()

                except:
                    self.showAlert("An error occured")
                else:
                    self.showAlert("Operation was successful")

            content = self.ids.scrn_branches
            content.clear_widgets()

            branches = self.get_branches()
            branchestable = DataTable(table=branches)
            content.add_widget(branchestable)

            self.brachnamed.text = ''
        except Exception as exception:
            self.showAlert(str(exception))


    def add_branch_fields(self):
        target = self.ids.ops_fields_branches
        target.clear_widgets()

        self.branchname = TextInput(hint_text='Branch Name', multiline=False, write_tab=False)
        crud_submit = Button(text='Add', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_branch(self.branchname.text.strip()))

        target.add_widget(self.branchname)
        target.add_widget(crud_submit)

    def add_branch(self, bothnames):
        try:
            datte = {}
            datte["name"] = bothnames

            if (bothnames == '' or bothnames):
                self.notify.add_widget(Label(text='[color=#FF0000][b]Enter the branch name[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:
                try:
                    overall.db.child("braches").child(bothnames).set(datte)
                except:
                    self.showAlert("An error occured")
                else:
                    self.showAlert("Operation was successful")

            content = self.ids.scrn_branches
            content.clear_widgets()

            branches = self.get_branches()
            branchestable = DataTable(table=branches)
            content.add_widget(branchestable)

            self.branchname.text = ''
        except Exception as exception:
            self.showAlert(str(exception))


    def print_special_receipt(self):

        try:
            # Get the transaction code
            ztransactioncode = self.ids.transactioncode.text.strip()
            if ztransactioncode:

                path = overall.dbs.reference("sales")
                snapshot = path.child(ztransactioncode).get()

                if snapshot:
                    date = snapshot['date']
                    month = snapshot['month']
                    year = snapshot['year']
                    day = snapshot['day']
                    amount = snapshot['amount']
                    number = snapshot['number']
                    payment = snapshot['payment']
                    served = snapshot['served']
                    location = snapshot['location']
                    customerpay = snapshot['customerpay']
                    balance = snapshot['balance']
                    confirmationcode = snapshot['confirmationcode']
                    products = str(snapshot['products'])

                    companyName = "Hilton Steel and Cement Center\nLimited"
                    paytype = payment
                    companyName = companyName + "\n\nSale Receipt\n\nOpp Golden Life Mall\nP.O BOX 0000\nTEL:0727441192\nEMAIL: cocabtechsolutions@gmail.com"
                    receiptNo = randint(1, 100000)
                    finalString = companyName + "\n\nReceipt No:" + str(receiptNo) + "\n\n" + products \
                                  + "\n____________________________\n" + "Total Due:        " + amount + "\n_____________________________\n\n" + "Paid In:     " + paytype + "\n\n" + "Served By:     " + served + "\n" + "Payment:           " + customerpay + "\nBalance:            " + balance + "\n\n\nWelcome Back"

                    # printdata =bytes([29, 76, 205, 0, 29, 97, 169,7])+ b'\x1dL#\x00\x1dW\xa9\x01' + finalString.encode('utf-8')

                    with open(self.filename, "w") as outf:
                        outf.write(finalString)
                    os.startfile(self.filename, "print")

                    # pdf = fpdf.FPDF(format='letter')
                    # pdf.add_page()
                    # pdf.set_xy(0, 0)
                    # pdf.set_font("Arial", size=12)
                    # pdf.write(5, finalString)
                    # pdf.ln()
                    # pdf.output("C:/CocabTechSolutionsPos/Sales/sample.pdf")
                    # # os.startfile("C:/Users/John/Desktop/PDF/sample.pdf", "print")
                    # webbrowser.open('C:/CocabTechSolutionsPos/Sales/sample.pdf')


                else:
                    self.showAlert("No such entry.\nCheck your code")

                self.ids.transactioncode.text = ''
            else:
                self.showAlert("Enter the transaction code")

        except Exception as exception:
            self.showAlert(str(exception))


    def refresh_branches(self):
        content = self.ids.scrn_branches
        content.clear_widgets()
        branches = self.get_branches()
        branchestable = DataTable(table=branches)
        content.add_widget(branchestable)

    def loadEverything(self):

        try:
            self.displayall_active_standalone_clients()

            self.filename = tempfile.mktemp(".txt")

            overall.location = self.mylocation

            content = self.ids.scrn_contents
            content.clear_widgets()

            content = self.ids.display_sales
            content.clear_widgets()

            content = self.ids.scrn_branches
            content.clear_widgets()

            # Load the recyclerview
            self.get_users_new()

            content = self.ids.scrn_contents
            users = self.get_users()
            userstable = DataTable(table=users)
            content.add_widget(userstable)

            content = self.ids.scrn_branches
            branches = self.get_branches()
            branchestable = DataTable(table=branches)
            content.add_widget(branchestable)

            self.get_products()

            salesContents = self.ids.display_sales
            sales = self.get_sales()
            if sales:
                salestable = DataTable(sales)
                salesContents.add_widget(salestable)

            self.loadspinners()
            self.loadtheinitiator()

            self.loadspinnerssec()
            self.loadtheinitiatorsec()

            self.loadspinnersthird()
            self.loadtheinitiatorthird()

            self.overalldata = {}

            self.departure()

        except Exception as exception:
            self.showAlert(str(exception))



    def loadEverythingSec(self):
        try:
            self.displayall_active_standalone_clients()

            self.filename = tempfile.mktemp(".txt")

            overall.location = self.mylocation

            self.loadspinners()
            self.loadtheinitiator()

            self.loadspinnerssec()
            self.loadtheinitiatorsec()

            self.loadspinnersthird()
            self.loadtheinitiatorthird()

            self.overalldata = {}

        except Exception as exception:
            self.showAlert(str(exception))



    def refreshRecyclerView(self):
        # Load the recyclerview
        try:
            self.get_users_new()
        except Exception as exception:
            self.showAlert(str(exception))


    def searchInventory(self):
        try:
            input = self.ids.nipe.text.strip()

            if input:

                ref = overall.dbs.reference('mycharacter')
                snapshot = ref.order_by_child('name').start_at(input).end_at(input + "\uf8ff").get() or ref.order_by_child('code').start_at(input.capitalize()).end_at(input.capitalize() + "\uf8ff").get()

                if snapshot:

                    list = []
                    for value in snapshot.values():
                        name = value['name']
                        maincategory = value['maincategory']
                        stock = value['stock']
                        available = value['available']
                        buyingprice = value['buyingprice']
                        sellingprice = value['sellingprice']
                        code = value['code']

                        list.append((name, maincategory, stock, available, buyingprice, sellingprice, code))

                    self.data_items = []

                    # create data_items
                    for row in list:
                        for col in row: \
                                self.data_items.append(col)

                else:
                    self.showAlert("Couldn't find such record")

            else:
               pass

        except Exception as exception:
            self.showAlert(str(exception))



    def choose(self):
        try:
            # Select image file types, returned image should be used as source of Image widget.
            Tk().withdraw()  # avoids window accompanying tkinter FileChooser
            path = askopenfilename(initialdir="/", title="Select file",
                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))

            try:
                thedata = open(path, 'rb').read()
                self.blob_value = thedata
            except:
                pass
        except Exception as exception:
            self.showAlert(str(exception))

    def export_Sales(self):
        try:
            sales = self.salesForToday()
            data = pd.DataFrame(sales)


            datatoExcel = pd.ExcelWriter("C:\CocabTechSolutionsPos\Sales_For_Today.xlsx", engine='xlsxwriter')
            data.to_excel(datatoExcel, sheet_name='Sheet1')
            datatoExcel.save()

        except Exception as exception:
            self.showAlert(str(exception))
        else:
            self.showAlert("Operation was successful")

    def print_sales(self):

        try:
            path = overall.dbs.reference("sales")
            snapshot = path.get()

            df = pd.DataFrame(data=snapshot)
            df = (df.T)

            datatoExcel = pd.ExcelWriter("C:\CocabTechSolutionsPos\All_The_Sales.xlsx", engine='xlsxwriter')
            df.to_excel(datatoExcel, sheet_name='Sheet1')
            datatoExcel.save()

        except Exception as exception:
            self.showAlert(str(exception))
        else:
            self.showAlert("Operation was successful")

    def salesForToday(self):

        try:
            d4 = datetime.datetime.today().strftime("%Y-%m-%d")

            date = []
            amount = []
            payment = []
            served = []
            location = []
            confirmationcode = []
            customerpay = []
            balance = []

            # SEARCH IF EXISTS
            path = overall.dbs.reference("sales")
            snapshot = path.order_by_child('date').get()

            for sale in snapshot.values():
                retrieve_date = sale['date']
                tengenezaDate = datetime.datetime.strptime(retrieve_date, '%Y-%m-%d')
                leo = datetime.datetime.strptime(d4, '%Y-%m-%d')

                if tengenezaDate == leo:

                    date.append(retrieve_date)

                    retrieve_amount = sale['amount']
                    amount.append(retrieve_amount)

                    retrieve_payment = sale['payment']
                    payment.append(retrieve_payment)

                    retrieve_served = sale['served']
                    served.append(retrieve_served)

                    retrieve_location = sale['location']
                    location.append(retrieve_location)

                    retrieve_confirmationcode = sale['confirmationcode']
                    confirmationcode.append(retrieve_confirmationcode)

                    retrieve_customerpay = sale['customerpay']
                    customerpay.append(retrieve_customerpay)

                    retrieve_balance = sale['balance']
                    balance.append(retrieve_balance)

            _sales = dict()
            _sales['Date'] = {}
            _sales['Amount'] = {}
            _sales['Payment'] = {}
            _sales['Served'] = {}
            _sales['Location'] = {}
            _sales['Code'] = {}
            _sales['Customerpay'] = {}
            _sales['Balance'] = {}

            users_length = len(date)
            idx = 0
            while idx < users_length:
                _sales['Date'][idx] = date[idx]
                _sales['Amount'][idx] = amount[idx]
                _sales['Payment'][idx] = payment[idx]
                _sales['Served'][idx] = served[idx]
                _sales['Location'][idx] = location[idx]
                _sales['Code'][idx] = confirmationcode[idx]
                _sales['Customerpay'][idx] = customerpay[idx]
                _sales['Balance'][idx] = balance[idx]

                idx += 1

            return _sales

        except Exception as exception:
            self.showAlert(str(exception))


    def exportInventory(self):

        try:
            path = overall.dbs.reference("mycharacter")
            snapshot = path.get()

            df = pd.DataFrame(data=snapshot)
            df = (df.T)

            datatoExcel = pd.ExcelWriter("C:\CocabTechSolutionsPos\Inventory.xlsx", engine='xlsxwriter')
            df.to_excel(datatoExcel, sheet_name='Sheet1')
            datatoExcel.save()

            # text_file = open("C:\CocabTechSolutionsPos\Inventory.txt", "w")
            # text_file.write("Purchase Amount: %s" % str(df))
            # text_file.close()

            # pdf = fpdf.FPDF(format='letter')
            # pdf.add_page()
            # pdf.set_font("Arial", size=12)
            # pdf.write(5, s)
            # pdf.ln()
            # pdf.output("C:\CocabTechSolutionsPos\Inventory.pdf")


        except Exception as exception:
            self.showAlert(str(exception))
        else:
            self.showAlert("Operation was successful")


    def reload_screen(self):
        # Change Screen
        content = self.ids.display_searched_products
        content.clear_widgets()

    def get_users_new(self):
        try:
            self.data_items = []

            path = overall.dbs.reference("mycharacter")
            items = path.get()

            arrows = len(items)
            self.ids.total_inventory.text = str(arrows) + " Products"

            list = []
            for value in items.values():
                name = value['name']
                maincategory = value['maincategory']
                stock = value['stock']
                available = value['available']
                buyingprice = value['buyingprice']
                sellingprice = value['sellingprice']
                code = value['code']

                list.append((name, maincategory, stock, available, buyingprice, sellingprice, code))

            # create data_items
            for row in list:
                for col in row: \
                        self.data_items.append(col)
        except Exception as exception:
            self.showAlert(str(exception))



    def loadtheinitiator(self):
        self.sgday = '0'
        self.sgmonth = '0'
        self.sgyear = '0'

        self.egday = '0'
        self.egmonth = '0'
        self.egyear = '0'

    def loadtheinitiatorsec(self):
        self.sgdaysec = '0'
        self.sgmonthsec = '0'
        self.sgyearsec = '0'

        self.egdaysec = '0'
        self.egmonthsec = '0'
        self.egyearsec = '0'


    def loadtheinitiatorthird(self):
        self.sgdaythird = '0'
        self.sgmonththird = '0'
        self.sgyearthird = '0'

        self.egdaythird = '0'
        self.egmonththird = '0'
        self.egyearthird = '0'


    def loadspinners(self):
        # Prepare the spinners
        self.sday = self.ids.sday
        self.sday.values = [str(x) for x in range(32)]
        self.sday.bind(text=self.sssday)

        self.smonth = self.ids.smonth
        self.smonth.values = [str(x) for x in range(13)]
        self.smonth.bind(text=self.sssmonth)

        self.syear = self.ids.syear
        self.syear.values = [str(x) for x in range(2020, 2030)]
        self.syear.bind(text=self.sssyear)

        # Prepare the spinners
        self.eday = self.ids.eday
        self.eday.values = [str(x) for x in range(32)]
        self.eday.bind(text=self.eeeday)

        self.emonth = self.ids.emonth
        self.emonth.values = [str(x) for x in range(13)]
        self.emonth.bind(text=self.eeemonth)

        self.eyear = self.ids.eyear
        self.eyear.values = [str(x) for x in range(2020, 2030)]
        self.eyear.bind(text=self.eeeyear)


    def loadspinnerssec(self):
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


    def loadspinnersthird(self):
        # Prepare the spinners
        self.sdaythird = self.ids.sdaythird
        self.sdaythird.values = [str(x) for x in range(32)]
        self.sdaythird.bind(text=self.sssdaythird)

        self.smonththird = self.ids.smonththird
        self.smonththird.values = [str(x) for x in range(13)]
        self.smonththird.bind(text=self.sssmonththird)

        self.syearthird = self.ids.syearthird
        self.syearthird.values = [str(x) for x in range(2020, 2030)]
        self.syearthird.bind(text=self.sssyearthird)

        # Prepare the spinners
        self.edaythird = self.ids.edaythird
        self.edaythird.values = [str(x) for x in range(32)]
        self.edaythird.bind(text=self.eeedaythird)

        self.emonththird = self.ids.emonththird
        self.emonththird.values = [str(x) for x in range(13)]
        self.emonththird.bind(text=self.eeemonththird)

        self.eyearthird = self.ids.eyearthird
        self.eyearthird.values = [str(x) for x in range(2020, 2030)]
        self.eyearthird.bind(text=self.eeeyearsec)


    def sssday(self, spinner, text):
        self.sgday = text

    def sssmonth(self, spinner, text):
        self.sgmonth = text

    def sssyear(self, spinner, text):
        self.sgyear = text

    def eeeday(self, spinner, text):
        self.egday = text

    def eeemonth(self, spinner, text):
        self.egmonth = text

    def eeeyear(self, spinner, text):
        self.egyear = text




    def sssdaysec(self, spinner, text):
        self.sgdaysec = text

    def sssmonthsec(self, spinner, text):
        self.sgmonthsec = text

    def sssyearsec(self, spinner, text):
        self.sgyearsec = text

    def eeedaysec(self, spinner, text):
        self.egdaysec = text

    def eeemonthsec(self, spinner, text):
        self.egmonthsec = text

    def eeeyearsec(self, spinner, text):
        self.egyearsec = text



    def sssdaythird(self, spinner, text):
        self.sgdaythird = text

    def sssmonththird(self, spinner, text):
        self.sgmonththird = text

    def sssyearthird(self, spinner, text):
        self.sgyearthird = text

    def eeedaythird(self, spinner, text):
        self.egdaythird = text

    def eeemonththird(self, spinner, text):
        self.egmonththird = text

    def eeeyearthird(self, spinner, text):
        self.egyearthird = text



    def periodicsearch(self):
        beginday = self.ids.sday.text.strip()
        beginmonth = self.ids.smonth.text.strip()
        beginyear = self.ids.syear.text.strip()

        endday = self.ids.eday.text.strip()
        endmonth = self.ids.emonth.text.strip()
        endyear = self.ids.eyear.text.strip()

        mindate = beginyear + "-" + beginmonth + "-" + beginday
        maxdate = endyear + "-" + endmonth + "-" + endday

        datte = {}
        datte['mindate'] = mindate
        datte['maxdate'] = maxdate

        try:
            editedmindate = datetime.datetime.strptime(mindate, '%Y-%m-%d')
            editedmaxdate = datetime.datetime.strptime(maxdate, '%Y-%m-%d')


            date = []
            amount = []
            payment = []
            served = []
            location = []
            confirmationcode = []
            customerpay = []
            balance = []

            the_total_search = []

            path = overall.dbs.reference("sales")
            snapshot = path.order_by_child('date').get()

            if snapshot:
                for sale in snapshot.values():
                    thedate = sale['date']
                    editeddate = datetime.datetime.strptime(thedate, '%Y-%m-%d')

                    if editeddate <= editedmaxdate and editeddate >= editedmindate:

                        retrieve_date = sale['date']
                        date.append(retrieve_date)

                        retrieve_amount = sale['amount']
                        amount.append(retrieve_amount)
                        the_total_search.append(float(retrieve_amount))

                        retrieve_payment = sale['payment']
                        payment.append(retrieve_payment)

                        retrieve_served = sale['served']
                        served.append(retrieve_served)

                        retrieve_location = sale['location']
                        location.append(retrieve_location)

                        retrieve_confirmationcode = sale['confirmationcode']
                        confirmationcode.append(retrieve_confirmationcode)

                        retrieve_customerpay = sale['customerpay']
                        customerpay.append(retrieve_customerpay)

                        retrieve_balance = sale['balance']
                        balance.append(retrieve_balance)

                total = str(sum(the_total_search))

                _sales = dict()
                _sales['Date'] = {}
                _sales['Amount'] = {}
                _sales['Payment'] = {}
                _sales['Served'] = {}
                _sales['Location'] = {}
                _sales['Code'] = {}
                _sales['Customerpay'] = {}
                _sales['Balance'] = {}

                users_length = len(date)
                idx = 0
                while idx < users_length:
                    _sales['Date'][idx] = date[idx]
                    _sales['Amount'][idx] = amount[idx]
                    _sales['Payment'][idx] = payment[idx]
                    _sales['Served'][idx] = served[idx]
                    _sales['Location'][idx] = location[idx]
                    _sales['Code'][idx] = confirmationcode[idx]
                    _sales['Customerpay'][idx] = customerpay[idx]
                    _sales['Balance'][idx] = balance[idx]

                    idx += 1

                # Change the text values
                self.ids.total_sales_select.text = "TOT: KES:" + " " + total
                # Change Screen
                content = self.ids.display_sales
                content.clear_widgets()
                salestable = DataTable(_sales)
                content.add_widget(salestable)

            else:
                self.Alert('Could not find data')

        except:
            self.showAlert("Reset your dates")

    def logout(self):
        self.parent.parent.current = 'scrn_login'

    def search_Field(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        self.crud_search_word = TextInput(hint_text='Enter Product Code or Product name')
        # Load the values from the database
        crud_search_criteria = Spinner(text='code', values=['code', 'name'])
        crud_submit = Button(text='Search', size_hint_x=None, width=100,
                             on_release=lambda x: self.dotheSearch(self.crud_search_word.text.strip(),
                                                                   crud_search_criteria.text.strip()))

        target.add_widget(self.crud_search_word)
        target.add_widget(crud_search_criteria)
        target.add_widget(crud_submit)

    def dotheSearch(self, searchWord, searchCriteria):

        try:
            if searchWord.isalnum() == False:
                self.showAlert("Enter numbers and letters only")
            else:

                content = self.ids.display_searched_products
                content.clear_widgets()

                try:
                    if searchCriteria == '' or searchWord == '':
                        self.notify.add_widget(
                            Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
                        self.notify.open()
                        Clock.schedule_once(self.killswitch, 5)
                    else:

                        ref = overall.dbs.reference('products')
                        snapshot = None

                        if searchCriteria == 'code':

                            snapshot = ref.order_by_child("code").start_at(searchWord).end_at(
                                searchWord + "\uf8ff").get() \
                                       or ref.order_by_child("code").start_at(searchWord.capitalize()).end_at(
                                searchWord + "\uf8ff").get()

                        elif searchCriteria == 'name':

                            snapshot = ref.order_by_child("name").start_at(searchWord).end_at(
                                searchWord + "\uf8ff").get() \
                                       or ref.order_by_child("name").start_at(searchWord.capitalize()).end_at(
                                searchWord + "\uf8ff").get()

                    if snapshot:
                        for value in snapshot.values():
                            name = value['name']
                            code = value['code']
                            buyingprice = value['buyingprice']
                            sellingprice = value['sellingprice']
                            category = value['category']

                            _products = dict()
                            _products['name'] = {}
                            _products['code'] = {}
                            _products['buyingprice'] = {}
                            _products['sellingprice'] = {}
                            _products['category'] = {}

                            users_length = len(name)
                            idx = 0
                            while idx < users_length:
                                _products['name'][idx] = name[idx]
                                _products['code'][idx] = code[idx]
                                _products['buyingprice'][idx] = buyingprice[idx]
                                _products['sellingprice'][idx] = sellingprice[idx]
                                _products['category'][idx] = category[idx]

                                idx += 1

                        # Change Screen
                        self.ids.scrn_mngr.current = 'screen_search_product'

                        # Change the text values
                        # self.ids.total_sales.text = [sum((float(value[4]) for value in data))]

                        productContents = self.ids.display_searched_products
                        productstable = DataTable(_products)
                        productContents.add_widget(productstable)

                        self.crud_search_word.text = ''
                    else:
                        self.showAlert("No entries found!!")

                except Exception as exception:
                    self.showAlert(str(exception))
        except Exception as exception:
            self.showAlert(str(exception))




    def view_categories(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        ref = overall.dbs.reference('categorylist')
        snapshot = ref.order_by_child('name').get()
        name = [value['name'] for value in snapshot.values()]
        newList = name

        # Load the values from the database
        crud_category = Spinner(text='Select', values=newList)
        crud_submit = Button(text='View', size_hint_x=None, width=100,
                             on_release=lambda x: self.show_product_in_chosen_categories(crud_category.text.strip()))

        target.add_widget(crud_category)
        target.add_widget(crud_submit)

    def show_product_in_chosen_categories(self, crud_category):

        try:
            path = overall.dbs.reference('products')
            theshot = path.order_by_child('category').equal_to(crud_category).get()

            if theshot:

                name = [value['name'] for value in theshot.values()]
                code = [value['code'] for value in theshot.values()]
                buyingprice = [value['buyingprice'] for value in theshot.values()]
                sellingprice = [value['sellingprice'] for value in theshot.values()]
                category = [value['category'] for value in theshot.values()]

                _products = dict()
                _products['name'] = {}
                _products['code'] = {}
                _products['buyingprice'] = {}
                _products['sellingprice'] = {}
                _products['category'] = {}

                users_length = len(name)
                idx = 0
                while idx < users_length:
                    _products['name'][idx] = name[idx]
                    _products['code'][idx] = code[idx]
                    _products['buyingprice'][idx] = buyingprice[idx]
                    _products['sellingprice'][idx] = sellingprice[idx]
                    _products['category'][idx] = category[idx]

                    idx += 1

                content = self.ids.scrn_product_contents
                content.clear_widgets()

                productContents = self.ids.scrn_product_contents
                products = _products
                productstable = DataTable(products)
                productContents.add_widget(productstable)

            else:
                self.showAlert("No such product available")

        except Exception as exception:
            self.showAlert(str(exception))


    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        self.crud_code = TextInput(hint_text='Product Code')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_product(self.crud_code.text.strip()))

        target.add_widget(self.crud_code)
        target.add_widget(crud_submit)

    def remove_product(self, code):
        try:
            if code == '':
                self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:
                ref = overall.dbs.reference('products')
                snapshot = ref.order_by_child('code').equal_to(code).get()

                if snapshot:
                    for key in snapshot.keys():
                        try:
                            overall.db.child("products").child(key).remove()

                        except Exception as exception:
                            self.showAlert(str(exception))

                        else:
                            self.showAlert("Operation Complete")

                else:
                    self.showAlert("Error! Ensure you enter correct id")

            self.crud_code.text = ''
            self.get_products()


        except Exception as exception:
            self.showAlert(str(exception))


    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text='Product Code(Id No.)', multiline=False, write_tab=False)
        crud_name = TextInput(hint_text='Product Name', multiline=False, write_tab=False)
        crud_buyingprice = TextInput(hint_text='Buying Price', input_filter = 'float', multiline=False, write_tab=False)
        crud_selling_price = TextInput(hint_text='Selling Price',  input_filter = 'float', multiline=False, write_tab=False)

        prods = self.db.child("MainPos").child("categorylist").get().val()
        # Load the values from the database
        crud_category = Spinner(text='Prod Category', values=prods.values())
        crud_submit = Button(text='Add', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_product(crud_code.text.strip(),
                                                                   crud_name.text.strip(),
                                                                   crud_buyingprice.text.strip(),
                                                                   crud_selling_price.text.strip(),
                                                                   crud_category.text.strip()))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_buyingprice)
        target.add_widget(crud_selling_price)
        target.add_widget(crud_category)
        target.add_widget(crud_submit)

    def add_product_category_field(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        self.categoryName = TextInput(hint_text='Name of the category', multiline=False, write_tab=False)
        crud_submit = Button(text='Add Category', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_product_category(self.categoryName.text.strip()))

        target.add_widget(self.categoryName)
        target.add_widget(crud_submit)

    def add_product_category(self, categoryName):

        try:
            if categoryName == '' or categoryName.isalnum() == False:
                self.notify.add_widget(
                    Label(text='[color=#FF0000][b]All Fields Required \n Alphanumerical[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)

            else:

                datte = {}
                datte["name"] = categoryName.capitalize()

                try:

                    overall.db.child("categorylist").push(datte)

                except:
                    self.showAlert("An error occured")

                else:

                    path = overall.dbs.reference("categorylist")
                    snapshot = path.get()

                    vals = []
                    for value in snapshot.values():
                        name = value['name']
                    prods = vals

                    # self.parent.parent.parent.pos_widget.thespinner = self.parent.parent.parent.pos_widget.ids.thespinners
                    # self.parent.parent.parent.pos_widget.thespinner.values = prods

                    self.showAlert("Operation was successful")

            # content = self.ids.scrn_product_contents
            # content.clear_widgets()

            self.categoryName.text = ''

        except Exception as exception:
            self.showAlert(str(exception))


    def change_screen_alpha(self):
        try:

            self.kingusername = overall.username
            self.kinglocation = overall.location
            self.parent.parent.current = 'scrn_pos'

        except:

            self.showAlert("An error occured")


    def change_screen(self, instance):

        try:
            if instance.text == 'Manage Products':
                self.get_products()
                self.ids.scrn_mngr.current = 'scrn_product_content'

            elif instance.text == 'Manage Users':
                self.ids.scrn_mngr.current = 'scrn_content_manage_users'

            elif instance.text == 'Point Of Sale':
                self.parent.parent.current = 'scrn_pos'

            elif instance.text == 'Additions':
                self.ids.scrn_mngr.current = 'added'

            elif instance.text == 'Sales':
                content = self.ids.display_sales
                content.clear_widgets()

                salesContents = self.ids.display_sales
                sales = self.get_sales()
                salestable = DataTable(sales)
                salesContents.add_widget(salestable)
                self.ids.scrn_mngr.current = 'screen_display_sales'

            elif instance.text == 'Inventory':
                self.ids.scrn_mngr.current = 'screen_inventory'

            elif instance.text == 'Braches':
                target = self.ids.ops_fields_p
                target.clear_widgets()
                self.ids.scrn_mngr.current = 'scrn_branches'

            elif instance.text == 'Refresh':
                try:
                    self.loadEverythingSec()
                except Exception as exception:
                    self.showAlert(str(exception))
                else:
                    self.showAlert('Refresh Complete')


            elif instance.text == 'StandAlone':
                target = self.ids.ops_fields_p
                target.clear_widgets()
                self.ids.scrn_mngr.current = 'scrn_StandAlone'

            else:
                pass
        except Exception as exception:
            self.showAlert(str(exception))



    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        self.crud_code = TextInput(hint_text='DT830', multiline=False, write_tab=False)
        self.crud_name = TextInput(hint_text='Jane-456', multiline=False, write_tab=False)
        self.crud_buyingprice = TextInput(hint_text='Buying Price', input_filter = 'float', multiline=False, write_tab=False)
        self.crud_selling_price = TextInput(hint_text='Selling Price',  input_filter = 'float', multiline=False, write_tab=False)
        self.crud_kilograms = TextInput(hint_text='Kgs', input_filter = 'float', multiline=False, write_tab=False)

        path = overall.dbs.reference('mycharacter')
        theshot = path.get()
        subcategories = [value['name'] for value in theshot.values()]

        path = overall.dbs.reference('categorylist')
        theshotsec = path.get()
        maincategories = [value['name'] for value in theshotsec.values()]

        # Load the values from the database
        sub_category = Spinner(text='Sub Cat', values=subcategories)
        self.crud_category = Spinner(text='Main Cat', values=maincategories)
        crud_submit = Button(text='Add', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_product(self.crud_code.text.strip(), self.crud_name.text.strip(),
                                                                   self.crud_buyingprice.text.strip(),
                                                                   self.crud_selling_price.text.strip(),
                                                                   sub_category.text.strip(),
                                                                   self.crud_category.text.strip(),
                                                                   self.crud_kilograms.text.strip()))

        target.add_widget(self.crud_code)
        target.add_widget(self.crud_name)
        #target.add_widget(self.crud_buyingprice)
        #target.add_widget(self.crud_selling_price)
        target.add_widget(self.crud_kilograms)

        target.add_widget(sub_category)
        target.add_widget(self.crud_category)
        target.add_widget(crud_submit)



    def add_product(self, code, name, buyingprice, sellingprice, sub_category, category, kilograms):
        try:
            # self.validate_Item(name)

            x = name
            y = ("-".join(x.split()))

            self.choose()

            #Load the buying and selling price based on sub category
            buyingprice = 'N.P'
            sellingprice = 'N.p'
            total = 'Unavailable'

            ref = overall.dbs.reference('mycharacter')
            snapshot = ref.order_by_child('name').equal_to(sub_category).get()

            if snapshot:
                for value in snapshot.values():
                    buyingprice = value['buyingprice']
                    sellingprice = value['sellingprice']
                    total = str(float(sellingprice) * float(kilograms))
            else:
               self.showAlert("One operation being skipped.....")

            datte = {}
            datte["code"] = code
            datte["name"] = name
            datte["buyingprice"] = buyingprice
            datte["sellingprice"] = sellingprice
            datte["category"] = category
            datte["location"] = str(self.mylocation)
            datte["image"] = self.blob_value
            datte["availabilitiy"] = 'Available'
            datte["stock"] = kilograms
            datte["subcategory"] = sub_category
            datte["total"] = total
            datte["date"] = str(self.today.date())

            if name == '' or kilograms == '':
                self.notify.add_widget(
                    Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:

                overall.db.child("products").push(datte)

                ref = overall.dbs.reference('mycharacter')
                first = ref.order_by_child('name')
                first.equal_to(sub_category)

                snapshot = first.get()

                if snapshot:
                    got_Stock = snapshot[sub_category]['stock']
                    new_Stock = float(got_Stock) + float(kilograms)

                    datte = {}
                    datte["stock"] = new_Stock

                    path = overall.dbs.reference("mycharacter")
                    snapshot = path.order_by_child('name').get()

                    for value in snapshot.values():
                        keys = None
                        for parent, oval in snapshot.items():
                            revDict = dict((v, k) for k, v in oval.items())
                            if sub_category in revDict:
                                keys = [parent, revDict[sub_category]]
                                break
                        if keys:
                            overall.dbs.reference("mycharacter").child(keys[0]).update(datte)
                        else:
                            pass

                else:
                    print("Unavaadkfhaksjdfhiauef")


                # Empty the widgets
                self.crud_code.text = ''
                self.crud_name.text = ''
                self.crud_buyingprice.text = ''
                self.crud_selling_price.text = ''
                self.crud_kilograms.text = ''

                self.get_products()
        except Exception as error:
            self.showAlert(str(error))

    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        self.user = TextInput(hint_text='Id Number', input_filter = 'float', multiline = False, write_tab = False)
        crud_submit = Button(text='Remove', size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_user(self.user.text.strip()))

        target.add_widget(self.user)
        target.add_widget(crud_submit)

    def showAlert(self, message):
        self.notify.add_widget(Label(text='[color=#FF0000][b]' + message + '[/b][/color]', markup=True))
        self.notify.open()
        Clock.schedule_once(self.killswitch, 5)

    def remove_user(self, user):

        try:
            if user == '':
                self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:

                try:
                    overall.db.child("users").child(user).remove()
                except:
                    self.showAlert("An error occured")
                else:
                    self.showAlert("Operation was successful")

            self.user.text = ''
            content = self.ids.scrn_contents
            content.clear_widgets()

            users = self.get_users()
            userstable = DataTable(table=users)
            content.add_widget(userstable)

        except Exception as exception:
            self.showAlert(str(exception))


    def update_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()

        self.name = TextInput(hint_text='Both Names', multiline=False, write_tab=False)
        self.theid = TextInput(hint_text='id', multiline=False, input_filter = 'float', write_tab=False)
        self.mobile = TextInput(hint_text='Mobile', input_filter = 'float', multiline=False, write_tab=False)
        designation = Spinner(text='Operator', values=['Operator', 'Administrator'])
        crud_submit = Button(text='Update', size_hint_x=None, width=100,
                             on_release=lambda x: self.update_user(self.name.text.strip(), self.theid.text.strip(), designation.text.strip(),
                                                                   self.mobile.text.strip()))

        target.add_widget(self.name)
        target.add_widget(self.theid)
        target.add_widget(designation)
        target.add_widget(self.mobile)
        target.add_widget(crud_submit)

    def update_user(self, name, id, designation, mobile):
        if name == '' or id == '' or mobile == '' or designation == '' or name.isalnum() == False:
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 5)

        else:
            try:
                datte = {}
                datte["name"] = name
                datte["mobile"] = mobile
                datte["uid"] = id
                datte["designation"] = designation

                try:
                    overall.dbs.reference("users").child(id).update(datte)

                except Exception as exception:
                    self.showAlert(str(exception))

                else:
                    self.showAlert("Operation was successful")

                content = self.ids.scrn_contents
                content.clear_widgets()

                users = self.get_users()
                userstable = DataTable(table=users)
                content.add_widget(userstable)

                # Empty the widgets
                self.name.text = ''
                self.theid.text = ''
                self.mobile.text = ''

            except Exception as exception:
                self.showAlert(str(exception))


    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()

        self.bothnames = TextInput(hint_text='Both Names', multiline=False, write_tab=False)
        self.mobile = TextInput(hint_text='Mobile', input_filter = 'float', multiline=False, write_tab=False)
        self.idnumber = TextInput(hint_text='Id Number', input_filter = 'float', multiline=False, write_tab=False)
        designation = Spinner(text='Operator', values=['Operator', 'Administrator'])

        crud_submit = Button(text='Add', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_user(self.bothnames.text.strip(), self.mobile.text.strip(),
                                                                self.idnumber.text.strip(),
                                                                designation.text.strip()))

        target.add_widget(self.bothnames)
        target.add_widget(self.mobile)
        target.add_widget(self.idnumber)
        target.add_widget(designation)
        target.add_widget(crud_submit)

    def add_user(self, bothnames, mobile, idnumber, designation):
        try:
            datte = {}
            datte["name"] = bothnames
            datte["mobile"] = mobile
            datte["uid"] = idnumber
            datte["designation"] = designation
            datte["location"] = str(self.mylocation)

            if (bothnames == '' or mobile == '' or idnumber == '' or designation == ''):
                self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:

                try:
                    overall.db.child("users").child(idnumber).set(datte)

                except Exception as exception:

                    self.showAlert(str(exception))

                else:

                    self.showAlert("Operation was successful")

            content = self.ids.scrn_contents
            content.clear_widgets()

            users = self.get_users()
            userstable = DataTable(table=users)
            content.add_widget(userstable)

            self.bothnames.text = ''
            self.mobile.text = ''
            self.idnumber.text = ''

        except Exception as exception:
            self.showAlert(str(exception))




    def get_users(self):

        try:

            path = overall.dbs.reference('users')
            theshot = path.get()

            name = []
            mobile = []
            id = []
            designation = []

            for user in theshot.values():
                retrieve_name = user['name']
                name.append(retrieve_name)

                retrieve_mobile = user['mobile']
                mobile.append(retrieve_mobile)

                retrieve_id = user['uid']
                id.append(retrieve_id)

                retrieve_designation = user['designation']
                designation.append(retrieve_designation)

            _users = dict()
            _users['Name'] = {}
            _users['Mobile'] = {}
            _users['Id Number'] = {}
            _users['Designation'] = {}

            users_length = len(name)
            idx = 0
            while idx < users_length:
                _users['Name'][idx] = name[idx]
                _users['Mobile'][idx] = mobile[idx]
                _users['Id Number'][idx] = id[idx]
                _users['Designation'][idx] = designation[idx]

                idx += 1

            return _users


        except Exception as exception:
            self.showAlert(str(exception))



    def get_branches(self):

        try:
            path = overall.dbs.reference("braches")
            snapshot = path.order_by_child('name').get()
            name = []
            if snapshot:

                for user in snapshot.values():
                    retrieve_name = user['name']
                    name.append(retrieve_name)

                _users = dict()
                _users['Name'] = {}

                users_length = len(name)
                idx = 0
                while idx < users_length:
                    _users['Name'][idx] = name[idx]
                    idx += 1

                return _users
        except Exception as exception:
            self.showAlert(str(exception))



    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def get_sales(self):
        try:

            path = overall.dbs.reference("sales")
            snapshot = path.get()

            date = []
            amount = []
            payment = []
            served = []
            location = []
            confirmationcode = []
            customerpay = []
            balance = []

            self.overalldata = snapshot

            for sale in snapshot.values():
                retrieve_date = sale['date']
                date.append(retrieve_date)

                retrieve_amount = sale['amount']
                amount.append(retrieve_amount)

                retrieve_payment = sale['payment']
                payment.append(retrieve_payment)

                retrieve_served = sale['served']
                served.append(retrieve_served)

                retrieve_location = sale['location']
                location.append(retrieve_location)

                retrieve_confirmationcode = sale["confirmationcode"]
                confirmationcode.append(retrieve_confirmationcode)

                retrieve_customerpay = sale['customerpay']
                customerpay.append(retrieve_customerpay)

                retrieve_balance = sale['balance']
                balance.append(retrieve_balance)

            _sales = dict()
            _sales['Date'] = {}
            _sales['Amount'] = {}
            _sales['Payment'] = {}
            _sales['Served'] = {}
            _sales['Location'] = {}
            _sales['Code'] = {}
            _sales['Customerpay'] = {}
            _sales['Balance'] = {}

            users_length = len(date)
            idx = 0
            while idx < users_length:
                _sales['Date'][idx] = date[idx]
                _sales['Amount'][idx] = amount[idx]
                _sales['Payment'][idx] = payment[idx]
                _sales['Served'][idx] = served[idx]
                _sales['Location'][idx] = location[idx]
                _sales['Code'][idx] = confirmationcode[idx]
                _sales['Customerpay'][idx] = customerpay[idx]
                _sales['Balance'][idx] = balance[idx]

                idx += 1

            return _sales
        except Exception as exception:
            self.showAlert(str(exception))


    def get_products(self):
        try:
            path = overall.dbs.reference('products')
            theshot = path.get()
            list = []

            if theshot:
                for user in theshot.values():
                    name = user['name']
                    code = user['code']
                    buyingprice = user['buyingprice']
                    sellingprice = user['sellingprice']
                    category = user['category']
                    date = user['date']
                    total = user['total']
                    stock = user['stock']
                    subcategory = user['subcategory']

                    list.append((name, code, buyingprice, sellingprice, category, date, total, stock, subcategory))

                self.data_items_sec = []
                # create data_items
                for row in list:
                    for col in row: self.data_items_sec.append(col)

        except Exception as exception:
            self.showAlert(str(exception))



class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__ == "__main__":
    active_App = AdminApp()
    active_App.run()
