import requests
from bs4 import BeautifulSoup
import sys
import re
import json
import datetime

import subprocess

from PySide2 import QtWidgets, QtCore

# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
qt_app = QtWidgets.QApplication(sys.argv)


class CreateProject(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.data_dict = {}
        self.json_path = './data/vakantieveilingen.json'

        # UI Stuff
        self.main_layout = QtWidgets.QVBoxLayout()

        self.urlbox = QtWidgets.QHBoxLayout()
        self.url_label = QtWidgets.QLabel('url: ')
        self.url_input = QtWidgets.QLineEdit()
        self.urlbox.addWidget(self.url_label)
        self.urlbox.addWidget(self.url_input)

        self.max_price_box = QtWidgets.QHBoxLayout()
        self.max_price_label = QtWidgets.QLabel('max price: ')
        self.max_price_input = QtWidgets.QSpinBox()
        self.max_price_input.setRange(1, 999)
        self.max_price_box.addWidget(self.max_price_label)
        self.max_price_box.addWidget(self.max_price_input)

        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.button = QtWidgets.QPushButton('Add to basket')
        self.button.clicked.connect(self.confirmed)
        self.remove_button = QtWidgets.QPushButton('Remove from basket')
        self.remove_button.clicked.connect(self.remove)

        self.button_layout.addWidget(self.button)
        self.button_layout.addWidget(self.remove_button)

        self.main_layout.addLayout(self.urlbox)
        self.main_layout.addLayout(self.max_price_box)
        self.main_layout.addWidget(self.table_widget)
        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)
        self.setWindowTitle('Basket')

        self.init()

    def init(self):
        """
        This function is executed as soon as the application is started.

        The first thing that gets done is a subprocess is launched which will check the json every minute.
        When a url gets added, this json is updated for the scraper script to pick up in its next iteration.
        This link then gets checked every minute, until the product gets close to its deadline, then,
        we launch an individually created script for said product, which will launch a browser instance and
        checks against the deadline and price a lot more frequently.

        This function also takes care of the initial UI drawing,
        fetching items that are still left in the basket from last time.
        """
        # Launch scraping file
        python_path = '%s' % 'scraper_vakantieveilingen.py'
        cmd = 'python %s' % python_path
        subprocess.Popen(cmd, shell=False)

        try:
            with open(self.json_path) as in_file:
                self.data_dict = json.load(in_file)
        except FileNotFoundError:
            # Create json file
            with open(self.json_path, 'w') as in_file:
                json.dump({}, in_file)

        if len(self.data_dict) > 0:
            self.init_table_widget()
            self.table_widget.setRowCount(len(self.data_dict))

            for i, key in enumerate(self.data_dict.keys()):
                self.table_widget.setItem(i, 0, QtWidgets.QTableWidgetItem(self.data_dict[key]['title']))
                self.table_widget.setItem(i, 1, QtWidgets.QTableWidgetItem((self.data_dict[key]['deadline']).replace('T', ' ')))
                self.table_widget.setItem(i, 2, QtWidgets.QTableWidgetItem('€ ' + str(self.data_dict[key]['max_price'])))

                max_bid = int(float(self.data_dict[key]['max_price']) - float(self.data_dict[key]['fees']))
                fees_string = '€ %d, Highest Bid: € %d' % (int(round(float(self.data_dict[key]['fees']))), max_bid)
                self.table_widget.setItem(i, 3, QtWidgets.QTableWidgetItem(fees_string))

    def init_table_widget(self):
        self.table_widget.setColumnCount(4)

        self.table_widget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('tile'))
        self.table_widget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('deadline'))
        self.table_widget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('max price'))
        self.table_widget.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem('additional fees'))

        self.table_widget.setColumnWidth(0, 320)
        self.table_widget.setColumnWidth(1, 130)
        self.table_widget.setColumnWidth(2, 100)
        self.table_widget.setColumnWidth(3, 150)

    def remove(self):
        selected_indexes = self.table_widget.selectionModel().selectedIndexes()
        rows = []

        # Update dictionary
        for index in selected_indexes:
            row = index.row()
            rows.append(row)

        for key in self.data_dict.keys():
                # If the key still exists
                if self.data_dict.get(key, None):
                    # If it still has a title
                    if self.data_dict[key].get('title', None):
                        # If the title is the same as the clicked index's title
                        if self.data_dict[key]['title'] == self.table_widget.item(row, 0).text():
                            del self.data_dict[key]
                            break

        # Update UI
        deleted_rows = []
        for current_row in rows:
            for deleted_row in deleted_rows:
                if deleted_row < current_row:
                    current_row -= 1
            self.table_widget.removeRow(current_row)
            deleted_rows.append(current_row)

        # Update json file
        with open(self.json_path, 'w') as out_file:
            json.dump(self.data_dict, out_file)

    def confirmed(self):
        """
        This function gets ran when clicking the 'add to basket' button.

        It will take the given url, fetch the following data:
            - Expiry date
            - Title

        Afterwards, it will check for the json file storing the other items in your basket.
        A new key is created and the json file is updated.

        Lastly, the UI window is update
        """

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
        }

        # Fetch given url's data
        page = requests.get(self.url_input.text(), headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Isolate the bidding block
        block = str(soup.find(id='biddingBlock'))
        expires_begin = block[block.find('data-lot-expires="')+len('data-lot-expires="'):]

        # Fetch expiry date
        expires_date_str = str(expires_begin[:expires_begin.find('"')])
        # Fetch title
        title = str(soup.find(id='lotTitle').get_text())
        # Fetch extra costs
        paragraphs = soup.find_all('p')
        added_fees = 0.0
        for p in paragraphs:
            if '€' in str(p):
                # Add ,00 if there are no cents specified for uniform naming conventions in the price string
                prices_string = str(p).replace(',-', ',00')
                # Isolate the actual amount of the fee(s)
                prices_isolated = re.findall('(€\\s\\d,([0-9]+))', prices_string)
                for price in prices_isolated:
                    # Strip out the '€ ' and replace the comma by a point so the string can be converted to float
                    added_fees += float(str(price[0])[2:].replace(',', '.'))
                break
        max_bid = int(float(str(self.max_price_input.value())) - added_fees)

        # Check whether expiry date is in the current time zone GMT+2, only then proceed
        if '+02:00' in expires_date_str:
            # Fetch data, if file exists
            try:
                with open(self.json_path) as in_file:
                    data = json.load(in_file)
            except FileNotFoundError:
                # Initialize data dict to be empty
                data = {}

            # Append new item to the basket
            data.update(
                {
                    self.url_input.text(): {
                        'max_price': self.max_price_input.value(),
                        'fees': added_fees,
                        'max_bid': max_bid,
                        'deadline': expires_date_str.split('+')[0],
                        'title': title,
                    }
                }
            )

            # Update json
            with open(self.json_path, 'w') as out_file:
                json.dump(data, out_file)

            # Update 'global' dict
            self.data_dict = data

            # Update UI
            if self.table_widget.rowCount() == 0:
                # Init table widget
                self.init_table_widget()

            next_index = self.table_widget.rowCount() + 1
            self.table_widget.setRowCount(next_index)

            self.table_widget.setItem(next_index - 1, 0, QtWidgets.QTableWidgetItem(title))
            self.table_widget.setItem(next_index - 1, 1, QtWidgets.QTableWidgetItem(expires_date_str.split('+')[0].replace('T', ' ')))
            self.table_widget.setItem(next_index - 1, 2, QtWidgets.QTableWidgetItem('€ ' + str(self.max_price_input.value())))
            fees_string = '€ %d, Highest Bid: € %d' % (int(round(added_fees)), max_bid)
            self.table_widget.setItem(next_index - 1, 3, QtWidgets.QTableWidgetItem(fees_string))

            # Reset inputs
            self.url_input.setText('')
            self.max_price_input.setValue(1)
        else:
            print('wrong timezone')

    def run(self):
        # Show the window
        self.show()
        # Run the qt application
        qt_app.exec_()

    def closeEvent(self, *args, **kwargs):
        # Simulate crash so that the subprocess of the other script
        # also terminates when closing this window
        subprocess.Popen('^c ^c ^c ^c', shell=False)


# LAUNCH
CreateProject().run()
