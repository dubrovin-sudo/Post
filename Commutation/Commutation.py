"""
Программа проверки коммутации
"""
import sys
import time
import random
import socket
import struct
import pyautogui
import operator
import statistics
import pandas as pd
from colorcet import fire
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from numpy import arange
from pythonping import ping
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QApplication


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1250, 731)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        """ Пользовательские глобальные переменные """
        self.IP_4201 = '192.168.10.100'  # переменная для ip PV-4201
        self.IP_4202 = '192.168.10.100'  # переменная для ip PV-4201
        self.PING = False  # дефолтная boolean переменная для пинга
        self.text = ""  # дефолтная переменная для текстовых данных
        self.db = 10  # дефолтная переменная для порогового значения

        # дефолтная команда 0х80 для перевода блока ЦОС в режим паузы
        # (её значение будет изменено пользователем в окне настроек)
        self.c_pause = '2e:00:80:00:00:00:00:14:00:00:00:00:6a:18:00:00:38:00:00:00:' \
                       '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:00:00:4c:80'
        # команда для работы только интерфейсной платы
        self.c_pause_1 = '2e:00:80:00:00:00:00:14:00:00:00:00:6a:18:00:00:38:00:00:00:' \
                         '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:00:00:4c:80'
        # команда для работы блока цос без БК и МУП
        self.c_pause_2 = '2e:00:80:00:00:00:00:14:00:00:00:00:6a:18:00:00:38:00:00:00:' \
                         '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:00:00:0c:80'
        # команда для работы блока цос вместе с БК и МУП
        self.c_pause_3 = '2e:00:80:00:00:00:00:10:00:00:00:00:6a:18:00:00:38:00:00:00:' \
                         '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:00:00:08:80'
        self.c_pause_1 = self.c_pause_1.split(':')
        self.c_pause_1 = ''.join(self.c_pause_1)  # преобразует байты в строку
        self.c_pause_2 = self.c_pause_2.split(':')
        self.c_pause_2 = ''.join(self.c_pause_2)  # преобразует байты в строку
        self.c_pause_3 = self.c_pause_3.split(':')
        self.c_pause_3 = ''.join(self.c_pause_3)  # преобразует байты в строку
        # команда 0х8А для перевода блока ЦОС в режим тестирования и смены
        # частоты
        self.c_freq = '26:00:8a:00:02:00:08:00:03:00:00:00:00:00:00:00:00:00:00:00:' \
                      '00:00:00:00:00:00:00:00:08:00:ff:0f:ff:00:01:00:01:00:36:00'
        self.c_freq = self.c_freq.split(':')
        self.c_freq = ''.join(self.c_freq)
        # дефолтная команда 0х80 для перевода блока ЦОС в технологический режим
        # (её значение будет изменено пользователем в окне настроек)
        self.c_techn = '2e:00:80:00:00:00:00:14:00:00:00:00:6a:18:00:00:38:00:00:00:' \
                       '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:05:00:4c:80'
        # команда для работы только интерфейсной платы
        self.c_techn_1 = '2e:00:80:00:00:00:00:14:00:00:00:00:6a:18:00:00:38:00:00:00:' \
                         '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:05:00:4c:80'
        # команда для работы блока цос без БК и МУП
        self.c_techn_2 = '2e:00:80:00:00:00:00:14:00:00:00:00:6a:18:00:00:38:00:00:00:' \
                         '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:05:00:0c:80'
        # команда для работы блока цос вместе с БК и МУП
        self.c_techn_3 = '2e:00:80:00:00:00:00:10:00:00:00:00:6a:18:00:00:38:00:00:00:' \
                         '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:05:00:08:80'
        self.c_techn_1 = self.c_techn_1.split(':')
        self.c_techn_1 = ''.join(self.c_techn_1)  # преобразует байты в строку
        self.c_techn_2 = self.c_techn_2.split(':')
        self.c_techn_2 = ''.join(self.c_techn_2)  # преобразует байты в строку
        self.c_techn_3 = self.c_techn_3.split(':')
        self.c_techn_3 = ''.join(self.c_techn_3)  # преобразует байты в строку
        #
        self.D2 = []
        self.D3 = []
        self.D4 = []
        self.D5 = []
        # инициализация словаря для хранения амплитуд кассет ЦОС
        self.plot = {
            'D2': self.D2,
            'D3': self.D3,
            'D4': self.D4,
            'D5': self.D5}
        # переменная с бинарным значением иконки кнопки настроек
        self.icon = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x1e" \
                    b"\x00\x00\x00\x1e\x08\x06\x00\x00\x00\x3b\x30\xae\xa2\x00\x00\x00\x01\x73\x52\x47" \
                    b"\x42\x00\xae\xce\x1c\xe9\x00\x00\x00\x04\x67\x41\x4d\x41\x00\x00\xb1\x8f\x0b\xfc" \
                    b"\x61\x05\x00\x00\x00\x09\x70\x48\x59\x73\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95" \
                    b"\x2b\x0e\x1b\x00\x00\x00\x41\x74\x45\x58\x74\x43\x6f\x6d\x6d\x65\x6e\x74\x00\x43" \
                    b"\x52\x45\x41\x54\x4f\x52\x3a\x20\x67\x64\x2d\x6a\x70\x65\x67\x20\x76\x31\x2e\x30" \
                    b"\x20\x28\x75\x73\x69\x6e\x67\x20\x49\x4a\x47\x20\x4a\x50\x45\x47\x20\x76\x36\x32" \
                    b"\x29\x2c\x20\x71\x75\x61\x6c\x69\x74\x79\x20\x3d\x20\x38\x35\x0a\xcc\xf0\xc6\xe1" \
                    b"\x00\x00\x03\x89\x49\x44\x41\x54\x48\x4b\x7d\x96\x4b\x4e\x2c\x31\x0c\x45\x0b\x9a" \
                    b"\xbf\x40\x02\x86\x2d\xc4\x9e\x40\xc0\x88\x55\x20\x3e\x62\x8a\x10\x30\xa1\xc7\xbd" \
                    b"\x0b\xf6\x81\xc4\x98\x7d\x80\xf8\x7f\xea\x71\x4c\x9f\xe0\xce\x2b\xb8\x52\x14\x97" \
                    b"\x63\x5f\xdf\x38\xa9\xea\x6e\xda\x2f\x7c\x7e\x7e\xb6\x6f\x6f\x6f\x98\x61\xbf\xbf" \
                    b"\xbf\x87\x2d\x78\xfe\xf8\xf8\x18\x3d\xb5\x61\x13\xa7\xef\xf5\xf5\x35\xe6\x1c\xc7" \
                    b"\x3a\x03\xc0\x9d\xe3\x89\x8b\xc2\x02\x47\x2e\x9a\x8b\xd5\x90\x14\x40\x9c\xf3\x58" \
                    b"\xcb\x22\x32\x14\xd4\xb8\xd3\x1a\x99\x38\xdb\x90\x5d\x5c\x5c\xb4\x47\x47\x47\xed" \
                    b"\xc1\xc1\x41\x7b\x79\x79\x19\x7e\x62\x5e\x5e\x5e\xc2\x06\x5d\x42\x04\x1d\x8a\x1d" \
                    b"\xe7\xe2\x06\x18\xdc\xa5\xba\xd7\xeb\xb5\x4d\xd3\xb4\x93\x93\x93\x31\x1e\x1e\x1e" \
                    b"\x46\x2b\xdf\xc8\x45\x32\x9e\x9f\x9f\x0b\x5f\xe3\xf9\x64\xe4\x1d\x82\x3a\x66\x62" \
                    b"\x62\xa2\x10\x60\x0b\xf2\xf0\x9b\x9f\x45\xe7\x0d\x81\x72\xc6\x59\x25\x09\x77\x77" \
                    b"\x77\xb1\xb3\x8d\x8d\x8d\x91\xf7\x1b\xec\x70\x6d\x6d\x2d\x6c\x72\x96\x97\x97\x63" \
                    b"\xf7\xe4\xc8\xb1\xb3\xb3\xd3\xce\xcc\xcc\x94\xae\xd5\x20\x36\x0a\x67\x35\xee\x0e" \
                    b"\x32\xc6\xd4\xd4\x54\xb1\xe7\xe7\xe7\x63\x56\xb5\x58\x5c\x5c\x2c\x6d\x67\xdd\x79" \
                    b"\x6e\x6e\x2e\xd6\xe1\x37\xc7\x63\x6d\x6c\x87\x33\x01\xb3\xb3\xb3\x91\x08\xf2\x85" \
                    b"\xc9\x2d\xcf\x3b\x21\xa7\xe6\x01\x70\xd0\x35\x5f\x27\x8b\x33\x37\x99\xc0\xa4\xdd" \
                    b"\xdd\xdd\x50\xcd\xb3\xc1\x20\xdb\xb9\x4b\xbf\x81\xc2\x1e\x55\x16\x84\x1d\xdb\x22" \
                    b"\x59\x02\x09\x51\xaa\x9d\xc5\xa1\xfe\xe9\xe9\x29\x6e\x68\xee\x86\xc4\x8a\x65\x20" \
                    b"\x1e\xe4\x4e\x19\x57\x2e\x97\x85\x99\x21\x47\x6d\xbe\xfe\xf8\x21\xc0\xcf\xe0\xf2" \
                    b"\x30\x73\xab\x39\xfb\x1a\x88\xcd\x37\x5e\x1e\x31\xf6\x3a\xe5\xf7\x19\x52\xc1\x0e" \
                    b"\x59\xa3\x0b\x0c\x44\x48\x44\x81\x9b\x9b\x9b\x28\xa2\x50\x7c\xc4\x10\x0b\x3f\x36" \
                    b"\x03\x98\x1b\xec\x8f\x8f\x8f\xe1\x94\x0c\x12\x0a\x67\x21\xfa\x6c\x7b\xdd\xbe\xdb" \
                    b"\xdb\xdb\x31\xb1\x0a\xf5\xae\x64\x2e\x50\x22\xcf\xce\xce\x22\x91\xd1\xef\xf7\x47" \
                    b"\xde\x1f\x31\xbc\x56\x40\xe5\x00\x1b\x42\x7d\xe4\xde\xdf\xdf\x87\x0d\xf0\xaf\xae" \
                    b"\xae\x86\x1f\xe1\xe7\xe7\xe7\xe1\x47\x7c\xb9\xd5\xfb\xfb\xfb\xa1\x50\x65\xf8\x2d" \
                    b"\xba\xb7\xb7\x17\xc9\xae\xe9\x37\x57\x5c\x5d\x5d\x95\x0b\xa5\x18\x67\xb8\x0f\x0f" \
                    b"\x0f\xc3\xc6\x17\x3b\xc6\x38\x3e\x3e\x0e\x72\x21\x29\x6b\x74\x40\x42\x20\x19\xc8" \
                    b"\x36\xb7\xdc\xb8\xff\x5a\xfb\xc5\xcd\x0f\x8b\x88\x4a\xec\x60\x38\x1c\x46\x3b\x18" \
                    b"\xeb\xeb\xeb\xb1\x28\x20\xf7\x52\x81\x2c\x0a\x58\x04\xf2\xa5\xa5\xa5\xf0\xdb\x95" \
                    b"\x95\x95\x95\xe0\x9c\x9e\x9e\x6e\x4f\x4f\x4f\xc3\x07\x4a\xab\x09\x46\x31\x97\x86" \
                    b"\xf3\xcc\x85\x00\xc9\x3e\x43\x9a\xd7\x00\x37\xba\xce\xe1\x93\x69\x9e\x42\x00\x76" \
                    b"\xe9\x6d\xbe\xa5\x80\x04\xc1\x8e\x10\x05\x51\x4d\x20\x88\xa7\xb0\x3c\xb6\x9d\xa2" \
                    b"\x99\xdb\x8f\x4e\x93\x15\x4a\xc4\x22\x6d\xb3\x1b\xfa\xaf\xaf\xaf\x83\xcc\xbb\x10" \
                    b"\xca\xbf\x6c\x46\xbe\x03\xc0\x35\x91\xeb\x60\xc7\x4a\x56\x64\x80\xaf\x4f\x16\x03" \
                    b"\x22\x69\x54\x8c\x5d\xfa\xd5\xc2\x8f\x50\xe2\xb1\x19\x70\xf0\xec\x1d\xc8\xdd\x88" \
                    b"\xc2\x16\x13\x9b\x9b\x9b\x91\x44\x40\xbd\xd6\x05\x88\xed\x4e\x06\xe2\xf8\x6d\x56" \
                    b"\x3c\xd0\x2e\xbd\xc0\x41\x32\x85\x38\xab\xdc\x26\x80\x08\x0a\xb8\x1b\x61\x41\x2e" \
                    b"\x17\x3b\xe2\xf3\x2a\x10\x0f\x0f\xfe\xdc\x09\x46\xb0\xff\xa6\x96\x44\xda\x89\xcd" \
                    b"\x19\x62\xe3\xb3\xb0\xf3\xc2\xc2\xc2\x58\xbc\xf7\x00\x1b\x41\xa0\xde\x75\x14\xf6" \
                    b"\x0c\x80\x64\x80\xc4\xad\xad\xad\xd1\xd3\x37\xf0\x51\x48\xf8\xaf\x44\x40\xba\xbd" \
                    b"\xbd\x1d\xbe\xcc\x5b\xa3\xfc\x03\x01\x79\xe7\xf8\x79\x76\x06\x5e\x30\xfe\xa1\x98" \
                    b"\xe7\xbb\x4b\x8c\x47\x01\x32\x6f\x17\xc6\xce\x38\xcf\x40\x3b\x77\x81\xf3\x62\x37" \
                    b"\x79\xb8\xb3\xcc\xd1\x75\x7c\x19\xf1\x1e\xd7\x05\x98\xff\x52\x7e\x72\x72\x12\x1f" \
                    b"\x7c\xbe\xbd\x83\xc1\x20\x7c\xc6\xe5\x82\x59\x70\x8d\xb1\x0f\x08\xb6\xed\xec\x2a" \
                    b"\xc8\xba\x7e\x66\x46\x7d\x0c\xa0\x2b\xb7\x46\x69\xb5\xb7\x0f\x90\x58\x0b\x02\xb5" \
                    b"\xbf\x0b\xb6\xfd\xef\x56\xb7\xed\x3f\x08\x56\x3b\x83\x25\x50\xf3\x50\x00\x00\x00" \
                    b"\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
        """                                        """
        self.gbA_1 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_1.setGeometry(QtCore.QRect(100, 170, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_1.setFont(font)
        self.gbA_1.setObjectName("gbA_1")
        self.label_5 = QtWidgets.QLabel(self.gbA_1)
        self.label_5.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.gbA_1)
        self.label_6.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.d2_1_1 = QtWidgets.QTextEdit(self.gbA_1)
        self.d2_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_1_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_1_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_1_1.setReadOnly(True)
        self.d2_1_1.setObjectName("d2_1_1")
        self.d2_1_2 = QtWidgets.QTextEdit(self.gbA_1)
        self.d2_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_1_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_1_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_1_2.setReadOnly(True)
        self.d2_1_2.setObjectName("d2_1_2")
        self.d3_1_1 = QtWidgets.QTextEdit(self.gbA_1)
        self.d3_1_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_1_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_1_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_1_1.setReadOnly(True)
        self.d3_1_1.setObjectName("d3_1_1")
        self.d3_1_2 = QtWidgets.QTextEdit(self.gbA_1)
        self.d3_1_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_1_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_1_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_1_2.setReadOnly(True)
        self.d3_1_2.setObjectName("d3_1_2")
        self.gbA_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_2.setGeometry(QtCore.QRect(170, 170, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_2.setFont(font)
        self.gbA_2.setObjectName("gbA_2")
        self.label_7 = QtWidgets.QLabel(self.gbA_2)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.gbA_2)
        self.label_8.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.d2_2_1 = QtWidgets.QTextEdit(self.gbA_2)
        self.d2_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_2_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_2_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_2_1.setReadOnly(True)
        self.d2_2_1.setObjectName("d2_2_1")
        self.d2_2_2 = QtWidgets.QTextEdit(self.gbA_2)
        self.d2_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_2_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_2_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_2_2.setReadOnly(True)
        self.d2_2_2.setObjectName("d2_2_2")
        self.d3_2_1 = QtWidgets.QTextEdit(self.gbA_2)
        self.d3_2_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_2_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_2_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_2_1.setReadOnly(True)
        self.d3_2_1.setObjectName("d3_2_1")
        self.d3_2_2 = QtWidgets.QTextEdit(self.gbA_2)
        self.d3_2_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_2_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_2_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_2_2.setReadOnly(True)
        self.d3_2_2.setObjectName("d3_2_2")
        self.gbA_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_3.setGeometry(QtCore.QRect(240, 170, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_3.setFont(font)
        self.gbA_3.setObjectName("gbA_3")
        self.label_9 = QtWidgets.QLabel(self.gbA_3)
        self.label_9.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.gbA_3)
        self.label_10.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.d2_3_1 = QtWidgets.QTextEdit(self.gbA_3)
        self.d2_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_3_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_3_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_3_1.setReadOnly(True)
        self.d2_3_1.setObjectName("d2_3_1")
        self.d2_3_2 = QtWidgets.QTextEdit(self.gbA_3)
        self.d2_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_3_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_3_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_3_2.setReadOnly(True)
        self.d2_3_2.setObjectName("d2_3_2")
        self.d3_3_1 = QtWidgets.QTextEdit(self.gbA_3)
        self.d3_3_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_3_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_3_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_3_1.setReadOnly(True)
        self.d3_3_1.setObjectName("d3_3_1")
        self.d3_3_2 = QtWidgets.QTextEdit(self.gbA_3)
        self.d3_3_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_3_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_3_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_3_2.setReadOnly(True)
        self.d3_3_2.setObjectName("d3_3_2")
        self.gbA_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_4.setGeometry(QtCore.QRect(310, 170, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_4.setFont(font)
        self.gbA_4.setObjectName("gbA_4")
        self.label_11 = QtWidgets.QLabel(self.gbA_4)
        self.label_11.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.gbA_4)
        self.label_12.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.d2_4_1 = QtWidgets.QTextEdit(self.gbA_4)
        self.d2_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_4_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_4_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_4_1.setReadOnly(True)
        self.d2_4_1.setObjectName("d2_4_1")
        self.d2_4_2 = QtWidgets.QTextEdit(self.gbA_4)
        self.d2_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_4_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_4_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_4_2.setReadOnly(True)
        self.d2_4_2.setObjectName("d2_4_2")
        self.d3_4_1 = QtWidgets.QTextEdit(self.gbA_4)
        self.d3_4_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_4_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_4_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_4_1.setReadOnly(True)
        self.d3_4_1.setObjectName("d3_4_1")
        self.d3_4_2 = QtWidgets.QTextEdit(self.gbA_4)
        self.d3_4_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_4_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_4_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_4_2.setReadOnly(True)
        self.d3_4_2.setObjectName("d3_4_2")
        self.gbA_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_5.setGeometry(QtCore.QRect(100, 280, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_5.setFont(font)
        self.gbA_5.setObjectName("gbA_5")
        self.label_13 = QtWidgets.QLabel(self.gbA_5)
        self.label_13.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.gbA_5)
        self.label_14.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.d2_5_1 = QtWidgets.QTextEdit(self.gbA_5)
        self.d2_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_5_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_5_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_5_1.setReadOnly(True)
        self.d2_5_1.setObjectName("d2_5_1")
        self.d2_5_2 = QtWidgets.QTextEdit(self.gbA_5)
        self.d2_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_5_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_5_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_5_2.setReadOnly(True)
        self.d2_5_2.setObjectName("d2_5_2")
        self.d3_5_1 = QtWidgets.QTextEdit(self.gbA_5)
        self.d3_5_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_5_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_5_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_5_1.setReadOnly(True)
        self.d3_5_1.setObjectName("d3_5_1")
        self.d3_5_2 = QtWidgets.QTextEdit(self.gbA_5)
        self.d3_5_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_5_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_5_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_5_2.setReadOnly(True)
        self.d3_5_2.setObjectName("d3_5_2")
        self.gbA_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_6.setGeometry(QtCore.QRect(170, 280, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_6.setFont(font)
        self.gbA_6.setObjectName("gbA_6")
        self.label_15 = QtWidgets.QLabel(self.gbA_6)
        self.label_15.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.gbA_6)
        self.label_16.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.d2_6_1 = QtWidgets.QTextEdit(self.gbA_6)
        self.d2_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_6_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_6_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_6_1.setReadOnly(True)
        self.d2_6_1.setObjectName("d2_6_1")
        self.d2_6_2 = QtWidgets.QTextEdit(self.gbA_6)
        self.d2_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_6_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_6_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_6_2.setReadOnly(True)
        self.d2_6_2.setObjectName("d2_6_2")
        self.d3_6_1 = QtWidgets.QTextEdit(self.gbA_6)
        self.d3_6_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_6_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_6_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_6_1.setReadOnly(True)
        self.d3_6_1.setObjectName("d3_6_1")
        self.d3_6_2 = QtWidgets.QTextEdit(self.gbA_6)
        self.d3_6_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_6_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_6_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_6_2.setReadOnly(True)
        self.d3_6_2.setObjectName("d3_6_2")
        self.gbA_7 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_7.setGeometry(QtCore.QRect(240, 280, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_7.setFont(font)
        self.gbA_7.setObjectName("gbA_7")
        self.label_17 = QtWidgets.QLabel(self.gbA_7)
        self.label_17.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.gbA_7)
        self.label_18.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.d2_7_1 = QtWidgets.QTextEdit(self.gbA_7)
        self.d2_7_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_7_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_7_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_7_1.setReadOnly(True)
        self.d2_7_1.setObjectName("d2_7_1")
        self.d2_7_2 = QtWidgets.QTextEdit(self.gbA_7)
        self.d2_7_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_7_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_7_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_7_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_7_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_7_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_7_2.setReadOnly(True)
        self.d2_7_2.setObjectName("d2_7_2")
        self.d3_7_1 = QtWidgets.QTextEdit(self.gbA_7)
        self.d3_7_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_7_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_7_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_7_1.setReadOnly(True)
        self.d3_7_1.setObjectName("d3_7_1")
        self.d3_7_2 = QtWidgets.QTextEdit(self.gbA_7)
        self.d3_7_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_7_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_7_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_7_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_7_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_7_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_7_2.setReadOnly(True)
        self.d3_7_2.setObjectName("d3_7_2")
        self.gbA_8 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_8.setGeometry(QtCore.QRect(310, 280, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_8.setFont(font)
        self.gbA_8.setObjectName("gbA_8")
        self.label_19 = QtWidgets.QLabel(self.gbA_8)
        self.label_19.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.gbA_8)
        self.label_20.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.d2_8_1 = QtWidgets.QTextEdit(self.gbA_8)
        self.d2_8_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_8_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_8_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_8_1.setReadOnly(True)
        self.d2_8_1.setObjectName("d2_8_1")
        self.d2_8_2 = QtWidgets.QTextEdit(self.gbA_8)
        self.d2_8_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_8_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_8_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_8_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_8_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_8_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_8_2.setReadOnly(True)
        self.d2_8_2.setObjectName("d2_8_2")
        self.d3_8_1 = QtWidgets.QTextEdit(self.gbA_8)
        self.d3_8_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_8_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_8_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_8_1.setReadOnly(True)
        self.d3_8_1.setObjectName("d3_8_1")
        self.d3_8_2 = QtWidgets.QTextEdit(self.gbA_8)
        self.d3_8_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_8_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_8_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_8_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_8_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_8_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_8_2.setReadOnly(True)
        self.d3_8_2.setObjectName("d3_8_2")
        self.gbA_9 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_9.setGeometry(QtCore.QRect(100, 390, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_9.setFont(font)
        self.gbA_9.setObjectName("gbA_9")
        self.label_21 = QtWidgets.QLabel(self.gbA_9)
        self.label_21.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.gbA_9)
        self.label_22.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.d2_9_1 = QtWidgets.QTextEdit(self.gbA_9)
        self.d2_9_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_9_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_9_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_9_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_9_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_9_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_9_1.setReadOnly(True)
        self.d2_9_1.setObjectName("d2_9_1")
        self.d2_9_2 = QtWidgets.QTextEdit(self.gbA_9)
        self.d2_9_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_9_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d2_9_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_9_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_9_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_9_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_9_2.setReadOnly(True)
        self.d2_9_2.setObjectName("d2_9_2")
        self.d3_9_1 = QtWidgets.QTextEdit(self.gbA_9)
        self.d3_9_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_9_1.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_9_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_9_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_9_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_9_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_9_1.setReadOnly(True)
        self.d3_9_1.setObjectName("d3_9_1")
        self.d3_9_2 = QtWidgets.QTextEdit(self.gbA_9)
        self.d3_9_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_9_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d3_9_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_9_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_9_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_9_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_9_2.setReadOnly(True)
        self.d3_9_2.setObjectName("d3_9_2")
        self.gbA_10 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_10.setGeometry(QtCore.QRect(170, 390, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_10.setFont(font)
        self.gbA_10.setObjectName("gbA_10")
        self.label_23 = QtWidgets.QLabel(self.gbA_10)
        self.label_23.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.gbA_10)
        self.label_24.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.d2_10_1 = QtWidgets.QTextEdit(self.gbA_10)
        self.d2_10_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_10_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d2_10_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_10_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_10_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_10_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_10_1.setReadOnly(True)
        self.d2_10_1.setObjectName("d2_10_1")
        self.d2_10_2 = QtWidgets.QTextEdit(self.gbA_10)
        self.d2_10_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_10_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d2_10_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_10_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_10_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_10_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_10_2.setReadOnly(True)
        self.d2_10_2.setObjectName("d2_10_2")
        self.d3_10_1 = QtWidgets.QTextEdit(self.gbA_10)
        self.d3_10_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_10_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d3_10_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_10_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_10_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_10_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_10_1.setReadOnly(True)
        self.d3_10_1.setObjectName("d3_10_1")
        self.d3_10_2 = QtWidgets.QTextEdit(self.gbA_10)
        self.d3_10_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_10_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d3_10_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_10_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_10_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_10_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_10_2.setReadOnly(True)
        self.d3_10_2.setObjectName("d3_10_2")
        self.gbA_11 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_11.setGeometry(QtCore.QRect(240, 390, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_11.setFont(font)
        self.gbA_11.setObjectName("gbA_11")
        self.label_25 = QtWidgets.QLabel(self.gbA_11)
        self.label_25.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.label_26 = QtWidgets.QLabel(self.gbA_11)
        self.label_26.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.d2_11_1 = QtWidgets.QTextEdit(self.gbA_11)
        self.d2_11_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_11_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d2_11_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_11_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_11_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_11_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_11_1.setReadOnly(True)
        self.d2_11_1.setObjectName("d2_11_1")
        self.d2_11_2 = QtWidgets.QTextEdit(self.gbA_11)
        self.d2_11_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_11_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d2_11_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_11_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_11_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_11_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_11_2.setReadOnly(True)
        self.d2_11_2.setObjectName("d2_11_2")
        self.d3_11_1 = QtWidgets.QTextEdit(self.gbA_11)
        self.d3_11_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_11_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d3_11_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_11_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_11_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_11_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_11_1.setReadOnly(True)
        self.d3_11_1.setObjectName("d3_11_1")
        self.d3_11_2 = QtWidgets.QTextEdit(self.gbA_11)
        self.d3_11_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_11_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d3_11_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_11_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_11_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_11_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_11_2.setReadOnly(True)
        self.d3_11_2.setObjectName("d3_11_2")
        self.gbA_12 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_12.setGeometry(QtCore.QRect(310, 390, 71, 101))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_12.setFont(font)
        self.gbA_12.setObjectName("gbA_12")
        self.label_27 = QtWidgets.QLabel(self.gbA_12)
        self.label_27.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.label_28 = QtWidgets.QLabel(self.gbA_12)
        self.label_28.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.d2_12_1 = QtWidgets.QTextEdit(self.gbA_12)
        self.d2_12_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d2_12_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d2_12_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_12_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_12_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_12_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_12_1.setReadOnly(True)
        self.d2_12_1.setObjectName("d2_12_1")
        self.d2_12_2 = QtWidgets.QTextEdit(self.gbA_12)
        self.d2_12_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d2_12_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d2_12_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d2_12_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d2_12_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_12_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d2_12_2.setReadOnly(True)
        self.d2_12_2.setObjectName("d2_12_2")
        self.d3_12_1 = QtWidgets.QTextEdit(self.gbA_12)
        self.d3_12_1.setGeometry(QtCore.QRect(10, 70, 21, 21))
        self.d3_12_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d3_12_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_12_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_12_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_12_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_12_1.setReadOnly(True)
        self.d3_12_1.setObjectName("d3_12_1")
        self.d3_12_2 = QtWidgets.QTextEdit(self.gbA_12)
        self.d3_12_2.setGeometry(QtCore.QRect(40, 70, 21, 21))
        self.d3_12_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d3_12_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d3_12_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d3_12_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_12_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d3_12_2.setReadOnly(True)
        self.d3_12_2.setObjectName("d3_12_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 210, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 240, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 530, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gbB_1 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_1.setGeometry(QtCore.QRect(400, 20, 281, 161))
        self.gbB_1.setObjectName("gbB_1")
        self.groupBox_7 = QtWidgets.QGroupBox(self.gbB_1)
        self.groupBox_7.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_7.setObjectName("groupBox_7")
        self.label_29 = QtWidgets.QLabel(self.groupBox_7)
        self.label_29.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.groupBox_7)
        self.label_30.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.d4_1_1_1 = QtWidgets.QTextEdit(self.groupBox_7)
        self.d4_1_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_1_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_1_1.setReadOnly(True)
        self.d4_1_1_1.setObjectName("d4_1_1_1")
        self.d4_1_1_2 = QtWidgets.QTextEdit(self.groupBox_7)
        self.d4_1_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_1_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_1_2.setReadOnly(True)
        self.d4_1_1_2.setObjectName("d4_1_1_2")
        self.groupBox_8 = QtWidgets.QGroupBox(self.gbB_1)
        self.groupBox_8.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_8.setObjectName("groupBox_8")
        self.label_33 = QtWidgets.QLabel(self.groupBox_8)
        self.label_33.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(self.groupBox_8)
        self.label_34.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.d4_1_5_1 = QtWidgets.QTextEdit(self.groupBox_8)
        self.d4_1_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_1_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_5_1.setReadOnly(True)
        self.d4_1_5_1.setObjectName("d4_1_5_1")
        self.d4_1_5_2 = QtWidgets.QTextEdit(self.groupBox_8)
        self.d4_1_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_1_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_5_2.setReadOnly(True)
        self.d4_1_5_2.setObjectName("d4_1_5_2")
        self.groupBox_9 = QtWidgets.QGroupBox(self.gbB_1)
        self.groupBox_9.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_9.setObjectName("groupBox_9")
        self.label_35 = QtWidgets.QLabel(self.groupBox_9)
        self.label_35.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_35.setFont(font)
        self.label_35.setObjectName("label_35")
        self.label_36 = QtWidgets.QLabel(self.groupBox_9)
        self.label_36.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.d4_1_2_1 = QtWidgets.QTextEdit(self.groupBox_9)
        self.d4_1_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_1_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_2_1.setReadOnly(True)
        self.d4_1_2_1.setObjectName("d4_1_2_1")
        self.d4_1_2_2 = QtWidgets.QTextEdit(self.groupBox_9)
        self.d4_1_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_1_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_2_2.setReadOnly(True)
        self.d4_1_2_2.setObjectName("d4_1_2_2")
        self.groupBox_10 = QtWidgets.QGroupBox(self.gbB_1)
        self.groupBox_10.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_10.setObjectName("groupBox_10")
        self.label_37 = QtWidgets.QLabel(self.groupBox_10)
        self.label_37.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.groupBox_10)
        self.label_38.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.d4_1_6_1 = QtWidgets.QTextEdit(self.groupBox_10)
        self.d4_1_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_1_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_6_1.setReadOnly(True)
        self.d4_1_6_1.setObjectName("d4_1_6_1")
        self.d4_1_6_2 = QtWidgets.QTextEdit(self.groupBox_10)
        self.d4_1_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_1_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_6_2.setReadOnly(True)
        self.d4_1_6_2.setObjectName("d4_1_6_2")
        self.groupBox_11 = QtWidgets.QGroupBox(self.gbB_1)
        self.groupBox_11.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_11.setObjectName("groupBox_11")
        self.label_39 = QtWidgets.QLabel(self.groupBox_11)
        self.label_39.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_39.setFont(font)
        self.label_39.setObjectName("label_39")
        self.label_40 = QtWidgets.QLabel(self.groupBox_11)
        self.label_40.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_40.setFont(font)
        self.label_40.setObjectName("label_40")
        self.d4_1_3_1 = QtWidgets.QTextEdit(self.groupBox_11)
        self.d4_1_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_1_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_3_1.setReadOnly(True)
        self.d4_1_3_1.setObjectName("d4_1_3_1")
        self.d4_1_3_2 = QtWidgets.QTextEdit(self.groupBox_11)
        self.d4_1_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_1_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_3_2.setReadOnly(True)
        self.d4_1_3_2.setObjectName("d4_1_3_2")
        self.groupBox_12 = QtWidgets.QGroupBox(self.gbB_1)
        self.groupBox_12.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_12.setObjectName("groupBox_12")
        self.label_42 = QtWidgets.QLabel(self.groupBox_12)
        self.label_42.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_42.setFont(font)
        self.label_42.setObjectName("label_42")
        self.d4_1_7_1 = QtWidgets.QTextEdit(self.groupBox_12)
        self.d4_1_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_1_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_7_1.setReadOnly(True)
        self.d4_1_7_1.setObjectName("d4_1_7_1")
        self.groupBox_13 = QtWidgets.QGroupBox(self.gbB_1)
        self.groupBox_13.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_13.setObjectName("groupBox_13")
        self.label_43 = QtWidgets.QLabel(self.groupBox_13)
        self.label_43.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_43.setFont(font)
        self.label_43.setObjectName("label_43")
        self.label_44 = QtWidgets.QLabel(self.groupBox_13)
        self.label_44.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_44.setFont(font)
        self.label_44.setObjectName("label_44")
        self.d4_1_4_1 = QtWidgets.QTextEdit(self.groupBox_13)
        self.d4_1_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_1_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_4_1.setReadOnly(True)
        self.d4_1_4_1.setObjectName("d4_1_4_1")
        self.d4_1_4_2 = QtWidgets.QTextEdit(self.groupBox_13)
        self.d4_1_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_1_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_4_2.setReadOnly(True)
        self.d4_1_4_2.setObjectName("d4_1_4_2")
        self.groupBox_14 = QtWidgets.QGroupBox(self.gbB_1)
        self.groupBox_14.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_14.setObjectName("groupBox_14")
        self.label_46 = QtWidgets.QLabel(self.groupBox_14)
        self.label_46.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_46.setFont(font)
        self.label_46.setObjectName("label_46")
        self.d4_1_8_1 = QtWidgets.QTextEdit(self.groupBox_14)
        self.d4_1_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_1_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_1_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_1_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_1_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_1_8_1.setReadOnly(True)
        self.d4_1_8_1.setObjectName("d4_1_8_1")
        self.gbB_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_3.setGeometry(QtCore.QRect(680, 20, 281, 161))
        self.gbB_3.setObjectName("gbB_3")
        self.groupBox_15 = QtWidgets.QGroupBox(self.gbB_3)
        self.groupBox_15.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_15.setObjectName("groupBox_15")
        self.label_47 = QtWidgets.QLabel(self.groupBox_15)
        self.label_47.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_47.setFont(font)
        self.label_47.setObjectName("label_47")
        self.label_48 = QtWidgets.QLabel(self.groupBox_15)
        self.label_48.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_48.setFont(font)
        self.label_48.setObjectName("label_48")
        self.d4_3_1_1 = QtWidgets.QTextEdit(self.groupBox_15)
        self.d4_3_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_3_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_1_1.setReadOnly(True)
        self.d4_3_1_1.setObjectName("d4_3_1_1")
        self.d4_3_1_2 = QtWidgets.QTextEdit(self.groupBox_15)
        self.d4_3_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_3_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_1_2.setReadOnly(True)
        self.d4_3_1_2.setObjectName("d4_3_1_2")
        self.groupBox_16 = QtWidgets.QGroupBox(self.gbB_3)
        self.groupBox_16.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_16.setObjectName("groupBox_16")
        self.label_49 = QtWidgets.QLabel(self.groupBox_16)
        self.label_49.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_49.setFont(font)
        self.label_49.setObjectName("label_49")
        self.label_50 = QtWidgets.QLabel(self.groupBox_16)
        self.label_50.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_50.setFont(font)
        self.label_50.setObjectName("label_50")
        self.d4_3_5_1 = QtWidgets.QTextEdit(self.groupBox_16)
        self.d4_3_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_3_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_5_1.setReadOnly(True)
        self.d4_3_5_1.setObjectName("d4_3_5_1")
        self.d4_3_5_2 = QtWidgets.QTextEdit(self.groupBox_16)
        self.d4_3_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_3_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_5_2.setReadOnly(True)
        self.d4_3_5_2.setObjectName("d4_3_5_2")
        self.groupBox_17 = QtWidgets.QGroupBox(self.gbB_3)
        self.groupBox_17.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_17.setObjectName("groupBox_17")
        self.label_51 = QtWidgets.QLabel(self.groupBox_17)
        self.label_51.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_51.setFont(font)
        self.label_51.setObjectName("label_51")
        self.label_52 = QtWidgets.QLabel(self.groupBox_17)
        self.label_52.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_52.setFont(font)
        self.label_52.setObjectName("label_52")
        self.d4_3_2_1 = QtWidgets.QTextEdit(self.groupBox_17)
        self.d4_3_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_3_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_2_1.setReadOnly(True)
        self.d4_3_2_1.setObjectName("d4_3_2_1")
        self.d4_3_2_2 = QtWidgets.QTextEdit(self.groupBox_17)
        self.d4_3_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_3_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_2_2.setReadOnly(True)
        self.d4_3_2_2.setObjectName("d4_3_2_2")
        self.groupBox_18 = QtWidgets.QGroupBox(self.gbB_3)
        self.groupBox_18.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_18.setObjectName("groupBox_18")
        self.label_53 = QtWidgets.QLabel(self.groupBox_18)
        self.label_53.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_53.setFont(font)
        self.label_53.setObjectName("label_53")
        self.label_54 = QtWidgets.QLabel(self.groupBox_18)
        self.label_54.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_54.setFont(font)
        self.label_54.setObjectName("label_54")
        self.d4_3_6_1 = QtWidgets.QTextEdit(self.groupBox_18)
        self.d4_3_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_3_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_6_1.setReadOnly(True)
        self.d4_3_6_1.setObjectName("d4_3_6_1")
        self.d4_3_6_2 = QtWidgets.QTextEdit(self.groupBox_18)
        self.d4_3_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_3_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_6_2.setReadOnly(True)
        self.d4_3_6_2.setObjectName("d4_3_6_2")
        self.groupBox_19 = QtWidgets.QGroupBox(self.gbB_3)
        self.groupBox_19.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_19.setObjectName("groupBox_19")
        self.label_55 = QtWidgets.QLabel(self.groupBox_19)
        self.label_55.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_55.setFont(font)
        self.label_55.setObjectName("label_55")
        self.label_56 = QtWidgets.QLabel(self.groupBox_19)
        self.label_56.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_56.setFont(font)
        self.label_56.setObjectName("label_56")
        self.d4_3_3_1 = QtWidgets.QTextEdit(self.groupBox_19)
        self.d4_3_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_3_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_3_1.setReadOnly(True)
        self.d4_3_3_1.setObjectName("d4_3_3_1")
        self.d4_3_3_2 = QtWidgets.QTextEdit(self.groupBox_19)
        self.d4_3_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_3_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_3_2.setReadOnly(True)
        self.d4_3_3_2.setObjectName("d4_3_3_2")
        self.groupBox_20 = QtWidgets.QGroupBox(self.gbB_3)
        self.groupBox_20.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_20.setObjectName("groupBox_20")
        self.label_58 = QtWidgets.QLabel(self.groupBox_20)
        self.label_58.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_58.setFont(font)
        self.label_58.setObjectName("label_58")
        self.d4_3_7_1 = QtWidgets.QTextEdit(self.groupBox_20)
        self.d4_3_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_3_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_7_1.setReadOnly(True)
        self.d4_3_7_1.setObjectName("d4_3_7_1")
        self.groupBox_21 = QtWidgets.QGroupBox(self.gbB_3)
        self.groupBox_21.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_21.setObjectName("groupBox_21")
        self.label_59 = QtWidgets.QLabel(self.groupBox_21)
        self.label_59.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_59.setFont(font)
        self.label_59.setObjectName("label_59")
        self.label_60 = QtWidgets.QLabel(self.groupBox_21)
        self.label_60.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_60.setFont(font)
        self.label_60.setObjectName("label_60")
        self.d4_3_4_1 = QtWidgets.QTextEdit(self.groupBox_21)
        self.d4_3_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_3_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_4_1.setReadOnly(True)
        self.d4_3_4_1.setObjectName("d4_3_4_1")
        self.d4_3_4_2 = QtWidgets.QTextEdit(self.groupBox_21)
        self.d4_3_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_3_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_4_2.setReadOnly(True)
        self.d4_3_4_2.setObjectName("d4_3_4_2")
        self.groupBox_22 = QtWidgets.QGroupBox(self.gbB_3)
        self.groupBox_22.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_22.setObjectName("groupBox_22")
        self.label_62 = QtWidgets.QLabel(self.groupBox_22)
        self.label_62.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_62.setFont(font)
        self.label_62.setObjectName("label_62")
        self.d4_3_8_1 = QtWidgets.QTextEdit(self.groupBox_22)
        self.d4_3_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_3_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_3_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_3_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_3_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_3_8_1.setReadOnly(True)
        self.d4_3_8_1.setObjectName("d4_3_8_1")
        self.gbB_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_5.setGeometry(QtCore.QRect(960, 20, 281, 161))
        self.gbB_5.setObjectName("gbB_5")
        self.groupBox_31 = QtWidgets.QGroupBox(self.gbB_5)
        self.groupBox_31.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_31.setObjectName("groupBox_31")
        self.label_79 = QtWidgets.QLabel(self.groupBox_31)
        self.label_79.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_79.setFont(font)
        self.label_79.setObjectName("label_79")
        self.label_80 = QtWidgets.QLabel(self.groupBox_31)
        self.label_80.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_80.setFont(font)
        self.label_80.setObjectName("label_80")
        self.d4_5_1_1 = QtWidgets.QTextEdit(self.groupBox_31)
        self.d4_5_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_5_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_1_1.setReadOnly(True)
        self.d4_5_1_1.setObjectName("d4_5_1_1")
        self.d4_5_1_2 = QtWidgets.QTextEdit(self.groupBox_31)
        self.d4_5_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_5_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_1_2.setReadOnly(True)
        self.d4_5_1_2.setObjectName("d4_5_1_2")
        self.groupBox_32 = QtWidgets.QGroupBox(self.gbB_5)
        self.groupBox_32.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_32.setObjectName("groupBox_32")
        self.label_81 = QtWidgets.QLabel(self.groupBox_32)
        self.label_81.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_81.setFont(font)
        self.label_81.setObjectName("label_81")
        self.label_82 = QtWidgets.QLabel(self.groupBox_32)
        self.label_82.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_82.setFont(font)
        self.label_82.setObjectName("label_82")
        self.d4_5_5_1 = QtWidgets.QTextEdit(self.groupBox_32)
        self.d4_5_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_5_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_5_1.setReadOnly(True)
        self.d4_5_5_1.setObjectName("d4_5_5_1")
        self.d4_5_5_2 = QtWidgets.QTextEdit(self.groupBox_32)
        self.d4_5_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_5_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_5_2.setReadOnly(True)
        self.d4_5_5_2.setObjectName("d4_5_5_2")
        self.groupBox_33 = QtWidgets.QGroupBox(self.gbB_5)
        self.groupBox_33.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_33.setObjectName("groupBox_33")
        self.label_83 = QtWidgets.QLabel(self.groupBox_33)
        self.label_83.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_83.setFont(font)
        self.label_83.setObjectName("label_83")
        self.label_84 = QtWidgets.QLabel(self.groupBox_33)
        self.label_84.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_84.setFont(font)
        self.label_84.setObjectName("label_84")
        self.d4_5_2_1 = QtWidgets.QTextEdit(self.groupBox_33)
        self.d4_5_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_5_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_2_1.setReadOnly(True)
        self.d4_5_2_1.setObjectName("d4_5_2_1")
        self.d4_5_2_2 = QtWidgets.QTextEdit(self.groupBox_33)
        self.d4_5_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_5_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_2_2.setReadOnly(True)
        self.d4_5_2_2.setObjectName("d4_5_2_2")
        self.groupBox_34 = QtWidgets.QGroupBox(self.gbB_5)
        self.groupBox_34.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_34.setObjectName("groupBox_34")
        self.label_85 = QtWidgets.QLabel(self.groupBox_34)
        self.label_85.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_85.setFont(font)
        self.label_85.setObjectName("label_85")
        self.label_86 = QtWidgets.QLabel(self.groupBox_34)
        self.label_86.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_86.setFont(font)
        self.label_86.setObjectName("label_86")
        self.d4_5_6_1 = QtWidgets.QTextEdit(self.groupBox_34)
        self.d4_5_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_5_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_6_1.setReadOnly(True)
        self.d4_5_6_1.setObjectName("d4_5_6_1")
        self.d4_5_6_2 = QtWidgets.QTextEdit(self.groupBox_34)
        self.d4_5_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_5_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_6_2.setReadOnly(True)
        self.d4_5_6_2.setObjectName("d4_5_6_2")
        self.groupBox_35 = QtWidgets.QGroupBox(self.gbB_5)
        self.groupBox_35.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_35.setObjectName("groupBox_35")
        self.label_87 = QtWidgets.QLabel(self.groupBox_35)
        self.label_87.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_87.setFont(font)
        self.label_87.setObjectName("label_87")
        self.label_88 = QtWidgets.QLabel(self.groupBox_35)
        self.label_88.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_88.setFont(font)
        self.label_88.setObjectName("label_88")
        self.d4_5_3_1 = QtWidgets.QTextEdit(self.groupBox_35)
        self.d4_5_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_5_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_3_1.setReadOnly(True)
        self.d4_5_3_1.setObjectName("d4_5_3_1")
        self.d4_5_3_2 = QtWidgets.QTextEdit(self.groupBox_35)
        self.d4_5_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_5_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_3_2.setReadOnly(True)
        self.d4_5_3_2.setObjectName("d4_5_3_2")
        self.groupBox_36 = QtWidgets.QGroupBox(self.gbB_5)
        self.groupBox_36.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_36.setObjectName("groupBox_36")
        self.label_90 = QtWidgets.QLabel(self.groupBox_36)
        self.label_90.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_90.setFont(font)
        self.label_90.setObjectName("label_90")
        self.d4_5_7_1 = QtWidgets.QTextEdit(self.groupBox_36)
        self.d4_5_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_5_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_7_1.setReadOnly(True)
        self.d4_5_7_1.setObjectName("d4_5_7_1")
        self.groupBox_37 = QtWidgets.QGroupBox(self.gbB_5)
        self.groupBox_37.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_37.setObjectName("groupBox_37")
        self.label_91 = QtWidgets.QLabel(self.groupBox_37)
        self.label_91.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_91.setFont(font)
        self.label_91.setObjectName("label_91")
        self.label_92 = QtWidgets.QLabel(self.groupBox_37)
        self.label_92.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_92.setFont(font)
        self.label_92.setObjectName("label_92")
        self.d4_5_4_1 = QtWidgets.QTextEdit(self.groupBox_37)
        self.d4_5_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_5_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_4_1.setReadOnly(True)
        self.d4_5_4_1.setObjectName("d4_5_4_1")
        self.d4_5_4_2 = QtWidgets.QTextEdit(self.groupBox_37)
        self.d4_5_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_5_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_4_2.setReadOnly(True)
        self.d4_5_4_2.setObjectName("d4_5_4_2")
        self.groupBox_38 = QtWidgets.QGroupBox(self.gbB_5)
        self.groupBox_38.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_38.setObjectName("groupBox_38")
        self.label_94 = QtWidgets.QLabel(self.groupBox_38)
        self.label_94.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_94.setFont(font)
        self.label_94.setObjectName("label_94")
        self.d4_5_8_1 = QtWidgets.QTextEdit(self.groupBox_38)
        self.d4_5_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_5_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_5_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_5_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_5_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_5_8_1.setReadOnly(True)
        self.d4_5_8_1.setObjectName("d4_5_8_1")
        self.gbB_7 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_7.setGeometry(QtCore.QRect(400, 180, 281, 161))
        self.gbB_7.setObjectName("gbB_7")
        self.groupBox_39 = QtWidgets.QGroupBox(self.gbB_7)
        self.groupBox_39.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_39.setObjectName("groupBox_39")
        self.label_95 = QtWidgets.QLabel(self.groupBox_39)
        self.label_95.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_95.setFont(font)
        self.label_95.setObjectName("label_95")
        self.label_96 = QtWidgets.QLabel(self.groupBox_39)
        self.label_96.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_96.setFont(font)
        self.label_96.setObjectName("label_96")
        self.d4_7_1_1 = QtWidgets.QTextEdit(self.groupBox_39)
        self.d4_7_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_7_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_1_1.setReadOnly(True)
        self.d4_7_1_1.setObjectName("d4_7_1_1")
        self.d4_7_1_2 = QtWidgets.QTextEdit(self.groupBox_39)
        self.d4_7_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_7_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_1_2.setReadOnly(True)
        self.d4_7_1_2.setObjectName("d4_7_1_2")
        self.groupBox_40 = QtWidgets.QGroupBox(self.gbB_7)
        self.groupBox_40.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_40.setObjectName("groupBox_40")
        self.label_97 = QtWidgets.QLabel(self.groupBox_40)
        self.label_97.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_97.setFont(font)
        self.label_97.setObjectName("label_97")
        self.label_98 = QtWidgets.QLabel(self.groupBox_40)
        self.label_98.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_98.setFont(font)
        self.label_98.setObjectName("label_98")
        self.d4_7_5_1 = QtWidgets.QTextEdit(self.groupBox_40)
        self.d4_7_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_7_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_5_1.setReadOnly(True)
        self.d4_7_5_1.setObjectName("d4_7_5_1")
        self.d4_7_5_2 = QtWidgets.QTextEdit(self.groupBox_40)
        self.d4_7_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_7_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_5_2.setReadOnly(True)
        self.d4_7_5_2.setObjectName("d4_7_5_2")
        self.groupBox_41 = QtWidgets.QGroupBox(self.gbB_7)
        self.groupBox_41.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_41.setObjectName("groupBox_41")
        self.label_99 = QtWidgets.QLabel(self.groupBox_41)
        self.label_99.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_99.setFont(font)
        self.label_99.setObjectName("label_99")
        self.label_100 = QtWidgets.QLabel(self.groupBox_41)
        self.label_100.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_100.setFont(font)
        self.label_100.setObjectName("label_100")
        self.d4_7_2_1 = QtWidgets.QTextEdit(self.groupBox_41)
        self.d4_7_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_7_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_2_1.setReadOnly(True)
        self.d4_7_2_1.setObjectName("d4_7_2_1")
        self.d4_7_2_2 = QtWidgets.QTextEdit(self.groupBox_41)
        self.d4_7_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_7_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_2_2.setReadOnly(True)
        self.d4_7_2_2.setObjectName("d4_7_2_2")
        self.groupBox_42 = QtWidgets.QGroupBox(self.gbB_7)
        self.groupBox_42.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_42.setObjectName("groupBox_42")
        self.label_101 = QtWidgets.QLabel(self.groupBox_42)
        self.label_101.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_101.setFont(font)
        self.label_101.setObjectName("label_101")
        self.label_102 = QtWidgets.QLabel(self.groupBox_42)
        self.label_102.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_102.setFont(font)
        self.label_102.setObjectName("label_102")
        self.d4_7_6_1 = QtWidgets.QTextEdit(self.groupBox_42)
        self.d4_7_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_7_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_6_1.setReadOnly(True)
        self.d4_7_6_1.setObjectName("d4_7_6_1")
        self.d4_7_6_2 = QtWidgets.QTextEdit(self.groupBox_42)
        self.d4_7_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_7_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_6_2.setReadOnly(True)
        self.d4_7_6_2.setObjectName("d4_7_6_2")
        self.groupBox_43 = QtWidgets.QGroupBox(self.gbB_7)
        self.groupBox_43.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_43.setObjectName("groupBox_43")
        self.label_103 = QtWidgets.QLabel(self.groupBox_43)
        self.label_103.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_103.setFont(font)
        self.label_103.setObjectName("label_103")
        self.label_104 = QtWidgets.QLabel(self.groupBox_43)
        self.label_104.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_104.setFont(font)
        self.label_104.setObjectName("label_104")
        self.d4_7_3_1 = QtWidgets.QTextEdit(self.groupBox_43)
        self.d4_7_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_7_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_3_1.setReadOnly(True)
        self.d4_7_3_1.setObjectName("d4_7_3_1")
        self.d4_7_3_2 = QtWidgets.QTextEdit(self.groupBox_43)
        self.d4_7_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_7_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_3_2.setReadOnly(True)
        self.d4_7_3_2.setObjectName("d4_7_3_2")
        self.groupBox_44 = QtWidgets.QGroupBox(self.gbB_7)
        self.groupBox_44.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_44.setObjectName("groupBox_44")
        self.label_106 = QtWidgets.QLabel(self.groupBox_44)
        self.label_106.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_106.setFont(font)
        self.label_106.setObjectName("label_106")
        self.d4_7_7_1 = QtWidgets.QTextEdit(self.groupBox_44)
        self.d4_7_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_7_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_7_1.setReadOnly(True)
        self.d4_7_7_1.setObjectName("d4_7_7_1")
        self.groupBox_45 = QtWidgets.QGroupBox(self.gbB_7)
        self.groupBox_45.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_45.setObjectName("groupBox_45")
        self.label_107 = QtWidgets.QLabel(self.groupBox_45)
        self.label_107.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_107.setFont(font)
        self.label_107.setObjectName("label_107")
        self.label_108 = QtWidgets.QLabel(self.groupBox_45)
        self.label_108.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_108.setFont(font)
        self.label_108.setObjectName("label_108")
        self.d4_7_4_1 = QtWidgets.QTextEdit(self.groupBox_45)
        self.d4_7_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_7_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_4_1.setReadOnly(True)
        self.d4_7_4_1.setObjectName("d4_7_4_1")
        self.d4_7_4_2 = QtWidgets.QTextEdit(self.groupBox_45)
        self.d4_7_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_7_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_4_2.setReadOnly(True)
        self.d4_7_4_2.setObjectName("d4_7_4_2")
        self.groupBox_46 = QtWidgets.QGroupBox(self.gbB_7)
        self.groupBox_46.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_46.setObjectName("groupBox_46")
        self.label_110 = QtWidgets.QLabel(self.groupBox_46)
        self.label_110.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_110.setFont(font)
        self.label_110.setObjectName("label_110")
        self.d4_7_8_1 = QtWidgets.QTextEdit(self.groupBox_46)
        self.d4_7_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_7_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_7_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_7_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_7_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_7_8_1.setReadOnly(True)
        self.d4_7_8_1.setObjectName("d4_7_8_1")
        self.gbB_9 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_9.setGeometry(QtCore.QRect(680, 180, 281, 161))
        self.gbB_9.setObjectName("gbB_9")
        self.groupBox_47 = QtWidgets.QGroupBox(self.gbB_9)
        self.groupBox_47.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_47.setObjectName("groupBox_47")
        self.label_111 = QtWidgets.QLabel(self.groupBox_47)
        self.label_111.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_111.setFont(font)
        self.label_111.setObjectName("label_111")
        self.label_112 = QtWidgets.QLabel(self.groupBox_47)
        self.label_112.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_112.setFont(font)
        self.label_112.setObjectName("label_112")
        self.d4_9_1_1 = QtWidgets.QTextEdit(self.groupBox_47)
        self.d4_9_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_9_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_1_1.setReadOnly(True)
        self.d4_9_1_1.setObjectName("d4_9_1_1")
        self.d4_9_1_2 = QtWidgets.QTextEdit(self.groupBox_47)
        self.d4_9_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_9_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_1_2.setReadOnly(True)
        self.d4_9_1_2.setObjectName("d4_9_1_2")
        self.groupBox_48 = QtWidgets.QGroupBox(self.gbB_9)
        self.groupBox_48.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_48.setObjectName("groupBox_48")
        self.label_113 = QtWidgets.QLabel(self.groupBox_48)
        self.label_113.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_113.setFont(font)
        self.label_113.setObjectName("label_113")
        self.label_114 = QtWidgets.QLabel(self.groupBox_48)
        self.label_114.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_114.setFont(font)
        self.label_114.setObjectName("label_114")
        self.d4_9_5_1 = QtWidgets.QTextEdit(self.groupBox_48)
        self.d4_9_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_9_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_5_1.setReadOnly(True)
        self.d4_9_5_1.setObjectName("d4_9_5_1")
        self.d4_9_5_2 = QtWidgets.QTextEdit(self.groupBox_48)
        self.d4_9_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_9_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_5_2.setReadOnly(True)
        self.d4_9_5_2.setObjectName("d4_9_5_2")
        self.groupBox_49 = QtWidgets.QGroupBox(self.gbB_9)
        self.groupBox_49.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_49.setObjectName("groupBox_49")
        self.label_115 = QtWidgets.QLabel(self.groupBox_49)
        self.label_115.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_115.setFont(font)
        self.label_115.setObjectName("label_115")
        self.label_116 = QtWidgets.QLabel(self.groupBox_49)
        self.label_116.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_116.setFont(font)
        self.label_116.setObjectName("label_116")
        self.d4_9_2_1 = QtWidgets.QTextEdit(self.groupBox_49)
        self.d4_9_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_9_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_2_1.setReadOnly(True)
        self.d4_9_2_1.setObjectName("d4_9_2_1")
        self.d4_9_2_2 = QtWidgets.QTextEdit(self.groupBox_49)
        self.d4_9_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_9_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_2_2.setReadOnly(True)
        self.d4_9_2_2.setObjectName("d4_9_2_2")
        self.groupBox_50 = QtWidgets.QGroupBox(self.gbB_9)
        self.groupBox_50.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_50.setObjectName("groupBox_50")
        self.label_117 = QtWidgets.QLabel(self.groupBox_50)
        self.label_117.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_117.setFont(font)
        self.label_117.setObjectName("label_117")
        self.label_118 = QtWidgets.QLabel(self.groupBox_50)
        self.label_118.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_118.setFont(font)
        self.label_118.setObjectName("label_118")
        self.d4_9_6_1 = QtWidgets.QTextEdit(self.groupBox_50)
        self.d4_9_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_9_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_6_1.setReadOnly(True)
        self.d4_9_6_1.setObjectName("d4_9_6_1")
        self.d4_9_6_2 = QtWidgets.QTextEdit(self.groupBox_50)
        self.d4_9_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_9_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_6_2.setReadOnly(True)
        self.d4_9_6_2.setObjectName("d4_9_6_2")
        self.groupBox_51 = QtWidgets.QGroupBox(self.gbB_9)
        self.groupBox_51.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_51.setObjectName("groupBox_51")
        self.label_119 = QtWidgets.QLabel(self.groupBox_51)
        self.label_119.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_119.setFont(font)
        self.label_119.setObjectName("label_119")
        self.label_120 = QtWidgets.QLabel(self.groupBox_51)
        self.label_120.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_120.setFont(font)
        self.label_120.setObjectName("label_120")
        self.d4_9_3_1 = QtWidgets.QTextEdit(self.groupBox_51)
        self.d4_9_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_9_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_3_1.setReadOnly(True)
        self.d4_9_3_1.setObjectName("d4_9_3_1")
        self.d4_9_3_2 = QtWidgets.QTextEdit(self.groupBox_51)
        self.d4_9_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_9_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_3_2.setReadOnly(True)
        self.d4_9_3_2.setObjectName("d4_9_3_2")
        self.groupBox_52 = QtWidgets.QGroupBox(self.gbB_9)
        self.groupBox_52.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_52.setObjectName("groupBox_52")
        self.label_122 = QtWidgets.QLabel(self.groupBox_52)
        self.label_122.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_122.setFont(font)
        self.label_122.setObjectName("label_122")
        self.d4_9_7_1 = QtWidgets.QTextEdit(self.groupBox_52)
        self.d4_9_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_9_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_7_1.setReadOnly(True)
        self.d4_9_7_1.setObjectName("d4_9_7_1")
        self.groupBox_53 = QtWidgets.QGroupBox(self.gbB_9)
        self.groupBox_53.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_53.setObjectName("groupBox_53")
        self.label_123 = QtWidgets.QLabel(self.groupBox_53)
        self.label_123.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_123.setFont(font)
        self.label_123.setObjectName("label_123")
        self.label_124 = QtWidgets.QLabel(self.groupBox_53)
        self.label_124.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_124.setFont(font)
        self.label_124.setObjectName("label_124")
        self.d4_9_4_1 = QtWidgets.QTextEdit(self.groupBox_53)
        self.d4_9_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_9_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_4_1.setReadOnly(True)
        self.d4_9_4_1.setObjectName("d4_9_4_1")
        self.d4_9_4_2 = QtWidgets.QTextEdit(self.groupBox_53)
        self.d4_9_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_9_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_4_2.setReadOnly(True)
        self.d4_9_4_2.setObjectName("d4_9_4_2")
        self.groupBox_54 = QtWidgets.QGroupBox(self.gbB_9)
        self.groupBox_54.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_54.setObjectName("groupBox_54")
        self.label_126 = QtWidgets.QLabel(self.groupBox_54)
        self.label_126.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_126.setFont(font)
        self.label_126.setObjectName("label_126")
        self.d4_9_8_1 = QtWidgets.QTextEdit(self.groupBox_54)
        self.d4_9_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_9_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_9_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_9_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_9_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_9_8_1.setReadOnly(True)
        self.d4_9_8_1.setObjectName("d4_9_8_1")
        self.gbB_11 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_11.setGeometry(QtCore.QRect(960, 180, 281, 161))
        self.gbB_11.setObjectName("gbB_11")
        self.groupBox_55 = QtWidgets.QGroupBox(self.gbB_11)
        self.groupBox_55.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_55.setObjectName("groupBox_55")
        self.label_127 = QtWidgets.QLabel(self.groupBox_55)
        self.label_127.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_127.setFont(font)
        self.label_127.setObjectName("label_127")
        self.label_128 = QtWidgets.QLabel(self.groupBox_55)
        self.label_128.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_128.setFont(font)
        self.label_128.setObjectName("label_128")
        self.d4_11_1_1 = QtWidgets.QTextEdit(self.groupBox_55)
        self.d4_11_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_11_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_1_1.setReadOnly(True)
        self.d4_11_1_1.setObjectName("d4_11_1_1")
        self.d4_11_1_2 = QtWidgets.QTextEdit(self.groupBox_55)
        self.d4_11_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_11_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_1_2.setReadOnly(True)
        self.d4_11_1_2.setObjectName("d4_11_1_2")
        self.groupBox_56 = QtWidgets.QGroupBox(self.gbB_11)
        self.groupBox_56.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_56.setObjectName("groupBox_56")
        self.label_129 = QtWidgets.QLabel(self.groupBox_56)
        self.label_129.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_129.setFont(font)
        self.label_129.setObjectName("label_129")
        self.label_130 = QtWidgets.QLabel(self.groupBox_56)
        self.label_130.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_130.setFont(font)
        self.label_130.setObjectName("label_130")
        self.d4_11_5_1 = QtWidgets.QTextEdit(self.groupBox_56)
        self.d4_11_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_11_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_5_1.setReadOnly(True)
        self.d4_11_5_1.setObjectName("d4_11_5_1")
        self.d4_11_5_2 = QtWidgets.QTextEdit(self.groupBox_56)
        self.d4_11_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_11_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_5_2.setReadOnly(True)
        self.d4_11_5_2.setObjectName("d4_11_5_2")
        self.groupBox_57 = QtWidgets.QGroupBox(self.gbB_11)
        self.groupBox_57.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_57.setObjectName("groupBox_57")
        self.label_131 = QtWidgets.QLabel(self.groupBox_57)
        self.label_131.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_131.setFont(font)
        self.label_131.setObjectName("label_131")
        self.label_132 = QtWidgets.QLabel(self.groupBox_57)
        self.label_132.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_132.setFont(font)
        self.label_132.setObjectName("label_132")
        self.d4_11_2_1 = QtWidgets.QTextEdit(self.groupBox_57)
        self.d4_11_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_11_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_2_1.setReadOnly(True)
        self.d4_11_2_1.setObjectName("d4_11_2_1")
        self.d4_11_2_2 = QtWidgets.QTextEdit(self.groupBox_57)
        self.d4_11_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_11_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_2_2.setReadOnly(True)
        self.d4_11_2_2.setObjectName("d4_11_2_2")
        self.groupBox_58 = QtWidgets.QGroupBox(self.gbB_11)
        self.groupBox_58.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_58.setObjectName("groupBox_58")
        self.label_133 = QtWidgets.QLabel(self.groupBox_58)
        self.label_133.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_133.setFont(font)
        self.label_133.setObjectName("label_133")
        self.label_134 = QtWidgets.QLabel(self.groupBox_58)
        self.label_134.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_134.setFont(font)
        self.label_134.setObjectName("label_134")
        self.d4_11_6_1 = QtWidgets.QTextEdit(self.groupBox_58)
        self.d4_11_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_11_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_6_1.setReadOnly(True)
        self.d4_11_6_1.setObjectName("d4_11_6_1")
        self.d4_11_6_2 = QtWidgets.QTextEdit(self.groupBox_58)
        self.d4_11_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_11_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_6_2.setReadOnly(True)
        self.d4_11_6_2.setObjectName("d4_11_6_2")
        self.groupBox_59 = QtWidgets.QGroupBox(self.gbB_11)
        self.groupBox_59.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_59.setObjectName("groupBox_59")
        self.label_135 = QtWidgets.QLabel(self.groupBox_59)
        self.label_135.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_135.setFont(font)
        self.label_135.setObjectName("label_135")
        self.label_136 = QtWidgets.QLabel(self.groupBox_59)
        self.label_136.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_136.setFont(font)
        self.label_136.setObjectName("label_136")
        self.d4_11_3_1 = QtWidgets.QTextEdit(self.groupBox_59)
        self.d4_11_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_11_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_3_1.setReadOnly(True)
        self.d4_11_3_1.setObjectName("d4_11_3_1")
        self.d4_11_3_2 = QtWidgets.QTextEdit(self.groupBox_59)
        self.d4_11_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_11_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_3_2.setReadOnly(True)
        self.d4_11_3_2.setObjectName("d4_11_3_2")
        self.groupBox_60 = QtWidgets.QGroupBox(self.gbB_11)
        self.groupBox_60.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_60.setObjectName("groupBox_60")
        self.label_138 = QtWidgets.QLabel(self.groupBox_60)
        self.label_138.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_138.setFont(font)
        self.label_138.setObjectName("label_138")
        self.d4_11_7_1 = QtWidgets.QTextEdit(self.groupBox_60)
        self.d4_11_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_11_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_7_1.setReadOnly(True)
        self.d4_11_7_1.setObjectName("d4_11_7_1")
        self.groupBox_61 = QtWidgets.QGroupBox(self.gbB_11)
        self.groupBox_61.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_61.setObjectName("groupBox_61")
        self.label_139 = QtWidgets.QLabel(self.groupBox_61)
        self.label_139.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_139.setFont(font)
        self.label_139.setObjectName("label_139")
        self.label_140 = QtWidgets.QLabel(self.groupBox_61)
        self.label_140.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_140.setFont(font)
        self.label_140.setObjectName("label_140")
        self.d4_11_4_1 = QtWidgets.QTextEdit(self.groupBox_61)
        self.d4_11_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d4_11_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_4_1.setReadOnly(True)
        self.d4_11_4_1.setObjectName("d4_11_4_1")
        self.d4_11_4_2 = QtWidgets.QTextEdit(self.groupBox_61)
        self.d4_11_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d4_11_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_4_2.setReadOnly(True)
        self.d4_11_4_2.setObjectName("d4_11_4_2")
        self.groupBox_62 = QtWidgets.QGroupBox(self.gbB_11)
        self.groupBox_62.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_62.setObjectName("groupBox_62")
        self.label_142 = QtWidgets.QLabel(self.groupBox_62)
        self.label_142.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_142.setFont(font)
        self.label_142.setObjectName("label_142")
        self.d4_11_8_1 = QtWidgets.QTextEdit(self.groupBox_62)
        self.d4_11_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d4_11_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d4_11_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d4_11_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d4_11_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d4_11_8_1.setReadOnly(True)
        self.d4_11_8_1.setObjectName("d4_11_8_1")
        self.label_143 = QtWidgets.QLabel(self.centralwidget)
        self.label_143.setGeometry(QtCore.QRect(400, 0, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_143.setFont(font)
        self.label_143.setObjectName("label_143")
        self.gbB_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_2.setGeometry(QtCore.QRect(400, 370, 281, 161))
        self.gbB_2.setObjectName("gbB_2")
        self.groupBox_64 = QtWidgets.QGroupBox(self.gbB_2)
        self.groupBox_64.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_64.setObjectName("groupBox_64")
        self.label_144 = QtWidgets.QLabel(self.groupBox_64)
        self.label_144.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_144.setFont(font)
        self.label_144.setObjectName("label_144")
        self.label_145 = QtWidgets.QLabel(self.groupBox_64)
        self.label_145.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_145.setFont(font)
        self.label_145.setObjectName("label_145")
        self.d5_2_1_1 = QtWidgets.QTextEdit(self.groupBox_64)
        self.d5_2_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_2_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_1_1.setReadOnly(True)
        self.d5_2_1_1.setObjectName("d5_2_1_1")
        self.d5_2_1_2 = QtWidgets.QTextEdit(self.groupBox_64)
        self.d5_2_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_2_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_1_2.setReadOnly(True)
        self.d5_2_1_2.setObjectName("d5_2_1_2")
        self.groupBox_65 = QtWidgets.QGroupBox(self.gbB_2)
        self.groupBox_65.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_65.setObjectName("groupBox_65")
        self.label_146 = QtWidgets.QLabel(self.groupBox_65)
        self.label_146.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_146.setFont(font)
        self.label_146.setObjectName("label_146")
        self.label_147 = QtWidgets.QLabel(self.groupBox_65)
        self.label_147.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_147.setFont(font)
        self.label_147.setObjectName("label_147")
        self.d5_2_5_1 = QtWidgets.QTextEdit(self.groupBox_65)
        self.d5_2_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_2_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_5_1.setReadOnly(True)
        self.d5_2_5_1.setObjectName("d5_2_5_1")
        self.d5_2_5_2 = QtWidgets.QTextEdit(self.groupBox_65)
        self.d5_2_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_2_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_5_2.setReadOnly(True)
        self.d5_2_5_2.setObjectName("d5_2_5_2")
        self.groupBox_66 = QtWidgets.QGroupBox(self.gbB_2)
        self.groupBox_66.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_66.setObjectName("groupBox_66")
        self.label_148 = QtWidgets.QLabel(self.groupBox_66)
        self.label_148.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_148.setFont(font)
        self.label_148.setObjectName("label_148")
        self.label_149 = QtWidgets.QLabel(self.groupBox_66)
        self.label_149.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_149.setFont(font)
        self.label_149.setObjectName("label_149")
        self.d5_2_2_1 = QtWidgets.QTextEdit(self.groupBox_66)
        self.d5_2_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_2_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_2_1.setReadOnly(True)
        self.d5_2_2_1.setObjectName("d5_2_2_1")
        self.d5_2_2_2 = QtWidgets.QTextEdit(self.groupBox_66)
        self.d5_2_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_2_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_2_2.setReadOnly(True)
        self.d5_2_2_2.setObjectName("d5_2_2_2")
        self.groupBox_67 = QtWidgets.QGroupBox(self.gbB_2)
        self.groupBox_67.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_67.setObjectName("groupBox_67")
        self.label_150 = QtWidgets.QLabel(self.groupBox_67)
        self.label_150.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_150.setFont(font)
        self.label_150.setObjectName("label_150")
        self.label_151 = QtWidgets.QLabel(self.groupBox_67)
        self.label_151.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_151.setFont(font)
        self.label_151.setObjectName("label_151")
        self.d5_2_6_1 = QtWidgets.QTextEdit(self.groupBox_67)
        self.d5_2_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_2_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_6_1.setReadOnly(True)
        self.d5_2_6_1.setObjectName("d5_2_6_1")
        self.d5_2_6_2 = QtWidgets.QTextEdit(self.groupBox_67)
        self.d5_2_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_2_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_6_2.setReadOnly(True)
        self.d5_2_6_2.setObjectName("d5_2_6_2")
        self.groupBox_68 = QtWidgets.QGroupBox(self.gbB_2)
        self.groupBox_68.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_68.setObjectName("groupBox_68")
        self.label_152 = QtWidgets.QLabel(self.groupBox_68)
        self.label_152.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_152.setFont(font)
        self.label_152.setObjectName("label_152")
        self.label_153 = QtWidgets.QLabel(self.groupBox_68)
        self.label_153.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_153.setFont(font)
        self.label_153.setObjectName("label_153")
        self.d5_2_3_1 = QtWidgets.QTextEdit(self.groupBox_68)
        self.d5_2_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_2_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_3_1.setReadOnly(True)
        self.d5_2_3_1.setObjectName("d5_2_3_1")
        self.d5_2_3_2 = QtWidgets.QTextEdit(self.groupBox_68)
        self.d5_2_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_2_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_3_2.setReadOnly(True)
        self.d5_2_3_2.setObjectName("d5_2_3_2")
        self.groupBox_69 = QtWidgets.QGroupBox(self.gbB_2)
        self.groupBox_69.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_69.setObjectName("groupBox_69")
        self.label_155 = QtWidgets.QLabel(self.groupBox_69)
        self.label_155.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_155.setFont(font)
        self.label_155.setObjectName("label_155")
        self.d5_2_7_1 = QtWidgets.QTextEdit(self.groupBox_69)
        self.d5_2_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_2_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_7_1.setReadOnly(True)
        self.d5_2_7_1.setObjectName("d5_2_7_1")
        self.groupBox_70 = QtWidgets.QGroupBox(self.gbB_2)
        self.groupBox_70.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_70.setObjectName("groupBox_70")
        self.label_156 = QtWidgets.QLabel(self.groupBox_70)
        self.label_156.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_156.setFont(font)
        self.label_156.setObjectName("label_156")
        self.label_157 = QtWidgets.QLabel(self.groupBox_70)
        self.label_157.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_157.setFont(font)
        self.label_157.setObjectName("label_157")
        self.d5_2_4_1 = QtWidgets.QTextEdit(self.groupBox_70)
        self.d5_2_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_2_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_4_1.setReadOnly(True)
        self.d5_2_4_1.setObjectName("d5_2_4_1")
        self.d5_2_4_2 = QtWidgets.QTextEdit(self.groupBox_70)
        self.d5_2_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_2_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_4_2.setReadOnly(True)
        self.d5_2_4_2.setObjectName("d5_2_4_2")
        self.groupBox_71 = QtWidgets.QGroupBox(self.gbB_2)
        self.groupBox_71.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_71.setObjectName("groupBox_71")
        self.label_159 = QtWidgets.QLabel(self.groupBox_71)
        self.label_159.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_159.setFont(font)
        self.label_159.setObjectName("label_159")
        self.d5_2_8_1 = QtWidgets.QTextEdit(self.groupBox_71)
        self.d5_2_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_2_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_2_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_2_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_2_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_2_8_1.setReadOnly(True)
        self.d5_2_8_1.setObjectName("d5_2_8_1")
        self.gbB_6 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_6.setGeometry(QtCore.QRect(960, 370, 281, 161))
        self.gbB_6.setObjectName("gbB_6")
        self.groupBox_73 = QtWidgets.QGroupBox(self.gbB_6)
        self.groupBox_73.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_73.setObjectName("groupBox_73")
        self.label_160 = QtWidgets.QLabel(self.groupBox_73)
        self.label_160.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_160.setFont(font)
        self.label_160.setObjectName("label_160")
        self.label_161 = QtWidgets.QLabel(self.groupBox_73)
        self.label_161.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_161.setFont(font)
        self.label_161.setObjectName("label_161")
        self.d5_6_1_1 = QtWidgets.QTextEdit(self.groupBox_73)
        self.d5_6_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_6_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_1_1.setReadOnly(True)
        self.d5_6_1_1.setObjectName("d5_6_1_1")
        self.d5_6_1_2 = QtWidgets.QTextEdit(self.groupBox_73)
        self.d5_6_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_6_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_1_2.setReadOnly(True)
        self.d5_6_1_2.setObjectName("d5_6_1_2")
        self.groupBox_74 = QtWidgets.QGroupBox(self.gbB_6)
        self.groupBox_74.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_74.setObjectName("groupBox_74")
        self.label_162 = QtWidgets.QLabel(self.groupBox_74)
        self.label_162.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_162.setFont(font)
        self.label_162.setObjectName("label_162")
        self.label_163 = QtWidgets.QLabel(self.groupBox_74)
        self.label_163.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_163.setFont(font)
        self.label_163.setObjectName("label_163")
        self.d5_6_5_1 = QtWidgets.QTextEdit(self.groupBox_74)
        self.d5_6_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_6_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_5_1.setReadOnly(True)
        self.d5_6_5_1.setObjectName("d5_6_5_1")
        self.d5_6_5_2 = QtWidgets.QTextEdit(self.groupBox_74)
        self.d5_6_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_6_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_5_2.setReadOnly(True)
        self.d5_6_5_2.setObjectName("d5_6_5_2")
        self.groupBox_75 = QtWidgets.QGroupBox(self.gbB_6)
        self.groupBox_75.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_75.setObjectName("groupBox_75")
        self.label_164 = QtWidgets.QLabel(self.groupBox_75)
        self.label_164.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_164.setFont(font)
        self.label_164.setObjectName("label_164")
        self.label_165 = QtWidgets.QLabel(self.groupBox_75)
        self.label_165.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_165.setFont(font)
        self.label_165.setObjectName("label_165")
        self.d5_6_2_1 = QtWidgets.QTextEdit(self.groupBox_75)
        self.d5_6_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_6_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_2_1.setReadOnly(True)
        self.d5_6_2_1.setObjectName("d5_6_2_1")
        self.d5_6_2_2 = QtWidgets.QTextEdit(self.groupBox_75)
        self.d5_6_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_6_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_2_2.setReadOnly(True)
        self.d5_6_2_2.setObjectName("d5_6_2_2")
        self.groupBox_76 = QtWidgets.QGroupBox(self.gbB_6)
        self.groupBox_76.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_76.setObjectName("groupBox_76")
        self.label_166 = QtWidgets.QLabel(self.groupBox_76)
        self.label_166.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_166.setFont(font)
        self.label_166.setObjectName("label_166")
        self.label_167 = QtWidgets.QLabel(self.groupBox_76)
        self.label_167.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_167.setFont(font)
        self.label_167.setObjectName("label_167")
        self.d5_6_6_1 = QtWidgets.QTextEdit(self.groupBox_76)
        self.d5_6_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_6_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_6_1.setReadOnly(True)
        self.d5_6_6_1.setObjectName("d5_6_6_1")
        self.d5_6_6_2 = QtWidgets.QTextEdit(self.groupBox_76)
        self.d5_6_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_6_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_6_2.setReadOnly(True)
        self.d5_6_6_2.setObjectName("d5_6_6_2")
        self.groupBox_77 = QtWidgets.QGroupBox(self.gbB_6)
        self.groupBox_77.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_77.setObjectName("groupBox_77")
        self.label_168 = QtWidgets.QLabel(self.groupBox_77)
        self.label_168.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_168.setFont(font)
        self.label_168.setObjectName("label_168")
        self.label_169 = QtWidgets.QLabel(self.groupBox_77)
        self.label_169.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_169.setFont(font)
        self.label_169.setObjectName("label_169")
        self.d5_6_3_1 = QtWidgets.QTextEdit(self.groupBox_77)
        self.d5_6_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_6_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_3_1.setReadOnly(True)
        self.d5_6_3_1.setObjectName("d5_6_3_1")
        self.d5_6_3_2 = QtWidgets.QTextEdit(self.groupBox_77)
        self.d5_6_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_6_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_3_2.setReadOnly(True)
        self.d5_6_3_2.setObjectName("d5_6_3_2")
        self.groupBox_78 = QtWidgets.QGroupBox(self.gbB_6)
        self.groupBox_78.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_78.setObjectName("groupBox_78")
        self.label_171 = QtWidgets.QLabel(self.groupBox_78)
        self.label_171.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_171.setFont(font)
        self.label_171.setObjectName("label_171")
        self.d5_6_7_1 = QtWidgets.QTextEdit(self.groupBox_78)
        self.d5_6_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_6_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_7_1.setReadOnly(True)
        self.d5_6_7_1.setObjectName("d5_6_7_1")
        self.groupBox_79 = QtWidgets.QGroupBox(self.gbB_6)
        self.groupBox_79.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_79.setObjectName("groupBox_79")
        self.label_172 = QtWidgets.QLabel(self.groupBox_79)
        self.label_172.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_172.setFont(font)
        self.label_172.setObjectName("label_172")
        self.label_173 = QtWidgets.QLabel(self.groupBox_79)
        self.label_173.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_173.setFont(font)
        self.label_173.setObjectName("label_173")
        self.d5_6_4_1 = QtWidgets.QTextEdit(self.groupBox_79)
        self.d5_6_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_6_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_4_1.setReadOnly(True)
        self.d5_6_4_1.setObjectName("d5_6_4_1")
        self.d5_6_4_2 = QtWidgets.QTextEdit(self.groupBox_79)
        self.d5_6_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_6_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_4_2.setReadOnly(True)
        self.d5_6_4_2.setObjectName("d5_6_4_2")
        self.groupBox_80 = QtWidgets.QGroupBox(self.gbB_6)
        self.groupBox_80.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_80.setObjectName("groupBox_80")
        self.label_175 = QtWidgets.QLabel(self.groupBox_80)
        self.label_175.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_175.setFont(font)
        self.label_175.setObjectName("label_175")
        self.d5_6_8_1 = QtWidgets.QTextEdit(self.groupBox_80)
        self.d5_6_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_6_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_6_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_6_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_6_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_6_8_1.setReadOnly(True)
        self.d5_6_8_1.setObjectName("d5_6_8_1")
        self.gbB_12 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_12.setGeometry(QtCore.QRect(960, 530, 281, 161))
        self.gbB_12.setObjectName("gbB_12")
        self.groupBox_82 = QtWidgets.QGroupBox(self.gbB_12)
        self.groupBox_82.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_82.setObjectName("groupBox_82")
        self.label_176 = QtWidgets.QLabel(self.groupBox_82)
        self.label_176.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_176.setFont(font)
        self.label_176.setObjectName("label_176")
        self.label_177 = QtWidgets.QLabel(self.groupBox_82)
        self.label_177.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_177.setFont(font)
        self.label_177.setObjectName("label_177")
        self.d5_12_1_1 = QtWidgets.QTextEdit(self.groupBox_82)
        self.d5_12_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_12_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_1_1.setReadOnly(True)
        self.d5_12_1_1.setObjectName("d5_12_1_1")
        self.d5_12_1_2 = QtWidgets.QTextEdit(self.groupBox_82)
        self.d5_12_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_12_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_1_2.setReadOnly(True)
        self.d5_12_1_2.setObjectName("d5_12_1_2")
        self.groupBox_83 = QtWidgets.QGroupBox(self.gbB_12)
        self.groupBox_83.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_83.setObjectName("groupBox_83")
        self.label_178 = QtWidgets.QLabel(self.groupBox_83)
        self.label_178.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_178.setFont(font)
        self.label_178.setObjectName("label_178")
        self.label_179 = QtWidgets.QLabel(self.groupBox_83)
        self.label_179.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_179.setFont(font)
        self.label_179.setObjectName("label_179")
        self.d5_12_5_1 = QtWidgets.QTextEdit(self.groupBox_83)
        self.d5_12_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_12_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_5_1.setReadOnly(True)
        self.d5_12_5_1.setObjectName("d5_12_5_1")
        self.d5_12_5_2 = QtWidgets.QTextEdit(self.groupBox_83)
        self.d5_12_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_12_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_5_2.setReadOnly(True)
        self.d5_12_5_2.setObjectName("d5_12_5_2")
        self.groupBox_84 = QtWidgets.QGroupBox(self.gbB_12)
        self.groupBox_84.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_84.setObjectName("groupBox_84")
        self.label_180 = QtWidgets.QLabel(self.groupBox_84)
        self.label_180.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_180.setFont(font)
        self.label_180.setObjectName("label_180")
        self.label_181 = QtWidgets.QLabel(self.groupBox_84)
        self.label_181.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_181.setFont(font)
        self.label_181.setObjectName("label_181")
        self.d5_12_2_1 = QtWidgets.QTextEdit(self.groupBox_84)
        self.d5_12_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_12_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_2_1.setReadOnly(True)
        self.d5_12_2_1.setObjectName("d5_12_2_1")
        self.d5_12_2_2 = QtWidgets.QTextEdit(self.groupBox_84)
        self.d5_12_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_12_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_2_2.setReadOnly(True)
        self.d5_12_2_2.setObjectName("d5_12_2_2")
        self.groupBox_85 = QtWidgets.QGroupBox(self.gbB_12)
        self.groupBox_85.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_85.setObjectName("groupBox_85")
        self.label_182 = QtWidgets.QLabel(self.groupBox_85)
        self.label_182.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_182.setFont(font)
        self.label_182.setObjectName("label_182")
        self.label_183 = QtWidgets.QLabel(self.groupBox_85)
        self.label_183.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_183.setFont(font)
        self.label_183.setObjectName("label_183")
        self.d5_12_6_1 = QtWidgets.QTextEdit(self.groupBox_85)
        self.d5_12_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_12_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_6_1.setReadOnly(True)
        self.d5_12_6_1.setObjectName("d5_12_6_1")
        self.d5_12_6_2 = QtWidgets.QTextEdit(self.groupBox_85)
        self.d5_12_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_12_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_6_2.setReadOnly(True)
        self.d5_12_6_2.setObjectName("d5_12_6_2")
        self.groupBox_86 = QtWidgets.QGroupBox(self.gbB_12)
        self.groupBox_86.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_86.setObjectName("groupBox_86")
        self.label_184 = QtWidgets.QLabel(self.groupBox_86)
        self.label_184.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_184.setFont(font)
        self.label_184.setObjectName("label_184")
        self.label_185 = QtWidgets.QLabel(self.groupBox_86)
        self.label_185.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_185.setFont(font)
        self.label_185.setObjectName("label_185")
        self.d5_12_3_1 = QtWidgets.QTextEdit(self.groupBox_86)
        self.d5_12_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_12_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_3_1.setReadOnly(True)
        self.d5_12_3_1.setObjectName("d5_12_3_1")
        self.d5_12_3_2 = QtWidgets.QTextEdit(self.groupBox_86)
        self.d5_12_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_12_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_3_2.setReadOnly(True)
        self.d5_12_3_2.setObjectName("d5_12_3_2")
        self.groupBox_87 = QtWidgets.QGroupBox(self.gbB_12)
        self.groupBox_87.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_87.setObjectName("groupBox_87")
        self.label_187 = QtWidgets.QLabel(self.groupBox_87)
        self.label_187.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_187.setFont(font)
        self.label_187.setObjectName("label_187")
        self.d5_12_7_1 = QtWidgets.QTextEdit(self.groupBox_87)
        self.d5_12_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_12_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_7_1.setReadOnly(True)
        self.d5_12_7_1.setObjectName("d5_12_7_1")
        self.groupBox_88 = QtWidgets.QGroupBox(self.gbB_12)
        self.groupBox_88.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_88.setObjectName("groupBox_88")
        self.label_188 = QtWidgets.QLabel(self.groupBox_88)
        self.label_188.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_188.setFont(font)
        self.label_188.setObjectName("label_188")
        self.label_189 = QtWidgets.QLabel(self.groupBox_88)
        self.label_189.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_189.setFont(font)
        self.label_189.setObjectName("label_189")
        self.d5_12_4_1 = QtWidgets.QTextEdit(self.groupBox_88)
        self.d5_12_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_12_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_4_1.setReadOnly(True)
        self.d5_12_4_1.setObjectName("d5_12_4_1")
        self.d5_12_4_2 = QtWidgets.QTextEdit(self.groupBox_88)
        self.d5_12_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_12_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_4_2.setReadOnly(True)
        self.d5_12_4_2.setObjectName("d5_12_4_2")
        self.groupBox_89 = QtWidgets.QGroupBox(self.gbB_12)
        self.groupBox_89.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_89.setObjectName("groupBox_89")
        self.label_191 = QtWidgets.QLabel(self.groupBox_89)
        self.label_191.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_191.setFont(font)
        self.label_191.setObjectName("label_191")
        self.d5_12_8_1 = QtWidgets.QTextEdit(self.groupBox_89)
        self.d5_12_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_12_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_12_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_12_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_12_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_12_8_1.setReadOnly(True)
        self.d5_12_8_1.setObjectName("d5_12_8_1")
        self.label_192 = QtWidgets.QLabel(self.centralwidget)
        self.label_192.setGeometry(QtCore.QRect(400, 350, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_192.setFont(font)
        self.label_192.setObjectName("label_192")
        self.gbB_10 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_10.setGeometry(QtCore.QRect(680, 530, 281, 161))
        self.gbB_10.setObjectName("gbB_10")
        self.groupBox_91 = QtWidgets.QGroupBox(self.gbB_10)
        self.groupBox_91.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_91.setObjectName("groupBox_91")
        self.label_193 = QtWidgets.QLabel(self.groupBox_91)
        self.label_193.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_193.setFont(font)
        self.label_193.setObjectName("label_193")
        self.label_194 = QtWidgets.QLabel(self.groupBox_91)
        self.label_194.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_194.setFont(font)
        self.label_194.setObjectName("label_194")
        self.d5_10_1_1 = QtWidgets.QTextEdit(self.groupBox_91)
        self.d5_10_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_10_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_1_1.setReadOnly(True)
        self.d5_10_1_1.setObjectName("d5_10_1_1")
        self.d5_10_1_2 = QtWidgets.QTextEdit(self.groupBox_91)
        self.d5_10_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_10_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_1_2.setReadOnly(True)
        self.d5_10_1_2.setObjectName("d5_10_1_2")
        self.groupBox_92 = QtWidgets.QGroupBox(self.gbB_10)
        self.groupBox_92.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_92.setObjectName("groupBox_92")
        self.label_195 = QtWidgets.QLabel(self.groupBox_92)
        self.label_195.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_195.setFont(font)
        self.label_195.setObjectName("label_195")
        self.label_196 = QtWidgets.QLabel(self.groupBox_92)
        self.label_196.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_196.setFont(font)
        self.label_196.setObjectName("label_196")
        self.d5_10_5_1 = QtWidgets.QTextEdit(self.groupBox_92)
        self.d5_10_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_10_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_5_1.setReadOnly(True)
        self.d5_10_5_1.setObjectName("d5_10_5_1")
        self.d5_10_5_2 = QtWidgets.QTextEdit(self.groupBox_92)
        self.d5_10_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_10_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_5_2.setReadOnly(True)
        self.d5_10_5_2.setObjectName("d5_10_5_2")
        self.groupBox_93 = QtWidgets.QGroupBox(self.gbB_10)
        self.groupBox_93.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_93.setObjectName("groupBox_93")
        self.label_197 = QtWidgets.QLabel(self.groupBox_93)
        self.label_197.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_197.setFont(font)
        self.label_197.setObjectName("label_197")
        self.label_198 = QtWidgets.QLabel(self.groupBox_93)
        self.label_198.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_198.setFont(font)
        self.label_198.setObjectName("label_198")
        self.d5_10_2_1 = QtWidgets.QTextEdit(self.groupBox_93)
        self.d5_10_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_10_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_2_1.setReadOnly(True)
        self.d5_10_2_1.setObjectName("d5_10_2_1")
        self.d5_10_2_2 = QtWidgets.QTextEdit(self.groupBox_93)
        self.d5_10_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_10_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_2_2.setReadOnly(True)
        self.d5_10_2_2.setObjectName("d5_10_2_2")
        self.groupBox_94 = QtWidgets.QGroupBox(self.gbB_10)
        self.groupBox_94.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_94.setObjectName("groupBox_94")
        self.label_199 = QtWidgets.QLabel(self.groupBox_94)
        self.label_199.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_199.setFont(font)
        self.label_199.setObjectName("label_199")
        self.label_200 = QtWidgets.QLabel(self.groupBox_94)
        self.label_200.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_200.setFont(font)
        self.label_200.setObjectName("label_200")
        self.d5_10_6_1 = QtWidgets.QTextEdit(self.groupBox_94)
        self.d5_10_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_10_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_6_1.setReadOnly(True)
        self.d5_10_6_1.setObjectName("d5_10_6_1")
        self.d5_10_6_2 = QtWidgets.QTextEdit(self.groupBox_94)
        self.d5_10_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_10_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_6_2.setReadOnly(True)
        self.d5_10_6_2.setObjectName("d5_10_6_2")
        self.groupBox_95 = QtWidgets.QGroupBox(self.gbB_10)
        self.groupBox_95.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_95.setObjectName("groupBox_95")
        self.label_201 = QtWidgets.QLabel(self.groupBox_95)
        self.label_201.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_201.setFont(font)
        self.label_201.setObjectName("label_201")
        self.label_202 = QtWidgets.QLabel(self.groupBox_95)
        self.label_202.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_202.setFont(font)
        self.label_202.setObjectName("label_202")
        self.d5_10_3_1 = QtWidgets.QTextEdit(self.groupBox_95)
        self.d5_10_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_10_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_3_1.setReadOnly(True)
        self.d5_10_3_1.setObjectName("d5_10_3_1")
        self.d5_10_3_2 = QtWidgets.QTextEdit(self.groupBox_95)
        self.d5_10_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_10_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_3_2.setReadOnly(True)
        self.d5_10_3_2.setObjectName("d5_10_3_2")
        self.groupBox_96 = QtWidgets.QGroupBox(self.gbB_10)
        self.groupBox_96.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_96.setObjectName("groupBox_96")
        self.label_204 = QtWidgets.QLabel(self.groupBox_96)
        self.label_204.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_204.setFont(font)
        self.label_204.setObjectName("label_204")
        self.d5_10_7_1 = QtWidgets.QTextEdit(self.groupBox_96)
        self.d5_10_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_10_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_7_1.setReadOnly(True)
        self.d5_10_7_1.setObjectName("d5_10_7_1")
        self.groupBox_97 = QtWidgets.QGroupBox(self.gbB_10)
        self.groupBox_97.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_97.setObjectName("groupBox_97")
        self.label_205 = QtWidgets.QLabel(self.groupBox_97)
        self.label_205.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_205.setFont(font)
        self.label_205.setObjectName("label_205")
        self.label_206 = QtWidgets.QLabel(self.groupBox_97)
        self.label_206.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_206.setFont(font)
        self.label_206.setObjectName("label_206")
        self.d5_10_4_1 = QtWidgets.QTextEdit(self.groupBox_97)
        self.d5_10_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_10_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_4_1.setReadOnly(True)
        self.d5_10_4_1.setObjectName("d5_10_4_1")
        self.d5_10_4_2 = QtWidgets.QTextEdit(self.groupBox_97)
        self.d5_10_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_10_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_4_2.setReadOnly(True)
        self.d5_10_4_2.setObjectName("d5_10_4_2")
        self.groupBox_98 = QtWidgets.QGroupBox(self.gbB_10)
        self.groupBox_98.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_98.setObjectName("groupBox_98")
        self.label_208 = QtWidgets.QLabel(self.groupBox_98)
        self.label_208.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_208.setFont(font)
        self.label_208.setObjectName("label_208")
        self.d5_10_8_1 = QtWidgets.QTextEdit(self.groupBox_98)
        self.d5_10_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_10_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_10_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_10_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_10_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_10_8_1.setReadOnly(True)
        self.d5_10_8_1.setObjectName("d5_10_8_1")
        self.gbB_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_4.setGeometry(QtCore.QRect(680, 370, 281, 161))
        self.gbB_4.setObjectName("gbB_4")
        self.groupBox_100 = QtWidgets.QGroupBox(self.gbB_4)
        self.groupBox_100.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_100.setObjectName("groupBox_100")
        self.label_209 = QtWidgets.QLabel(self.groupBox_100)
        self.label_209.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_209.setFont(font)
        self.label_209.setObjectName("label_209")
        self.label_210 = QtWidgets.QLabel(self.groupBox_100)
        self.label_210.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_210.setFont(font)
        self.label_210.setObjectName("label_210")
        self.d5_4_1_1 = QtWidgets.QTextEdit(self.groupBox_100)
        self.d5_4_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_4_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_1_1.setReadOnly(True)
        self.d5_4_1_1.setObjectName("d5_4_1_1")
        self.d5_4_1_2 = QtWidgets.QTextEdit(self.groupBox_100)
        self.d5_4_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_4_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_1_2.setReadOnly(True)
        self.d5_4_1_2.setObjectName("d5_4_1_2")
        self.groupBox_101 = QtWidgets.QGroupBox(self.gbB_4)
        self.groupBox_101.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_101.setObjectName("groupBox_101")
        self.label_211 = QtWidgets.QLabel(self.groupBox_101)
        self.label_211.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_211.setFont(font)
        self.label_211.setObjectName("label_211")
        self.label_212 = QtWidgets.QLabel(self.groupBox_101)
        self.label_212.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_212.setFont(font)
        self.label_212.setObjectName("label_212")
        self.d5_4_5_1 = QtWidgets.QTextEdit(self.groupBox_101)
        self.d5_4_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_4_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_5_1.setReadOnly(True)
        self.d5_4_5_1.setObjectName("d5_4_5_1")
        self.d5_4_5_2 = QtWidgets.QTextEdit(self.groupBox_101)
        self.d5_4_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_4_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_5_2.setReadOnly(True)
        self.d5_4_5_2.setObjectName("d5_4_5_2")
        self.groupBox_102 = QtWidgets.QGroupBox(self.gbB_4)
        self.groupBox_102.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_102.setObjectName("groupBox_102")
        self.label_213 = QtWidgets.QLabel(self.groupBox_102)
        self.label_213.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_213.setFont(font)
        self.label_213.setObjectName("label_213")
        self.label_214 = QtWidgets.QLabel(self.groupBox_102)
        self.label_214.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_214.setFont(font)
        self.label_214.setObjectName("label_214")
        self.d5_4_2_1 = QtWidgets.QTextEdit(self.groupBox_102)
        self.d5_4_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_4_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_2_1.setReadOnly(True)
        self.d5_4_2_1.setObjectName("d5_4_2_1")
        self.d5_4_2_2 = QtWidgets.QTextEdit(self.groupBox_102)
        self.d5_4_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_4_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_2_2.setReadOnly(True)
        self.d5_4_2_2.setObjectName("d5_4_2_2")
        self.groupBox_103 = QtWidgets.QGroupBox(self.gbB_4)
        self.groupBox_103.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_103.setObjectName("groupBox_103")
        self.label_215 = QtWidgets.QLabel(self.groupBox_103)
        self.label_215.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_215.setFont(font)
        self.label_215.setObjectName("label_215")
        self.label_216 = QtWidgets.QLabel(self.groupBox_103)
        self.label_216.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_216.setFont(font)
        self.label_216.setObjectName("label_216")
        self.d5_4_6_1 = QtWidgets.QTextEdit(self.groupBox_103)
        self.d5_4_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_4_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_6_1.setReadOnly(True)
        self.d5_4_6_1.setObjectName("d5_4_6_1")
        self.d5_4_6_2 = QtWidgets.QTextEdit(self.groupBox_103)
        self.d5_4_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_4_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_6_2.setReadOnly(True)
        self.d5_4_6_2.setObjectName("d5_4_6_2")
        self.groupBox_104 = QtWidgets.QGroupBox(self.gbB_4)
        self.groupBox_104.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_104.setObjectName("groupBox_104")
        self.label_217 = QtWidgets.QLabel(self.groupBox_104)
        self.label_217.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_217.setFont(font)
        self.label_217.setObjectName("label_217")
        self.label_218 = QtWidgets.QLabel(self.groupBox_104)
        self.label_218.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_218.setFont(font)
        self.label_218.setObjectName("label_218")
        self.d5_4_3_1 = QtWidgets.QTextEdit(self.groupBox_104)
        self.d5_4_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_4_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_3_1.setReadOnly(True)
        self.d5_4_3_1.setObjectName("d5_4_3_1")
        self.d5_4_3_2 = QtWidgets.QTextEdit(self.groupBox_104)
        self.d5_4_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_4_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_3_2.setReadOnly(True)
        self.d5_4_3_2.setObjectName("d5_4_3_2")
        self.groupBox_105 = QtWidgets.QGroupBox(self.gbB_4)
        self.groupBox_105.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_105.setObjectName("groupBox_105")
        self.label_220 = QtWidgets.QLabel(self.groupBox_105)
        self.label_220.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_220.setFont(font)
        self.label_220.setObjectName("label_220")
        self.d5_4_7_1 = QtWidgets.QTextEdit(self.groupBox_105)
        self.d5_4_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_4_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_7_1.setReadOnly(True)
        self.d5_4_7_1.setObjectName("d5_4_7_1")
        self.groupBox_106 = QtWidgets.QGroupBox(self.gbB_4)
        self.groupBox_106.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_106.setObjectName("groupBox_106")
        self.label_221 = QtWidgets.QLabel(self.groupBox_106)
        self.label_221.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_221.setFont(font)
        self.label_221.setObjectName("label_221")
        self.label_222 = QtWidgets.QLabel(self.groupBox_106)
        self.label_222.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_222.setFont(font)
        self.label_222.setObjectName("label_222")
        self.d5_4_4_1 = QtWidgets.QTextEdit(self.groupBox_106)
        self.d5_4_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_4_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_4_1.setReadOnly(True)
        self.d5_4_4_1.setObjectName("d5_4_4_1")
        self.d5_4_4_2 = QtWidgets.QTextEdit(self.groupBox_106)
        self.d5_4_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_4_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_4_2.setReadOnly(True)
        self.d5_4_4_2.setObjectName("d5_4_4_2")
        self.groupBox_107 = QtWidgets.QGroupBox(self.gbB_4)
        self.groupBox_107.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_107.setObjectName("groupBox_107")
        self.label_224 = QtWidgets.QLabel(self.groupBox_107)
        self.label_224.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        self.label_224.setFont(font)
        self.label_224.setObjectName("label_224")
        self.d5_4_8_1 = QtWidgets.QTextEdit(self.groupBox_107)
        self.d5_4_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_4_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_4_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_4_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_4_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_4_8_1.setReadOnly(True)
        self.d5_4_8_1.setObjectName("d5_4_8_1")
        self.gbB_8 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbB_8.setGeometry(QtCore.QRect(400, 530, 281, 161))
        self.gbB_8.setObjectName("gbB_8")
        self.groupBox_109 = QtWidgets.QGroupBox(self.gbB_8)
        self.groupBox_109.setGeometry(QtCore.QRect(0, 20, 71, 71))
        self.groupBox_109.setObjectName("groupBox_109")
        self.label_225 = QtWidgets.QLabel(self.groupBox_109)
        self.label_225.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_225.setFont(font)
        self.label_225.setObjectName("label_225")
        self.label_226 = QtWidgets.QLabel(self.groupBox_109)
        self.label_226.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_226.setFont(font)
        self.label_226.setObjectName("label_226")
        self.d5_8_1_1 = QtWidgets.QTextEdit(self.groupBox_109)
        self.d5_8_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_8_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_1_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_1_1.setReadOnly(True)
        self.d5_8_1_1.setObjectName("d5_8_1_1")
        self.d5_8_1_2 = QtWidgets.QTextEdit(self.groupBox_109)
        self.d5_8_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_8_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_1_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_1_2.setReadOnly(True)
        self.d5_8_1_2.setObjectName("d5_8_1_2")
        self.groupBox_110 = QtWidgets.QGroupBox(self.gbB_8)
        self.groupBox_110.setGeometry(QtCore.QRect(0, 90, 71, 71))
        self.groupBox_110.setObjectName("groupBox_110")
        self.label_227 = QtWidgets.QLabel(self.groupBox_110)
        self.label_227.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_227.setFont(font)
        self.label_227.setObjectName("label_227")
        self.label_228 = QtWidgets.QLabel(self.groupBox_110)
        self.label_228.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_228.setFont(font)
        self.label_228.setObjectName("label_228")
        self.d5_8_5_1 = QtWidgets.QTextEdit(self.groupBox_110)
        self.d5_8_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_8_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_5_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_5_1.setReadOnly(True)
        self.d5_8_5_1.setObjectName("d5_8_5_1")
        self.d5_8_5_2 = QtWidgets.QTextEdit(self.groupBox_110)
        self.d5_8_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_8_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_5_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_5_2.setReadOnly(True)
        self.d5_8_5_2.setObjectName("d5_8_5_2")
        self.groupBox_111 = QtWidgets.QGroupBox(self.gbB_8)
        self.groupBox_111.setGeometry(QtCore.QRect(70, 20, 71, 71))
        self.groupBox_111.setObjectName("groupBox_111")
        self.label_229 = QtWidgets.QLabel(self.groupBox_111)
        self.label_229.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_229.setFont(font)
        self.label_229.setObjectName("label_229")
        self.label_230 = QtWidgets.QLabel(self.groupBox_111)
        self.label_230.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_230.setFont(font)
        self.label_230.setObjectName("label_230")
        self.d5_8_2_1 = QtWidgets.QTextEdit(self.groupBox_111)
        self.d5_8_2_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_8_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_2_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_2_1.setReadOnly(True)
        self.d5_8_2_1.setObjectName("d5_8_2_1")
        self.d5_8_2_2 = QtWidgets.QTextEdit(self.groupBox_111)
        self.d5_8_2_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_8_2_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_2_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_2_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_2_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_2_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_2_2.setReadOnly(True)
        self.d5_8_2_2.setObjectName("d5_8_2_2")
        self.groupBox_112 = QtWidgets.QGroupBox(self.gbB_8)
        self.groupBox_112.setGeometry(QtCore.QRect(70, 90, 71, 71))
        self.groupBox_112.setObjectName("groupBox_112")
        self.label_231 = QtWidgets.QLabel(self.groupBox_112)
        self.label_231.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_231.setFont(font)
        self.label_231.setObjectName("label_231")
        self.label_232 = QtWidgets.QLabel(self.groupBox_112)
        self.label_232.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_232.setFont(font)
        self.label_232.setObjectName("label_232")
        self.d5_8_6_1 = QtWidgets.QTextEdit(self.groupBox_112)
        self.d5_8_6_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_8_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_6_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_6_1.setReadOnly(True)
        self.d5_8_6_1.setObjectName("d5_8_6_1")
        self.d5_8_6_2 = QtWidgets.QTextEdit(self.groupBox_112)
        self.d5_8_6_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_8_6_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_6_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_6_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_6_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_6_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_6_2.setReadOnly(True)
        self.d5_8_6_2.setObjectName("d5_8_6_2")
        self.groupBox_113 = QtWidgets.QGroupBox(self.gbB_8)
        self.groupBox_113.setGeometry(QtCore.QRect(140, 20, 71, 71))
        self.groupBox_113.setObjectName("groupBox_113")
        self.label_233 = QtWidgets.QLabel(self.groupBox_113)
        self.label_233.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_233.setFont(font)
        self.label_233.setObjectName("label_233")
        self.label_234 = QtWidgets.QLabel(self.groupBox_113)
        self.label_234.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_234.setFont(font)
        self.label_234.setObjectName("label_234")
        self.d5_8_3_1 = QtWidgets.QTextEdit(self.groupBox_113)
        self.d5_8_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_8_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_3_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_3_1.setReadOnly(True)
        self.d5_8_3_1.setObjectName("d5_8_3_1")
        self.d5_8_3_2 = QtWidgets.QTextEdit(self.groupBox_113)
        self.d5_8_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_8_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_3_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_3_2.setReadOnly(True)
        self.d5_8_3_2.setObjectName("d5_8_3_2")
        self.groupBox_114 = QtWidgets.QGroupBox(self.gbB_8)
        self.groupBox_114.setGeometry(QtCore.QRect(140, 90, 71, 71))
        self.groupBox_114.setObjectName("groupBox_114")
        self.label_236 = QtWidgets.QLabel(self.groupBox_114)
        self.label_236.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_236.setFont(font)
        self.label_236.setObjectName("label_236")
        self.d5_8_7_1 = QtWidgets.QTextEdit(self.groupBox_114)
        self.d5_8_7_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_8_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_7_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_7_1.setReadOnly(True)
        self.d5_8_7_1.setObjectName("d5_8_7_1")
        self.groupBox_115 = QtWidgets.QGroupBox(self.gbB_8)
        self.groupBox_115.setGeometry(QtCore.QRect(210, 20, 71, 71))
        self.groupBox_115.setObjectName("groupBox_115")
        self.label_237 = QtWidgets.QLabel(self.groupBox_115)
        self.label_237.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_237.setFont(font)
        self.label_237.setObjectName("label_237")
        self.label_238 = QtWidgets.QLabel(self.groupBox_115)
        self.label_238.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_238.setFont(font)
        self.label_238.setObjectName("label_238")
        self.d5_8_4_1 = QtWidgets.QTextEdit(self.groupBox_115)
        self.d5_8_4_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d5_8_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_4_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_4_1.setReadOnly(True)
        self.d5_8_4_1.setObjectName("d5_8_4_1")
        self.d5_8_4_2 = QtWidgets.QTextEdit(self.groupBox_115)
        self.d5_8_4_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d5_8_4_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_4_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_4_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_4_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_4_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_4_2.setReadOnly(True)
        self.d5_8_4_2.setObjectName("d5_8_4_2")
        self.groupBox_116 = QtWidgets.QGroupBox(self.gbB_8)
        self.groupBox_116.setGeometry(QtCore.QRect(210, 90, 71, 71))
        self.groupBox_116.setObjectName("groupBox_116")
        self.label_240 = QtWidgets.QLabel(self.groupBox_116)
        self.label_240.setGeometry(QtCore.QRect(20, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_240.setFont(font)
        self.label_240.setObjectName("label_240")
        self.d5_8_8_1 = QtWidgets.QTextEdit(self.groupBox_116)
        self.d5_8_8_1.setGeometry(QtCore.QRect(20, 40, 31, 21))
        self.d5_8_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5_8_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5_8_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5_8_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_8_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5_8_8_1.setReadOnly(True)
        self.d5_8_8_1.setObjectName("d5_8_8_1")
        self.label_31 = QtWidgets.QLabel(self.centralwidget)
        self.label_31.setGeometry(QtCore.QRect(10, 350, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.label_63 = QtWidgets.QLabel(self.centralwidget)
        self.label_63.setGeometry(QtCore.QRect(10, 320, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_63.setFont(font)
        self.label_63.setObjectName("label_63")
        self.label_64 = QtWidgets.QLabel(self.centralwidget)
        self.label_64.setGeometry(QtCore.QRect(10, 460, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_64.setFont(font)
        self.label_64.setObjectName("label_64")
        self.label_66 = QtWidgets.QLabel(self.centralwidget)
        self.label_66.setGeometry(QtCore.QRect(10, 430, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_66.setFont(font)
        self.label_66.setObjectName("label_66")
        self.label_241 = QtWidgets.QLabel(self.centralwidget)
        self.label_241.setGeometry(QtCore.QRect(230, 530, 151, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_241.setFont(font)
        self.label_241.setObjectName("label_241")
        self.gbA_13 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_13.setGeometry(QtCore.QRect(230, 620, 51, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_13.setFont(font)
        self.gbA_13.setObjectName("gbA_13")
        self.label_243 = QtWidgets.QLabel(self.gbA_13)
        self.label_243.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_243.setFont(font)
        self.label_243.setObjectName("label_243")
        self.d5o_8_1 = QtWidgets.QTextEdit(self.gbA_13)
        self.d5o_8_1.setGeometry(QtCore.QRect(10, 40, 31, 21))
        self.d5o_8_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d5o_8_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5o_8_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5o_8_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_8_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_8_1.setReadOnly(True)
        self.d5o_8_1.setObjectName("d5o_8_1")
        self.gbA_15 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_15.setGeometry(QtCore.QRect(330, 620, 51, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_15.setFont(font)
        self.gbA_15.setObjectName("gbA_15")
        self.label_247 = QtWidgets.QLabel(self.gbA_15)
        self.label_247.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_247.setFont(font)
        self.label_247.setObjectName("label_247")
        self.d5o_12_1 = QtWidgets.QTextEdit(self.gbA_15)
        self.d5o_12_1.setGeometry(QtCore.QRect(10, 40, 31, 21))
        self.d5o_12_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5o_12_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5o_12_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5o_12_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_12_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_12_1.setReadOnly(True)
        self.d5o_12_1.setObjectName("d5o_12_1")
        self.gbA_16 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_16.setGeometry(QtCore.QRect(230, 550, 51, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_16.setFont(font)
        self.gbA_16.setObjectName("gbA_16")
        self.label_249 = QtWidgets.QLabel(self.gbA_16)
        self.label_249.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_249.setFont(font)
        self.label_249.setObjectName("label_249")
        self.d5o_2_1 = QtWidgets.QTextEdit(self.gbA_16)
        self.d5o_2_1.setGeometry(QtCore.QRect(10, 40, 31, 21))
        self.d5o_2_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d5o_2_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5o_2_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5o_2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_2_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_2_1.setReadOnly(True)
        self.d5o_2_1.setObjectName("d5o_2_1")
        self.gbA_17 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_17.setGeometry(QtCore.QRect(330, 550, 51, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_17.setFont(font)
        self.gbA_17.setObjectName("gbA_17")
        self.label_251 = QtWidgets.QLabel(self.gbA_17)
        self.label_251.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_251.setFont(font)
        self.label_251.setObjectName("label_251")
        self.d5o_6_1 = QtWidgets.QTextEdit(self.gbA_17)
        self.d5o_6_1.setGeometry(QtCore.QRect(10, 40, 31, 21))
        self.d5o_6_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d5o_6_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5o_6_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5o_6_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_6_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_6_1.setReadOnly(True)
        self.d5o_6_1.setObjectName("d5o_6_1")
        self.gbA_18 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_18.setGeometry(QtCore.QRect(280, 550, 51, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_18.setFont(font)
        self.gbA_18.setObjectName("gbA_18")
        self.label_253 = QtWidgets.QLabel(self.gbA_18)
        self.label_253.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_253.setFont(font)
        self.label_253.setObjectName("label_253")
        self.d5o_4_1 = QtWidgets.QTextEdit(self.gbA_18)
        self.d5o_4_1.setGeometry(QtCore.QRect(10, 40, 31, 21))
        self.d5o_4_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d5o_4_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5o_4_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5o_4_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_4_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_4_1.setReadOnly(True)
        self.d5o_4_1.setObjectName("d5o_4_1")
        self.gbA_14 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_14.setGeometry(QtCore.QRect(280, 620, 51, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_14.setFont(font)
        self.gbA_14.setObjectName("gbA_14")
        self.label_245 = QtWidgets.QLabel(self.gbA_14)
        self.label_245.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_245.setFont(font)
        self.label_245.setObjectName("label_245")
        self.d5o_10_1 = QtWidgets.QTextEdit(self.gbA_14)
        self.d5o_10_1.setGeometry(QtCore.QRect(10, 40, 31, 21))
        self.d5o_10_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d5o_10_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d5o_10_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d5o_10_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_10_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d5o_10_1.setReadOnly(True)
        self.d5o_10_1.setObjectName("d5o_10_1")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 5, 160, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setEnabled(False)
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(50, 5, 160, 30))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 5, 30, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pixmap = QtGui.QPixmap()
        self.pixmap.loadFromData(QtCore.QByteArray(self.icon), 'png')
        self.pushButton_2.setIcon(QIcon(self.pixmap))
        self.pushButton_2.setIconSize(QSize(25, 25))
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 170, 80, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.hide()
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 40, 370, 120))
        self.textEdit.setReadOnly(True)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.gbA_19 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_19.setGeometry(QtCore.QRect(150, 620, 71, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_19.setFont(font)
        self.gbA_19.setObjectName("gbA_19")
        self.label_248 = QtWidgets.QLabel(self.gbA_19)
        self.label_248.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_248.setFont(font)
        self.label_248.setObjectName("label_248")
        self.label_65 = QtWidgets.QLabel(self.gbA_19)
        self.label_65.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_65.setFont(font)
        self.label_65.setObjectName("label_65")
        self.d24_11_1 = QtWidgets.QTextEdit(self.gbA_19)
        self.d24_11_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d24_11_1.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d24_11_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_11_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_11_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_11_1.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_11_1.setReadOnly(True)
        self.d24_11_1.setObjectName("d24_11_1")
        self.d24_11_2 = QtWidgets.QTextEdit(self.gbA_19)
        self.d24_11_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d24_11_2.viewport().setProperty(
            "cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.d24_11_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_11_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_11_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_11_2.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_11_2.setReadOnly(True)
        self.d24_11_2.setObjectName("d24_11_2")
        self.gbA_20 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_20.setGeometry(QtCore.QRect(150, 550, 71, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_20.setFont(font)
        self.gbA_20.setObjectName("gbA_20")
        self.label_252 = QtWidgets.QLabel(self.gbA_20)
        self.label_252.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_252.setFont(font)
        self.label_252.setObjectName("label_252")
        self.label_45 = QtWidgets.QLabel(self.gbA_20)
        self.label_45.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_45.setFont(font)
        self.label_45.setObjectName("label_45")
        self.d24_5_1 = QtWidgets.QTextEdit(self.gbA_20)
        self.d24_5_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d24_5_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_5_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_5_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_5_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_5_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_5_1.setReadOnly(True)
        self.d24_5_1.setObjectName("d24_5_1")
        self.d24_5_2 = QtWidgets.QTextEdit(self.gbA_20)
        self.d24_5_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d24_5_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_5_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_5_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_5_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_5_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_5_2.setReadOnly(True)
        self.d24_5_2.setObjectName("d24_5_2")
        self.gbA_21 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_21.setGeometry(QtCore.QRect(80, 620, 71, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_21.setFont(font)
        self.gbA_21.setObjectName("gbA_21")
        self.label_246 = QtWidgets.QLabel(self.gbA_21)
        self.label_246.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_246.setFont(font)
        self.label_246.setObjectName("label_246")
        self.label_61 = QtWidgets.QLabel(self.gbA_21)
        self.label_61.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_61.setFont(font)
        self.label_61.setObjectName("label_61")
        self.d24_9_1 = QtWidgets.QTextEdit(self.gbA_21)
        self.d24_9_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d24_9_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_9_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_9_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_9_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_9_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_9_1.setReadOnly(True)
        self.d24_9_1.setObjectName("d24_9_1")
        self.d24_9_2 = QtWidgets.QTextEdit(self.gbA_21)
        self.d24_9_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d24_9_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_9_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_9_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_9_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_9_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_9_2.setReadOnly(True)
        self.d24_9_2.setObjectName("d24_9_2")
        self.gbA_22 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_22.setGeometry(QtCore.QRect(10, 550, 71, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_22.setFont(font)
        self.gbA_22.setObjectName("gbA_22")
        self.label_250 = QtWidgets.QLabel(self.gbA_22)
        self.label_250.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_250.setFont(font)
        self.label_250.setObjectName("label_250")
        self.label_32 = QtWidgets.QLabel(self.gbA_22)
        self.label_32.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.d24_1_1 = QtWidgets.QTextEdit(self.gbA_22)
        self.d24_1_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d24_1_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_1_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_1_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_1_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_1_1.setReadOnly(True)
        self.d24_1_1.setObjectName("d24_1_1")
        self.d24_1_2 = QtWidgets.QTextEdit(self.gbA_22)
        self.d24_1_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d24_1_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_1_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_1_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_1_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_1_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_1_2.setReadOnly(True)
        self.d24_1_2.setObjectName("d24_1_2")
        self.gbA_23 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_23.setGeometry(QtCore.QRect(80, 550, 71, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_23.setFont(font)
        self.gbA_23.setObjectName("gbA_23")
        self.label_254 = QtWidgets.QLabel(self.gbA_23)
        self.label_254.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_254.setFont(font)
        self.label_254.setObjectName("label_254")
        self.label_41 = QtWidgets.QLabel(self.gbA_23)
        self.label_41.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_41.setFont(font)
        self.label_41.setObjectName("label_41")
        self.d24_3_1 = QtWidgets.QTextEdit(self.gbA_23)
        self.d24_3_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d24_3_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_3_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_3_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_3_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_3_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_3_1.setReadOnly(True)
        self.d24_3_1.setObjectName("d24_3_1")
        self.d24_3_2 = QtWidgets.QTextEdit(self.gbA_23)
        self.d24_3_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d24_3_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_3_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_3_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_3_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_3_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_3_2.setReadOnly(True)
        self.d24_3_2.setObjectName("d24_3_2")
        self.gbA_24 = QtWidgets.QGroupBox(self.centralwidget)
        self.gbA_24.setGeometry(QtCore.QRect(10, 620, 71, 71))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.gbA_24.setFont(font)
        self.gbA_24.setObjectName("gbA_24")
        self.label_244 = QtWidgets.QLabel(self.gbA_24)
        self.label_244.setGeometry(QtCore.QRect(10, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_244.setFont(font)
        self.label_244.setObjectName("label_244")
        self.label_57 = QtWidgets.QLabel(self.gbA_24)
        self.label_57.setGeometry(QtCore.QRect(40, 20, 25, 10))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        self.label_57.setFont(font)
        self.label_57.setObjectName("label_57")
        self.d24_7_1 = QtWidgets.QTextEdit(self.gbA_24)
        self.d24_7_1.setGeometry(QtCore.QRect(10, 40, 21, 21))
        self.d24_7_1.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_7_1.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_7_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_7_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_7_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_7_1.setReadOnly(True)
        self.d24_7_1.setObjectName("d24_7_1")
        self.d24_7_2 = QtWidgets.QTextEdit(self.gbA_24)
        self.d24_7_2.setGeometry(QtCore.QRect(40, 40, 21, 21))
        self.d24_7_2.viewport().setProperty(
            "cursor", QtGui.QCursor(
                QtCore.Qt.ArrowCursor))
        self.d24_7_2.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.d24_7_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.d24_7_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_7_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.d24_7_2.setReadOnly(True)
        self.d24_7_2.setObjectName("d24_7_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1250, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate(
                "MainWindow",
                "Проверка коммутации МШУ в станции ПОСТ-3М"))
        self.gbA_1.setTitle(_translate("MainWindow", "1 сектор"))
        self.label_5.setText(_translate("MainWindow", "1 Вых"))
        self.label_6.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_2.setTitle(_translate("MainWindow", "2 сектор"))
        self.label_7.setText(_translate("MainWindow", "1 Вых"))
        self.label_8.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_3.setTitle(_translate("MainWindow", "3 сектор"))
        self.label_9.setText(_translate("MainWindow", "1 Вых"))
        self.label_10.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_4.setTitle(_translate("MainWindow", "4 сектор"))
        self.label_11.setText(_translate("MainWindow", "1 Вых"))
        self.label_12.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_5.setTitle(_translate("MainWindow", "5 сектор"))
        self.label_13.setText(_translate("MainWindow", "1 Вых"))
        self.label_14.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_6.setTitle(_translate("MainWindow", "6 сектор"))
        self.label_15.setText(_translate("MainWindow", "1 Вых"))
        self.label_16.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_7.setTitle(_translate("MainWindow", "7 сектор"))
        self.label_17.setText(_translate("MainWindow", "1 Вых"))
        self.label_18.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_8.setTitle(_translate("MainWindow", "8 сектор"))
        self.label_19.setText(_translate("MainWindow", "1 Вых"))
        self.label_20.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_9.setTitle(_translate("MainWindow", "9 сектор"))
        self.label_21.setText(_translate("MainWindow", "1 Вых"))
        self.label_22.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_10.setTitle(_translate("MainWindow", "10 сектор"))
        self.label_23.setText(_translate("MainWindow", "1 Вых"))
        self.label_24.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_11.setTitle(_translate("MainWindow", "11 сектор"))
        self.label_25.setText(_translate("MainWindow", "1 Вых"))
        self.label_26.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_12.setTitle(_translate("MainWindow", "12 сектор"))
        self.label_27.setText(_translate("MainWindow", "1 Вых"))
        self.label_28.setText(_translate("MainWindow", "2 Вых"))
        self.label_2.setText(_translate("MainWindow", "МШУ Д2"))
        self.label_3.setText(_translate("MainWindow", "МШУ Д3"))
        self.label_4.setText(_translate("MainWindow", "МШУ Д2-Д4"))
        self.gbB_1.setTitle(_translate("MainWindow", "1 сектор"))
        self.groupBox_7.setTitle(_translate("MainWindow", "1 луч"))
        self.label_29.setText(_translate("MainWindow", "2 Вых"))
        self.label_30.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_8.setTitle(_translate("MainWindow", "5 луч"))
        self.label_33.setText(_translate("MainWindow", "2 Вых"))
        self.label_34.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_9.setTitle(_translate("MainWindow", "2 луч"))
        self.label_35.setText(_translate("MainWindow", "2 Вых"))
        self.label_36.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_10.setTitle(_translate("MainWindow", "6 луч"))
        self.label_37.setText(_translate("MainWindow", "2 Вых"))
        self.label_38.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_11.setTitle(_translate("MainWindow", "3 луч"))
        self.label_39.setText(_translate("MainWindow", "2 Вых"))
        self.label_40.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_12.setTitle(_translate("MainWindow", "7 луч"))
        self.label_42.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_13.setTitle(_translate("MainWindow", "4 луч"))
        self.label_43.setText(_translate("MainWindow", "2 Вых"))
        self.label_44.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_14.setTitle(_translate("MainWindow", "8 луч"))
        self.label_46.setText(_translate("MainWindow", "1 Вых"))
        self.gbB_3.setTitle(_translate("MainWindow", "3 сектор"))
        self.groupBox_15.setTitle(_translate("MainWindow", "1 луч"))
        self.label_47.setText(_translate("MainWindow", "2 Вых"))
        self.label_48.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_16.setTitle(_translate("MainWindow", "5 луч"))
        self.label_49.setText(_translate("MainWindow", "2 Вых"))
        self.label_50.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_17.setTitle(_translate("MainWindow", "2 луч"))
        self.label_51.setText(_translate("MainWindow", "2 Вых"))
        self.label_52.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_18.setTitle(_translate("MainWindow", "6 луч"))
        self.label_53.setText(_translate("MainWindow", "2 Вых"))
        self.label_54.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_19.setTitle(_translate("MainWindow", "3 луч"))
        self.label_55.setText(_translate("MainWindow", "2 Вых"))
        self.label_56.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_20.setTitle(_translate("MainWindow", "7 луч"))
        self.label_58.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_21.setTitle(_translate("MainWindow", "4 луч"))
        self.label_59.setText(_translate("MainWindow", "2 Вых"))
        self.label_60.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_22.setTitle(_translate("MainWindow", "8 луч"))
        self.label_62.setText(_translate("MainWindow", "1 Вых"))
        self.gbB_5.setTitle(_translate("MainWindow", "5 сектор"))
        self.groupBox_31.setTitle(_translate("MainWindow", "1 луч"))
        self.label_79.setText(_translate("MainWindow", "2 Вых"))
        self.label_80.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_32.setTitle(_translate("MainWindow", "5 луч"))
        self.label_81.setText(_translate("MainWindow", "2 Вых"))
        self.label_82.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_33.setTitle(_translate("MainWindow", "2 луч"))
        self.label_83.setText(_translate("MainWindow", "2 Вых"))
        self.label_84.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_34.setTitle(_translate("MainWindow", "6 луч"))
        self.label_85.setText(_translate("MainWindow", "2 Вых"))
        self.label_86.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_35.setTitle(_translate("MainWindow", "3 луч"))
        self.label_87.setText(_translate("MainWindow", "2 Вых"))
        self.label_88.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_36.setTitle(_translate("MainWindow", "7 луч"))
        self.label_90.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_37.setTitle(_translate("MainWindow", "4 луч"))
        self.label_91.setText(_translate("MainWindow", "2 Вых"))
        self.label_92.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_38.setTitle(_translate("MainWindow", "8 луч"))
        self.label_94.setText(_translate("MainWindow", "1 Вых"))
        self.gbB_7.setTitle(_translate("MainWindow", "7 сектор"))
        self.groupBox_39.setTitle(_translate("MainWindow", "1 луч"))
        self.label_95.setText(_translate("MainWindow", "2 Вых"))
        self.label_96.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_40.setTitle(_translate("MainWindow", "5 луч"))
        self.label_97.setText(_translate("MainWindow", "2 Вых"))
        self.label_98.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_41.setTitle(_translate("MainWindow", "2 луч"))
        self.label_99.setText(_translate("MainWindow", "2 Вых"))
        self.label_100.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_42.setTitle(_translate("MainWindow", "6 луч"))
        self.label_101.setText(_translate("MainWindow", "2 Вых"))
        self.label_102.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_43.setTitle(_translate("MainWindow", "3 луч"))
        self.label_103.setText(_translate("MainWindow", "2 Вых"))
        self.label_104.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_44.setTitle(_translate("MainWindow", "7 луч"))
        self.label_106.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_45.setTitle(_translate("MainWindow", "4 луч"))
        self.label_107.setText(_translate("MainWindow", "2 Вых"))
        self.label_108.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_46.setTitle(_translate("MainWindow", "8 луч"))
        self.label_110.setText(_translate("MainWindow", "1 Вых"))
        self.gbB_9.setTitle(_translate("MainWindow", "9 сектор"))
        self.groupBox_47.setTitle(_translate("MainWindow", "1 луч"))
        self.label_111.setText(_translate("MainWindow", "2 Вых"))
        self.label_112.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_48.setTitle(_translate("MainWindow", "5 луч"))
        self.label_113.setText(_translate("MainWindow", "2 Вых"))
        self.label_114.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_49.setTitle(_translate("MainWindow", "2 луч"))
        self.label_115.setText(_translate("MainWindow", "2 Вых"))
        self.label_116.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_50.setTitle(_translate("MainWindow", "6 луч"))
        self.label_117.setText(_translate("MainWindow", "2 Вых"))
        self.label_118.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_51.setTitle(_translate("MainWindow", "3 луч"))
        self.label_119.setText(_translate("MainWindow", "2 Вых"))
        self.label_120.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_52.setTitle(_translate("MainWindow", "7 луч"))
        self.label_122.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_53.setTitle(_translate("MainWindow", "4 луч"))
        self.label_123.setText(_translate("MainWindow", "2 Вых"))
        self.label_124.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_54.setTitle(_translate("MainWindow", "8 луч"))
        self.label_126.setText(_translate("MainWindow", "1 Вых"))
        self.gbB_11.setTitle(_translate("MainWindow", "11 сектор"))
        self.groupBox_55.setTitle(_translate("MainWindow", "1 луч"))
        self.label_127.setText(_translate("MainWindow", "2 Вых"))
        self.label_128.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_56.setTitle(_translate("MainWindow", "5 луч"))
        self.label_129.setText(_translate("MainWindow", "2 Вых"))
        self.label_130.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_57.setTitle(_translate("MainWindow", "2 луч"))
        self.label_131.setText(_translate("MainWindow", "2 Вых"))
        self.label_132.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_58.setTitle(_translate("MainWindow", "6 луч"))
        self.label_133.setText(_translate("MainWindow", "2 Вых"))
        self.label_134.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_59.setTitle(_translate("MainWindow", "3 луч"))
        self.label_135.setText(_translate("MainWindow", "2 Вых"))
        self.label_136.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_60.setTitle(_translate("MainWindow", "7 луч"))
        self.label_138.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_61.setTitle(_translate("MainWindow", "4 луч"))
        self.label_139.setText(_translate("MainWindow", "2 Вых"))
        self.label_140.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_62.setTitle(_translate("MainWindow", "8 луч"))
        self.label_142.setText(_translate("MainWindow", "1 Вых"))
        self.label_143.setText(_translate("MainWindow", "МШУ Д4"))
        self.gbB_2.setTitle(_translate("MainWindow", "2 сектор"))
        self.groupBox_64.setTitle(_translate("MainWindow", "1 луч"))
        self.label_144.setText(_translate("MainWindow", "2 Вых"))
        self.label_145.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_65.setTitle(_translate("MainWindow", "5 луч"))
        self.label_146.setText(_translate("MainWindow", "2 Вых"))
        self.label_147.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_66.setTitle(_translate("MainWindow", "2 луч"))
        self.label_148.setText(_translate("MainWindow", "2 Вых"))
        self.label_149.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_67.setTitle(_translate("MainWindow", "6 луч"))
        self.label_150.setText(_translate("MainWindow", "2 Вых"))
        self.label_151.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_68.setTitle(_translate("MainWindow", "3 луч"))
        self.label_152.setText(_translate("MainWindow", "2 Вых"))
        self.label_153.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_69.setTitle(_translate("MainWindow", "7 луч"))
        self.label_155.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_70.setTitle(_translate("MainWindow", "4 луч"))
        self.label_156.setText(_translate("MainWindow", "2 Вых"))
        self.label_157.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_71.setTitle(_translate("MainWindow", "8 луч"))
        self.label_159.setText(_translate("MainWindow", "1 Вых"))
        self.gbB_6.setTitle(_translate("MainWindow", "6 сектор"))
        self.groupBox_73.setTitle(_translate("MainWindow", "1 луч"))
        self.label_160.setText(_translate("MainWindow", "2 Вых"))
        self.label_161.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_74.setTitle(_translate("MainWindow", "5 луч"))
        self.label_162.setText(_translate("MainWindow", "2 Вых"))
        self.label_163.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_75.setTitle(_translate("MainWindow", "2 луч"))
        self.label_164.setText(_translate("MainWindow", "2 Вых"))
        self.label_165.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_76.setTitle(_translate("MainWindow", "6 луч"))
        self.label_166.setText(_translate("MainWindow", "2 Вых"))
        self.label_167.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_77.setTitle(_translate("MainWindow", "3 луч"))
        self.label_168.setText(_translate("MainWindow", "2 Вых"))
        self.label_169.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_78.setTitle(_translate("MainWindow", "7 луч"))
        self.label_171.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_79.setTitle(_translate("MainWindow", "4 луч"))
        self.label_172.setText(_translate("MainWindow", "2 Вых"))
        self.label_173.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_80.setTitle(_translate("MainWindow", "8 луч"))
        self.label_175.setText(_translate("MainWindow", "1 Вых"))
        self.gbB_12.setTitle(_translate("MainWindow", "12 сектор"))
        self.groupBox_82.setTitle(_translate("MainWindow", "1 луч"))
        self.label_176.setText(_translate("MainWindow", "2 Вых"))
        self.label_177.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_83.setTitle(_translate("MainWindow", "5 луч"))
        self.label_178.setText(_translate("MainWindow", "2 Вых"))
        self.label_179.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_84.setTitle(_translate("MainWindow", "2 луч"))
        self.label_180.setText(_translate("MainWindow", "2 Вых"))
        self.label_181.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_85.setTitle(_translate("MainWindow", "6 луч"))
        self.label_182.setText(_translate("MainWindow", "2 Вых"))
        self.label_183.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_86.setTitle(_translate("MainWindow", "3 луч"))
        self.label_184.setText(_translate("MainWindow", "2 Вых"))
        self.label_185.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_87.setTitle(_translate("MainWindow", "7 луч"))
        self.label_187.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_88.setTitle(_translate("MainWindow", "4 луч"))
        self.label_188.setText(_translate("MainWindow", "2 Вых"))
        self.label_189.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_89.setTitle(_translate("MainWindow", "8 луч"))
        self.label_191.setText(_translate("MainWindow", "1 Вых"))
        self.label_192.setText(_translate("MainWindow", "МШУ Д5"))
        self.gbB_10.setTitle(_translate("MainWindow", "10 сектор"))
        self.groupBox_91.setTitle(_translate("MainWindow", "1 луч"))
        self.label_193.setText(_translate("MainWindow", "2 Вых"))
        self.label_194.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_92.setTitle(_translate("MainWindow", "5 луч"))
        self.label_195.setText(_translate("MainWindow", "2 Вых"))
        self.label_196.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_93.setTitle(_translate("MainWindow", "2 луч"))
        self.label_197.setText(_translate("MainWindow", "2 Вых"))
        self.label_198.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_94.setTitle(_translate("MainWindow", "6 луч"))
        self.label_199.setText(_translate("MainWindow", "2 Вых"))
        self.label_200.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_95.setTitle(_translate("MainWindow", "3 луч"))
        self.label_201.setText(_translate("MainWindow", "2 Вых"))
        self.label_202.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_96.setTitle(_translate("MainWindow", "7 луч"))
        self.label_204.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_97.setTitle(_translate("MainWindow", "4 луч"))
        self.label_205.setText(_translate("MainWindow", "2 Вых"))
        self.label_206.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_98.setTitle(_translate("MainWindow", "8 луч"))
        self.label_208.setText(_translate("MainWindow", "1 Вых"))
        self.gbB_4.setTitle(_translate("MainWindow", "4 сектор"))
        self.groupBox_100.setTitle(_translate("MainWindow", "1 луч"))
        self.label_209.setText(_translate("MainWindow", "2 Вых"))
        self.label_210.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_101.setTitle(_translate("MainWindow", "5 луч"))
        self.label_211.setText(_translate("MainWindow", "2 Вых"))
        self.label_212.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_102.setTitle(_translate("MainWindow", "2 луч"))
        self.label_213.setText(_translate("MainWindow", "2 Вых"))
        self.label_214.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_103.setTitle(_translate("MainWindow", "6 луч"))
        self.label_215.setText(_translate("MainWindow", "2 Вых"))
        self.label_216.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_104.setTitle(_translate("MainWindow", "3 луч"))
        self.label_217.setText(_translate("MainWindow", "2 Вых"))
        self.label_218.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_105.setTitle(_translate("MainWindow", "7 луч"))
        self.label_220.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_106.setTitle(_translate("MainWindow", "4 луч"))
        self.label_221.setText(_translate("MainWindow", "2 Вых"))
        self.label_222.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_107.setTitle(_translate("MainWindow", "8 луч"))
        self.label_224.setText(_translate("MainWindow", "1 Вых"))
        self.gbB_8.setTitle(_translate("MainWindow", "8 сектор"))
        self.groupBox_109.setTitle(_translate("MainWindow", "1 луч"))
        self.label_225.setText(_translate("MainWindow", "2 Вых"))
        self.label_226.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_110.setTitle(_translate("MainWindow", "5 луч"))
        self.label_227.setText(_translate("MainWindow", "2 Вых"))
        self.label_228.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_111.setTitle(_translate("MainWindow", "2 луч"))
        self.label_229.setText(_translate("MainWindow", "2 Вых"))
        self.label_230.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_112.setTitle(_translate("MainWindow", "6 луч"))
        self.label_231.setText(_translate("MainWindow", "2 Вых"))
        self.label_232.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_113.setTitle(_translate("MainWindow", "3 луч"))
        self.label_233.setText(_translate("MainWindow", "2 Вых"))
        self.label_234.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_114.setTitle(_translate("MainWindow", "7 луч"))
        self.label_236.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_115.setTitle(_translate("MainWindow", "4 луч"))
        self.label_237.setText(_translate("MainWindow", "2 Вых"))
        self.label_238.setText(_translate("MainWindow", "1 Вых"))
        self.groupBox_116.setTitle(_translate("MainWindow", "8 луч"))
        self.label_240.setText(_translate("MainWindow", "1 Вых"))
        self.label_31.setText(_translate("MainWindow", "МШУ Д3"))
        self.label_63.setText(_translate("MainWindow", "МШУ Д2"))
        self.label_64.setText(_translate("MainWindow", "МШУ Д3"))
        self.label_66.setText(_translate("MainWindow", "МШУ Д2"))
        self.label_241.setText(_translate("MainWindow", "МШУ Д5 - обзорные"))
        self.gbA_13.setTitle(_translate("MainWindow", "8 сект"))
        self.label_243.setText(_translate("MainWindow", "1 Вых"))
        self.gbA_15.setTitle(_translate("MainWindow", "12 сект"))
        self.label_247.setText(_translate("MainWindow", "1 Вых"))
        self.gbA_16.setTitle(_translate("MainWindow", "2 сект"))
        self.label_249.setText(_translate("MainWindow", "1 Вых"))
        self.gbA_17.setTitle(_translate("MainWindow", "6 сект"))
        self.label_251.setText(_translate("MainWindow", "1 Вых"))
        self.gbA_18.setTitle(_translate("MainWindow", "4 сект"))
        self.label_253.setText(_translate("MainWindow", "1 Вых"))
        self.gbA_14.setTitle(_translate("MainWindow", "10 сект"))
        self.label_245.setText(_translate("MainWindow", "1 Вых"))
        self.pushButton.setText(_translate("MainWindow", "Старт"))
        self.pushButton_1.setText(
            _translate(
                "MainWindow",
                "Проверить подключение"))
        self.pushButton_2.setText(_translate("MainWindow", ""))
        self.pushButton_3.setText(_translate("MainWindow", "Magic Noise"))
        self.gbA_19.setTitle(_translate("MainWindow", "11 сект"))
        self.label_248.setText(_translate("MainWindow", "1 Вых"))
        self.label_65.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_20.setTitle(_translate("MainWindow", "5 сект"))
        self.label_252.setText(_translate("MainWindow", "1 Вых"))
        self.label_45.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_21.setTitle(_translate("MainWindow", "9 сект"))
        self.label_246.setText(_translate("MainWindow", "1 Вых"))
        self.label_61.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_22.setTitle(_translate("MainWindow", "1 сект"))
        self.label_250.setText(_translate("MainWindow", "1 Вых"))
        self.label_32.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_23.setTitle(_translate("MainWindow", "3 сект"))
        self.label_254.setText(_translate("MainWindow", "1 Вых"))
        self.label_41.setText(_translate("MainWindow", "2 Вых"))
        self.gbA_24.setTitle(_translate("MainWindow", "7 сект"))
        self.label_244.setText(_translate("MainWindow", "1 Вых"))
        self.label_57.setText(_translate("MainWindow", "2 Вых"))

# конструктор окна IP-settings


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(310, 430)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SpushButton = QtWidgets.QPushButton(self.centralwidget)
        self.SpushButton.setGeometry(QtCore.QRect(40, 365, 101, 31))
        self.SpushButton.setObjectName("SpushButton")
        self.SpushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.SpushButton_2.setGeometry(QtCore.QRect(170, 365, 101, 31))
        self.SpushButton_2.setObjectName("SpushButton_2")
        self.SpushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.SpushButton_3.setGeometry(QtCore.QRect(170, 185, 101, 31))
        self.SpushButton_3.setObjectName("SpushButton_3")
        self.SpushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.SpushButton_4.setGeometry(QtCore.QRect(170, 95, 101, 31))
        self.SpushButton_4.setObjectName("SpushButton_4")
        self.SpushButton_4.setEnabled(False)
        self.SpushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.SpushButton_5.setGeometry(QtCore.QRect(170, 30, 101, 31))
        self.SpushButton_5.setObjectName("SpushButton_4")
        self.Slabel = QtWidgets.QLabel(self.centralwidget)
        self.Slabel.setGeometry(QtCore.QRect(40, 240, 221, 21))
        self.Slabel.setObjectName("Slabel")
        self.Slabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.Slabel_2.setGeometry(QtCore.QRect(40, 300, 221, 21))
        self.Slabel_2.setObjectName("Slabel_2")
        self.Slabel_3 = QtWidgets.QLabel(self.centralwidget)
        self.Slabel_3.setGeometry(QtCore.QRect(40, 390, 241, 31))
        self.Slabel_3.setObjectName("Slabel_3")
        self.Slabel_3.setStyleSheet('color: red')
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.Slabel_3.setFont(font)
        self.Slabel_3.hide()
        self.Slabel_4 = QtWidgets.QLabel(self.centralwidget)
        self.Slabel_4.setGeometry(QtCore.QRect(40, 150, 221, 31))
        self.Slabel_4.setObjectName("Slabel_4")
        self.Slabel_5 = QtWidgets.QLabel(self.centralwidget)
        self.Slabel_5.setGeometry(QtCore.QRect(40, 210, 241, 31))
        self.Slabel_5.setObjectName("Slabel_5")
        self.Slabel_5.setStyleSheet('color: red')
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.Slabel_5.setFont(font)
        self.Slabel_5.hide()
        self.Slabel_6 = QtWidgets.QLabel(self.centralwidget)
        self.Slabel_6.setGeometry(QtCore.QRect(40, 120, 241, 31))
        self.Slabel_6.setObjectName("Slabel_6")
        self.Slabel_6.setStyleSheet('color: red')
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.Slabel_6.setFont(font)
        self.Slabel_6.hide()
        self.Slabel_7 = QtWidgets.QLabel(self.centralwidget)
        self.Slabel_7.setGeometry(QtCore.QRect(40, 70, 221, 31))
        self.Slabel_7.setObjectName("Slabel_7")
        self.Slabel_8 = QtWidgets.QLabel(self.centralwidget)
        self.Slabel_8.setGeometry(QtCore.QRect(40, 5, 221, 31))
        self.Slabel_8.setObjectName("Slabel_8")
        self.SCombo = QtWidgets.QComboBox(self.centralwidget)
        self.SCombo.setGeometry(QtCore.QRect(40, 30, 101, 31))
        self.SCombo.setObjectName("SCombo")
        self.Smode = ['Инт. плата',
                      'ИП и ЦОС',
                      'ЦОС, МУП, БК']
        self.SCombo.addItems(self.Smode)
        self.SLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.SLineEdit.setGeometry(QtCore.QRect(40, 260, 51, 31))
        self.SLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.SLineEdit.setMaxLength(3)
        self.SLineEdit.setValidator(QIntValidator())
        self.SL = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SLineEdit.setFont(font)
        self.SLineEdit.setObjectName("SLineEdit")
        self.SLineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.SLineEdit_2.setGeometry(QtCore.QRect(100, 260, 51, 31))
        self.SLineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.SLineEdit_2.setMaxLength(3)
        self.SLineEdit_2.setValidator(QIntValidator())
        self.SL_2 = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SLineEdit_2.setFont(font)
        self.SLineEdit_2.setObjectName("SLineEdit_2")
        self.SLineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.SLineEdit_3.setGeometry(QtCore.QRect(160, 260, 51, 31))
        self.SLineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.SLineEdit_3.setMaxLength(3)
        self.SLineEdit_3.setValidator(QIntValidator())
        self.SL_3 = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SLineEdit_3.setFont(font)
        self.SLineEdit_3.setObjectName("SLineEdit_3")
        self.SLineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.SLineEdit_4.setGeometry(QtCore.QRect(220, 260, 51, 31))
        self.SLineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.SLineEdit_4.setMaxLength(3)
        self.SLineEdit_4.setValidator(QIntValidator())
        self.SL_4 = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SLineEdit_4.setFont(font)
        self.SLineEdit_4.setObjectName("SLineEdit_4")
        self.SLineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.SLineEdit_5.setGeometry(QtCore.QRect(40, 320, 51, 31))
        self.SLineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.SLineEdit_5.setMaxLength(3)
        self.SLineEdit_5.setValidator(QIntValidator())
        self.SL_5 = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SLineEdit_5.setFont(font)
        self.SLineEdit_5.setObjectName("SLineEdit_5")
        self.SLineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.SLineEdit_6.setGeometry(QtCore.QRect(100, 320, 51, 31))
        self.SLineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.SLineEdit_6.setMaxLength(3)
        self.SLineEdit_6.setValidator(QIntValidator())
        self.SL_6 = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SLineEdit_6.setFont(font)
        self.SLineEdit_6.setObjectName("SLineEdit_6")
        self.SLineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.SLineEdit_7.setGeometry(QtCore.QRect(160, 320, 51, 31))
        self.SLineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.SLineEdit_7.setMaxLength(3)
        self.SLineEdit_7.setValidator(QIntValidator())
        self.SL_7 = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SLineEdit_7.setFont(font)
        self.SLineEdit_7.setObjectName("SLineEdit_7")
        self.SLineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.SLineEdit_8.setGeometry(QtCore.QRect(220, 320, 51, 31))
        self.SLineEdit_8.setAlignment(QtCore.Qt.AlignCenter)
        self.SLineEdit_8.setMaxLength(3)
        self.SLineEdit_8.setValidator(QIntValidator())
        self.SL_8 = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SLineEdit_8.setFont(font)
        self.SLineEdit_8.setObjectName("SLineEdit_8")
        self.SLineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.SLineEdit_9.setGeometry(QtCore.QRect(40, 185, 101, 31))
        self.SLineEdit_9.setAlignment(QtCore.Qt.AlignCenter)
        self.SLineEdit_9.setMaxLength(3)
        self.SLineEdit_9.setValidator(QIntValidator())
        self.SL_9 = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SLineEdit_9.setFont(font)
        self.SLineEdit_9.setObjectName("SLineEdit_9")
        self.SSpinBox_10 = QtWidgets.QSpinBox(self.centralwidget)
        self.SSpinBox_10.setGeometry(QtCore.QRect(40, 95, 101, 31))
        self.SSpinBox_10.setRange(50, 500)
        self.SSpinBox_10.setAlignment(QtCore.Qt.AlignCenter)
        self.SL_10 = ''
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        self.SSpinBox_10.setFont(font)
        self.SSpinBox_10.setObjectName("SSpinBox_10")
        self.SSpinBox_10.setEnabled(False)
        SettingsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SettingsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 300, 21))
        self.menubar.setObjectName("menubar")
        SettingsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SettingsWindow)
        self.statusbar.setObjectName("statusbar")
        SettingsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(
            _translate("SettingsWindow", "Settings"))
        self.SpushButton.setText(
            _translate("SettingsWindow",
                       "Установить IP"))
        self.SpushButton_2.setText(
            _translate(
                "SettingsWindow",
                "Закрыть"))
        self.SpushButton_3.setText(
            _translate(
                "SettingsWindow",
                "Применить"))
        self.SpushButton_4.setText(
            _translate(
                "SettingsWindow",
                "Применить"))
        self.SpushButton_5.setText(
            _translate(
                "SettingsWindow",
                "Применить"))
        self.Slabel.setText(
            _translate(
                "SettingsWindow",
                "Введите IP-адресс PV-4201:"))
        self.Slabel_2.setText(
            _translate(
                "SettingsWindow",
                "Введите IP-адресс PV-4202:"))
        self.Slabel_3.setText(
            _translate(
                "SettingsWindow",
                "Необходимо заполнить все поля IP-адреса!"))
        self.Slabel_4.setText(
            _translate(
                "SettingsWindow",
                "Введите пороговое значение\n"
                "чувствительности амплитуды, дБ:"))
        self.Slabel_5.setText(
            _translate(
                "SettingsWindow",
                "Необходимо задать пороговое значение!"))
        self.Slabel_6.setText(
            _translate(
                "SettingsWindow",
                "Необходимо задать время задержки!"))
        self.Slabel_7.setText(
            _translate(
                "SettingsWindow",
                "Введите время задержки МШУ (50-500), мкс:"))
        self.Slabel_8.setText(
            _translate(
                "SettingsWindow",
                "Выберите режим работы ЦОС:"))


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()  # маска для обращения к конструктору основного окна
        self.ui.setupUi(self)
        self.window = QtWidgets.QMainWindow()
        self.uiS = Ui_SettingsWindow()  # маска для обращения к конструктору окна IP-settings
        self.uiS.setupUi(self.window)
        # сигналы кнопок интерфейса (выполняют соответствующие методы данного класса)
        self.ui.pushButton.clicked.connect(self.btnClicked)
        self.ui.pushButton_1.clicked.connect(self.btn_1Clicked)
        self.ui.pushButton_2.clicked.connect(self.IP_btn)
        self.ui.pushButton_3.clicked.connect(self.Noise_btn)
        self.uiS.SpushButton.clicked.connect(self.ChangeIP)
        self.uiS.SpushButton_2.clicked.connect(self.Quit)
        self.uiS.SpushButton_3.clicked.connect(self.ChangeDB)
        self.uiS.SpushButton_4.clicked.connect(self.ChangeDelay)
        self.uiS.SpushButton_5.clicked.connect(self.ChangeMode)
        self.ui.text = 'Пороговое значение чувствительности: ' + \
                       str(self.ui.db) + ', дБ\n'
        # запись в переменную text информации о текущих IP-адресах касет
        self.ui.text = 'IP-адрес PV-4201: ' + self.ui.IP_4201 + '\n'
        self.ui.text += 'IP-адрес PV-4202: ' + self.ui.IP_4202 + '\n'
        # вывод значения переменной text в текстовое окно
        self.ui.textEdit.setText(self.ui.text)

    """ Метод получения логов при ошибке """

    def log_uncaught_exceptions(ex_cls, ex, tb):
        text = '{}: {}:\n'.format(ex_cls.__name__, ex)
        import traceback
        text += ''.join(traceback.format_tb(tb))

        print(text)
        quit()

    sys.excepthook = log_uncaught_exceptions

    def Noise_btn(self):
        ang_d2_d4_c = (15, 75, 135, 195, 255, 315)
        ang_d5_c = (45, 105, 165, 225, 285, 345)
        ang_d2_d3_s = (15, 45, 75, 105, 135, 165, 195, 225, 255, 285, 315, 345)
        ang_d4_s = [x for x in arange(1.875, 360, 3.75) if not x // 30 % 2]
        ang_d5_s = [x for x in arange(31.875, 360, 3.75) if x // 30 % 2]
        fig = make_subplots(rows=2, cols=2, specs=[
                            [{'type': 'polar'}] * 2] * 2)
        fig.add_trace(go.Scatterpolar(
            name='D2',
            r=self.ui.plot['D2'][23:],
            theta=ang_d2_d4_c,
        ), 1, 1)
        fig.add_trace(go.Scatterpolar(
            name='D3',
            r=self.ui.plot['D3'][23:],
            theta=ang_d2_d4_c,
        ), 1, 2)
        fig.add_trace(go.Scatterpolar(
            name='D4',
            r=self.ui.plot['D4'][83:],
            theta=ang_d2_d4_c,
        ), 2, 1)
        fig.add_trace(go.Scatterpolar(
            name='D5',
            r=self.ui.plot['D5'][83:],
            theta=ang_d5_c,
        ), 2, 2)
        fig.add_trace(go.Scatterpolar(
            name='D2',
            visible=False,
            r=self.ui.plot['D2'][:23:2],
            theta=ang_d2_d3_s,
        ), 1, 1)
        fig.add_trace(go.Scatterpolar(
            name='D3',
            visible=False,
            r=self.ui.plot['D3'][:23:2],
            theta=ang_d2_d3_s,
        ), 1, 2)
        fig.add_trace(go.Scatterpolar(
            name='D4',
            r=self.ui.plot['D4'][:81:2] + self.ui.plot['D4'][82:84],
            visible=False,
            theta=ang_d4_s,
        ), 2, 1)
        fig.add_trace(go.Scatterpolar(
            name='D5',
            visible=False,
            r=self.ui.plot['D5'][:81:2] + self.ui.plot['D5'][82:84],
            theta=ang_d5_s,
        ), 2, 2)

        fig.update_traces(fill='toself')
        fig.update_layout(
            polar1=dict(
                angularaxis=dict(
                    direction="clockwise",
                    dtick=15)
            ),
            polar2=dict(
                angularaxis=dict(
                    direction="clockwise",
                    dtick=15)
            ),
            polar3=dict(
                angularaxis=dict(
                    direction="clockwise",
                    dtick=15)
            ),
            polar4=dict(
                angularaxis=dict(
                    direction="clockwise",
                    dtick=15)
            )
        )

        fig.layout.update(
            updatemenus=[
                go.layout.Updatemenu(
                    type="buttons", direction="right", active=0, x=0.1, y=1.2,
                    buttons=list(
                        [
                            dict(
                                label="Circle", method="update",
                                args=[{"visible": [True, True, True, True, False, False, False, False]}]
                            ),
                            dict(
                                label="Sector", method="update",
                                args=[{"visible": [False, False, False, False, True, True, True, True]}]
                            )
                        ]
                    )
                )
            ]
        )

        # Add annotation
        fig.update_layout(
            annotations=[
                dict(text="Trace type:", showarrow=False,
                     x=0, y=1.08, yref="paper", align="left")
            ]
        )

        fig.show()

    def Quit(self):
        # разблокировка неактивных виджетов
        self.uiS.SpushButton_4.setEnabled(True)
        self.uiS.SSpinBox_10.setEnabled(True)
        self.uiS.SpushButton_5.setEnabled(True)
        self.uiS.SCombo.setEnabled(True)
        # отображение принятых значений в главном текстовом окне
        TextMode = ['только интерфейсная плата.',
                    'интерфейсная плата и блок ЦОС',
                    'блок ЦОС, МУП, БК']
        self.ui.text = 'Режим работы: ' + \
                       TextMode[self.uiS.SCombo.currentIndex()] + '\n'
        self.ui.text += 'Пороговое значение чувствительности: ' + \
                        str(self.ui.db) + ', дБ\n'
        self.ui.text += 'IP-адрес PV-4201: ' + self.ui.IP_4201 + '\n'
        self.ui.text += 'IP-адрес PV-4202: ' + self.ui.IP_4202 + '\n'
        self.ui.textEdit.setText(self.ui.text)
        QApplication.processEvents()
        # закрытие окна настроек
        self.window.close()

    # код работы кнопки "Применить" (смена режима)
    def ChangeMode(self):
        # переменная в которую записывается текущий индекс выпадающего меню
        ComboIndex = self.uiS.SCombo.currentIndex()
        # создание списков с набором команд для различных режимов работы
        pauseList = [self.ui.c_pause_1, self.ui.c_pause_2, self.ui.c_pause_3]
        technList = [self.ui.c_techn_1, self.ui.c_techn_2, self.ui.c_techn_3]
        # запись в рабочую переменную режима соответствующего индексу выпадающего меню
        self.ui.c_pause = pauseList[ComboIndex]
        self.ui.c_techn = technList[ComboIndex]
        self.uiS.SpushButton_5.setStyleSheet('color: green')
        # запрет пользователю вносить дальнейшие изменения в режим работы,
        # поскольку далее в команде 0х80 необходимо изменить регистры задержки МШУ
        self.uiS.SpushButton_5.setEnabled(False)
        self.uiS.SCombo.setEnabled(False)
        # разблокировка интерфейса изменения задержки МШУ, для
        # последовательной корректировки команды 0х80
        self.uiS.SpushButton_4.setEnabled(True)
        self.uiS.SSpinBox_10.setEnabled(True)

    # код работы кнопки "Применить"(задержка),
    # находящейся в окне настроек IP-адреса
    def ChangeDelay(self):
        # запись в переменную, значения записанного в spinbox
        self.uiS.SL_10 = self.uiS.SSpinBox_10.value()
        # преобразование микросекунд в значение задержки
        # в шестнадцатиричном формате
        eq = int((int(self.uiS.SL_10) * (10 ** 6)) / 8000)
        eq = str(hex(eq))
        eq = eq.replace("0x", "")
        # расстановка старшего и младшего байта в правильной последовательности
        eq = eq[2:] + eq[:2]
        # внесение изменений в регистры задержки команды 0х80
        self.ui.c_pause = self.ui.c_pause[:24] + eq + self.ui.c_pause[28:]
        self.ui.c_techn = self.ui.c_techn[:24] + eq + self.ui.c_techn[28:]
        self.uiS.SpushButton_4.setStyleSheet('color: green')
        # Запрет на внесение
        self.uiS.SpushButton_4.setEnabled(False)
        self.uiS.SSpinBox_10.setEnabled(False)

    # код работы кнопки "Применить(порог)",
    # находящейся в окне настроек IP-адреса
    def ChangeDB(self):
        self.uiS.SL_9 = self.uiS.SLineEdit_9.text()
        # проверка на пустое поля ввода
        if self.uiS.SL_9 == '':
            # вывод предупреждения
            self.uiS.Slabel_5.show()
            self.uiS.SpushButton_3.setStyleSheet('color: red')
        else:
            # изменение значения переменной с порогом
            self.ui.db = int(self.uiS.SL_9)
            self.uiS.Slabel_5.hide()
            self.uiS.SpushButton_3.setStyleSheet('color: green')

    # код работы кнопки "Установить IP",
    # находящейся в окне настроек IP-адреса
    def ChangeIP(self):
        # массив переменных в которые будут записаны
        # данные IP-адесов разделенные по маске
        IP_var = [
            self.uiS.SL,
            self.uiS.SL_2,
            self.uiS.SL_3,
            self.uiS.SL_4,
            self.uiS.SL_5,
            self.uiS.SL_6,
            self.uiS.SL_7,
            self.uiS.SL_8]

        # массив полей ввода из которых будут извлечены
        # текущие данные IP-адесов
        IP_ins = [
            self.uiS.SLineEdit.text(),
            self.uiS.SLineEdit_2.text(),
            self.uiS.SLineEdit_3.text(),
            self.uiS.SLineEdit_4.text(),
            self.uiS.SLineEdit_5.text(),
            self.uiS.SLineEdit_6.text(),
            self.uiS.SLineEdit_7.text(),
            self.uiS.SLineEdit_8.text()]

        # запись данных из полей ввода IP-адресов
        # в соответствующие переменные
        IP_var[:] = IP_ins[:]
        # логическая переменная для проверки
        # полей ввода на пустые значения
        bool = True
        # проверка на пустое значение в полях ввода
        for i in IP_var:
            if i == '':
                # отображение предупреждения о пустом поле ввода
                self.uiS.Slabel_3.show()
                self.uiS.SpushButton.setStyleSheet('color: red')
                bool = False
            else:
                pass

        # код записи данных в переменные IP-адресов
        if bool == True:
            IP_4201 = []
            IP_4202 = []
            # создание массивов со значениями IP-адресов
            for i in IP_var[:4]:
                IP_4201.append(i)
            for i in IP_var[4:]:
                IP_4202.append(i)
            # запись IP-адреса PV-4201 из массива
            self.ui.IP_4201 = '.'.join(IP_4201)
            # запись IP-адреса PV-4202 из массива
            self.ui.IP_4202 = '.'.join(IP_4202)
            self.uiS.Slabel_3.hide()
            self.uiS.SpushButton.setStyleSheet('color: green')

    # код работы кнопки "Шестеренка"
    def IP_btn(self):
        # выставление всех значений и цветов лэйблов
        # разделение IP-адреса по маске
        IP_4201 = self.ui.IP_4201.split('.')
        IP_4202 = self.ui.IP_4202.split('.')
        # вывод значений IP-адреса по маске в окно настроек
        self.uiS.SLineEdit.setText(IP_4201[0])
        self.uiS.SLineEdit_2.setText(IP_4201[1])
        self.uiS.SLineEdit_3.setText(IP_4201[2])
        self.uiS.SLineEdit_4.setText(IP_4201[3])
        self.uiS.SLineEdit_5.setText(IP_4202[0])
        self.uiS.SLineEdit_6.setText(IP_4202[1])
        self.uiS.SLineEdit_7.setText(IP_4202[2])
        self.uiS.SLineEdit_8.setText(IP_4202[3])
        self.uiS.SLineEdit_9.setText(str(self.ui.db))
        self.uiS.Slabel_3.hide()
        self.uiS.Slabel_5.hide()
        self.uiS.Slabel_6.hide()
        self.uiS.SpushButton.setStyleSheet('color: black')
        self.uiS.SpushButton_3.setStyleSheet('color: black')
        self.uiS.SpushButton_4.setStyleSheet('color: black')
        self.uiS.SpushButton_5.setStyleSheet('color: black')
        # открытие окна настроек
        self.window.show()

    def btn_1Clicked(self):
        self.ui.text = 'Запрос ответа от PV-4201 и PV-4202...\n'
        self.ui.textEdit.setText(self.ui.text)
        self.ui.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        QApplication.processEvents()
        # response_list_0 = ping(self.ui.IP_4201, size=40, count=10)  # PV-4201
        # response_list_1 = ping(self.ui.IP_4202, size=40, count=10)  # PV-4202
        #
        # if 0 < response_list_0.rtt_avg_ms < 2 and 0 < response_list_1.rtt_avg_ms < 2:  # проверка времени пинга
        #     self.ui.text = 'Подключение установлено.\n'
        #     self.ui.text += 'Нажмите кнопку Старт...\n'
        #     self.ui.pushButton.setEnabled(True)
        #     self.ui.pushButton_2.setEnabled(False)
        #     self.ui.PING = True
        #
        # else:
        #     self.ui.text = 'Ответа нет!\n'
        #     if 0 < response_list_0.rtt_avg_ms < 1:
        #         pass
        #     else:
        #         self.ui.text += 'Проверьте подключение PV-4201!\n'
        #         self.ui.PING = False
        #     if 0 < response_list_1.rtt_avg_ms < 1:
        #         pass
        #     else:
        #         self.ui.text += 'Проверьте подключение PV-4202!\n'
        #         self.ui.PING = False
        #     self.ui.pushButton.setEnabled(False)
        #     self.ui.pushButton_2.setEnabled(True)
        # self.ui.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        # self.ui.textEdit.setText(self.ui.text)

        """
        Код выше раскомментить. Код ниже для имитации работы кнопки "Проверка подключения" (подлежит удалению).
        """
        self.ui.PING = True  # изменить значение переменной для наличия/отсутствия подключения при имитации

        if self.ui.PING:
            self.ui.text = 'Подключение установлено.\n'
            self.ui.text += 'Нажмите кнопку Старт...\n'
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton_2.setEnabled(False)
        else:
            time.sleep(5)
            self.ui.text = 'Ответа нет!\n'
            self.ui.text += 'Проверьте подключение PV-4201!\n'
            self.ui.text += 'Проверьте подключение PV-4202!\n'
            self.ui.pushButton.setEnabled(False)
            self.ui.pushButton_2.setEnabled(True)

        self.ui.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.ui.textEdit.setText(self.ui.text)

    def btnClicked(self):

        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_1.setEnabled(False)

        d2 = (
            self.ui.d2_1_1,
            self.ui.d2_1_2,
            self.ui.d2_2_1,
            self.ui.d2_2_2,
            self.ui.d2_3_1,
            self.ui.d2_3_2,
            self.ui.d2_4_1,
            self.ui.d2_4_2,
            self.ui.d2_5_1,
            self.ui.d2_5_2,
            self.ui.d2_6_1,
            self.ui.d2_6_2,
            self.ui.d2_7_1,
            self.ui.d2_7_2,
            self.ui.d2_8_1,
            self.ui.d2_8_2,
            self.ui.d2_9_1,
            self.ui.d2_9_2,
            self.ui.d2_10_1,
            self.ui.d2_10_2,
            self.ui.d2_11_1,
            self.ui.d2_11_2,
            self.ui.d2_12_1,
            self.ui.d2_12_2,
            self.ui.d24_1_1,
            self.ui.d24_3_1,
            self.ui.d24_5_1,
            self.ui.d24_7_1,
            self.ui.d24_9_1,
            self.ui.d24_11_1)
        d3 = (
            self.ui.d3_1_1,
            self.ui.d3_1_2,
            self.ui.d3_2_1,
            self.ui.d3_2_2,
            self.ui.d3_3_1,
            self.ui.d3_3_2,
            self.ui.d3_4_1,
            self.ui.d3_4_2,
            self.ui.d3_5_1,
            self.ui.d3_5_2,
            self.ui.d3_6_1,
            self.ui.d3_6_2,
            self.ui.d3_7_1,
            self.ui.d3_7_2,
            self.ui.d3_8_1,
            self.ui.d3_8_2,
            self.ui.d3_9_1,
            self.ui.d3_9_2,
            self.ui.d3_10_1,
            self.ui.d3_10_2,
            self.ui.d3_11_1,
            self.ui.d3_11_2,
            self.ui.d3_12_1,
            self.ui.d3_12_2,
            self.ui.d24_1_1,
            self.ui.d24_3_1,
            self.ui.d24_5_1,
            self.ui.d24_7_1,
            self.ui.d24_9_1,
            self.ui.d24_11_1)
        d4 = (
            self.ui.d4_1_1_1,
            self.ui.d4_1_1_2,
            self.ui.d4_1_2_1,
            self.ui.d4_1_2_2,
            self.ui.d4_1_3_1,
            self.ui.d4_1_3_2,
            self.ui.d4_1_4_1,
            self.ui.d4_1_4_2,
            self.ui.d4_1_5_1,
            self.ui.d4_1_5_2,
            self.ui.d4_1_6_1,
            self.ui.d4_1_6_2,
            self.ui.d4_1_7_1,
            self.ui.d4_1_8_1,
            self.ui.d4_3_1_1,
            self.ui.d4_3_1_2,
            self.ui.d4_3_2_1,
            self.ui.d4_3_2_2,
            self.ui.d4_3_3_1,
            self.ui.d4_3_3_2,
            self.ui.d4_3_4_1,
            self.ui.d4_3_4_2,
            self.ui.d4_3_5_1,
            self.ui.d4_3_5_2,
            self.ui.d4_3_6_1,
            self.ui.d4_3_6_2,
            self.ui.d4_3_7_1,
            self.ui.d4_3_8_1,
            self.ui.d4_5_1_1,
            self.ui.d4_5_1_2,
            self.ui.d4_5_2_1,
            self.ui.d4_5_2_2,
            self.ui.d4_5_3_1,
            self.ui.d4_5_3_2,
            self.ui.d4_5_4_1,
            self.ui.d4_5_4_2,
            self.ui.d4_5_5_1,
            self.ui.d4_5_5_2,
            self.ui.d4_5_6_1,
            self.ui.d4_5_6_2,
            self.ui.d4_5_7_1,
            self.ui.d4_5_8_1,
            self.ui.d4_7_1_1,
            self.ui.d4_7_1_2,
            self.ui.d4_7_2_1,
            self.ui.d4_7_2_2,
            self.ui.d4_7_3_1,
            self.ui.d4_7_3_2,
            self.ui.d4_7_4_1,
            self.ui.d4_7_4_2,
            self.ui.d4_7_5_1,
            self.ui.d4_7_5_2,
            self.ui.d4_7_6_1,
            self.ui.d4_7_6_2,
            self.ui.d4_7_7_1,
            self.ui.d4_7_8_1,
            self.ui.d4_9_1_1,
            self.ui.d4_9_1_2,
            self.ui.d4_9_2_1,
            self.ui.d4_9_2_2,
            self.ui.d4_9_3_1,
            self.ui.d4_9_3_2,
            self.ui.d4_9_4_1,
            self.ui.d4_9_4_2,
            self.ui.d4_9_5_1,
            self.ui.d4_9_5_2,
            self.ui.d4_9_6_1,
            self.ui.d4_9_6_2,
            self.ui.d4_9_7_1,
            self.ui.d4_9_8_1,
            self.ui.d4_11_1_1,
            self.ui.d4_11_1_2,
            self.ui.d4_11_2_1,
            self.ui.d4_11_2_2,
            self.ui.d4_11_3_1,
            self.ui.d4_11_3_2,
            self.ui.d4_11_4_1,
            self.ui.d4_11_4_2,
            self.ui.d4_11_5_1,
            self.ui.d4_11_5_2,
            self.ui.d4_11_6_1,
            self.ui.d4_11_6_2,
            self.ui.d4_11_7_1,
            self.ui.d4_11_8_1,
            self.ui.d24_1_2,
            self.ui.d24_3_2,
            self.ui.d24_5_2,
            self.ui.d24_7_2,
            self.ui.d24_9_2,
            self.ui.d24_11_2)
        d5 = (
            self.ui.d5_2_1_1,
            self.ui.d5_2_1_2,
            self.ui.d5_2_2_1,
            self.ui.d5_2_2_2,
            self.ui.d5_2_3_1,
            self.ui.d5_2_3_2,
            self.ui.d5_2_4_1,
            self.ui.d5_2_4_2,
            self.ui.d5_2_5_1,
            self.ui.d5_2_5_2,
            self.ui.d5_2_6_1,
            self.ui.d5_2_6_2,
            self.ui.d5_2_7_1,
            self.ui.d5_2_8_1,
            self.ui.d5_4_1_1,
            self.ui.d5_4_1_2,
            self.ui.d5_4_2_1,
            self.ui.d5_4_2_2,
            self.ui.d5_4_3_1,
            self.ui.d5_4_3_2,
            self.ui.d5_4_4_1,
            self.ui.d5_4_4_2,
            self.ui.d5_4_5_1,
            self.ui.d5_4_5_2,
            self.ui.d5_4_6_1,
            self.ui.d5_4_6_2,
            self.ui.d5_4_7_1,
            self.ui.d5_4_8_1,
            self.ui.d5_6_1_1,
            self.ui.d5_6_1_2,
            self.ui.d5_6_2_1,
            self.ui.d5_6_2_2,
            self.ui.d5_6_3_1,
            self.ui.d5_6_3_2,
            self.ui.d5_6_4_1,
            self.ui.d5_6_4_2,
            self.ui.d5_6_5_1,
            self.ui.d5_6_5_2,
            self.ui.d5_6_6_1,
            self.ui.d5_6_6_2,
            self.ui.d5_6_7_1,
            self.ui.d5_6_8_1,
            self.ui.d5_8_1_1,
            self.ui.d5_8_1_2,
            self.ui.d5_8_2_1,
            self.ui.d5_8_2_2,
            self.ui.d5_8_3_1,
            self.ui.d5_8_3_2,
            self.ui.d5_8_4_1,
            self.ui.d5_8_4_2,
            self.ui.d5_8_5_1,
            self.ui.d5_8_5_2,
            self.ui.d5_8_6_1,
            self.ui.d5_8_6_2,
            self.ui.d5_8_7_1,
            self.ui.d5_8_8_1,
            self.ui.d5_10_1_1,
            self.ui.d5_10_1_2,
            self.ui.d5_10_2_1,
            self.ui.d5_10_2_2,
            self.ui.d5_10_3_1,
            self.ui.d5_10_3_2,
            self.ui.d5_10_4_1,
            self.ui.d5_10_4_2,
            self.ui.d5_10_5_1,
            self.ui.d5_10_5_2,
            self.ui.d5_10_6_1,
            self.ui.d5_10_6_2,
            self.ui.d5_10_7_1,
            self.ui.d5_10_8_1,
            self.ui.d5_12_1_1,
            self.ui.d5_12_1_2,
            self.ui.d5_12_2_1,
            self.ui.d5_12_2_2,
            self.ui.d5_12_3_1,
            self.ui.d5_12_3_2,
            self.ui.d5_12_4_1,
            self.ui.d5_12_4_2,
            self.ui.d5_12_5_1,
            self.ui.d5_12_5_2,
            self.ui.d5_12_6_1,
            self.ui.d5_12_6_2,
            self.ui.d5_12_7_1,
            self.ui.d5_12_8_1,
            self.ui.d5o_2_1,
            self.ui.d5o_4_1,
            self.ui.d5o_6_1,
            self.ui.d5o_8_1,
            self.ui.d5o_10_1,
            self.ui.d5o_12_1)

        # Эталонные значение № кассет ЦОС
        std_d2 = (4, 1, 8, 5, 4, 2, 8, 6, 4, 3, 8, 7, 4, 1,
                  8, 5, 4, 2, 8, 6, 4, 3, 8, 7, 1, 5, 2, 6, 3, 7)
        std_d4 = (1, 2, 5, 6, 1, 3, 5, 7, 1, 4, 5, 8, 1, 5,
                  1, 2, 5, 6, 1, 3, 5, 7, 1, 4, 5, 8, 1, 5,
                  1, 2, 5, 6, 1, 3, 5, 7, 1, 4, 5, 8, 1, 5,
                  1, 2, 5, 6, 1, 3, 5, 7, 1, 4, 5, 8, 1, 5,
                  1, 2, 5, 6, 1, 3, 5, 7, 1, 4, 5, 8, 1, 5,
                  1, 2, 5, 6, 1, 3, 5, 7, 1, 4, 5, 8, 1, 5, 2, 3, 4, 8, 7, 6)
        std_d5 = (1, 3, 2, 4, 1, 5, 2, 6, 1, 7, 2, 8, 1, 2,
                  1, 3, 2, 4, 1, 5, 2, 6, 1, 7, 2, 8, 1, 2,
                  1, 3, 2, 4, 1, 5, 2, 6, 1, 7, 2, 8, 1, 2,
                  1, 3, 2, 4, 1, 5, 2, 6, 1, 7, 2, 8, 1, 2,
                  1, 3, 2, 4, 1, 5, 2, 6, 1, 7, 2, 8, 1, 2,
                  1, 3, 2, 4, 1, 5, 2, 6, 1, 7, 2, 8, 1, 2, 3, 5, 7, 8, 6, 4)

        if self.ui.PING:

            # Команда 0х80 для перевода блока ЦОС в режим паузы
            c_pause = '2e:00:80:00:00:00:00:14:00:00:00:00:00:00:00:00:38:00:00:00:' \
                      '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:00:00:4c:80'
            c_pause = c_pause.split(':')
            c_pause = ''.join(c_pause)  # преобразует байты в строку
            # Команда ?
            c_techn = '2e:00:80:00:00:00:00:14:00:00:00:00:00:00:00:00:38:00:00:00:' \
                      '08:00:64:00:64:00:00:00:00:00:00:00:00:00:00:00:00:00:64:00:00:00:10:00:05:00:4c:80'
            c_techn = c_techn.split(':')
            c_techn = ''.join(c_techn)  # преобразует байты в строку
            # Команда 0х8А для перевода блока ЦОС в режим тестирования и смены
            # частоты
            c_freq = '26:00:8a:00:02:00:08:00:03:00:00:00:00:00:00:00:00:00:00:00:' \
                     '00:00:00:00:00:00:00:00:08:00:ff:0f:ff:00:01:00:01:00:36:00'
            c_freq = c_freq.split(':')
            c_freq = ''.join(c_freq)

            """
            При входе в технологический режим предполагается, что блок ЦОС предварительно переведен
            в режим паузы командой 0х80, а затем РПУ переведен в Режим тестирования и настроен на
            требуемую частоту приема и прочие параметры, при помощи отладочного пакета управления РПУ 0х8А.
            """

            """ Перевод в технологический режим  ЦОС 4201 НД """
            # sock_send = socket.socket(
            #     socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            # sock_send.bind(('', 2000))
            # # Перевод блока ЦОС в режим паузы командой 0х80
            # sock_send.sendto(bytes.fromhex(c_pause), (IP_4201, 2000))
            # time.sleep(1)
            # # Перевод РПУ переведен в режим тестирования (командой 0х8А????)
            # sock_send.sendto(bytes.fromhex(c_techn), (IP_4201, 2000))
            # """ Перевод в технологический режим ЦОС 4201 ВД """
            # sock_send = socket.socket(
            #     socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            # sock_send.bind(('', 2000))
            # # Перевод блока ЦОС в режим паузы командой 0х80
            # sock_send.sendto(bytes.fromhex(c_pause), (IP_4202, 2000))
            # time.sleep(1)
            # # Перевод РПУ переведен в режим тестирования (командой 0х8А????)
            # sock_send.sendto(bytes.fromhex(c_techn), (IP_4202, 2000))

            # обращение к интерфейсу
            bands = {'D2': d2, 'D3': d3, 'D4': d4, 'D5': d5}
            # длина поссылки
            band_len = {'D2': 244, 'D3': 244, 'D4': 724, 'D5': 724}
            # ip адрес
            ip = {
                'D2': self.ui.IP_4201,
                'D3': self.ui.IP_4201,
                'D4': self.ui.IP_4201,
                'D5': self.ui.IP_4202}
            # код частоты
            freq = {'D2': '00', 'D3': '08', 'D4': '18', 'D5': '00'}
            # эталонный массив № кассет ЦОС
            std = {'D2': std_d2, 'D3': std_d2, 'D4': std_d4, 'D5': std_d5}
            # текст для бегущей строки
            band_rus = {'D2': 'Д2 - ', 'D3': 'Д3 - ', 'D4': 'Д4 - ', 'D5': 'Д5 - '}
            # инициализация словаря для хранения амплитуд кассет ЦОС
            plot = {}

            for band in bands:
                # Отладочный пакет управления РПУ 0х8А с установленной частотой
                # freq[band] ГГц
                c_freq = c_freq[:12] + freq[band] + c_freq[14:]
                # # Настройка порта
                # sock_send = socket.socket(
                #     socket.AF_INET, socket.SOCK_DGRAM)  # UDP
                # sock_send.bind(('', 2000))
                # # Отправка отладочного пакета управления РПУ 0х8А с установленной частотой freq[band] ГГц на адрес ip[band]
                # sock_send.sendto(bytes.fromhex(c_freq), (ip[band], 2000))
                time.sleep(0.2)  # определить задержу в будущем

                data = [
                    random.randint(
                        0,
                        20) for i in range(
                        band_len[band])]
                # Прием ответа на запрос
                while True:
                    # # формируем буфер
                    # data, adrr = sock_listen.recvfrom(2048)
                    # # проверка посылки на длительность
                    if len(data) == band_len[band]:
                        # # преобразование посылки из hex в dec (младший байт
                        # # первый, старший байт второй)
                        # data = list(struct.unpack('<' + 'H' * band_len[band],
                        # data))  # преобразование посылки
                        pass
                    else:
                        # ждем ответа, если не пришел пакет длительностью
                        # band_len[band]
                        continue

                    # удаление первых 4 символов протокола(размер посылки, команда, кол-во пакетов,
                    # номер пакета)
                    del data[0:4]
                    # деление посылки на отрезки по 8 каналов
                    data = [data[i:i + 8] for i in range(0, len(data), 8)]
                    # print(data)
                    # амплитуда шума на входе канала (ch_level - номера кассет
                    # с неподключенным входом ЦОС)
                    ch_level = [index + 1 for index,
                                value in enumerate(list(map(statistics.mean,
                                                            zip(*data)))) if value < 9]
                    # поиск номера кассеты с максимальной амплитудой в блоке
                    # ЦОС
                    max_lst_id = [i.index(max(i)) + 1 for i in data]
                    # массив значений максимумов для каждого состояния (среди 8
                    # кассет ЦОС)
                    max_lst = (i.pop(i.index(max(i))) for i in data)
                    # массив средне арифметических значений для каждого
                    # состояния (среди 8 кассет ЦОС)
                    mean_lst = (statistics.mean(i) for i in data)
                    # массив средне арифметических значений к максимальному для
                    # каждого состояния (среди 8 кассет ЦОС)
                    comparison = (i for i in map(operator.truediv, max_lst, mean_lst))
                    # пороговое значение для определения работоспособности МШУ
                    db = self.ui.db

                    # Эти данные надо применить для диаграмм
                    # запись массива максимальных амплитуд для каждого диапазона в словарь.
                    # Доступ к массиву амлпитуд диапазона по ключу band
                    self.ui.plot[band] = max_lst_id
                    # вывод массив амплитуд
                    # print(self.ui.plot[band])

                    """
                    Число "к = max_lst/mean_lst" (разы) является порогом определения работоспособности МШУ.
                    Не рабочий усилитель в МШУ не будет вностить вклад в уровениь шумовой полки приемника.
                    Значение порога необходимо определить в ходе тестирования (примерно 10 дБ).
                    Его необходимо задавать из окна на лицевой панели, при этом пользователь должен задавать его в Дб
                    Формула к = 10^(дБ*0,1)   (Дб = 10*lg(k))
                    """
                    # поиск совпадений с эталонным массивом
                    mshu_status = ['broken' if k < 10**(db * 0.1) else i for i, k in zip(
                        map(operator.eq, std[band], max_lst_id), comparison)]
                    # поиск совпадений с массивом кассет с неподключенным
                    # входом ЦОС
                    mshu_status = (
                        'empty' if k in ch_level else i for i, k in zip(
                            mshu_status, std[band]))
                    k = -1
                    for i in mshu_status:
                        k += 1
                        if i is True:
                            color = "background-color: rgb(10, 150, 10);"
                            status = " connected\n"
                        elif i == 'broken':
                            color = "background-color: rgb(232, 225, 16);"
                            status = " possibly broken\n"
                        elif i == 'empty':
                            color = "background-color: rgb(48, 41, 41);"
                            status = " has no input noise\n"
                        elif i is False:
                            color = "background-color: rgb(150, 10, 10);"
                            status = " not connected\n"
                        # Обращение к интерфейсу (цвет ячейки, надпись в
                        # строке)
                        bands[band][k].setStyleSheet(
                            color)
                        if i == 'empty':
                            self.ui.text += band_rus[band] + str(
                                k + 1) + ' channel ' + str(std[band][k]) + status
                        else:
                            self.ui.text += band_rus[band] + \
                                str(k + 1) + status
                        self.ui.textEdit.setText(self.ui.text)
                        self.ui.textEdit.moveCursor(
                            QtGui.QTextCursor.End)
                        self.ui.textEdit.ensureCursorVisible()
                        QApplication.processEvents()
                    break

            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton_1.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)
            self.ui.pushButton_3.show()

        else:
            print('Not connection')


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    SettingsWindow = QtWidgets.QMainWindow()
    uiS = Ui_SettingsWindow()
    uiS.setupUi(SettingsWindow)
    SettingsWindow.show()
    sys.exit(app.exec_())
