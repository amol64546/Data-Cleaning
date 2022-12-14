from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import pandas as pd
import random


class MyWidget(QMainWindow):

	def center_window(self):
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())  	
	
	def __init__(self):
		super(MyWidget, self).__init__()
		uic.loadUi("gui.ui", self)
		self.setFixedSize(523, 325)		
		self.center_window()
		

		self.pushButton = self.findChild(QPushButton,"pushButton")
		self.pushButton.clicked.connect(self.clicker)

		self.pushButton_2 = self.findChild(QPushButton,"pushButton_2")
		self.pushButton_2.clicked.connect(self.clicker_2)

		self.checkBox = self.findChild(QCheckBox,"checkBox")
		self.checkBox_2 = self.findChild(QCheckBox,"checkBox_2")
		self.checkBox_4 = self.findChild(QCheckBox,"checkBox_4")

		self.lineEdit = self.findChild(QLineEdit,"lineEdit")
		self.lineEdit_2 = self.findChild(QLineEdit,"lineEdit_2")

		self.show()

	


	def clicker(self):
		self.fname = QFileDialog.getOpenFileName(self, "Open File","/","CSV or Excel (*.csv , *.xlsx);;")        
		if self.fname:							
			self.lineEdit.setText(self.fname[0])
			self.path = self.fname[0]		


	
			
	def clicker_2(self):		

		#Import
		try:
			if self.path[-1]=='v':
				self.df = pd.read_csv(self.path)
			else:
				self.df = pd.read_excel(self.path)
		except:		
			msg = QMessageBox(self)
			msg.setWindowTitle("Error")
			msg.setText("Please Select File")
			msg.setIcon(QMessageBox.Critical)
			msg.exec_()
		

				
		try:
			#Empty file	
			if self.df.empty:			
				msg = QMessageBox(self)
				msg.setWindowTitle("Error")
				msg.setText("File is Empty")
				msg.setIcon(QMessageBox.Critical)
				msg.exec_()
				return

			

		
			#check headers

			#Strip Headers
			self.df.columns = self.df.columns.str.strip()

			flag = False

			#empty
			if self.checkBox.isChecked():
				self.df.dropna(inplace=True)
				flag = True

			#duplicates
			if self.checkBox_2.isChecked():
				self.df.drop_duplicates(inplace=True)
				flag = True


			#format
			if self.checkBox_4.isChecked():
				col = int(self.lineEdit_2.text()) - 1			
				self.df.iloc[:,col] = pd.to_datetime(self.df.iloc[:,col])
				flag = True

			#Export
			if flag:

				#Generating new fname
				rand = random.randint(1, 1000)
				list = self.path.split("/")
				start_path = ''
				for i in range(len(list)-1):
					start_path += '/' + list[i]
				export_fname = start_path +'/clean'+ str(rand) +'_'+ list[-1]

				if self.path[-1]=='v':
					self.df.to_csv(export_fname,index=False)
				else:
					self.df.to_excel(export_fname,index=False)	
				
				msg = QMessageBox(self)			
				msg.setText("Cleaned Successfully")			
				msg.exec_()

			else:
				msg = QMessageBox(self)			
				msg.setText("Select at least 1 option")			
				msg.exec_()

		except:
			pass

	def center_window(self):
   		qtRectangle = self.frameGeometry()
   		centerPoint = QDesktopWidget().availableGeometry().center()
   		qtRectangle.moveCenter(centerPoint)
   		self.move(qtRectangle.topLeft())
		


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()    
    app.exec_()



