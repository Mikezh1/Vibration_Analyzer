from PyQt5.QtWidgets import QMainWindow, QApplication 

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QGraphicsView,QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QGridLayout

from PyQt5.QtCore import Qt,QThread,pyqtSlot,pyqtSignal


import sys

import time

import keyboard

import traceback

import numpy as np

import matplotlib.pyplot as plt



import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib import pyplot

pyplot.rcParams['font.sans-serif'] = ['SimHei'] 
pyplot.rcParams['axes.unicode_minus'] = False

from PyQt5.QtWidgets import QMainWindow, QApplication

import sys

import traceback

import serial
import serial.tools.list_ports #pip install pyserial

import mainwindow #py file auto generated from ui file


class MyFigure(FigureCanvasQTAgg):
   def __init__(self,width=5,height=4,dpi = 100):
      # 1. Create a figure object to draw
      self.fig = Figure(figsize=(width,height),dpi=dpi) 
      # 2. Activate the figure window and inherit the parent class properties
      super(MyFigure, self).__init__(self.fig)

   # Plot 
   #def plotSin(self,x,y):
   #   self.axes0 = self.fig.add_subplot(111)
   #   self.axes0.plot(x,y)


class MainDialog(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow,self).__init__(parent)  
        self.ui = mainwindow.Ui_Vibration_analyzer()  
        self.ui.setupUi(self)
        
        self.ui.comboBox_baudrate.setCurrentIndex(5) #default: 115200
        self.ui.lineEdit_peak_freq.setReadOnly(True) # read only
        
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint) #disable maximize button 
        self.setFixedSize(self.width(), self.height()) #disable window resize
        
        
        self.Port_detection()
               
        self.thread = Thread()

       
        ## Connect signals 
        self.ui.pushButton_start.released.connect(self.start_thread)
        self.ui.pushButton_stop.released.connect(self.stop_thread)
        self.ui.pushButton_refresh_port.released.connect(self.Port_detection)
        
        self.ui.actionAbout_Hardware_Connection.triggered.connect(self.show_about_HW_connect_dialog)
        

        self.thread.signal_display_peak_freq.connect(self.show_peak_freq)
        self.thread.signal_array_to_plot.connect(self.plot_spectrum)
        
        self.thread.started.connect(self.thread_started)
        self.thread.finished.connect(self.thread_finished)
        
        
        # e.g. 
        # self.ui.Button_port_detection.released.connect(self.Port_detection)
        # print(self.ui.comboBox.currentText())
        
        self.ui.statusbar.showMessage("Ready")
        
    ## Slot functions

    def start_thread(self):
        if not self.thread.isRunning():
            try:
                self.thread.port = str(self.ui.comboBox_port.currentText()).split("-")[-1] 
            except:
                self.thread.port = "(no port)"
                
            self.thread.baud_rate = int(self.ui.comboBox_baudrate.currentText())
            self.thread.start()


    def stop_thread(self):
        if self.thread.isRunning():
            self.thread.stop()
            print("1")

        if self.thread.at_least_1_loop is False and self.thread.isRunning():
            print("2")
            # Terminate the thread
            self.thread.terminate() 
            self.thread.wait()  
            QMessageBox.warning(self, "Warning", "serial read stucked just now. The baud rate may be not high enough.")
            
        
    def thread_started(self):
        print("Thread started")
        self.ui.pushButton_start.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(True)
        self.ui.pushButton_refresh_port.setEnabled(False)
        
        self.ui.comboBox_port.setEnabled(False)
        self.ui.comboBox_baudrate.setEnabled(False)
        
        self.ui.statusbar.showMessage("Started")
        

    def thread_finished(self):
        print("Thread finished")
        
        try:
            if self.thread.ser.isOpen() is False:
                QMessageBox.warning(self, "Warning", "No serial port was opened. This serial port may not exist.")
        
            self.thread.ser.close()
        except:
            # Warn no serial port
            QMessageBox.warning(self, "Warning", "This serial port may not exist.")
        
        
        self.ui.pushButton_start.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(False)
        self.ui.pushButton_refresh_port.setEnabled(True)
        
        self.ui.comboBox_port.setEnabled(True) 
        self.ui.comboBox_baudrate.setEnabled(True)
        
        self.ui.statusbar.showMessage("Stopped")
        

    def show_peak_freq(self, data):

        self.ui.lineEdit_peak_freq.setText(str(data)) 
        
        
        
    def plot_spectrum(self,data_array,Freq_Increment):
        
        F1 = MyFigure(width=5, height=4, dpi=70)
        F1.axes1 = F1.fig.add_subplot(111)
        
        freq = np.arange(0, len(data_array)*Freq_Increment, Freq_Increment)
        F1.axes1.plot(freq, data_array)
        
        F1.axes1.set_xlabel('Frequency (Hz)', fontsize=18)
        F1.axes1.set_ylabel('FFT Magnitude (a.u.)', fontsize=18)
        F1.axes1.set_title('Spectrum', fontsize=20)
                
        F1.fig.tight_layout()  


        width,height = self.ui.graphicsView.width(),self.ui.graphicsView.height()
        F1.resize(width,height)
           

        scene = QGraphicsScene()  
        scene.addWidget(F1)  
        self.ui.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.graphicsView.setScene(scene) 

        
    def show_about_HW_connect_dialog(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("About Hardware Connection")
        msg_box.setText("Connect the open-source hardware to this computer via USB serial communication.\n\nThe baud rate should be 115200 if there is no change in the embedded software.")
        msg_box.exec_()

    ## Custom functions
    
    def Port_detection(self):
        # Detect all existing ports and store info in a dictionary
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        
        self.ui.comboBox_port.clear()
        for port in port_list:
            port_name = port[0]
            port_description = port[1]
            self.Com_Dict[port_name] = port_description
            #self.ui.comboBox_port.addItem(f"{port_name} - {port_description}")
            self.ui.comboBox_port.addItem(f"{port_description}-{port_name}")
        
        # No port
        if len(self.Com_Dict) == 0:
            self.ui.comboBox_port.addItem("no port")

        
    
    ## Event handlers

    def closeEvent(self, event):
        """
        Reimplement MainWindow's closeEvent 
        Exit all processes when closing
        """
        reply = QtWidgets.QMessageBox.question(self,'Vibration Analyzer',"Exit?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            
            self.stop_thread()
            
            self.thread.wait()  
            event.accept() 
            
        else:
            event.ignore()
    

## Thread class  

class Thread(QThread):
    
    signal_display_peak_freq=pyqtSignal(str) 
    signal_array_to_plot = pyqtSignal(list,float)
    
    def __init__(self):
        super(Thread,self).__init__()
        self.running = False    
        self.at_least_1_loop = False
        
        

        
        # Serial config
        #self.port = "COM8"  
        self.port = None
        self.baud_rate = 115200  

        self.NPT = 256  
        self.Fs = 500  
        self.Freq_Increment = self.Fs / self.NPT 

        

        # Data array
        self.data_array = []
        
        print("init of thread")
        
    

        

    def run(self):
        self.running = True
        
        self.at_least_1_loop=False
        

        #print(self.port)
        
        # Open serial port
        try:
            self.ser = serial.Serial(self.port, self.baud_rate)

        except:
            self.running = False

        while self.running:
            print("Thread is running")
            
            # Flags
            self.start_found = False
            self.end_found = False

            while True:
                
                if self.ser.in_waiting > 0:
                    # Read serial data
                    try:
                        self.line = self.ser.readline().decode().strip()
                    except:
                        pass
                    else:
                        if self.line == "Start":
                            # If find Start, set start_found True and clear data array
                            self.start_found = True
                            self.data_array = []
                        elif self.line == "End":
                            # If find End, set end_found True and break
                            self.end_found = True
                            break
                        elif self.start_found and not self.end_found:
                            try:
                                # Try to convert data to int and store in array
                                self.data = int(self.line)
                                self.data_array.append(self.data)
                            except ValueError:
                                # Invalid data, discard
                                pass
                            
            self.at_least_1_loop = True
             
                    


            self.data_array = self.data_array[:-1] if self.data_array else self.data_array
            
            if self.data_array == []:
                print("array is empty")
                continue
            
            #print(self.data_array)
            
            
            self.max_index = np.argmax(self.data_array)
            self.max_frequency = "{:.2f}".format(self.max_index * self.Freq_Increment)
            
            # Display max_frequency in lineEdit_peak_freq
            # Emit signal to update UI
            self.signal_display_peak_freq.emit(self.max_frequency)
            
            
            # Draw 
            self.signal_array_to_plot.emit(self.data_array,self.Freq_Increment)
            

            



    def stop(self):
        self.running = False



## Main

if __name__ == "__main__":

    app = QApplication(sys.argv)  
    main_win = MainDialog()  
    main_win.show()
    sys.exit(app.exec_())