import sys

import serial.tools.list_ports

import serial

import time

import re

from datetime import datetime, timezone

from Battery_Widget import BatteryWidget

from PyQt6.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox, QVBoxLayout)

import struct

# permette di lavorare sui campi vari
from PyQt6.QtCore import QRegularExpression, QLocale, QTimer
from PyQt6.QtGui import QRegularExpressionValidator, QDoubleValidator

from Battery_Widget import BatteryWidget

from PyQt6.uic import loadUi

# per interfacce batteria
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QRect, QSize
# ------------

from main_window import Ui_MainWindow

import immaginiLoghi
import risorse

# COSTANTI
NUM_ANALOG_SENSORS = 4
NUM_PINZE = 8
DIMENSIONE_DATI_SENSORI = 104

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ser = None
        self.min_voltageBatt = 3.2
        self.max_voltageBatt = 4.25
        self.min_voltageBattBackup = 2
        self.max_voltageBattBackup = 3.3
        self.segments = 10

        self.setupUi(self)
        self.connectSignalsSlots()
        self.findSerialPorts()


        self.graphicBattery = BatteryWidget(self, segments=self.segments, min_voltage=self.min_voltageBatt, max_voltage=self.max_voltageBatt, orientation=Qt.Orientation.Horizontal)
        self.graphicBattery.setFixedSize(150, 100)
        self.graphicBatteryBackup = BatteryWidget(self, segments=self.segments, min_voltage=self.min_voltageBattBackup, max_voltage=self.max_voltageBattBackup, orientation=Qt.Orientation.Horizontal)
        self.graphicBatteryBackup.setFixedSize(150, 100)
#        if self.frameGraficaBatterie.layout() is None:
#            layout = QVBoxLayout(self.frameGraficaBatterie)
#            self.frameGraficaBatterie.setLayout(layout)
        self.frameVBatt.layout().addWidget(self.graphicBattery)
        self.frameVBackup.layout().addWidget(self.graphicBatteryBackup)
        self.pushConfigLetture.setEnabled(False)



   
# qui collego i bottoni alle varie funzioni
    def SetLoRaParam(self):
        LoRaSetWin = SetLoRaParam(self)
        LoRaSetWin.exec()

    def SensorsData(self):
        LoRaSetWin = SensorsData(self)
        LoRaSetWin.show()
        

# qui definisco le azioni quando si preme qualcosa
    def connectSignalsSlots(self):
        self.action_Exit.triggered.connect(self.close)
        self.pushModificaLoRaConfig.clicked.connect(self.SetLoRaParam)
        self.push_SerialFind.clicked.connect(self.findSerialPorts)
        self.push_serialConnect.clicked.connect(self.serialButtonControl)
        self.pushLeggiDati.clicked.connect(self.LeggiConfigLoRa)
        self.push_SetOrario.clicked.connect(self.scriviOrario)
        self.pushConfigLetture.clicked.connect(self.SensorsData)


    def findSerialPorts(self):
#        if ports:
#            del ports
        # Ottiene la lista delle porte seriali disponibili
        ports = None
        port_list = None
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]

 #       # Aggiorna la ComboBox
        self.comboBox_comNumber.clear()
#        self.comboBox_comNumber.addItems(port_list)
        for port in ports:
            display_text = f"{port.device} - {port.description}"
            self.comboBox_comNumber.addItem(display_text, port.device)  # port.device come "data"
 
        # Se ci sono porte, seleziona la prima
        if port_list:
            self.comboBox_comNumber.setCurrentIndex(0)
            self.push_serialConnect.setEnabled(True)

    def getACK(self):
        ack = None
        self.ser.reset_input_buffer()
        ack = self.ser.read(1)
        if (len(ack) != 1):
            errore = 1
        else:
            errore = 0    
        if (ack == b'\xaf'):
            errore = 0
        else:
            print(f"0x{ack[0]:02x}")
#            print(ack)
            errore = 2
        return errore

    def scriviOrario(self):
        times = int(datetime.now(timezone.utc).timestamp())
        timeBytes = times.to_bytes(4, byteorder='little')
        size = len(timeBytes)
        errore = self.Scrividati(timeBytes, [0x06])
        if (errore == 0):
            #time.sleep(0.05)
            #self.ser.write(bytes(timeBytes))
            self.ser.reset_input_buffer()
            statoACK = self.getACK()
            if (statoACK == 0):
                errore = 0
                time.sleep(0.1)
                self.leggiOrario()
            else:
                errore = 1    
        else:
            errore = 1

        #if errore == 0:
        #    time.sleep(0.5)


    def serialDisconnect(self):
        try:
            # lavoro sul pin RTS
            self.ser.rts = True 
            time.sleep(0.5)
            self.ser.close()
            self.push_serialConnect.setText("Serial Connect")
#           del self.ser
            self.groupBox_LoRaConfiguration.setEnabled(False)
            self.comboBox_serialSpeed.setEnabled(True)
            self.comboBox_comNumber.setEnabled(True)
            self.push_SerialFind.setEnabled(True)
            self.pushConfigLetture.setEnabled(False)
#           self.push.setEnabled(False)
            return
        except serial.SerialException as e:
            QMessageBox.critical(self, "Errore", str(e))
            return        

    def serialConnect(self):
        try:
            port = self.comboBox_comNumber.currentData()
            baudRate = self.comboBox_serialSpeed.currentText()
            if not port:
                QMessageBox.warning(self, "Errore", "Nessuna porta selezionata")
                return
            self.ser = serial.Serial(port=port, baudrate=baudRate, timeout=5)
            self.groupBox_LoRaConfiguration.setEnabled(True)
            self.push_serialConnect.setText("Serial Disconnect")
            self.comboBox_serialSpeed.setEnabled(False)
            self.comboBox_comNumber.setEnabled(False)
            self.push_SerialFind.setEnabled(False)
            self.label_3.setText('<html><head/><body><p><img src=":/immaginiBottone/img/green.png"/></p></body></html>')
            self.pushModificaLoRaConfig.setEnabled(False)
            self.pushConfigLetture.setEnabled(True)
            self.comboBox_DRSelection.showPopup = lambda: None
            #alzo il pin RTSn
            self.ser.rts = False
            time.sleep(0.5)
            self.ser.rts = True
            time.sleep(0.5)
            self.ser.rts = False    
            QMessageBox.information(self, "OK", f"Connesso a {port}")
        except serial.SerialException as e:
            QMessageBox.critical(self, "Errore", str(e)) 

    def serialButtonControl(self):
        if self.ser is not None:
            if self.ser.is_open:
                self.serialDisconnect()
            else:
                self.serialConnect()
        else:
            self.serialConnect()
 

    # def LeggiDati(self):
    #     #self.ser.setRTS(True)
    #     hex_list = [0x00]
    #     self.ser.write(bytes(hex_list))
    #     ID = self.ser.read(1)
    #     if (ID == 0xAB)
    #         hex_list = [0x01]
    #         self.ser.write(bytes(hex_list))

    def bytes_to_hex_string(self, data: bytes) -> str:
        return data.hex(":").upper()  

    def LeggiConfigLoRa(self):
        time.sleep(0.5)
        # leggo il campo GetSWVersio
        errore, SWVersion = self.LeggiDati(4, [0x01])
        if errore != 0:
            QMessageBox.critical(self, "Errore", "Errore su porta seriale")
            return
        #leggo il campo LoRaDati
        #  spacchetto i dati di versione
        dimensioniSW = [1,1,1,1]
        SW4, SW3, SW2, SW1 = self.split_bytes(SWVersion, dimensioniSW)
        self.lineEdit_SWVersion.setText(f"{str(int.from_bytes(SW1, 'big'))}.{str(int.from_bytes(SW2, 'big'))}.{str(int.from_bytes(SW3, 'big'))}.{str(int.from_bytes(SW4, 'big'))}")
        errore, LoRaDati = self.LeggiDati(56, [0x02])
        size = len(LoRaDati)
        if errore != 0:
            return
        # spacchetto i valori delle varie variabili LoRa
        dimensioniLoRa = [4, 4, 8, 16, 16, 4, 4]
        DR, DevAddr, AppEUI, NSK, ASK, TXT, ADREnab = self.split_bytes(LoRaDati, dimensioniLoRa)
        self.line_devADDR.setText(self.bytes_to_hex_string(DevAddr))
        self.line_NSK.setText(self.bytes_to_hex_string(NSK))
        self.line_ASK.setText(self.bytes_to_hex_string(ASK))
        self.lineEdit_appEui.setText(self.bytes_to_hex_string(AppEUI))
        #print("La variabile 'basi' è di tipo:", type(ADREnab))
        if (ADREnab == b'\x00\x00\x00\x00'):
            self.checkBoxADR.setChecked(False)
        else:
            self.checkBoxADR.setChecked(True)
        self.lineEdit_TXInterva.setText(str(round(int.from_bytes(TXT, byteorder='big', signed=False)/1000)))
        self.comboBox_DRSelection.setCurrentIndex(int.from_bytes(DR, byteorder = 'big'))
        self.pushModificaLoRaConfig.setEnabled(True)
        self.leggiOrario()
        self.leggiTensioni()
        #QMessageBox.information(self, "Lettura corretta", "Letti tutti i campi LoRa")
        # poi leggiamo anche il tmestamp
#        errore, datiTimestamp = self.LeggiDati(4, [0x05])
#        size = len(datiTimestamp)
#        if errore != 0:
#            return
#        timestamp = int.from_bytes(datiTimestamp, byteorder='little')
#        dt = datetime.fromtimestamp(timestamp)
#        data_str = dt.strftime("%Y-%m-%d %H:%M:%S")
#        self.lineEdit_OrarioLetto.setText(data_str)
    def leggiTensioni(self):
        errore, tensioni = self.LeggiDati(4, [0x04])
        size = len(tensioni)
        if errore != 0:
            return
        valori = struct.unpack('<2H', tensioni)   # > = big endian, H = unsigned short (2 byte)
        valori = [x / 1000 for x in valori]
        if errore != 0:
            return
        # definisco i valore dei display
        self.lcdNumberVBatt.display(valori[0])
        self.lcdNumberVBackup.display(valori[1])
        # imposto i valori sul simbolo batteria
        self.graphicBattery.voltage = valori[0]
        self.graphicBatteryBackup.voltage = valori[1]

    def leggiOrario(self):
        errore, datiTimestamp = self.LeggiDati(4, [0x05])
        size = len(datiTimestamp)
        if errore != 0:
            return
        timestamp = int.from_bytes(datiTimestamp, byteorder='little')
        dt = datetime.fromtimestamp(timestamp)
        data_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        self.lineEdit_OrarioLetto.setText(data_str)            

    def Scrividati(self, dato, CMD):
            errore = 0
            data = 0
            hex_list = [0x00]
            self.ser.write(bytes(hex_list))
            self.ser.reset_input_buffer()
            ID = self.ser.read(1)
            if not ID:
                errore = 1
                return errore
            if ID and ID[0] == 0xAB:
                self.ser.write(bytes(CMD))
                statoACK = self.getACK()
                if statoACK == 0:
                    time.sleep(0.05)
                    self.ser.write(bytes(dato))
                    errore = 0
                    return errore
                else: 
                    errore = 4
                    return errore
            else:
                errore = 3
                return errore
                #self.ser.write(bytes(CMD))
                #ack = None
                #ack = self.ser.read(1)
                #if (len(ack) != 1):
                #    errore = 1
                #    return errore
                #if (ack == b'\xaf'):
                #    time.sleep(0.05)
                #    self.ser.write(bytes(dato))
                #    errore = 0
                #    return errore

    def LeggiDati(self, dimensioneAttesa, CMD):
        # controlliamo di essere collegati al nostro nodo
        self.ser.reset_input_buffer()
        errore = 0
        data = 0
        hex_list = [0x00]
        self.ser.write(bytes(hex_list))
        ID = self.ser.read(1)
        if not ID:
            errore = 1
            return errore, data
        if ID and ID[0] == 0xAB:
            self.ser.write(bytes(CMD))
            data = self.ser.read(dimensioneAttesa)
            if (len(data) != dimensioneAttesa):
                errore = 1
            #print("La variabile 'basi' è di tipo:", type(data))    
            return errore, data
        else:
            errore = 1
        return errore, data
    
    def invert_endianess(self, data):
        # Se è lista di interi, converte in bytes
        if isinstance(dato, list):
            dato = bytes(dato)
        elif not isinstance(dato, (bytes, bytearray)):
            raise TypeError("dato deve essere bytes, bytearray o lista di interi")
        # Inverte i byte
        inverted = dato[::-1]
        # Restituisce come bytes
        return bytes(inverted)

    #invertiamo l'endianess
    def split_bytes(self, data, sizes):
        parts = []
        offset = 0

        # inverto anche l'endianess di ogni chunk
        for size in sizes:
            chunk = data[offset:offset+size]
            parts.append(chunk[::-1])   # inversione endianess
            offset += size
        return parts

# qui carico le altre finestre che si possono aprire
class SetLoRaParam(QDialog):
    def __init__(self, parent):
    #def __init__(self, window):
    #    self.window = window 
        super().__init__(parent)
        self.main = parent
        loadUi("ui/setLoRaWindow.ui", self)
        self.connectSignalsSlots()

        rx = QRegularExpression("^[0-9A-Fa-f:]*$")
        validator = QRegularExpressionValidator(rx)
        
        num = QRegularExpression("^[0-9]*$")
        numberValidator = QRegularExpressionValidator(num)
        
        # carico i dati dalla schermata principale e copio le impostazioni, oltre a inserire le regole di scrittura
        self.line_devADDR.setText(self.main.line_devADDR.text())
        self.line_devADDR.setValidator(validator)  
        self.line_devADDR.setMaxLength(23)   #16 caratteri + 7 due punti
        self.line_devADDR.textEdited.connect(lambda t: self.format_hex_field(self.line_devADDR, t, bytes_len=4)) 

        self.line_NSK.setText(self.main.line_NSK.text())
        self.line_NSK.setValidator(validator)  
        self.line_NSK.setMaxLength(47)
        self.line_NSK.textEdited.connect(lambda t: self.format_hex_field(self.line_NSK, t, bytes_len=16))

        self.line_ASK.setText(self.main.line_ASK.text())
        self.line_ASK.setValidator(validator)  
        self.line_ASK.setMaxLength(47)
        self.line_ASK.textEdited.connect(lambda t: self.format_hex_field(self.line_ASK, t, bytes_len=16))

        self.lineEdit_appEui.setText(self.main.lineEdit_appEui.text())
        self.lineEdit_appEui.setValidator(validator)  
        self.lineEdit_appEui.setMaxLength(23)
        self.lineEdit_appEui.textEdited.connect(lambda t: self.format_hex_field(self.lineEdit_appEui, t, bytes_len=8))

        self.lineEdit_TXInterva.setText(self.main.lineEdit_TXInterva.text())
        self.lineEdit_TXInterva.setValidator(numberValidator)
        
        self.checkBoxADR.setChecked(self.main.checkBoxADR.isChecked())

        self.comboBox_DRSelection.setCurrentIndex(self.main.comboBox_DRSelection.currentIndex())


    def format_hex_field(self, line_edit, text, bytes_len, sep=":"):
        """
        Formatta un QLineEdit in esadecimale con separatore automatico.
        :param line_edit: QLineEdit da formattare
        :param text: testo corrente
        :param bytes_len: numero di byte (es. 8 → DevEUI)
        :param sep: separatore (default :)
        """
        # rimuove tutto ciò che non è hex
        clean = "".join(c for c in text if c in "0123456789ABCDEFabcdef")
        # limita alla lunghezza massima
        max_hex = bytes_len * 2
        clean = clean[:max_hex]
        # spezza in coppie
        pairs = [clean[i:i+2] for i in range(0, len(clean), 2)]
        # ricompone
        formatted = sep.join(pairs).upper()
        # evita loop
        if formatted != line_edit.text():
            line_edit.blockSignals(True)
            line_edit.setText(formatted)
            line_edit.blockSignals(False)

# qui definisco le azioni quando si preme qualcosa
    def connectSignalsSlots(self):
        self.pushSendLoRaConfig.clicked.connect(self.packAndSendLoRaData)

    def append_bytes_to_buffer(self, buf: bytearray, value: bytes, length_counter: list):
        if not isinstance(value, (bytes, bytearray)):
            raise TypeError("value deve essere di tipo bytes o bytearray")
        buf.extend(value)
        length_counter[0] += len(value)

    def packAndSendLoRaData(self):
        dimensioniLoRa = [4, 4, 8, 16, 16, 4, 4]
        buffer = bytearray()
        counter = [0]
        tempCounter = [0]
        #DR, DevAddr, AppEUI, NSK, ASK, TXT, ADREnab = self.split_bytes(LoRaDati, dimensioniLoRa)
        #attacco tre zeri per fare 4 byte per il DR

        #tempVV = self.comboBox_DRSelection.currentText()
        #self.main.comboBox_DRSelection.currentIndex()
        #num_str = int("".join(re.findall(r"\d+", tempVV))).to_bytes(1, 'little')
        num_str = self.comboBox_DRSelection.currentIndex().to_bytes(1, 'little')
        self.append_bytes_to_buffer(buffer, num_str, tempCounter)
        self.append_bytes_to_buffer(buffer, b'\x00\x00\x00', tempCounter)
        self.append_bytes_to_buffer(buffer, bytes.fromhex(self.line_devADDR.text().replace(":", ""))[::-1], tempCounter)
        self.append_bytes_to_buffer(buffer, bytes.fromhex(self.lineEdit_appEui.text().replace(":", ""))[::-1], tempCounter)
        self.append_bytes_to_buffer(buffer, bytes.fromhex(self.line_NSK.text().replace(":", ""))[::-1], tempCounter)
        self.append_bytes_to_buffer(buffer, bytes.fromhex(self.line_ASK.text().replace(":", ""))[::-1], tempCounter)
        tempValue = int(self.lineEdit_TXInterva.text())*1000
        self.append_bytes_to_buffer(buffer, tempValue.to_bytes(4, 'little'), tempCounter)
        #attacco tre zeri per fare 4 byte legate al bool
        if self.checkBoxADR.isChecked() == True:
            self.append_bytes_to_buffer(buffer, b'\x01', tempCounter)
        else:
            self.append_bytes_to_buffer(buffer, b'\x00', tempCounter)
        self.append_bytes_to_buffer(buffer, b'\x00\x00\x00', tempCounter)
    
        # ora posso inviare i dati
        errore = self.main.Scrividati(buffer, [0x03])
        statoACK = self.main.getACK()

        if (errore == 0 and statoACK == 0):
            QMessageBox.information(self, "invio corretto", "Inviati tutti i campi LoRa")
            self.close()

class SensorsData(QMainWindow):
    def __init__(self, parent):
    #def __init__(self, window):
    #    self.window = window 
        super().__init__(parent)
        self.main = parent
        loadUi("ui/test.ui", self)
        self.connectSignalsSlots()
        self.setupValidators()
        self.LeggiParametri()

    def connectSignalsSlots(self):
        self.pushButtonReadData.clicked.connect(self.LeggiParametri)
        self.pushButtonReadSensors.clicked.connect(self.LeggiSensori)
        self.pushButtonUpdateData.clicked.connect(self.inviaParametri)

    def  inviaParametri(self):
        self.InviaParametriPinze()
        self.InviaParametriAnalog()  

    def LeggiParametri(self):
        self.LeggiParametriPinze()  
        self.LeggiParametriAnalog()      

    def setupValidators(self):
        double_positive_validator = QDoubleValidator(0.0, float("inf"), 3, self)
        double_positive_validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        double_positive_validator.setLocale(QLocale(QLocale.Language.English))

        num = QRegularExpression("^[0-9]*$")
        positiveIntegerValidator = QRegularExpressionValidator(num) 

        self.samples_per_mean_fields = [
            self.lineEditSamplesPerMean_1,
            self.lineEditSamplesPerMean_2,
            self.lineEditSamplesPerMean_3,
            self.lineEditSamplesPerMean_4,
            self.lineEditSamplesPerMean_5,
            self.lineEditSamplesPerMean_6,
            self.lineEditSamplesPerMean_7,
            self.lineEditSamplesPerMean_8
        ]

        self.raggio_pinza_fields = [
            self.lineEditRaggioPinza_1,
            self.lineEditRaggioPinza_2,
            self.lineEditRaggioPinza_3,
            self.lineEditRaggioPinza_4,
            self.lineEditRaggioPinza_5,
            self.lineEditRaggioPinza_6,
            self.lineEditRaggioPinza_7,
            self.lineEditRaggioPinza_8
        ]

        self.lambda_pinza_fields = [
            self.lineEditLambdaPinza_1,
            self.lineEditLambdaPinza_2,
            self.lineEditLambdaPinza_3,
            self.lineEditLambdaPinza_4,
            self.lineEditLambdaPinza_5,
            self.lineEditLambdaPinza_6,
            self.lineEditLambdaPinza_7,
            self.lineEditLambdaPinza_8
        ]

        self.raggio_gancio_fields = [
            self.lineEditRaggioGancio_1,
            self.lineEditRaggioGancio_2,
            self.lineEditRaggioGancio_3,
            self.lineEditRaggioGancio_4,
            self.lineEditRaggioGancio_5,
            self.lineEditRaggioGancio_6,
            self.lineEditRaggioGancio_7,
            self.lineEditRaggioGancio_8
        ]

        self.lambda_gancio_fields = [
            self.lineEditLambdaGancio_1,
            self.lineEditLambdaGancio_2,
            self.lineEditLambdaGancio_3,
            self.lineEditLambdaGancio_4,
            self.lineEditLambdaGancio_5,
            self.lineEditLambdaGancio_6,
            self.lineEditLambdaGancio_7,
            self.lineEditLambdaGancio_8
        ]

        self.checkONPinza_fields = [
            self.checkONPinza_1,
            self.checkONPinza_2,
            self.checkONPinza_3,
            self.checkONPinza_4,
            self.checkONPinza_5,
            self.checkONPinza_6,
            self.checkONPinza_7,
            self.checkONPinza_8
        ]
        
        self.checkThermalPinza_fields = [
            self.checkThermalPinza_1,
            self.checkThermalPinza_2,
            self.checkThermalPinza_3,
            self.checkThermalPinza_4,
            self.checkThermalPinza_5,
            self.checkThermalPinza_6,
            self.checkThermalPinza_7,
            self.checkThermalPinza_8
        ]

        self.samples_per_mean_analog1_fields = [
            self.lineEditSamplesPerMeanAnalog1_1,
            self.lineEditSamplesPerMeanAnalog1_2,
            self.lineEditSamplesPerMeanAnalog1_3,
            self.lineEditSamplesPerMeanAnalog1_4
        ]

        self.wait_time_analog1_fields = [
            self.lineEditWaitTimeAnalog1_1,
            self.lineEditWaitTimeAnalog1_2,
            self.lineEditWaitTimeAnalog1_3,
            self.lineEditWaitTimeAnalog1_4
        ]

        self.check_on_analog1_fields = [
            self.checkONAnalog1_1,
            self.checkONAnalog1_2,
            self.checkONAnalog1_3,
            self.checkONAnalog1_4
        ]

        self.lcd_analog_raw1_fields = [
            self.lcdAnalogRaw1_1,
            self.lcdAnalogRaw1_2,
            self.lcdAnalogRaw1_3,
            self.lcdAnalogRaw1_4
        ]

        self.lcd_pinza_raw_fields = [
            self.lcdPinzaRaw_1,
            self.lcdPinzaRaw_2,
            self.lcdPinzaRaw_3,
            self.lcdPinzaRaw_4,
            self.lcdPinzaRaw_5,
            self.lcdPinzaRaw_6,
            self.lcdPinzaRaw_7,
            self.lcdPinzaRaw_8
        ]

        self.lcd_pinza_mm_fields = [
            self.lcdPinzamm_1,
            self.lcdPinzamm_2,
            self.lcdPinzamm_3,
            self.lcdPinzamm_4,
            self.lcdPinzamm_5,
            self.lcdPinzamm_6,
            self.lcdPinzamm_7,
            self.lcdPinzamm_8
        ]   

        self.lcd_pinza_temp_fields = [
            self.lcdPinzaTemp_1,
            self.lcdPinzaTemp_2,
            self.lcdPinzaTemp_3,
            self.lcdPinzaTemp_4,
            self.lcdPinzaTemp_5,
            self.lcdPinzaTemp_6,
            self.lcdPinzaTemp_7,
            self.lcdPinzaTemp_8
        ]     
        
        # assegnamo i validator
        for field in self.samples_per_mean_fields:
            field.setValidator(positiveIntegerValidator)

        for field in self.raggio_pinza_fields:
            field.setValidator(double_positive_validator)        

        for field in self.lambda_pinza_fields:
            field.setValidator(double_positive_validator) 

        for field in self.raggio_gancio_fields:
            field.setValidator(double_positive_validator) 

        for field in self.lambda_gancio_fields:
            field.setValidator(double_positive_validator) 
    
    def InviaParametriPinze(self):    
        packed_data = bytearray()
        for i in range(NUM_PINZE):
            PlierON = 1 if self.checkONPinza_fields[i].isChecked() else 0
            ThermalON = 1 if self.checkThermalPinza_fields[i].isChecked() else 0
            plierSamples = int(self.samples_per_mean_fields[i].text() or 0)
            radiusPlier = float(self.raggio_pinza_fields[i].text() or 0)
            lambdaPlier = float(self.lambda_pinza_fields[i].text() or 0)
            lClamp = float(self.raggio_gancio_fields[i].text() or 0)
            lambdaClamp = float(self.lambda_gancio_fields[i].text() or 0)
            dummy = 0
            packet = struct.pack(
                "<BBBBffff",
                ThermalON,
                plierSamples,
                PlierON,
                dummy,
                radiusPlier,
                lClamp,
                lambdaPlier,          
                lambdaClamp
            )
            packed_data.extend(packet)
        errore = self.main.Scrividati(bytes(packed_data), [0x11])
        self.main.ser.reset_input_buffer()
        statoACK = self.main.getACK()
        if (errore == 0 and statoACK == 0):
            QMessageBox.information(self, "invio corretto", "Inviati tutti i campi di Pinze")
        return
    
    def InviaParametriAnalog(self):    
        packed_data = bytearray()
        for i in range(NUM_ANALOG_SENSORS):
            preSample = int(self.wait_time_analog1_fields[i].text() or 0)
            numSamples = int(self.samples_per_mean_analog1_fields[i].text() or 0)
            EnableSensore = 1 if self.check_on_analog1_fields[i].isChecked() else 0
            packet = struct.pack(
                "<BBB",
                preSample,
                numSamples,
                EnableSensore
            )
            packed_data.extend(packet)
        errore = self.main.Scrividati(bytes(packed_data), [0x13])
        statoACK = self.main.getACK()
        if (errore == 0 and statoACK == 0):
            QMessageBox.information(self, "invio corretto", "Inviati tutti i campi di Sensori Analogici")
        return    
    
    def unpackPinze(self, data):
        FORMAT = "<BBBffff"
        SIZE_PACKET = 20
        SIZE_DATA = 7
        pinze = []
        for i in range(0, len(data), SIZE_PACKET):
            pinze = data[i:i+SIZE_PACKET]
            if len(pinze) < SIZE_PACKET:
                break
            # Scarta il quarto byte (indice 3)
            useful = pinze[:3] + pinze[4:]  # prende byte 0,1 + 3,4,5,6,7 → totale 7 byte
#            print(len(useful))
            ThermalON, plierSamples, PlierON, radiusPlier, lClamp, lambdaPlier, lambdacClamp = struct.unpack(FORMAT, useful)
            index = int(i/SIZE_PACKET)
            self.checkThermalPinza_fields[index].setChecked(ThermalON == 0x01)
            self.samples_per_mean_fields[index].setText(str(plierSamples))
            self.checkONPinza_fields[index].setChecked(PlierON == 0x01)
            self.raggio_pinza_fields[index].setText(f"{radiusPlier:.3f}")
            self.raggio_gancio_fields[index].setText(f"{lClamp:.3f}")
            self.lambda_pinza_fields[index].setText(f"{lambdaPlier:.3f}")
            self.lambda_gancio_fields[index].setText(f"{lambdacClamp:.3f}")           
        return
   
    def LeggiParametriPinze(self):
        errore, parametri = self.main.LeggiDati(20*NUM_PINZE, [0x10])
        if errore != 0:
            return
        self.unpackPinze(parametri)

    def LeggiParametriAnalog(self):
        errore, parametri = self.main.LeggiDati(3*NUM_ANALOG_SENSORS, [0x12])
        if errore != 0:
            return
        self.unpackAnalog(parametri)
    
    def LeggiSensori(self):
        errore, parametri = self.main.LeggiDati(DIMENSIONE_DATI_SENSORI, [0x14])
        if errore != 0:
            return
        self.unpackSensors(parametri)
        
    def unpackAnalog(self, data):    
        FORMAT = "<BBB"
        SIZE_PACKET = 3
        analog = []
        for i in range(0, len(data), SIZE_PACKET):
            analog = data[i:i+SIZE_PACKET]
            if len(analog) < SIZE_PACKET:
                break
            # Scarta il quarto byte (indice 3)
            preSample, numSample, EnableSensore = struct.unpack(FORMAT, analog)
            index = int(i/SIZE_PACKET)
            self.wait_time_analog1_fields[index].setText(str(preSample))
            self.samples_per_mean_analog1_fields[index].setText(str(numSample))
            self.check_on_analog1_fields[index].setChecked(EnableSensore == 0x01)
        return
    
    def unpackSensors(self, data):    
        FORMAT = "<ffffffff"
        # numero di elementi per ogni pacchetto
        SIZE_PACKET = NUM_PINZE * 4 #8 float
        sensors = []
        i = 0
        # leggo i primi tre array da NUM_PINZE float ciascuno
        sensorsByte = data[i:i+SIZE_PACKET]
        pinzeRaw = list(struct.unpack(FORMAT, sensorsByte))
        i = i + SIZE_PACKET
        sensorsByte = data[i:i+SIZE_PACKET]
        temperatura = list(struct.unpack(FORMAT, sensorsByte))
        i = i + SIZE_PACKET
        sensorsByte = data[i:i+SIZE_PACKET]
        pinzeDiametro = list(struct.unpack(FORMAT, sensorsByte))
        i = i + SIZE_PACKET
# ora leggo i valori analogici
        FORMAT = "<HHHH"
        SIZE_PACKET = NUM_ANALOG_SENSORS * 2 
        sensorsByte = data[i:i+SIZE_PACKET]
        analogLetture = list(struct.unpack(FORMAT, sensorsByte))

# poi aggiorno in campi LCD
        for lcd, value in zip(self.lcd_pinza_raw_fields, pinzeRaw):
            lcd.display(value)
        for lcd, value in zip(self.lcd_pinza_mm_fields, pinzeDiametro):
            lcd.display(value)
        for lcd, value in zip(self.lcd_pinza_temp_fields, temperatura):
            lcd.display(value)
        for lcd, value in zip(self.lcd_analog_raw1_fields, analogLetture):
            lcd.display(value)            
        return




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())