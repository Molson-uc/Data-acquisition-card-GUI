from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import MainPage
import SettingFileManager as sfm
import serial
import serial.tools.list_ports
import time


class MainPageApp(QtWidgets.QMainWindow, MainPage.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainPageApp, self).__init__(parent)
        self.setupUi(self)
        self.opnBtn.clicked.connect(self.open_port)
        self.portOpened = serial.Serial()
        self.buadrateList = ["9600", "115200", "19200", "4800", "2400"]
        self.brComboBox.addItems(self.buadrateList)
        self.clBtn.clicked.connect(self.close_port)
        self.fileManager = sfm.FileManager(
            "C:\\programing\\workspace\\workspacePython\\Data\\settings.json")
        self.keyWordCB.addItems(self.fileManager.get_settings_keys())
        self.factorFromJsonFileTB.setText(
            str(self.fileManager.load_setting_factor(
                self.keyWordCB.currentText())))
        self.keyWordCB.currentIndexChanged.connect(
            self.get_settings_key_selected)
        self.saveBtn.clicked.connect(self.save_factor)
        self.uploadBtn.clicked.connect(self.upload_settings)

    def get_from_settings_textBox(self):
        # print(self.factorFromJsonFileTB.toPlainText())
        return self.factorFromJsonFileTB.toPlainText()

    def save_factor(self):
        try:
            self.fileManager.change_setting_factor(
                self.keyWordCB.currentText(), float(
                    self.get_from_settings_textBox()))
        except ValueError:
            print("Could not convert data to an float")

    def get_settings_key_selected(self):
        self.factorFromJsonFileTB.setText(
            str(self.fileManager.load_setting_factor(
                self.keyWordCB.currentText())))
        return self.fileManager.load_setting_factor(
            self.keyWordCB.currentText())

    portsList = []

    def print_ports(self):
        ports = serial.tools.list_ports.comports()
        print(list(ports))

        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
            self.portsList.append(port)
            self.comboBox.addItem("{}: {} ".format(port, desc))

    def open_port(self):
        try:
            self.portOpened.baudrate = int(self.brComboBox.currentText())
        except ValueError as e:
            return e
        try:
            self.portOpened.port = self.portsList[self.comboBox.currentIndex()]
        except IndexError as e:
            return e
        self.portOpened.write_timeout = 1  # 1.0s
        self.portOpened.open()
        if(self.portOpened.is_open):
            self.opnBtn.setFlat(True)
            print("open port: " + self.portOpened.port)
            self.read_message_from_port()
        else:
            print("connection fail")
        # self.boardSettingTextBox.setText("pressed")
        print("press")

    def read_message_from_port(self):
        if (self.portOpened.in_waiting != 0):
            print(str(self.portOpened.readline()))
            self.boardSettingTextBox.setText("read")

    def close_port(self):
        self.portOpened.close()
        self.opnBtn.setFlat(False)

    def upload_settings(self):
        settingListToSend = [self.fileManager.get_all_factors()]
        self.portOpened.write(bytes(str(settingListToSend), encoding="UTF-8"))
        print('{}', str(settingListToSend))
        time.sleep(2)
        bytesToRead = self.portOpened.in_waiting
        print(bytesToRead)
        if (bytesToRead > 0):
            res = self.portOpened.read(bytesToRead)
            print(res)
            self.portOpened.reset_input_buffer()


def main():
    app = QApplication(sys.argv)
    form = MainPageApp()
    form.print_ports()
    form.show()
    app.exec_()


main()
