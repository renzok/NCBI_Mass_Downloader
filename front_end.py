#!/usr/bin/python3
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import sys
import re

from PyQt4 import QtGui, QtCore
from back_end import Downloader

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):
        ##Create widgets
        #Download button
        dlbtn = QtGui.QPushButton("Download!", self)
        dlbtn.setToolTip('Click to start downloading...')
        dlbtn.clicked.connect(self.statusChange)
        dlbtn.clicked.connect(self.runOnClick)
        dlbtn.resize(dlbtn.sizeHint())

        #Quit button
        qbtn = QtGui.QPushButton("Quit", self)
        qbtn.setToolTip('Click exit the program...')
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())

        #Progress bar
        self.progbar = QtGui.QProgressBar(self)
        #self.pbar.setValue(self."X") Reminder!

        #Status bar
        self.statusBar().showMessage('Ready')

        #Title lable
        self.title = QtGui.QLabel(self)
        self.title.setText("NCBI mass sequence downloader")
        self.title.setFont(QtGui.QFont("Sans", 16, QtGui.QFont.Bold, True))

        #Email line edit and respective label
        self.email_line = QtGui.QLineEdit(self)
        self.email_line.setFixedWidth(220)
        self.email_label = QtGui.QLabel(self)
        self.email_label.setText("Email address:")

        #Databases to search and respective label
        self.databases = QtGui.QComboBox(self)
        self.databases.addItem("nucleotide")
        self.databases.addItem("nuccore")
        self.databases.addItem("nucgss")
        self.databases.addItem("nucest")
        self.databases.addItem("protein")
        self.databases.addItem("genome")
        self.databases.addItem("popset")
        self.databases_label = QtGui.QLabel(self)
        self.databases_label.setText("Database to search:")

        #Search query line and respective label
        self.search_query = QtGui.QLineEdit(self)
        self.search_query.setFixedWidth(300)
        self.search_query_label = QtGui.QLabel(self)
        self.search_query_label.setText("Search Query:")

        #File management
        self.save_file_label = QtGui.QLabel(self)
        self.save_file_label.setText("File Location:")

        self.save_file_line = QtGui.QLineEdit(self)
        self.save_file_line.setFixedWidth(300)

        self.save_file_button = QtGui.QPushButton("Find...", self)
        self.save_file_button.resize(dlbtn.sizeHint())
        self.save_file_button.setToolTip('Click to select file location...')
        self.save_file_button.clicked.connect(self.fileHandle)

        #self.savefile = QtGui.QFileDialog.getSaveFileName(self, "Save to file...", "", ".fasta")

        #Container widget
        self.main_widget = QtGui.QWidget(self)

        ##Set layout
        #Containers
        self.main_layout = QtGui.QVBoxLayout(self.main_widget)
        self.main_layout.sizeConstraint = QtGui.QLayout.SetDefaultConstraint

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        #Box for progress bar
        self.progressBox = QtGui.QHBoxLayout()
        self.progressBox.addWidget(self.progbar)

        #Box for search query
        self.queryBox = QtGui.QHBoxLayout()
        self.queryBox.addWidget(self.search_query_label)
        self.queryBox.addWidget(self.search_query)
        self.queryBox.addStretch(1)

        #Box for email and database
        self.email_database_box = QtGui.QHBoxLayout()
        self.email_database_box.addWidget(self.email_label)
        self.email_database_box.addWidget(self.email_line)

        self.email_database_box.addStretch(1)

        self.email_database_box.addWidget(self.databases_label)
        self.email_database_box.addWidget(self.databases)

        #Box for file management
        self.file_box = QtGui.QHBoxLayout()
        self.file_box.addWidget(self.save_file_label)
        self.file_box.addWidget(self.save_file_line)
        self.file_box.addWidget(self.save_file_button)

        #Box for Title
        self.titlebox = QtGui.QHBoxLayout()
        self.titlebox.addStretch(1)
        self.titlebox.addWidget(self.title)
        self.titlebox.addStretch(1)

        #Box for bottom buttons
        self.bottomBox = QtGui.QHBoxLayout()
        self.bottomBox.addStretch(1)
        self.bottomBox.addWidget(dlbtn)
        self.bottomBox.addWidget(qbtn)

        #Vertical stack
        self.main_layout.addLayout(self.titlebox)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.email_database_box)
        self.main_layout.addLayout(self.queryBox)
        self.main_layout.addLayout(self.file_box)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.progressBox)
        self.main_layout.addLayout(self.bottomBox)


        #MainWindow proprieties
        self.setWindowTitle('NCBI mass downloader')
        self.setWindowIcon(QtGui.QIcon('assets/Icon.png'))

        #Draw it!
        self.show()

    def statusChange(self):
        if self.statusBar().currentMessage() == "Ready":
            self.statusBar().showMessage("Downloading...")
        elif self.statusBar().currentMessage() == "Downloading...":
            self.statusBar().showMessage("Ready")

    def fileHandle(self):
        self.savefile = QtGui.QFileDialog.getSaveFileName(self, "Save to file...", "", "Fasta Files (*.fasta);;All Files (*)")
        self.save_file_line.setText(self.savefile)

    def runOnClick(self):
        self.email_address = self.email_line.displayText()
        self.database_to_search = self.databases.currentText()
        self.search_term = self.search_query.displayText()
        self.file_to_handle = self.save_file_line.displayText()

        #TODO: Implement argument detection. (trust no-one)

        Get_data = DownloaderGui(self.email_address, self.database_to_search, self.search_term, self.file_to_handle, 1)
        Get_data.max_seq.connect(self.progbar.setMaximum)
        Get_data.prog_data.connect(self.progbar.setValue)
        Get_data.runEverything()

        reply = self.DlFinished()
        if reply == 2097152:
            self.close()
        else:
            self.cleanForms()
            self.statusChange()

    def cleanForms(self):
        self.search_query.setText("")
        self.save_file_line.setText("")

    def DlFinished(self):
        #Create message box
        self.question = QtGui.QMessageBox(self)
        self.question.setIcon(QtGui.QMessageBox.Question)
        self.question.setText("Download finished sucessfully!")
        self.question.setInformativeText("Would you like to reset the froms and make another download or close the program?")
        self.question.setStandardButtons(QtGui.QMessageBox.Reset | QtGui.QMessageBox.Close)

        reply = self.question.exec_()

        return reply

class DownloaderGui(Downloader, QtCore.QThread):
    #Just add PyQt magic to Downloader() and create emmiters in constructor.
    prog_data = QtCore.pyqtSignal(int)
    max_seq = QtCore.pyqtSignal(int)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()