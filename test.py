import sys

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QWidget, QGridLayout, QApplication


def prevSeaStat():
    qbCol = ["First Name", "Last Name", "Team", "GP", "Points", "Comp", "Pass Attempts", "Pass Yards", "Pass TDs",
             "Rush Yards", "Rush TDs"]

    rbCol = ["First Name", "Last Name", "Team", "GP", "Points", "Rush Attempts", "Rush Yards", "Rush TDs",
             "Targets", "Rec Yards", "Rec TDs"]

    recCol = ["First Name", "Last Name", "Team", "GP", "Points", "Targets", "Receptions", "Rec Yards", "Rec TDs"]

    kickerCol = ["First Name", "Last Name", "Team", "GP", "Points", "FG Made", "FG Att", "FG %", "XP Made"]

    defCol = ["First Name", "Last Name", "Team", "Points", "Sacks", "INTs", "Fumbles Rec", "Safeties", "Def TDs",
              "Pts Against"]

    df_qb = pd.read_csv('Data/QB.csv', header=None, names=qbCol)
    df_rb = pd.read_csv('Data/RB.csv', header=None, names=rbCol)
    df_wr = pd.read_csv('Data/WR.csv', header=None, names=recCol)
    df_te = pd.read_csv('Data/TE.csv', header=None, names=recCol)
    df_k = pd.read_csv('Data/K.csv', header=None, names=kickerCol)
    df_def = pd.read_csv('Data/DEF.csv', header=None, names=defCol)

    data = {'QB': df_qb,
            'RB': df_rb,
            'WR': df_wr,
            'TE': df_te,
            'K': df_k,
            'DEF': df_def}

    df_full = pd.concat(data)
    # df_full.to_csv('Data/seaStat.csv', header=True)

    print(df_full.iloc[2])


def projStats():
    df_qb = pd.read_csv('Data/qbProj.csv')
    df_rb = pd.read_csv('Data/rbProj.csv')
    df_wr = pd.read_csv('Data/wrProj.csv')
    df_te = pd.read_csv('Data/teProj.csv')
    df_k = pd.read_csv('Data/kProj.csv')
    df_def = pd.read_csv('Data/defProj.csv')

    data = {'QB': df_qb,
            'RB': df_rb,
            'WR': df_wr,
            'TE': df_te,
            'K': df_k,
            'DEF': df_def}

    df_full = pd.concat(data)
    df_full.to_csv('Data/seaProj.csv', header=True)

    print(df_full)


def testDF():
    df = pd.read_csv('Data/seaStats.csv')
    fname = 'Pittsburgh'
    lname = 'Steelers'

    playerSea = df.loc[(df['First Name'] == 'Pittsburgh') & (df['Last Name'] == 'Steelers')].copy()

    if playerSea.empty:
        playerSea.loc[0, 3:] = 'N/A'

    print(playerSea)


def dictComp():
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

    titleLbl = {f'titleLbl{k}': v for (k, v) in lblNum.items()}
    for item, row in titleLbl.items():
        item = QLabel()


def ImageResize():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Image Resize')
    layout = QGridLayout()

    image = QPixmap('Images/football.jpg')
    logo = QPixmap('Images/Teams/CHI.png')
    resizedImg = image.scaled(400, 500, Qt.KeepAspectRatio)
    logoResized = logo.scaled(350, 350, Qt.KeepAspectRatio)

    imgLbl = QLabel()
    imgLbl2 = QLabel()
    logoLbl = QLabel()
    logoLbl2 = QLabel()

    imgLbl.setPixmap(resizedImg)
    imgLbl2.setPixmap(image)
    logoLbl.setPixmap(logoResized)
    logoLbl2.setPixmap(logo)

    layout.addWidget(imgLbl, 0, 0)
    layout.addWidget(logoLbl, 0, 1)
    layout.addWidget(imgLbl2, 1, 0)
    layout.addWidget(logoLbl2, 1, 1)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec_())


####################################################

# projStats()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# ImageResize()

testDF()
