import sys, time, random
import serial
from serial.tools import list_ports


from PyQt5 import QtCore, QtWidgets, QtGui, QtSerialPort
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtMultimedia import QAudioDeviceInfo, QAudio, QCameraInfo

# from gui import Ui_MainWindow


class Dialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(Dialog, self).__init__(parent)
		self.portname_comboBox = QtWidgets.QComboBox()
		self.baudrate_comboBox = QtWidgets.QComboBox()

		for info in QtSerialPort.QSerialPortInfo.availablePorts():
			self.portname_comboBox.addItem(info.portName())

		for baudrate in QtSerialPort.QSerialPortInfo.standardBaudRates():
			self.baudrate_comboBox.addItem(str(baudrate), baudrate)

		buttonBox = QtWidgets.QDialogButtonBox()
		buttonBox.setOrientation(QtCore.Qt.Horizontal)
		buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)

		lay = QtWidgets.QFormLayout(self)
		lay.addRow("Port Name:", self.portname_comboBox)
		lay.addRow("BaudRate:", self.baudrate_comboBox)
		lay.addRow(buttonBox)
		self.setFixedSize(self.sizeHint())

	def get_results(self):
		return self.portname_comboBox.currentText(), self.baudrate_comboBox.currentData()


class portReader(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)

		
		self.swithces_values = ""
		self.swithces_values = [1,1,1,1,1,1,1,1,1,1,1,1]
		self.line = b'000000000000\n'


	def get_switched_values(self, bytes_raw_line):
		print("sw6: ", bytes_raw_line[-6 -1: -5-1])
		return [        
			int(bytes_raw_line[-1 -1: -0-1]), # sw 1
			int(bytes_raw_line[-2 -1: -1-1]), # sw 2
			int(bytes_raw_line[-3 -1: -2-1]), # sw 3
			int(bytes_raw_line[-4 -1: -3-1]), # sw 4
			int(bytes_raw_line[-5 -1: -4-1]), # sw 5
			int(bytes_raw_line[-6 -1: -5-1]), # sw 6

			int(bytes_raw_line[-7 -1: -6-1]), # sw 7
			int(bytes_raw_line[-8 -1: -7-1]), # sw 8
			int(bytes_raw_line[-9 -1: -8-1]), # sw 9
			int(bytes_raw_line[-10 -1: -9-1]), # sw 10
			int(bytes_raw_line[-11 -1: -10-1]), # sw 11
			int(bytes_raw_line[-12 -1: -11-1]) # sw 12

		]


	def run(self):
		# while True:
		# 	self.line = "{}{}{}{}{}{}{}{}{}{}{}{}".format(random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]))			
		# 	time.sleep(1)
		ports = serial.tools.list_ports.comports()
		port = ports[0].device
		try:
			ser = serial.Serial(
				port=port,\
				baudrate=9600,\
				parity=serial.PARITY_NONE,\
				stopbits=serial.STOPBITS_ONE,\
				bytesize=serial.EIGHTBITS,\
				timeout=0
			)
			print("Success connect to port", port)
		except serial.serialutil.SerialException:
  			print('exception')

		# ser.write(b'0')
		time.sleep(1)
		# try:
		
		with ser:
			while True:
				self.line = ser.readline()
				try:
					if self.line:
						
						if b'0' in self.line:								
							# print("lol: ", self.line)
							print("make: ", self.get_switched_values(self.line))
							self.swithces_values = self.get_switched_values(self.line)						
							
				except ValueError:
					pass
		time.sleep(0.1)
			
		# except:
		# 	print("no com port")
		
		


	def ser_read(self):
		return self.swithces_values



class MainApp(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)		
		self.ui = uic.loadUi('gui/main.ui', self)
		# super(MainApp, self).__init__()
		# self.ui = Ui_MainWindow()
		# self.setupUi(self)
		
		self.setWindowTitle("DeploySystem switches v0.3")

		self.hide_all_switches() # make default view for all switches

		# set timer for dynamic update switches status
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.update_switches)
		self.timer.start(100)

		self.configureButton.clicked.connect(self.open_dialog)

		self.serial = QtSerialPort.QSerialPort(
			self,
			readyRead=self.receive
		)



	# it create thread for class which simulated usart incoming data
	def listen_port(self):
		self.listener_port = portReader()
		self.threads = []
		self.threads.append(self.listener_port)
		self.listener_port.start()

	# it make all switches hidden (switches in gui is layers and overlay each other)
	def hide_all_switches(self):
		# self.front_stock.setHidden(False)

		self.sw_1_off.setHidden(True)
		self.sw_1_on.setHidden(True)

		self.sw_2_off.setHidden(True)
		self.sw_2_on.setHidden(True)

		self.sw_3_off.setHidden(True)
		self.sw_3_on.setHidden(True)

		self.sw_4_off.setHidden(True)
		self.sw_4_on.setHidden(True)

		self.sw_5_off.setHidden(True)
		self.sw_5_on.setHidden(True)

		self.sw_6_off.setHidden(True)
		self.sw_6_on.setHidden(True)

		self.sw_7_off.setHidden(True)
		self.sw_7_on.setHidden(True)

		self.sw_8_off.setHidden(True)
		self.sw_8_on.setHidden(True)

		self.sw_9_off.setHidden(True)
		self.sw_9_on.setHidden(True)

		self.sw_10_off.setHidden(True)
		self.sw_10_on.setHidden(True)

		self.sw_11_off.setHidden(True)
		self.sw_11_on.setHidden(True)

		self.sw_12_off.setHidden(True)
		self.sw_12_on.setHidden(True)
		
		self.radio_sw_1.setChecked(False)
		self.radio_sw_2.setChecked(False)
		self.radio_sw_3.setChecked(False)
		self.radio_sw_4.setChecked(False)
		self.radio_sw_5.setChecked(False)
		self.radio_sw_6.setChecked(False)
		self.radio_sw_7.setChecked(False)
		self.radio_sw_8.setChecked(False)
		self.radio_sw_9.setChecked(False)
		self.radio_sw_10.setChecked(False)
		self.radio_sw_11.setChecked(False)
		self.radio_sw_12.setChecked(False)

	def set_sw_1_on(self):
		self.sw_1_off.setHidden(True)
		self.sw_1_on.setHidden(False)

		self.radio_sw_1.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_1_off(self):
		self.sw_1_off.setHidden(False)
		self.sw_1_on.setHidden(True)

		self.radio_sw_1.setChecked(False)

	def set_sw_2_on(self):
		self.sw_2_off.setHidden(True)
		self.sw_2_on.setHidden(False)

		self.radio_sw_2.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_2_off(self):
		self.sw_2_off.setHidden(False)
		self.sw_2_on.setHidden(True)

		self.radio_sw_2.setChecked(False)

	def set_sw_3_on(self):
		self.sw_3_off.setHidden(True)
		self.sw_3_on.setHidden(False)

		self.radio_sw_3.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_3_off(self):
		self.sw_3_off.setHidden(False)
		self.sw_3_on.setHidden(True)

		self.radio_sw_3.setChecked(False)

	
	def set_sw_4_on(self):
		self.sw_4_off.setHidden(True)
		self.sw_4_on.setHidden(False)

		self.radio_sw_4.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_4_off(self):
		self.sw_4_off.setHidden(False)
		self.sw_4_on.setHidden(True)

		self.radio_sw_4.setChecked(False)


	# method which make sw in gui on
	def set_sw_5_on(self):
		self.sw_5_off.setHidden(True)
		self.sw_5_on.setHidden(False)

		self.radio_sw_5.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_5_off(self):
		self.sw_5_off.setHidden(False)
		self.sw_5_on.setHidden(True)

		self.radio_sw_5.setChecked(False)


	# method which make sw in gui on
	def set_sw_6_on(self):
		self.sw_6_off.setHidden(True)
		self.sw_6_on.setHidden(False)

		self.radio_sw_6.setChecked(True)
		print("sw 6 is on")
	
	# method which make sw in gui off
	def set_sw_6_off(self):
		self.sw_6_off.setHidden(False)
		self.sw_6_on.setHidden(True)

		self.radio_sw_6.setChecked(False)
		print("sw 6 if off")

	# method which make sw in gui on
	def set_sw_7_on(self):
		self.sw_7_off.setHidden(True)
		self.sw_7_on.setHidden(False)

		self.radio_sw_7.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_7_off(self):
		self.sw_7_off.setHidden(False)
		self.sw_7_on.setHidden(True)

		self.radio_sw_7.setChecked(False)
		print("sw 7 if off")
	
	# method which make sw in gui on
	def set_sw_8_on(self):
		self.sw_8_off.setHidden(True)
		self.sw_8_on.setHidden(False)

		self.radio_sw_8.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_8_off(self):
		self.sw_8_off.setHidden(False)
		self.sw_8_on.setHidden(True)

		self.radio_sw_8.setChecked(False)
		print("sw 8 if off")


	# method which make sw in gui on
	def set_sw_9_on(self):
		self.sw_9_off.setHidden(True)
		self.sw_9_on.setHidden(False)

		self.radio_sw_9.setChecked(True)		
	
	# method which make sw in gui off
	def set_sw_9_off(self):
		self.sw_9_off.setHidden(False)
		self.sw_9_on.setHidden(True)

		self.radio_sw_9.setChecked(False)
		print("sw 9 is off")


	# method which make sw in gui on
	def set_sw_10_on(self):
		self.sw_10_off.setHidden(True)
		self.sw_10_on.setHidden(False)

		self.radio_sw_10.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_10_off(self):
		self.sw_10_off.setHidden(False)
		self.sw_10_on.setHidden(True)

		self.radio_sw_10.setChecked(False)
		print("sw 10 if off")

	
	# method which make sw in gui on
	def set_sw_11_on(self):
		self.sw_11_off.setHidden(True)
		self.sw_11_on.setHidden(False)

		self.radio_sw_11.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_11_off(self):
		self.sw_11_off.setHidden(False)
		self.sw_11_on.setHidden(True)

		self.radio_sw_11.setChecked(False)
		print("sw 10 if off")


	
	# method which make sw in gui on
	def set_sw_12_on(self):
		self.sw_12_off.setHidden(True)
		self.sw_12_on.setHidden(False)

		self.radio_sw_12.setChecked(True)
	
	# method which make sw in gui off
	def set_sw_12_off(self):
		self.sw_12_off.setHidden(False)
		self.sw_12_on.setHidden(True)

		self.radio_sw_12.setChecked(False)
		print("sw 12 if off")

	
	# parse data from usart and update all switch in gui
	def update_switches(self):
		line = self.listener_port.ser_read()
		list_line = list(line)

		for (index, sw) in enumerate(list_line):
			# print("sw: {}: status: {}".format(index + 1, sw))
			if index == 1 - 1:
				
				if sw == 1:
					self.set_sw_1_on()
				elif sw == 0:
					self.set_sw_1_off()
			
			if index == 2 - 1:
				
				if sw == 1:
					self.set_sw_2_on()
				elif sw == 0:
					self.set_sw_2_off()
			if index == 3 - 1:				
				if sw == 1:
					self.set_sw_3_on()
				elif sw == 0:
					self.set_sw_3_off()

			if index == 4 - 1:
				
				if sw == 1:
					self.set_sw_4_on()
				elif sw == 0:
					self.set_sw_4_off()
			
			if index == 5 - 1:
				
				if sw == 1:
					self.set_sw_5_on()
				elif sw == 0:
					self.set_sw_5_off()

			if index == 6 - 1:
				if sw == 1:
					self.set_sw_6_on()
				elif sw == 0:
					self.set_sw_6_off()
			
			if index == 7 - 1:
				if sw == 1:
					self.set_sw_7_on()
				elif sw == 0:
					self.set_sw_7_off()

			if index == 8 - 1:
				if sw == 1:
					self.set_sw_8_on()
				elif sw == 0:
					self.set_sw_8_off()

			if index == 9 - 1:
				if sw == 1:
					self.set_sw_9_on()
				elif sw == 0:
					self.set_sw_9_off()

			if index == 10 - 1:
				if sw == 1:
					self.set_sw_10_on()
				elif sw == 0:
					self.set_sw_10_off()

			if index == 11 - 1:
				if sw == 1:
					self.set_sw_11_on()
				elif sw == 0:
					self.set_sw_11_off()

			if index == 12 - 1:
				if sw == 1:
					self.set_sw_12_on()
				elif sw == 0:
					self.set_sw_12_off()
	
	
	@QtCore.pyqtSlot()
	def open_dialog(self):
		dialog = Dialog()
		if dialog.exec_():
			portname, baudrate = dialog.get_results()
			self.serial.setPortName(portname)
			self.serial.setBaudRate(baudrate)


	@QtCore.pyqtSlot()
	def receive(self):
		while self.serial.canReadLine():
			text = self.serial.readLine().data().decode()
			text = text.rstrip('\r\n')
			self.light_lineEdit.setText(text)
			print(text)
			


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainApp()
	mainWindow.show()
	mainWindow.listen_port()
	sys.exit(app.exec_())