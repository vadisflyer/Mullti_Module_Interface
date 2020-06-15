import os
#from os import path
import shlex, subprocess
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from Interface import *
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog, QTextEdit
from PyQt5.QtGui import QTextCursor


class mywindow(QtWidgets.QMainWindow):


	def __init__(self):
		
		self.PATH = ''
		self.MODULE = ''
		self.PARAMETRS = ''

		self.PATH_PROJECT = ''
		self.NAME_PROJECT = ''


		super(mywindow,self).__init__()
		self.ui = Ui_Multi_Modules_Interface()
		self.ui.setupUi(self)
		

		self.ui.textEdit_Directs.setLineWrapMode(1)
		self.ui.textEdit_Modules.setLineWrapMode(1)
		self.ui.textEdit_Console.setLineWrapMode(1) 

		self.ui.textEdit_Console.setReadOnly(True)

		self.ui.textEdit_Directs.textChanged.connect(self.Combobox_Dir_Edit)

		self.ui.comboBox_directs.activated.connect(self.Combobox_Dir_Activated)
		self.ui.comboBox_modules.activated.connect(self.Combobox_Modules_Activated)
		self.ui.pushButton_Info.clicked.connect(self.Info_Window)
		self.ui.lineEdit_Parametrs.textEdited.connect(self.Edit_Parametrs)
		self.ui.Start_module_Button.clicked.connect(self.Run_Module)
		self.ui.AddModule_Button.clicked.connect(self.Write_Module)
		self.ui.Start_modules_Button.clicked.connect(self.Run_Modules)
		self.ui.Clear_Button.clicked.connect(self.Clear_Console)

		self.ui.actionCreate.triggered.connect(self.Create)
		self.ui.actionLoad.triggered.connect(self.Load)
		self.ui.actionSave.triggered.connect(self.Save)
		self.ui.actionReload.triggered.connect(self.Reload)
		self.ui.actionClear_all.triggered.connect(self.Clear_all)

	def Clear_Console(self):
		self.ui.textEdit_Console.clear()

	def Run_Modules(self):
		self.Save()
		module = self.NAME_PROJECT + '_Modules.txt'
		list_function = list()
		output_text = ''
		
		with open(os.path.join(self.PATH_PROJECT,self.NAME_PROJECT, module), 'r', encoding = 'utf-8') as f:
			for line in f.readlines():
				
				if not line.isspace():			
					list_function.extend(shlex.split(line))
					operation = subprocess.Popen(list_function, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
					operation.wait()

					for tup in operation.stdout:	
						output_text  += tup.decode('utf-8') 
					output_text += '\n'
		
			self.ui.textEdit_Console.moveCursor(QTextCursor.End)
			self.ui.textEdit_Console.insertPlainText('\n' + output_text)
			
	
	def Write_Module(self):
		if len(self.PATH) >0 and len(self.MODULE)>0:

			self.ui.textEdit_Modules.moveCursor(QTextCursor.End)
			self.ui.textEdit_Modules.insertPlainText(os.path.join(self.PATH,self.MODULE) +' '+ self.PARAMETRS +' '+ '\n\n' )


	def Clear_all(self):
		self.Clear_the_field()
		
		self.PATH = ''
		self.MODULE = ''
		self.PARAMETRS = ''

		self.PATH_PROJECT = ''
		self.NAME_PROJECT = ''
		

	def Clear_the_field(self):
		self.ui.textEdit_Directs.clear()
		self.ui.textEdit_Modules.clear()
		self.ui.textEdit_Console.clear()

	def Reload(self):
		if len(self.PATH_PROJECT)>0 and len(self.NAME_PROJECT)>0:
			Projectfolder = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT)
			Inputfolder = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,'Input_Media_File')
			OutputOpenMVG = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT, 'OpenMVG_Output')
			OutputOpenMVS = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,'OpenMVS_Output')
			OutputOpenMVSScene= os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,'OpenMVS_Output','Scene')
						
			if 	not os.mkdir(Projectfolder):
				 os.makedir(Projectfolder)
			if 	not os.mkdir(Inputfolder) :
				os.makedir(Inputfolder)
			if 	not os.mkdir(OutputOpenMVG) :
				os.makedir(OutputOpenMVG)
			if 	 os.mkdir(OutputOpenMVS) :
				os.makedir(OutputOpenMVS)
			if  os.mkdir(OutputOpenMVSScene):
				os.makedir(OutputOpenMVSScene)
			self.Enter_Text_From_File()
		else:
			self.ui.textEdit_Console.moveCursor(QTextCursor.End)
			self.ui.textEdit_Console.insertPlainText('\n Project not Create or Select')
		

	def Save(self):
		
		if len(self.PATH_PROJECT)>0 and len(self.NAME_PROJECT)>0:

			Projectfolder = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT)
			Inputfolder = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,'Input_Media_File')
			OutputOpenMVG = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT, 'OpenMVG_Output')
			OutputOpenMVS = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,'OpenMVS_Output')
			OutputOpenMVSScene= os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,'OpenMVS_Output','Scene')
						
			if 	not os.path.exists(Projectfolder):
				 os.makedir(Projectfolder)
			if 	not os.path.exists(Inputfolder) :
				os.makedir(Inputfolder)
			if 	not os.path.exists(OutputOpenMVG) :
				os.makedir(OutputOpenMVG)
			if 	 not os.path.exists(OutputOpenMVS) :
				os.makedir(OutputOpenMVS)
			if  not os.path.exists(OutputOpenMVSScene):
				os.makedir(OutputOpenMVSScene)
			
			Dirfile  = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,self.NAME_PROJECT) + '_Directs.txt'
			with open(Dirfile, 'w', encoding = "utf-8") as f:
				f.write(self.ui.textEdit_Directs.toPlainText())
			
			
			Modfile  = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,self.NAME_PROJECT) + '_Modules.txt'
			with open(Modfile, 'w', encoding = 'utf-8') as f:
				f.write(self.ui.textEdit_Modules.toPlainText())
			
			Consfile  = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,self.NAME_PROJECT) + '_Output.txt'
			with open(Consfile, 'w', encoding = 'utf-8') as f:
				f.write(self.ui.textEdit_Console.toPlainText())
		else: self.Create()

		
	def Create(self):
			
		window = QDialog()
		window.setWindowTitle("Enter Name Project")
		window.resize(500,80)
		lineEdit = QtWidgets.QLineEdit()
		lineEdit.resize(480,40)
		button = QtWidgets.QPushButton("E&nter")
		button.clicked.connect(window.accept)

		hbox = QtWidgets.QHBoxLayout()
		hbox.addWidget(button)
		form = QtWidgets.QFormLayout()
		form.addRow("&Please, Enter Name Project", lineEdit)
		form.addRow(hbox)
		window.setLayout(form)
		window.show()


		window.exec_()
		self.NAME_PROJECT =lineEdit.text()

		self.PATH_PROJECT = QFileDialog.getExistingDirectory(self, "Open Directory", "/home",QFileDialog.ShowDirsOnly| QFileDialog.DontResolveSymlinks)
					
		if not os.path.exists(os.path.join(self.PATH_PROJECT,self.NAME_PROJECT)):
			found = '' 
			output = ''

			if  os.path.exists('/home/'+ os.getlogin()+'/openMVG_Build'):
				found += '/home/'+ os.getlogin()+'/openMVG_Build/Linux-x86_64-RELEASE' + '\n'
			else: found += 'not found path to Open_MVG_Build'
			if  os.path.exists('/home/'+ os.getlogin()+'/openMVS_build'):
				found += '/home/'+ os.getlogin()+'/openMVS_build/bin' + '\n'
			else: found += 'not found path to Open_MVS_build'

			Projectfolder = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT)
			Inputfolder = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,'Input_Media_File')
			OutputOpenMVG = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT, 'OpenMVG_Output')
			OutputOpenMVS = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,'OpenMVS_Output')
			OutputOpenMVSScene= os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,'OpenMVS_Output','Scene')
						
			if 	not os.mkdir(Projectfolder):
				output += Projectfolder + '\n'
			else: output += 'directory ' + Projectfolder + ' not created'
			if 	not os.mkdir(Inputfolder) :
				output += Inputfolder + '\n'
			else: output += 'directory ' + Inputfolder +  ' not created'
			if 	not os.mkdir(OutputOpenMVG) :
				output += OutputOpenMVG + '\n'
			else: output += 'directory ' + OutputOpenMVG + ' not created'
			if 	not os.mkdir(OutputOpenMVS) :
				output += OutputOpenMVS +'\n'
			else: output += 'directory ' + OutputOpenMVS + ' not created'
			if 	not os.mkdir(OutputOpenMVSScene):
				output += OutputOpenMVSScene + '\n'
			else: output += 'directory ' + OutputOpenMVSScene + ' not created'
			
			Dirfile  = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,self.NAME_PROJECT) + '_Directs.txt'
			with open(Dirfile, "a+", encoding = "utf-8") as f:
				
				f.write(found+'\n'+output) 
				output += Dirfile + '\n' 

			Modfile  = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,self.NAME_PROJECT) + '_Modules.txt'
			with open(Modfile, 'a+', encoding = 'utf-8') as f:
				output += Modfile  + '\n'
				
			Consfile  = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,self.NAME_PROJECT) + '_Output.txt'
			with open(Consfile, 'a+', encoding = 'utf-8') as f:
				output += Consfile + '\n'
				f.write('Found:\n '+ found + 'Created:\n' + output)


			os.chdir(Projectfolder)
		self.Enter_Text_From_File()
	
	def Load(self):
		self.Clear_the_field()
		inputpath = QFileDialog.getExistingDirectory(self, "Select Project Directory", "/home",QFileDialog.ShowDirsOnly| QFileDialog.DontResolveSymlinks)
		self.NAME_PROJECT = os.path.basename(inputpath)
		self.PATH_PROJECT = inputpath[:inputpath.rfind(self.NAME_PROJECT)]
#		print(self.NAME_PROJECT, ' in ', self.PATH_PROJECT)
		self.Enter_Text_From_File()
		
	def Enter_Text_From_File(self):
			
			Dirfile  = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,self.NAME_PROJECT) + '_Directs.txt'
			with open(Dirfile, 'r', encoding = "utf-8") as f:
				self.ui.textEdit_Directs.setPlainText(f.read())
			
			Modfile  = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,self.NAME_PROJECT) + '_Modules.txt'
			with open(Modfile, 'r', encoding = 'utf-8') as f:
				self.ui.textEdit_Modules.setPlainText(f.read())
			
			Consfile  = os.path.join(self.PATH_PROJECT,self.NAME_PROJECT,self.NAME_PROJECT) + '_Output.txt'
			with open(Consfile, 'r', encoding = 'utf-8') as f:
				self.ui.textEdit_Console.setPlainText(f.read())


	def Combobox_Dir_Edit(self):
		
		self.ui.comboBox_directs.clear()		
		directs_list = shlex.split(self.ui.textEdit_Directs.toPlainText())
		for tup in range(len(directs_list)):
			self.ui.comboBox_directs.addItem(directs_list[tup])


	def Combobox_Dir_Activated(self):
		self.PATH = self.ui.comboBox_directs.currentText()
		self.Combobox_Modules_Edit()

	def Combobox_Modules_Edit(self):
		
		self.MODULE = ''		
		self.ui.comboBox_modules.clear()
		
		files_list = os.listdir(self.PATH)
		files_list.sort()
		for tup in files_list:
			self.ui.comboBox_modules.addItem(tup)
			


	def Combobox_Modules_Activated(self):
		self.MODULE = self.ui.comboBox_modules.currentText()

	def Info_Window(self):
#		window = QDialog()
		
		window = QtWidgets.QDialog()
		window.setWindowTitle("Info")
		window.resize(700,250)

		edittext = QtWidgets.QTextEdit()
		edittext.setReadOnly(True)

		edittext.textChanged.connect(self.Combobox_Dir_Edit)
		
		button = QtWidgets.QPushButton("O&k")
		button.clicked.connect(window.accept)

		hbox = QtWidgets.QHBoxLayout()
		hbox.addWidget(button)
		
		form = QtWidgets.QFormLayout()
		form.addRow("&CONSOLEOUT:",edittext)
		form.addRow(hbox)
		
		window.setLayout(form)
		
		output_text = ''
		operation = subprocess.Popen([os.path.join(self.PATH, self.MODULE), "--help"], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		
		for line in operation.stdout:	
			output_text += line.decode('utf-8')
		operation.wait() 

		edittext.insertPlainText(output_text)
		window.show()
		window.exec_()
		

	def Edit_Parametrs(self):
		self.PARAMETRS = self.ui.lineEdit_Parametrs.text()

		
	def Run_Module(self):
		self.Edit_Parametrs()


		output_text = ''
		list_function = list()

		list_function.append(os.path.join(self.PATH, self.MODULE))

		list_function.extend(shlex.split(self.PARAMETRS))
		operation = subprocess.Popen(list_function, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
		operation.wait()
		
		for line in operation.stdout:	
			output_text  += line.decode('utf-8')

		
		self.ui.textEdit_Console.moveCursor(QTextCursor.End)
		self.ui.textEdit_Console.insertPlainText('\n' + output_text)
		
app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())
