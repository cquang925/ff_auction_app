# A fantasy football drafting app for auction drafts.

import csv
import os
import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QLineEdit, QRadioButton, QFormLayout, \
    QHBoxLayout, QMainWindow, QToolBar, QGridLayout, QVBoxLayout, QTableView, QButtonGroup, QFrame, \
    QSizePolicy, QHeaderView, QGroupBox, QLCDNumber, QDialog, QDialogButtonBox, QInputDialog, QMessageBox, QSpacerItem
from PyQt5.QtGui import QPixmap, QFont, QIntValidator, QIcon, QFontDatabase
from PlayerData import Database
import Teams


# main window, asks user to create new draft or load a draft, then will setup app based on response
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Auction Draft App')
        self.move(50, 25)

        self.teamNum = 0
        self.teamNames = []
        # ask for user to create or load draft
        self.choice = self.startDlg()

        if self.choice == 'Create':
            self.teamNum = self.getTeamNum()
            self.teamNames = self.getTeamNames(self.teamNum)
        elif self.choice == 'Load':
            self.teamNames = self.loadTeams()
            self.teamNum = len(self.teamNames)

        # creates object for Team.py and passes along variables to set up table
        self.teamObj = Teams.TeamView(self.choice, self.teamNum, self.teamNames)

        self.pld = Database(self.choice)

        # Window frames and positioning frames in grid
        self.search = Search()
        self.topPlayers = TopPlayers()
        self.display = Display()
        self.options = Options()
        self.bidding = Bidding()

        self.centralWidget = QWidget()
        self.centralLayout = QGridLayout()

        self.centralLayout.addWidget(self.topPlayers, 0, 0, 1, 3)
        self.centralLayout.addWidget(self.search, 1, 0, 1, 1)
        self.centralLayout.addWidget(self.display, 1, 1, 2, 2)
        self.centralLayout.addWidget(self.options, 3, 0, 1, 3)
        self.centralLayout.addWidget(self.bidding, 1, 0, 2, 1)
        self.centralLayout.addWidget(self.teamObj, 0, 0)
        self.centralWidget.setLayout(self.centralLayout)

        # Connecting frame buttons to methods
        self.search.searchBtn.clicked.connect(self.on_search_click)
        self.options.select.clicked.connect(self.on_select_click)
        self.options.start.clicked.connect(self.on_start_click)
        self.options.cancel.clicked.connect(self.on_reset_click)
        self.options.save.clicked.connect(self.on_save_click)
        self.bidding.winner.clicked.connect(self.on_winner_click)

        self.setStyleSheet("""
            QWidget {
                background-color: rgb(255, 255, 255);
                color: rgb(0, 0, 0);
            }
        """)

        self.setCentralWidget(self.centralWidget)
        self._createMenu()
        self._createToolBar()

    # initial pop up dialogs to accept user input, used to set up team table
    def startDlg(self):
        opt = ['Create', 'Load']
        choice, okBtn = QInputDialog.getItem(self, 'Load or Create New', 'Please select Create New or Load Draft',
                                             opt, current=0, editable=False)
        if okBtn:
            return choice

    def getTeamNum(self):
        teamNum, OkPressed = QInputDialog.getInt(self, "Number of Teams", "Enter Number of Teams: ", 2, 2, 20)

        if OkPressed:
            return teamNum

    def getTeamNames(self, number):
        teamDialog = QDialog()
        teamDialog.setWindowTitle('Team Names')

        gridBox = QGridLayout()
        enterLbl = QLabel('Enter Team Names Below: ')
        gridBox.addWidget(enterLbl, 0, 0, 1, 0)

        # creates list of generic names used for QLineEdits
        teams = []
        for i in range(number):
            teams.append('Team ' + str(i + 1))

        # creates QLineEdits and assigns name from teams list, places QLineEdit on grid, lastly adds QLineEdit to a list
        teamName = []
        i = 0
        r = 1
        while i < number:
            teams[i] = QLineEdit()
            gridBox.addWidget(teams[i], r, 0)
            teamName.append(teams[i])
            i += 1
            if i >= number:
                pass
            else:
                teams[i] = QLineEdit()
                gridBox.addWidget(teams[i], r, 1)
                teamName.append(teams[i])
            i += 1
            r += 1

        # creates button and places on last row on grid
        okBtn = QDialogButtonBox.Ok
        btnBox = QDialogButtonBox(okBtn)
        btnBox.accepted.connect(teamDialog.accept)

        lastRow = -((-number//2) - 1)
        gridBox.addWidget(btnBox, lastRow, 1)

        teamDialog.setLayout(gridBox)

        if teamDialog.exec_():
            # creates list of names from QLineEdits entries and returns list
            names = []
            for team in teamName:
                names.append(team.text())
            return names

    # loads saved draft from Saved folder
    def loadTeams(self):
        names = []
        with open('Saved/Team Names.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                names = row
        return names

    # window menu and tool bar. connects options to methods
    def _createMenu(self):
        self.menuBar().setStyleSheet("""
            QMenuBar{
                background: rgb(128, 128, 128);
                color: rgb(255, 255, 255);
                font: 10pt;
            }
            QMenuBar::item{
                spacing: 3px;
                padding: 2px 10px;
                border-radius: 1px;
            }
            QMenuBar::item:selected{
                background-color: rgb(0, 0, 100);
            }
        """)
        self.menu = self.menuBar().addMenu("Menu")
        self.menu.setStyleSheet("""
            QMenu{
                background: (255, 255, 240);
                color: (0, 0, 0);
            }
            QMenu::item{
                background-color: transparent;
            }
            QMenu::item:selected{
                background-color: rgb(0, 0, 128);
                color: rgb(255, 255, 255)
            }
        """)
        self.menu.addAction('Export to Excel', self.teamObj.export2excel)
        self.menu.addSeparator()
        self.menu.addAction('Exit', self.close)

        self.view = self.menuBar().addMenu('View')
        self.view.setStyleSheet("""
            QMenu{
                background: (255, 255, 240);
                color: (0, 0, 0);
            }
            QMenu::item{
                background-color: transparent;
            }
            QMenu::item:selected{
                background-color: rgb(0, 0, 128);
                color: rgb(255, 255, 255)
            }
        """)
        self.view.addAction('Search View', self.defaultView)
        self.view.addAction('Bidding View', self.biddingView)
        self.view.addAction('Team View', self.teamView)

    def _createToolBar(self):
        tools = QToolBar()
        tools.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        tools.addAction(QIcon('Images/magnifier.png'), 'Search View', self.defaultView)
        tools.addAction(QIcon('Images/money-bag-dollar.png'), 'Bidding View', self.biddingView)
        tools.addAction(QIcon('Images/users.png'), 'Team View', self.teamView)

        tools.setFloatable(False)

        tools.setStyleSheet("""
            QToolBar{
                background-color: rgb(70, 72, 74);
                color: rgb(242, 243, 244);
            }
            QToolButton {
                background-color: rgb(80, 81, 82);
                color: rgb(242, 243, 244);
                border-width: 2px;
                spacing: 5px;
                padding: 3px;
                border-radius: 3px;
            }
        """)

        self.addToolBar(tools)

    # methods for button clicks
    # collects search criteria and sends to PlayerData.py then passes information to Results frame
    def on_search_click(self):
        self.display.clearDisplay()
        self.options.start.setEnabled(False)
        self.options.cancel.setEnabled(False)
        position = self.search.btnGroup.checkedButton().text()
        firstName = self.search.fNameInput.text()
        firstName = firstName.title()
        lastName = self.search.lNameInput.text()
        lastName = lastName.title()

        self.search.displayTable(self.pld.playerSea(position, firstName, lastName))

    # collects selected player info, sends to PlayerData.py, and sends data to Display frame
    def on_select_click(self):
        # try/except catches error if no player is selected and displays pop up warning
        try:
            name = self.search.selected()
            player = self.pld.selectedPlayer(*name)
            self.display.displayPlayer(*player)
        except IndexError:
            errorMsg = QMessageBox()
            errorMsg.setIcon(QMessageBox.Warning)
            errorMsg.setWindowTitle('Index Error')
            errorMsg.setText('No player was selected. Please select player')
            errorMsg.setDefaultButton(QMessageBox.Close)
            errorMsg.exec_()
        self.options.start.setEnabled(True)
        self.options.cancel.setEnabled(True)

    # starts bidding and displays bidding frame
    def on_start_click(self):
        self.biddingView()
        self.options.select.setEnabled(False)

    # cancels bidding and returns to search frame
    def on_reset_click(self):
        self.defaultView()
        self.options.resetOptions()
        self.search.displayTable(self.pld.blank())
        self.display.clearDisplay()

    # saves progress of draft to CSV file and saves into Saved folder
    def on_save_click(self):
        self.pld.saveDF()
        self.teamObj.saveTeams()
        self.teamObj.saveTable()

        msgBox = QMessageBox()
        msgBox.setWindowTitle('Saved')
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText('Progress has been saved!')
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.exec_()

    # opens pop up window to select team winner
    def on_winner_click(self):
        amt = self.bidding.bidAmount.text()
        player = self.display.nameLbl.text()
        team = self.display.teamLbl.text()
        position = self.display.position.text()

        if not amt:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No amount was entered. Please enter amount.")
            msg.setWindowTitle("Invalid Data")
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec_()
        elif not player:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No player was selected. Please select a player.")
            msg.setWindowTitle("Invalid Data")
            msg.setStandardButtons(QMessageBox.Close)
            msg.exec_()
            self.on_reset_click()
        else:
            owner, okPressed = QInputDialog.getItem(self, 'Select Team', 'Please Select Team Winner', self.teamNames)

            if okPressed and owner:
                amtLeft = self.teamObj.getMoney(owner)
                if int(amt) > amtLeft:
                    msg = QMessageBox()
                    msg.setWindowTitle("No Money")
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText(f'{owner} only has ${amtLeft} left. Please check amount and team table.\n'
                                f'{player} has not been removed from data.')
                    msg.exec_()
                else:
                    self.confirm_winner(owner, amt, player, team, position)

    # pop up window to confirm winner, sends team winner, selected player, bid amount to team table to update
    def confirm_winner(self, owner, amt, player, team, position):
        # collects winner data
        index = [position, int(self.display.posNum.text())]

        # opens dialog window to confirm winning information
        dlg = QDialog()
        dlg.setWindowTitle('Winner. Winner. Chicken Dinner')
        dlg.resize(250, 250)

        imgLbl = QLabel()
        img = QPixmap('Images/congrats.jpg')
        imgLbl.setPixmap(img)
        imgLbl.setAlignment(Qt.AlignCenter)

        congratsLbl = QLabel(f'Congratulations {owner}')
        congratsLbl.setStyleSheet("""
            QLabel {
                color: blue;
                font-size: 40pt           
            }
        """)
        msgLbl = QLabel(f'{owner} has purchased {player} on {team} for ${amt}!\n'
                        f'Click OK to confirm')
        msgLbl.setStyleSheet("""
            QLabel {
                font-size: 20pt        
            }
        """)

        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(btns)
        buttonBox.accepted.connect(dlg.accept)
        buttonBox.rejected.connect(dlg.reject)

        layout = QVBoxLayout()
        layout.addWidget(imgLbl)
        layout.addWidget(congratsLbl)
        layout.addWidget(msgLbl)
        layout.addWidget(buttonBox)

        dlg.setLayout(layout)

        # if confirmed, sends data to Teams.py to update table, sends data to PlayerData.py to remove player, clears
        # window and return to search frame
        if dlg.exec_():
            self.teamObj.updateTable(owner, player, amt, position)
            if self.teamObj.updateComp:
                self.pld.removePlayer(*index)
            self.search.clearSearch()
            self.on_search_click()
            self.search.displayTable(self.pld.blank())
            self.bidding.clearBidAmt()
            self.options.resetOptions()
            self.defaultView()
        else:
            pass

    def playerTop(self, position):
        self.topPlayers.updateTopFive(*(self.pld.getTop(position)))

    def topTimer(self, i):
        topDisplay = self.topPlayers.top5Lbl[i]
        self.playerTop(topDisplay)

        i = (i + 1) % len(self.topPlayers.top5Lbl)

        if i < 6:
            QTimer.singleShot(7*1000, lambda: self.topTimer(i))

    # different window views, sets frames visibility to True or False
    def teamView(self):
        self.search.setVisible(False)
        self.topPlayers.setVisible(False)
        self.display.setVisible(False)
        self.options.setVisible(False)
        self.bidding.setVisible(False)
        self.teamObj.setVisible(True)

    def defaultView(self):
        self.search.setVisible(True)
        self.topPlayers.setVisible(True)
        self.display.setVisible(True)
        self.options.setVisible(True)
        self.bidding.setVisible(False)
        self.teamObj.setVisible(False)

    def biddingView(self):
        self.search.setVisible(False)
        self.topPlayers.setVisible(True)
        self.display.setVisible(True)
        self.options.setVisible(True)
        self.bidding.setVisible(True)
        self.teamObj.setVisible(False)


class TopPlayers(QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(65)

        self.topBox = QGroupBox()

        hbox = QHBoxLayout()

        self.top5Lbl = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
        self.nameLbl = [f'label{num}' for num in range(12)]
        self.labels = {}

        for i in range(12):
            self.labels[i] = QLabel('')
            hbox.addWidget(self.labels[i])

        QFontDatabase.addApplicationFont("Images/digital-7.ttf")
        self.setStyleSheet("""
            QLabel {
                color: rgb(0, 255, 0);
                font: 20pt;
                font-family: digital-7;
                spacing: 1px;
            }
            QWidget {
                background: rgb(0, 0, 100);
            }
        """)

        self.topBox.setLayout(hbox)
        self.topBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.topFrame = QHBoxLayout()
        self.topFrame.addWidget(self.topBox)

        self.setLayout(self.topFrame)
        self.show()

    def updateTopFive(self, *args):
        self.labels[0].setText(f'Top 5 {args[0]}: ')

        i = 1
        for player in args[1:]:
            self.labels[i].setText(player)
            i += 2


# search frame sends criteria to PlayerData and receives data, sends data to Results frame to display
# TODO app crashes when no players found when clicking on search
class Search(QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(500)

        searchBox = QGroupBox('Search')
        formLayout = QFormLayout()

        # creates radio buttons
        self.posRad = [QRadioButton('All'), QRadioButton('QB'), QRadioButton('RB'), QRadioButton('WR'),
                       QRadioButton('TE'), QRadioButton('K'), QRadioButton('DEF')]
        self.btnGroup = QButtonGroup()
        self.posRad[0].setChecked(True)
        self.hBox = QHBoxLayout()

        for i in range(len(self.posRad)):
            self.hBox.addWidget(self.posRad[i])
            self.btnGroup.addButton(self.posRad[i], i)

        formLayout.addRow('Position: ', self.hBox)

        # creates entry fields
        self.fNameInput = QLineEdit()
        self.lNameInput = QLineEdit()

        formLayout.addRow("First Name: ", self.fNameInput)
        formLayout.addRow("Last Name: ", self.lNameInput)

        # Search Button
        self.searchBtn = QPushButton('Search')

        formLayout.addRow(self.searchBtn)

        searchBox.setStyleSheet("""
            QPushButton{
                background: rgb(183, 186, 186);
                border-radius: 3px;
                color: rgb(0, 0, 153);
                font: 14pt;
            }
            QLineEdit{
                background: rgb(255, 255, 255);
                color: rgb(0, 0, 0);
                font: 10pt;
            }
            QLabel{
                font: 12pt;
            }
        """)

        searchBox.setLayout(formLayout)

        resultsBox = QGroupBox('Results')
        vbox = QVBoxLayout()

        self.playerTable = QTableView()
        self.playerTable.setSelectionBehavior(QTableView.SelectRows)
        self.playerTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.playerTable.setStyleSheet("""
            QHeaderView::section {
                background: rgb(192, 192, 192);
                color: rgb(0, 0, 0);
                border: 1px solid black;
                font: bold 12pt;
            }
            QTableView{
                background-color: rgb(240, 241, 242);
                color: rbg(0, 0, 0);
                font: 12pt;
            }
        """)
        vbox.addWidget(self.playerTable)

        resultsBox.setLayout(vbox)

        frameLayout = QVBoxLayout()
        frameLayout.addWidget(searchBox)
        frameLayout.addWidget(resultsBox)

        self.setLayout(frameLayout)
        self.resize(250, 100)
        self.maximumWidth()
        self.show()

    # clears search fields and sets radio button default
    def clearSearch(self):
        self.fNameInput.clear()
        self.lNameInput.clear()
        self.posRad[0].setChecked(True)

    # accepts a model and updates Qtableview
    def displayTable(self, model):
        self.playerTable.setModel(model)
        self.update()

    # collects index of selected player from Qtableview, sends to PlayerData.py to get player details, returns player
    def selected(self):
        index = self.playerTable.selectedIndexes()
        first = index[0].data()
        last = index[1].data()
        firstLast = [first, last]
        return firstLast


# TODO change position image size, set label font and size
# Display frame receives data from Results frame and displays selected player information and stats
class Display(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Display Player')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumWidth(800)

        self.displayGrid = QGridLayout()
        self.img = self.images()

        # display team image and position image
        self.teamImgLbl = QLabel(self)
        self.teamImgLbl.setAlignment(Qt.AlignCenter)
        self.teamImgLbl.setPixmap(self.img['shield'])
        # this work??? yes, yes it does
        self.teamImgLbl.setStyleSheet("""
            padding-left: 50px;
            padding-right: 50px
        """)

        self.posImgLbl = QLabel(self)
        self.posImgLbl.setAlignment(Qt.AlignCenter)
        self.posImgLbl.setPixmap(self.img['Football'])

        self.displayGrid.addWidget(self.posImgLbl, 0, 0, 1, 2)
        self.displayGrid.addWidget(self.teamImgLbl, 0, 2, 1, 2)

        # Player stat labels, blank initially
        nameFont = QFont("Times", 40, QFont.Bold)

        self.nameLbl = QLabel()
        self.nameLbl.setStyleSheet("""
            QLabel {
                color: rgb(0, 128, 255);
            }
        """)
        self.nameLbl.setFont(nameFont)
        self.displayGrid.addWidget(self.nameLbl, 1, 0, 1, 2)

        self.posLbl = QLabel()
        self.posLbl.setStyleSheet("""
            QLabel {
                color: rgb(204, 0, 0);
            }
        """)
        self.posLbl.setFont(nameFont)
        self.displayGrid.addWidget(self.posLbl, 1, 2)

        self.teamLbl = QLabel()
        self.teamLbl.setStyleSheet("""
            QLabel {
                color: rgb(204, 0, 0);
            }
            """)
        self.teamLbl.setFont(nameFont)
        self.displayGrid.addWidget(self.teamLbl, 1, 3)

        # dictionary used to name labels and position labels on grid
        self.titleLbl = {}
        self.statLbl = {}
        self.projTitle = {}
        self.projStat = {}
        lblNum = {
            '1': 2,
            '2': 3,
            '3': 4,
            '4': 5,
            '5': 6,
            '6': 7,
            '7': 8,
            '8': 9,
            '9': 10,
            '10': 11,
            '11': 12,
            '12': 13
        }

        statFont = QFont('Times', 15)
        for num, row in lblNum.items():
            self.titleLbl[num] = QLabel()
            self.statLbl[num] = QLabel()
            self.projTitle[num] = QLabel()
            self.projStat[num] = QLabel()
            self.titleLbl[num].setFont(statFont)
            self.statLbl[num].setFont(statFont)
            self.projTitle[num].setFont(statFont)
            self.projStat[num].setFont(statFont)
            self.displayGrid.addWidget(self.titleLbl[num], row, 0)
            self.displayGrid.addWidget(self.statLbl[num], row, 1)
            self.displayGrid.addWidget(self.projTitle[num], row, 2)
            self.displayGrid.addWidget(self.projStat[num], row, 3)

        self.titleLbl['2'].setAlignment(Qt.AlignCenter)
        self.titleLbl['2'].setStyleSheet("""
                    QLabel {
                        color: rgb(0, 128, 255);
                        font-size: 25pt;
                        font-weight: bold;
                        font-family: Times
                    }
                """)

        self.projTitle['2'].setAlignment(Qt.AlignCenter)
        self.projTitle['2'].setStyleSheet("""
            QLabel {
                color: rgb(200, 0, 0);
                font-size: 25pt;
                font-weight: bold;
                font-family: Times
            }
        """)

        # hidden labels, used to hold index of player
        self.position = QLabel()
        self.posNum = QLabel()

        self.setLayout(self.displayGrid)
        self.resize(500, 800)
        self.show()

    # definition accepts key word arguments from PlayerData.py, iterates through dictionary, places data in specified
    # labels on display frame
    def displayPlayer(self, *args):
        self.clearDisplay()
        season = args[0]
        projections = args[1]
        self.titleLbl['2'].setText('2023 Season Stats')
        self.projTitle['2'].setText('2024 Projected Stats')

        i = 3
        for key in season:
            self.titleLbl[str(i)].setText(key)
            self.statLbl[str(i)].setText(season[key])
            i += 1

        j = 2
        for key in projections:
            if key == 'Pos':
                self.posImgLbl.setPixmap(self.img[projections[key]])
                self.position.setText(projections[key])
                self.posLbl.setText(projections[key])
                continue
            if key == 'PosNum':
                self.posNum.setText(projections[key])
                continue
            if key == 'Name':
                self.nameLbl.setText(projections['Name'])
                continue
            if key == 'Team':
                self.teamLbl.setText(projections['Team'])
                self.teamImgLbl.setPixmap(self.img[projections[key]])
            else:
                self.projTitle[str(j)].setText(key)
                self.projStat[str(j)].setText(projections[key])
            j += 1

        self.update()

    # definition creates dictionary of images used in Display frame, returns dictionary
    def images(self):
        imgFootball = QPixmap('Images/football.jpg')
        imgQB = QPixmap('Images/QB.jpg')
        imgRB = QPixmap('Images/RB.jpg')
        imgWR = QPixmap('Images/WR.jpg')
        imgTE = QPixmap('Images/TE.jpg')
        imgK = QPixmap('Images/K.jpg')
        imgDEF = QPixmap('Images/DEF.jpg')
        shield = QPixmap("Images/Teams/shield.png")

        img = {
            'Football': imgFootball,
            'QB': imgQB,
            'RB': imgRB,
            'WR': imgWR,
            'TE': imgTE,
            'K': imgK,
            'DEF': imgDEF,
            'nan': shield,
        }

        path = r'Images/Teams'
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                fileSplit = filename.split('.')
                name = fileSplit[0]
                logo = QPixmap(os.path.join(path, filename))
                img[name] = logo

        return img

    # clears display frame
    def clearDisplay(self):
        self.posImgLbl.setPixmap(self.img['Football'])
        self.teamImgLbl.setPixmap(self.img['nan'])
        self.nameLbl.setText('')
        self.teamLbl.setText('')
        self.posLbl.setText('')
        for i in range(1, 13):
            self.titleLbl[str(i)].setText('')
            self.statLbl[str(i)].setText('')
            self.projTitle[str(i)].setText('')
            self.projStat[str(i)].setText('')


# frame has buttons that connects to other frames on window
class Options(QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(70)
        optLayout = QHBoxLayout()

        self.select = QPushButton('Select')
        self.start = QPushButton('Start Bid')
        self.cancel = QPushButton('Reset')
        self.save = QPushButton('Save')

        # self.setStyleSheet("""
        #     QPushButton{
        #         background-color: rgb(70, 72, 74);
        #         background: white;
        #         border-radius: 3px;
        #         font: 14pt;
        #     }
        # """)

        self.select.setStyleSheet("""
            QPushButton{
                background: rgb(183, 186, 186);
                border-radius: 3px;
                color: rgb(0, 0, 0);
                font: 14pt;
            }
        """)

        self.start.setStyleSheet("""
            QPushButton {
                background: rgb(183, 186, 186);
                border-radius: 3px;
                color: Green;
                font-size: 16pt;
            }
        """)
        self.start.setEnabled(False)

        self.cancel.setStyleSheet("""
            QPushButton {
                background: rgb(183, 186, 186);
                border-radius: 3px;
                color: rgb(153, 0, 0);
                font: 16pt;
            }
        """)
        self.cancel.setEnabled(False)

        self.save.setStyleSheet("""
            QPushButton {
                background: rgb(183, 186, 186);
                border-radius: 3px;
                color: rgb(0, 0, 153);
                font: 14pt;
            }
        """)

        optLayout.addWidget(self.select)
        optLayout.addSpacing(300)
        optLayout.addWidget(self.start)
        optLayout.addWidget(self.cancel)
        optLayout.addSpacing(300)
        optLayout.addWidget(self.save)

        optLayout.sizeHint()

        self.setLayout(optLayout)
        self.show()

    # resets option buttons to be enabled or disabled
    def resetOptions(self):
        self.select.setEnabled(True)
        self.start.setEnabled(False)
        self.cancel.setEnabled(False)


# frame is initially hidden and becomes visible when user is ready to start bidding
class Bidding(QWidget):
    def __init__(self):
        super().__init__()
        self.hide()
        self.setMaximumWidth(500)

        self.minutes = 0
        self.seconds = 8

        bidOutLay = QHBoxLayout()
        self.bidGroup = QGroupBox("Bidding Floor")
        self.bidGroup.setFont(QFont("Times", 10))
        bidOutLay.addWidget(self.bidGroup)

        bidInLay = QGridLayout()

        # timer and lcd display
        self.lcd = QLCDNumber()
        self.lcd.display('{0:0<2d}:{1:0>2d}'.format(self.minutes, self.seconds))
        self.lcd.setStyleSheet("""
            QLCDNumber {
                background: red;
                color: rgb(255, 255, 255);
            }
        """)
        # self.lcd.setMinimumHeight(100)

        self.timer = QTimer()
        self.timer.timeout.connect(self.start)
        bidInLay.addWidget(self.lcd, 0, 0, 1, 3)

        self.startBtn = QPushButton("Start")
        self.startBtn.clicked.connect(self.start)
        self.stopBtn = QPushButton("Stop")
        self.stopBtn.clicked.connect(self.reset)
        self.setStyleSheet("""
            QPushButton {
                background: rgb(20, 45, 245);
                border-radius: 3px;
                font: 12pt;
            }
        """)
        bidInLay.addWidget(self.startBtn, 1, 1, 1, 1)
        bidInLay.addWidget(self.stopBtn, 1, 2, 1, 1)

        # bidding amount labels and line edits
        self.moneyLbl = QLabel('$')
        self.moneyLbl.setStyleSheet("""
            QLabel {
                text-align: right;
                font-size: 80pt;
                color: rgb(0, 125, 0);
            }
        """)
        bidInLay.addWidget(self.moneyLbl, 2, 0, 2, 1)

        self.bidAmount = QLineEdit()
        self.bidAmount.setMaxLength(3)
        self.bidAmount.setMinimumHeight(100)
        self.bidAmount.setMaximumWidth(275)
        self.bidAmount.setStyleSheet("""
            QLineEdit {
                background: rgb(255, 255, 255);
                font-size: 100pt;
                color: rgb(0, 125, 0);
            }
        """)
        self.bidValid = QIntValidator(1, 300)
        self.bidAmount.setValidator(self.bidValid)
        bidInLay.addWidget(self.bidAmount, 2, 1, 2, 2)

        # winner button
        self.winner = QPushButton("WINNER!")
        self.winner.setStyleSheet("""
            QPushButton {
                background: rgb(25, 40, 255);
                border-radius: 3px;
                color: rgb(0, 125, 0);
                font-size: 20pt;
            }
        """)
        bidInLay.addWidget(self.winner, 3, 0, 1, 3)

        self.bidGroup.setLayout(bidInLay)
        self.setLayout(bidOutLay)

    # definitions control timer and timer display
    def countdown(self):
        self.lcd.display('{0:0<2d}:{1:0>2d}'.format(self.minutes, self.seconds))

    def start(self):
        self.seconds -= 1
        self.countdown()
        self.timer.start(1000)

        if self.seconds < 0:
            self.reset()

    def reset(self):
        self.timer.stop()
        self.seconds = 8
        self.countdown()

    # clears bid amount field
    def clearBidAmt(self):
        self.bidAmount.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    QTimer.singleShot(500, lambda: win.topTimer(0))
    win.show()
    sys.exit(app.exec())
