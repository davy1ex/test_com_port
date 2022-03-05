import sys, time
from PyQt5 import QtWidgets, uic, QtCore, QtSerialPort, QtGui
import serial
from serial.tools import list_ports



class MainWindow(QtWidgets.QMainWindow):
	title = "DeploySystem_switches v0.42"
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.ui = uic.loadUi("gui/cool.ui", self)
		
		self.update_comboBox()
		self.comboBox.view().pressed.connect(self.update_comboBox)
		
		for baudrate in QtSerialPort.QSerialPortInfo.standardBaudRates():
			self.comboBox_2.addItem(str(baudrate), baudrate)

		self.serial = QtSerialPort.QSerialPort(
			self,
			readyRead=self.receive
		)

		if len(QtSerialPort.QSerialPortInfo.availablePorts()) == 0:
			print("No ports")
			self.timer = QtCore.QTimer()
			self.timer.timeout.connect(self.wait_port)
			self.timer.start(100)


		self.line = ""
		

		self.pushButton.clicked.connect(self.connect_by_click_buttom)
		self.pushButton_2.clicked.connect(self.disconect_by_click_buttom)
		self.pushButton_2.setEnabled(False)
	
	def update_comboBox(self):
		print("updated portBox")
		ports = serial.tools.list_ports.comports()
		for p in ports:
			self.comboBox.addItem(str(p.device))
	

	def wait_port(self):
		if len(QtSerialPort.QSerialPortInfo.availablePorts()) > 0:
			self.update_comboBox()
			self.timer.stop()

	def timer_read_port(self):
		
		self.line += str(self.receive().data())
		print(line)

		self.textBrowser.setText("line")

	
	def connect_by_click_buttom(self):
		if self.comboBox.currentText() == "":
			self.alert(text_error="Open Error on port", text_information="No selected port to connect")
			self.update_comboBox()
			return
		elif len(QtSerialPort.QSerialPortInfo.availablePorts()) == 0:
			self.alert(text_error="No Success Conection", text_information="No selected port to connect")
			return 
		self.serial.setPortName(self.comboBox.currentText())
		self.serial.setBaudRate(int(self.comboBox_2.currentText()))
		self.serial.open(QtCore.QIODevice.ReadWrite)
		
		self.pushButton.setEnabled(False)
		self.pushButton_2.setEnabled(True)

		print("u clicked me c:")

	
	def disconect_by_click_buttom(self):
		self.serial.close()
		self.pushButton.setEnabled(True)
		self.pushButton_2.setEnabled(False)
	
	@QtCore.pyqtSlot()
	def receive(self):
		while self.serial.canReadLine():
			# text = self.serial.readLine().data().decode()
			text = self.serial.readLine()
			# text = text.rstrip('\r\n')
			self.textBrowser.setText(str(text))
			print(text)
		print("not while")

	def alert(self, text_error, text_information, title=None):
		if title == None:
			title = self.title
		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Information)

		msg.setText(text_error)
		msg.setInformativeText(text_information)
		msg.setWindowTitle(title)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
			
		retval = msg.exec_()



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.show()
	sys.exit(app.exec_())