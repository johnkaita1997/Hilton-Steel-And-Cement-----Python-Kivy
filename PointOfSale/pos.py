import os
import datetime
import webbrowser
from datetime import date

import fpdf
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.modalview import ModalView

Config.set('graphics', 'resizable', False)
from kivy.uix.boxlayout import BoxLayout
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '300')
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.properties import DictProperty
import overall
from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from random import randint
from BaseAdmin.admin import AdminWindow

import tempfile

Builder.load_file('PointOfSale/pos.kv')

class LongpressButton(Factory.Button):
    __events__ = ('on_long_press',)

    long_press_time = Factory.NumericProperty(1)

    def on_state(self, instance, value):
        if value == 'down':
            lpt = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, lpt)
        else:
            self._clockev.cancel()

    def _do_long_press(self, dt):
        self.dispatch('on_long_press')

    def on_long_press(self, *largs):
        pass


class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.3, .3)

class PosWindow(BoxLayout):
    thebox = ObjectProperty(None)
    dynamic_ids = DictProperty()
    headerlabel = StringProperty()
    reallocation = StringProperty()
    user = StringProperty()
    prods = ListProperty()
    thespinner = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:

            self.what = 0.0

            self.haschoosentopay = ''

            self.load_window()
            self.receipt_Preview = self.ids.receipt_Preview

            self.headerlabel = "Epic"

            self.filename = tempfile.mktemp(".txt")
            self.customerpayed = ''
            self.customerbalance = ''
            self.complete_total = 0.00
            self.discount = 0.00
            self.productList = {}
            self.final_Amount = 0.00
            self.amountinput = self.ids.amountinput.text.strip()  # Load those values from the database
            self.mpesacode = self.ids.mpesacode.text.strip()
            self.finalvariables = []
            self.notify = Notify()
            self.mylocation = self.reallocation
            self.totaltoBePaid = 0.0

            path = overall.dbs.reference("mycharacter")
            snapshot = path.get()

            data = [value['name'] for value in snapshot.values()]
            self.prods = data

            self.headerlabel = overall.heading + "                             |                                " + self.user + "                             "

            # Load the values from the database
            self.thespinner = self.ids.thespinner
            self.thespinner.values = self.prods

            # call back for the selection in spinner object
            self.theids = {}

            self.thesumsList = []

            self.listofKeys = []

            self.listofKeys = self.productList.keys()

            # Load the values from the database
            self.payment_spinner = self.ids.payment_spinner
            self.payment_spinner.values = ['Cash', 'M-Pesa', 'Card']

            self.payment_Mode = ''

            self.paymenthold = self.ids.paymenthold
            self.paymenthold.values = ['Hold', 'Resume', 'Clear']

            self.loadinititalproducts()

        except Exception as exception:
            self.showAlert(str(exception))


    def loadinititalproducts(self):

        try:
            # Add Widgets to button
            target = self.ids.thebox
            target.clear_widgets()

            path = overall.dbs.reference("products")
            snapshot = path.get()

            if snapshot:

                for value in snapshot.values():
                    name = value['name']
                    code = value['code']
                    sellingprice = value['selling']

                    name = Button(text=str(name) + " " + str(code) + " " + str(sellingprice),
                                  size_hint_x=1, width=40, size_hint_y=None, height=30,
                                  on_release=lambda button: self.show_result(button.text.strip()))

                    # if value[9]:
                    #     image = value[9]
                    #     data = io.BytesIO(image)
                    #     img = CoreImage(data, ext="png").texture
                    #     widget = Image(source='a.jpg')
                    #     widget.texture = img
                    #     widget.size_hint_y = None
                    #     widget.size_hint_x = 1
                    #     target.add_widget(widget)
                    #
                    # target.add_widget(name)
                    # name = Label(text='\n\n\n\n',
                    #              size_hint_x=1, width=40, size_hint_y=None, height=30)
                    target.add_widget(name)

        except Exception as exception:
            self.showAlert(str(exception))


    def checkifadmin(self):
        try:
            AdminWindow.loadEverythingSec(self.parent.parent.parent.admin_widget)
            self.parent.parent.current = 'scrn_admin'
        except Exception as exception:
            self.showAlert(str(exception))


    def on_purchase_spinner_select(self, text):

        try:
            self.receivedSpinnerText = text.strip()
            # Get the other variables and add them to the database
            today = date.today()
            total_amount = self.final_Amount

            self.amountinput = self.ids.amountinput.text.strip()
            self.mpesacode = self.ids.mpesacode.text.strip()

            # Retrieve the productList
            numberofitems = len(self.productList)
            paymenttype = text.strip()

            # Item already exists, try and get the name of the text
            thetext = self.ids.thetotal.text.strip()
            # Split on colon
            thetext_splitted = thetext.split(":")
            # Get last value (strip() removes spaces)
            last_value = thetext_splitted[-1].strip()
            self.payment_Mode = self.receivedSpinnerText
            today = datetime.datetime.today()
            confirmationcode = "None"

            if paymenttype == 'M-Pesa' or paymenttype == 'Cash':
                if self.amountinput == '':
                    self.showAlert("Enter Client Cash")
                else:
                    if self.mpesacode == '' or self.mpesacode.isalnum() == False:
                        self.showAlert('Enter Confirmation Code')
                    else:

                        toPrintA = '{:>0} {:>10} {:>10}'.format("Item", "Qty", "Amt")
                        toPrintB = []

                        for key, values in self.productList.items():
                            toPrintB.append('{:>0} {:>10} {:>10}'.format(key, values[3], values[2]))

                        assin = '\n'.join(map(str, toPrintB))

                        output = toPrintA + "\n" + assin

                        hour = overall.now.hour
                        minute = overall.now.minute
                        second = overall.now.second

                        confirmationcode = self.mpesacode
                        datte = {}
                        datte["date"] = str(today.date())
                        datte["month"] = str(today.month)
                        datte["year"] = str(today.year)
                        datte["day"] = str(today.day)
                        datte["amount"] = str(last_value)
                        datte["number"] = str(numberofitems)
                        datte["payment"] = str(paymenttype)
                        datte["served"] = str(self.user)
                        datte["location"] = str(self.reallocation)
                        datte["customerpay"] = str(self.amountinput)
                        datte["balance"] = str(float(self.amountinput) - float(last_value))
                        datte["confirmationcode"] = confirmationcode
                        datte["products"] = str(output)

                        self.totaltoBePaid = last_value

                        if float(last_value) > 0:
                            self.ids.thebalance.text = str(float(self.amountinput) - float(last_value))

                        self.customerbalance = str(float(self.amountinput) - float(last_value))
                        self.customerpayed = str(self.amountinput)

                        self.finalvariables.append(str(float(self.amountinput) - float(last_value)))
                        self.finalvariables.append(self.customerpayed)

                        if any(self.productList) == False:
                            self.notify.add_widget(
                                Label(text='[color=#FF0000][b]Add Items First[/b][/color]', markup=True))
                            self.notify.open()
                            Clock.schedule_once(self.killswitch, 5)
                        else:
                            try:
                                overall.db.child("sales").child(confirmationcode).set(datte)
                            except:
                                self.showAlert("An error occured\nC.Code must be unique")
                            else:
                                self.showAlert("Operation was successful")

            else:
                self.showAlert("Currently Unavailable")

        except Exception as exception:
            self.showAlert(str(exception))



    def on_spinner_select(self, text):

        try:
            self.spinnertext = text.strip()

            # Add Widgets to button
            target = self.ids.thebox
            target.clear_widgets()

            if (self.spinnertext != 'Select'):

                path = overall.dbs.reference("mycharacter")
                snapshot = path.order_by_child('name').equal_to(text).get()

                for value in snapshot.values():
                    name = value['name']
                    code = value['code']
                    sellingprice = value['sellingprice']
                    name = Button(text=str(name) + " " + str(code) + " " + str(sellingprice),
                                  size_hint_x=1, width=40, size_hint_y=None, height=30,
                                  on_release=lambda button: self.show_result(button.text.strip()))

                    target.add_widget(name)
                    name = Label(text='\n\n\n\n',
                                 size_hint_x=1, width=40, size_hint_y=None, height=30)
                    target.add_widget(name)

        except Exception as exception:
            self.showAlert(str(exception))



    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def showAlert(self, message):
        self.notify.add_widget(Label(text='[color=#FF0000][b]' + message + '[/b][/color]', markup=True))
        self.notify.open()
        Clock.schedule_once(self.killswitch, 5)

    def searchforproduct(self):
        try:
            self.searchQuery = self.ids.qty_inp.text.strip()

            # Add Widgets to button
            target = self.ids.thebox
            target.clear_widgets()

            if self.searchQuery == '' or self.searchQuery.isalnum() == False:
                self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)

            else:

                ref = overall.dbs.reference('mycharacter').order_by_child('name').start_at(self.searchQuery.capitalize()).end_at(self.searchQuery.capitalize() + "\uf8ff") or overall.dbs.reference('mycharacter').order_by_child('name').start_at(self.searchQuery.capitalize()).end_at(self.searchQuery.capitalize() + "\uf8ff")
                row = ref.get()

                if not row:

                    ref = overall.dbs.reference('mycharacter').order_by_child('name').start_at(self.searchQuery).end_at(self.searchQuery + "\uf8ff") or overall.dbs.reference('mycharacter').order_by_child('name').start_at(self.searchQuery.capitalize()).end_at(self.searchQuery.capitalize() + "\uf8ff")
                    urow = ref.get()

                    if not urow == []:
                        self.showAlert("No results found")

                    else:
                        for value in urow.values():
                            name = value['name']
                            code = value['code']
                            sellingprice = value['sellingprice']
                            name = Button(text=str(name) + " " + str(code) + " " + str(sellingprice),
                                          size_hint_x=1, width=40, size_hint_y=None, height=30,
                                          on_release=lambda button: self.show_result(button.text.strip()))

                            target.add_widget(name)
                            name = Label(text='\n\n\n\n',
                                         size_hint_x=1, width=40, size_hint_y=None, height=30)
                            target.add_widget(name)
                else:
                    for value in row.values():
                        name = value['name']
                        code = value['code']
                        sellingprice = value['sellingprice']
                        name = Button(text=str(name) + " " + str(code) + " " + str(sellingprice),
                                      size_hint_x=1, width=40, size_hint_y=None, height=30,
                                      on_release=lambda button: self.show_result(button.text.strip()))

                        target.add_widget(name)
                        name = Label(text='\n\n\n\n',
                                     size_hint_x=1, width=40, size_hint_y=None, height=30)
                        target.add_widget(name)

        except Exception as exception:
            self.showAlert(str(exception))


    def show_result(self, x):
        try:
            resultString = x
            # split the text
            words = resultString.split()

            self.callit()

            current_Item_Name = words[0]
            current_Item_Code = words[1]
            current_Item_Price = words[2]

            self.ids.cur_product.text = current_Item_Name  # Set the name
            self.ids.cur_price.text = "KES: " + current_Item_Price

            target = self.ids.receipt_Preview
            # target.clear_widgets()

            # Validate this product firs

            path = overall.dbs.reference("mycharacter")
            snapshot = path.order_by_child('name').equal_to(current_Item_Name).get()

            if (snapshot):
                # Loop through the values
                present = None
                stock = None

                for value in snapshot.values():
                    present = value['available']
                    stock = value['stock']

                if (present == 'Available'):
                    if (stock == '' or stock == None or stock == '0'):
                        self.showAlert("Item out of stock")
                    else:

                        # Check if buttton i s already in the dict meaining it has been added
                        if current_Item_Name in self.productList:

                            # BEGINNING OF OPERATION ON STRING

                            # Dynamic ids is simply a storage list that keeps list of the IDS
                            # Item already exists, try and get the name of the text
                            thetext = self.dynamic_ids[current_Item_Name].text

                            # Split on colon
                            thetext_splitted = thetext.split(":")

                            # Get last value (strip() removes spaces)
                            last_value = thetext_splitted[-1].strip()

                            thenumber = 1

                            # Firest of all get the text from the box, if it is null user has not entered the numbher.
                            getText = self.ids.number.text
                            if (getText == ''):
                                thenumber = 1

                            else:
                                thenumber = int(self.ids.number.text)

                            words.insert(3, thenumber)

                            new_last_value = str(int(last_value) + thenumber)

                            # Create the new list, updated with the new value
                            thetext_splitted[-1] = new_last_value

                            # Recreate "thetext"
                            new_thetext = ":".join(thetext_splitted)

                            # END OF OPERATION ON STRING I CAN NOW VALIDATE THE STRING

                            # Loop through the values
                            if float(new_last_value) > float(stock):
                                self.showAlert("Unable to add..Only " + stock + " kg left\n")
                            else:

                                # UPdating visible text with the new text including new number which is new_thetext
                                self.dynamic_ids[current_Item_Name].text = new_thetext

                                # Activate the active product
                                self.activ_product = current_Item_Name

                                # Update Complete Total
                                self.complete_total = current_Item_Price
                                self.ids.thetotal.text = self.complete_total

                                self.ids.number.text = ''

                                # Adding to the product list array...am  now adding the new number
                                self.productList[current_Item_Name][3] = new_last_value

                                for item in self.listofKeys:
                                    thequantity = self.productList[item][3]
                                    thecash = self.productList[item][2]
                                    multiplied = float(thequantity) * float(thecash)
                                    self.thesumsList.append(multiplied)

                                self.ids.thetotal.text = "Total Payable: " + str(
                                    sum(float(entry[2]) * float(entry[3]) for entry in self.productList.values()))

                        else:

                            # Loop through the values
                            if float(1) > float(stock):
                                self.showAlert("Unable to add..Only " + stock + " kg left")
                            else:

                                crud_submit = LongpressButton(long_press_time=2, id=current_Item_Name,
                                                              text=current_Item_Name + "    Price:" + current_Item_Price + "     Qty: 1",
                                                              size_hint_x=1, size_hint_y=None, height=30,
                                                              on_long_press=lambda button: self.longPressed(
                                                                  current_Item_Name,
                                                                  button),
                                                              on_press=lambda button: self.make_active_toChangeStuff(
                                                                  button.text.strip()))

                                target.add_widget(crud_submit)

                                # Activate the active product
                                self.activ_product = current_Item_Name

                                # Update Complete Total
                                self.complete_total = float(self.complete_total) + float(current_Item_Price)
                                self.ids.thetotal.text = str(self.complete_total)

                                # Add the product to product List
                                self.productList[current_Item_Name] = words

                                self.theids[current_Item_Name] = current_Item_Name
                                self.dynamic_ids[current_Item_Name] = crud_submit
                                # Adding quantity to be 1 in position 3 or Array
                                self.productList[current_Item_Name].insert(3, 1)

                                for item in self.listofKeys:
                                    thequantity = self.productList[item][3]
                                    thecash = self.productList[item][2]
                                    multiplied = float(thequantity) * float(thecash)
                                    self.thesumsList.append(multiplied)

                                self.ids.thetotal.text = "Total Payable: " + str(
                                    sum(float(entry[2]) * float(entry[3]) for entry in self.productList.values()))


                elif (present == 'Unavailable'):
                    self.showAlert("Item not available for sale")
                else:
                    self.showAlert("Not available for sale")

            else:
                self.showAlert("Errror!! \nCould not find item")

        except Exception as exception:
                self.showAlert(str(exception))




    def change_quantity(self):

        try:
            # Get the text given
            added_qty = self.ids.number.text.strip()
            # Get the item in 1st position from name, ie code
            if (added_qty):
                code = self.productList.get(self.activ_product)[1]

                # Validate this product firs

                path = overall.dbs.reference("mycharacter")
                snapshot = path.order_by_child('code').equal_to(code).get()

                stock = None

                for value in snapshot.values():
                    stock = str(value['stock'])

                if (stock):

                    try:
                        # Loop through the values
                        if float(added_qty) > float(stock):
                            self.showAlert("Only " + stock + " items left")
                        else:

                            if (added_qty == ''):
                                self.notify.add_widget(
                                    Label(text='[color=#FF0000][b] Enter valid Input[/b][/color]', markup=True))
                                self.notify.open()
                                Clock.schedule_once(self.killswitch, 5)
                            else:

                                # First of all load all the data bevore picking the quantity using code
                                # Get the current price
                                # Go into words and get the this active item
                                theresut = self.productList.get(self.activ_product)

                                # It is a good thng I was refreshing the values
                                # Now I only need to first validate then find the quotient
                                # newTotal = self.complete_total * float(theresut[2])
                                # self.complete_total = newTotal

                                theresut[3] = added_qty

                                # Item already exists, try and get the name of the text
                                thetext = self.dynamic_ids[self.activ_product].text
                                # Split on colon
                                thetext_splitted = thetext.split(":")
                                # Get last value (strip() removes spaces)
                                last_value = thetext_splitted[-1].strip()
                                # Firest of all get the text from the box, if it is null user has not entered the numbher.
                                finalNewQuantiy = added_qty
                                # Create the new list, updated with the new value
                                thetext_splitted[-1] = finalNewQuantiy
                                # Recreate "thetext"
                                new_thetext = ":".join(thetext_splitted)
                                self.dynamic_ids[self.activ_product].text = new_thetext

                                # Activate the active product
                                self.activ_product = self.activ_product

                                # Update Complete Total
                                self.ids.thetotal.text = str(self.complete_total)
                                self.ids.number.text = ''

                                self.productList[self.activ_product][3] = finalNewQuantiy

                                for item in self.listofKeys:
                                    thequantity = self.productList[item][3]
                                    thecash = self.productList[item][2]
                                    multiplied = float(thequantity) * float(thecash)
                                    self.thesumsList.append(multiplied)

                                self.ids.thetotal.text = "Total Payable: " + str(
                                    sum(float(entry[2]) * float(entry[3]) for entry in self.productList.values()))

                    except Exception as exception:
                        self.showAlert(str(exception))

                else:
                    self.showAlert("Error 1 occured")

            else:
                self.showAlert("You have to fill all fields")

        except Exception as exception:
            self.showAlert(str(exception))


    def change_discount(self):
        try:
            added_discount = self.ids.discount.text.strip()
            self.ids.discount.text = ''
            if not added_discount:
                self.notify.add_widget(Label(text='[color=#FF0000][b] Enter valid Input[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:
                if self.productList:
                    for item in self.listofKeys:
                        thequantity = self.productList[item][3]
                        thecash = self.productList[item][2]

                        multiplied = float(thequantity) * float(thecash)
                        self.thesumsList.append(multiplied)
                        self.what = multiplied

                    self.ids.thetotal.text = "Total Payable: " + str(sum( float(entry[2]) * float(entry[3]) for entry in self.productList.values()) - (float(added_discount)))
                    self.final_Amount = sum( float(entry[2]) * float(entry[3]) for entry in self.productList.values()) - (float(added_discount))
                    self.showAlert("Discount Added")

                else:
                    self.showAlert("Add items first")


        except Exception as exception:
            self.showAlert(str(exception))

    def longPressed(self, itemId, button):

        try:
            # Now get the active product and get the total and remove the total
            active = self.activ_product

            # Get the total amount of active product
            retrieve = self.productList.get(active)
            amount = retrieve[2]
            self.complete_total = float(self.complete_total) - float(amount)

            # Remove the widget
            target = self.ids.receipt_Preview

            button.size_hint_y = None
            button.opacity = 0
            button.height = 0

            # Remove item from the dictionary as well
            self.productList.pop(active, None)

            for item in self.listofKeys:
                thequantity = self.productList[item][3]
                thecash = self.productList[item][2]
                multiplied = float(thequantity) * float(thecash)
                self.thesumsList.append(multiplied)

            self.ids.cur_price.text = "0.0"
            self.ids.cur_product.text = "Default Product"

            self.ids.thetotal.text = "Total Payable: " + str(
                sum(float(entry[2]) * float(entry[3]) for entry in self.productList.values()))
        except Exception as exception:
            self.showAlert(str(exception))




    def make_active_toChangeStuff(self, text):
        try:
            thenewList = text.split()
            thename = thenewList[0]

            # Loop through active products and make the selected product active
            resultantList = self.productList.get(thename)

            self.ids.cur_product.text = resultantList[0]  # Set the name
            self.ids.cur_price.text = "KES: " + resultantList[2]
            self.activ_product = thename
        except Exception as exception:
            self.showAlert(str(exception))



    def load_window(self):
        # New size
        size = (1100, 630)

        # Get the actual pos and knowing the old size calcu +late the new one
        top = Window.top * Window.size[1] / size[1]
        left = Window.left * Window.size[0] / size[0]

        # Change the size
        Window.size = size

        # Fixing pos
        Window.top = top
        Window.left = left

    def callit(self):
        pass

    def on_age(self, *args):
        self.str_age = "Age: {}".format(self.age)

    def clearWidgets(self):
        try:
            self.ids.receipt_Preview.clear_widgets()
            self.thesumsList.clear()
            self.complete_total = 0.00
            self.ids.cur_price.text = "0.0"
            self.ids.cur_product.text = "Default Product"
            self.ids.thetotal.text = "Total: 0.0"
            self.final_Amount = 0.0
            self.ids.thebalance.text = 'Bal: 0.0'
            self.ids.mpesacode.text = ''
            self.ids.amountinput.text = ''
            target = self.ids.thebox
            target.clear_widgets()
        except Exception as exception:
            self.showAlert(str(exception))


    def logout(self):
        try:
            target = self.ids.thebox
            target.clear_widgets()
            self.thesumsList.clear()
            self.complete_total = 0.00
            self.ids.cur_price.text = "0.0"
            self.ids.cur_product.text = "Default Product"
            self.ids.thetotal.text = "Total: 0.0"
            self.final_Amount = 0.0
            self.ids.thebalance.text = 'Bal: 0.0'
            self.ids.mpesacode.text = ''
            self.ids.amountinput.text = ''
            self.parent.parent.current = 'scrn_login'

        except Exception as exception:
            self.showAlert(str(exception))



    def getproductList(self):
        try:
            toPrintA = '{:>0} {:>10} {:>10}'.format("Item", "Qty", "Amt")
            toPrintB = []

            for key, values in self.productList.items():
                toPrintB.append('{:>0} {:>10} {:>10}'.format(key, values[3], values[2]))

            assin = '\n'.join(map(str, toPrintB))

            return toPrintA + "\n" + assin
        except Exception as exception:
            self.showAlert(str(exception))





    def print_output(self):

        try:
            if any(self.productList) == False:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Add Items to cart first[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.killswitch, 5)
            else:
                # Item already exists, try and get the name of the text
                thetext = self.ids.thetotal.text.strip()
                # Split on colon
                thetext_splitted = thetext.split(":")
                # Get last value (strip() removes spaces)
                last_value = thetext_splitted[-1].strip()

                if (self.payment_Mode == ''):
                    self.notify.add_widget(Label(text='[color=#FF0000][b] Enter Mode Of Pay[/b][/color]', markup=True))
                    self.notify.open()
                    Clock.schedule_once(self.killswitch, 5)

                else:
                    companyName = "Hilton Steel and Cement Center\nLimited"
                    paytype = self.payment_Mode
                    companyName = companyName + "\n\nSale Receipt\n\nOpp Golden Life Mall\nP.O BOX 3404-20100\nTEL: 0727441192\nMail: hiltonltd@yandex.com"
                    receiptNo = randint(1, 100000)
                    finalString = companyName + "\n\nReceipt No:" + str(receiptNo) + "\n\n" + self.getproductList() \
                                  + "\n____________________________\n" + "Total Due:        " + str(
                        self.totaltoBePaid) + "\n____________________________\n\n" + "Paid In:     " + paytype + "\n\n" + "Served By:       " + str(
                        self.user) + "\n" + "Payment:           " + str(
                        self.finalvariables[1]) + "\nBalance:            " + str(self.finalvariables[0]) + "\n" + str(
                        date.today().strftime("%b-%d-%Y")) + "\n\n\nWelcome Back"

                    for key, values in self.productList.items():

                        code = values[1]
                        quantity = values[3]

                        # Load its current number using the code first
                        # Validate this product firs
                        path = overall.dbs.reference("mycharacter")
                        snapshot = path.child(key).get()

                        if snapshot:

                            stock = snapshot['stock']
                            newstock = float(float(stock) - float(quantity))

                            datte = {}
                            datte["stock"] = newstock

                            overall.dbs.reference("mycharacter").child(key).update(datte)

                        else:
                            self.showAlert('Operation Incomplete, Code Error')

                    self.productList.clear()
                    self.customerbalance = ''
                    self.customerpayed = ''
                    self.finalvariables.clear()

                    self.clearWidgets()

                    # # A List containing the system printers
                    # all_printers = [printer[2] for printer in win32print.EnumPrinters(2)]
                    # # Ask the user to select a printer
                    # printer_num = int(
                    #     input("Choose a printer:\n" + "\n".join([f"{n} {p}" for n, p in enumerate(all_printers)]) + "\n"))
                    # # set the default printer
                    # win32print.SetDefaultPrinter(all_printers[printer_num])
                    # pdf_dir = "C:/Users/John/Desktop/PDF"
                    # for f in glob(pdf_dir, recursive=True):
                    #     win32api.ShellExecute(0, "print", f, None, ".", 0)
                    #
                    # input("press any key to exit")

                    # pdf = fpdf.FPDF(format='letter')
                    # pdf.add_page()
                    # pdf.set_xy(0, 0)
                    # pdf.set_font("Arial", size=12)
                    # pdf.write(5, finalString)
                    # pdf.ln()
                    # pdf.output("C:/CocabTechSolutionsPos/Sales/sample.pdf")
                    # webbrowser.open('C:/CocabTechSolutionsPos/Sales/sample.pdf')

                    with open(self.filename, "w") as outf:
                        outf.write(finalString)
                    os.startfile(self.filename, "print")

        except Exception as exception:
            self.showAlert(str(exception))


class PosApp(App):

    def build(self):
        return PosWindow()


if __name__ == "__main__":
    sa = PosApp()
    sa.run()