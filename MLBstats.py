import sys
import brscraper

import PyQt5 
from PyQt5 import QtCore, QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QLineEdit, QInputDialog, QPushButton, QCompleter
from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem, QVBoxLayout


class Window(QtWidgets.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50,50,1140,500)
		self.setWindowTitle("MLB Stats")

		#code menu bar. first name the action, set it
		extractAction = QtWidgets.QAction("&Quit", self)
		extractAction.triggered.connect(self.close_application)
		#set shortcut and status bar info
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip('Leave The App')
		#init the stat bar
		self.statusBar()
		#make menu bar and add our action to it, under File
		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('&File')
		fileMenu.addAction(extractAction )

		self.home()

	def home(self):
		#the names of the column headers
		self.statLabels = ['Name', 'BA', 'HR', 'RBI', 'R', 'OBP', '2B', '3B', 'SB',   'AB', 'PA']
		self.currentRow = -1  #index to keep track of current row
		self.players = dict() #dictionary to hold stats

		#progress bar
		self.progress = QtWidgets.QProgressBar(self)
		self.progress.setGeometry(10, 35, 250, 20)
		#action for progress bar (download data)
		self.btn = QtWidgets.QPushButton("Download Data", self)
		self.btn.move(10, 60)
		self.btn.clicked.connect(self.getData)

		#text input  line to tye name of player
		self.le = QLineEdit(self)
		self.le.setPlaceholderText("Enter Hitter Name")
		self.le.move(10, 100)

		#autocomplete for text line
		completer = QCompleter()
		completer.setCaseSensitivity(Qt.CaseInsensitive)
		self.le.setCompleter(completer)
		self.model = QStringListModel()
		completer.setModel(self.model)

		#some buttons
		#add player button
		self.btn2 = QPushButton('Add Player', self)
		self.btn2.move(10, 140)
		self.btn2.clicked.connect(self.addPlayer)
		#remove player button
		self.rembtn = QPushButton('Remove Prev', self)
		self.rembtn.move(110, 140)
		self.rembtn.clicked.connect(self.removeLastRow)
		#clear table
		self.clearbtn = QPushButton('Clear Table', self)
		self.clearbtn.move(210, 140)
		self.clearbtn.clicked.connect(self.clearTable)
		#mquit application
		quitbtn = QtWidgets.QPushButton("Close App", self)
		quitbtn.clicked.connect(self.close_application)
		quitbtn.move(310, 140)

		#build table
		self.tableWidget = QTableWidget(self)
		# set row/column counts
		self.tableWidget.setRowCount(10)
		self.tableWidget.setColumnCount(11)
		self.tableWidget.move(10,180)
		self.tableWidget.resize(1400, 1000)
		#set name of headers
		self.tableWidget.setHorizontalHeaderLabels(self.statLabels)

		self.show()

	#clear table
	def clearTable(self):
		while (self.currentRow > -1):
			self.removeLastRow()

	#remove previously added player
	def removeLastRow(self):
		if (self.currentRow > -1):
			for i in range(0, self.tableWidget.columnCount()):
				self.tableWidget.setItem(self.currentRow, i, QTableWidgetItem(str("")))
			self.currentRow = (self.currentRow - 1)
		
	#add player stats into table
	def addPlayer(self):
		player = self.le.text() 
		#if table isn't full and player entered exists
		if (self.currentRow < 9) and (player in self.players): 
			self.currentRow = self.currentRow + 1
			self.tableWidget.setItem(self.currentRow, 0, QTableWidgetItem(player)) #nter name field

			statfields = self.players.get(player)
			for i in range(1, len(self.statLabels)):  #enter all other fields under appropriate header
				label = self.statLabels[i]
				s = statfields.get(label)

				#2 of the fields will require special formatting (truncating decimals)
				if (label == "BA") or (label == "OBP"):
					self.tableWidget.setItem(self.currentRow, i, QTableWidgetItem("{0:10.3f}".format(s)))
				else:
					self.tableWidget.setItem(self.currentRow, i, QTableWidgetItem(str(s)))

			self.le.clear() #clear text after successful insertion

	#function to fetch data
	def getData(self):
		self.btn.setText("Downloading...")  #tell client we are dowenloading
		scraper = brscraper.BRScraper()  #initialize scraper
		teams = ["ARI", "ATL", "BAL", "BOS", "CHC", "CHW" , "CIN", "CLE", "COL", \
		"DET", "HOU" , "KCR", "LAA", "LAD", "MIA", "MIL", "MIN", "NYM", "NYY",\
		"OAK", "PHI", "PIT", "SEA", "SDP", "SFG", "STL", "TBR", "TEX", "TOR", "WSN"]

		#fetch data for each team
		for num, team in enumerate(teams):
			data = scraper.parse_tables("teams/" + team + "/2016.shtml", table_ids= 'team_batting') #build team URL
			batting = data.get('team_batting') #we're only interested in hitting stats for now

			#for each entry, we add if its a new player, or consolidate if its an existing player.
			#some players will appear in multiple teams, so we need to be ready to combine stats.
			for row in batting:
				if row['Name'] in self.players:
					stats = self.players[row['Name']]
					stats['HR'] =+ int(row['HR'])
					stats['2B'] =+ int(row['2B'])
					stats['3B'] =+ int(row['3B'])
					stats['SB'] =+ int(row['SB'])
					stats['RBI'] =+ int(row['RBI'])
					stats['R'] =+ int(row['R'])

					oldba = stats['BA']
					oldobp = stats['OBP']
					oldab = stats['AB']
					oldpa = stats['PA']

					ba = float(row['BA'])
					obp = float(row['OBP'])
					ab = int(row['AB'])
					pa = int(row['PA'])

					if (oldab + ab > 0):
						stats['BA'] = (oldba*oldab + ba*ab)/(oldab + ab)
					if (oldpa + pa > 0):
						stats['OBP'] = (oldobp*oldpa + obp*pa)/(oldpa + pa)

					stats['PA'] = oldpa + pa
					stats['AB'] = oldba + ba

					self.players[row['Name']] = stats

				else:
					self.players[row['Name']] = {'BA' : float(row['BA']), 'OBP' : float(row['OBP']), 'HR' : int(row['HR']), \
					'2B' : int(row['2B']), '3B' : int(row['3B']), 'SB' : int(row['SB']), \
					'RBI' : int(row['RBI']), 'R' : int(row['R']), 'PA' : int(row['PA']), \
					'AB' : int(row['AB']) }
			self.progress.setValue((num+1)/len(teams)*100) #update progress bar

		#when data retrieval is done, disable download button
		self.btn.setText("Done!")
		self.btn.setEnabled(False)
		#add list of names to auto-completer	
		self.model.setStringList(self.players.keys())				

	def close_application(self):
		print("Thanks for using MLB Stats!")
		sys.exit()

def main():
	app = QtWidgets.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

main()