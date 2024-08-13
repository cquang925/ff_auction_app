# file holds data for players and stats

import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt


class Database:
    def __init__(self, choice):
        self.df_season = pd.read_csv('Data/seaStatsNew.csv', index_col=[0, 1])
        self.df_season = self.df_season.apply(pd.to_numeric, downcast='integer', errors='ignore')

        if choice == 'Create':
            # self.df_proj = pd.read_csv('Data/seaProj.csv', index_col=[0, 1])
            self.df_proj = pd.read_csv('Data/seaProjNew.csv', index_col=[0, 1])
        elif choice == 'Load':
            self.df_proj = pd.read_csv('Saved/df.csv', index_col=[0, 1])

        self.players = self.df_proj.loc[:, ['First Name', 'Last Name', 'Team']]

    def selectedPlayer(self, fname, lname):

        playerSea = self.df_season.loc[(self.df_season['First Name'] == fname) &
                                       (self.df_season['Last Name'] == lname)].copy()
        if playerSea.empty:
            playerSea.iloc[0, 3:] = 'N/A'

        playerProj = self.df_proj.loc[(self.df_proj['First Name'] == fname) & (self.df_proj['Last Name'] == lname)]
        indexProj = playerProj.index[0]

        # print(playerSea)

        # Use to future reference, to know column names
        # name = (playerSea.iloc[0, 0] + ' ' + playerSea.iloc[0, 1])
        # team = playerSea.iloc[0, 2]
        # gp = playerSea.iloc[0, 3]
        # pts = playerSea.iloc[0, 4]
        # comp = playerSea.iloc[0, 5]
        # pAtt = playerSea.iloc[0, 6]
        # pYrd = playerSea.iloc[0, 7]
        # pTDs = playerSea.iloc[0, 8]
        # rYrd = playerSea.iloc[0, 9]
        # rTDs = playerSea.iloc[0, 10]
        # rAtt = playerSea.iloc[0, 11]
        # targets = playerSea.iloc[0, 12]
        # recY = playerSea.iloc[0, 13]
        # recTDs = playerSea.iloc[0, 14]
        # rec = playerSea.iloc[0, 15]
        # fgMade = playerSea.iloc[0, 16]
        # fgAtt = playerSea.iloc[0, 17]
        # fgPer = playerSea.iloc[0, 18]
        # xp = playerSea.iloc[0, 19]
        # sacks = playerSea.iloc[0, 20]
        # inter = playerSea.iloc[0, 21]
        # fumbles = playerSea.iloc[0, 22]
        # safeties = playerSea.iloc[0, 23]
        # dTDs = playerSea.iloc[0, 24]
        # ptsAgst = playerSea.iloc[0, 25]

        if indexProj[0] == 'QB':
            season = {
                'Games Played': playerSea.iloc[0, 3],
                '2023 Fantasy Points': playerSea.iloc[0, 4],
                'Completions': playerSea.iloc[0, 5],
                'Pass Attempts': playerSea.iloc[0, 6],
                'Pass Yards': playerSea.iloc[0, 7],
                'Pass TDs': playerSea.iloc[0, 8],
                'Rush Yards': playerSea.iloc[0, 9],
                'Rush TDs': playerSea.iloc[0, 10]
            }
            projections = {
                'Pos': indexProj[0],
                'PosNum': indexProj[1],
                'Name': f'{playerProj.iloc[0, 0]} {playerProj.iloc[0, 1]}',
                'Team': playerProj.iloc[0, 2],
                'Bye': playerProj.iloc[0, 3],
                'Projected Points': playerProj.iloc[0, 4],
                'Completions': '',
                'Pass Attempts': playerProj.iloc[0, 6],
                'Pass Yards': playerProj.iloc[0, 7],
                'Pass TDs': playerProj.iloc[0, 8],
                'Rush Yards': playerProj.iloc[0, 9],
                'Rush TDs': playerProj.iloc[0, 10]
            }
            qbSeason = self.int2str(**season)
            qbProj = self.int2str(**projections)
            player = (qbSeason, qbProj)
            return player

        elif indexProj[0] == 'RB':
            season = {
                'Games Played': playerSea.iloc[0, 3],
                '2023 Fantasy Points': playerSea.iloc[0, 4],
                'Rush Attempts': playerSea.iloc[0, 11],
                'Rush Yards': playerSea.iloc[0, 9],
                'Rush TDs': playerSea.iloc[0, 10],
                'Targets': playerSea.iloc[0, 12],
                'Receiving Yards': playerSea.iloc[0, 13],
                'Receiving TDs': playerSea.iloc[0, 14]
            }
            projections = {
                'Pos': indexProj[0],
                'PosNum': indexProj[1],
                'Name': f'{playerProj.iloc[0, 0]} {playerProj.iloc[0, 1]}',
                'Team': playerProj.iloc[0, 2],
                'Bye': playerProj.iloc[0, 3],
                'Projected Points': playerProj.iloc[0, 4],
                'Rush Attempts': playerProj.iloc[0, 11],
                'Rush Yards': playerProj.iloc[0, 9],
                'Rush TDs': playerProj.iloc[0, 10],
                'Receptions': playerProj.iloc[0, 12],
                'Receiving Yards': playerProj.iloc[0, 13],
                'Receiving TDs': playerProj.iloc[0, 14]
            }
            rbSea = self.int2str(**season)
            rbProj = self.int2str(**projections)
            player = (rbSea, rbProj)
            return player

        elif indexProj[0] == 'WR' or indexProj[0] == 'TE':
            season = {
                'Games Played': playerSea.iloc[0, 3],
                '2023 Fantasy Points': playerSea.iloc[0, 4],
                'Targets': playerSea.iloc[0, 12],
                'Receptions': playerSea.iloc[0, 15],
                'Receiving Yards': playerSea.iloc[0, 13],
                'Receiving TDs': playerSea.iloc[0, 14]
            }
            projections = {
                'Pos': indexProj[0],
                'PosNum': indexProj[1],
                'Name': f'{playerProj.iloc[0, 0]} {playerProj.iloc[0, 1]}',
                'Team': playerProj.iloc[0, 2],
                'Bye': playerProj.iloc[0, 3],
                'Projected Points': playerProj.iloc[0, 4],
                'Targets': '',
                'Receptions': playerProj.iloc[0, 12],
                'Receiving Yards': playerProj.iloc[0, 13],
                'Receiving TDs': playerProj.iloc[0, 14]
            }
            wrSea = self.int2str(**season)
            wrProj = self.int2str(**projections)
            player = (wrSea, wrProj)
            return player

        elif indexProj[0] == 'K':
            season = {
                'Games Played': playerSea.iloc[0, 3],
                '2023 Fantasy Points': playerSea.iloc[0, 4],
                'Field Goals Made': playerSea.iloc[0, 16],
                'Field Goal Attempt': playerSea.iloc[0, 17],
                'Field Goal %': playerSea.iloc[0, 18],
                'Extra Points Made': playerSea.iloc[0, 19]
            }
            projections = {
                'Pos': indexProj[0],
                'PosNum': indexProj[1],
                'Name': f'{playerProj.iloc[0, 0]} {playerProj.iloc[0, 1]}',
                'Team': playerProj.iloc[0, 2],
                'Bye': playerProj.iloc[0, 3],
                'Projected Points': playerProj.iloc[0, 4],
                'Field Goals Made': playerProj.iloc[0, 15],
                'Field Goals Attempt': playerProj.iloc[0, 16],
                'Field Goal %': playerProj.iloc[0, 17],
                'Extra Points Made': playerProj.iloc[0, 18],
            }
            kSea = self.int2str(**season)
            kProj = self.int2str(**projections)
            player = (kSea, kProj)
            return player
        else:
            season = {
                'Games Played': '16',
                '2023 Fantasy Points': playerSea.iloc[0, 4],
                'Sacks': playerSea.iloc[0, 20],
                'Interceptions': playerSea.iloc[0, 21],
                'Fumbles Recovered': playerSea.iloc[0, 22],
                'Safeties': playerSea.iloc[0, 23],
                'Points Against': playerSea.iloc[0, 25],
                'Defensive TDs': playerSea.iloc[0, 24]
            }
            projections = {
                'Pos': indexProj[0],
                'PosNum': indexProj[1],
                'Name': f'{playerProj.iloc[0, 0]} {playerProj.iloc[0, 1]}',
                'Team': playerProj.iloc[0, 2],
                'Bye': playerProj.iloc[0, 3],
                'Projected Points': playerProj.iloc[0, 4],
                'Sacks': playerProj.iloc[0, 19],
                'Interceptions': playerProj.iloc[0, 20],
                'Fumbles Recovered': playerProj.iloc[0, 21],
                'Safeties': playerProj.iloc[0, 22],
                'Points Against': playerProj.iloc[0, 24],
                'Defensive TDs': playerProj.iloc[0, 23]
            }
            defSea = self.int2str(**season)
            defProj = self.int2str(**projections)
            defense = (defSea, defProj)
            return defense

    def int2str(self, **stat):
        strConv = stat.items()
        playerStat = {str(key): str(value) for key, value in strConv}
        return playerStat

    # TODO create if statement for fname and fname having entries
    def playerSea(self, pos, fName, lName):
        if pos == 'All':
            if len(fName) == 0 and len(lName) == 0:
                model = PandasModel(self.players)
                return model
            if len(fName) > 0 and len(lName) == 0:
                fnPlayers = self.players.loc[self.players['First Name'].str.contains(fName)]
                model = PandasModel(fnPlayers)
                return model
            if len(fName) == 0 and len(lName) > 0:
                lnPlayers = self.players.loc[self.players['Last Name'].str.contains(lName)]
                model = PandasModel(lnPlayers)
                return model
        elif pos == 'DEF':
            defense = (self.df_proj.loc[['DEF'], ['First Name', 'Last Name', 'Team']])
            model = PandasModel(defense)
            return model
        else:
            posSearch = self.players.loc[pos]
            if len(fName) == 0 and len(lName) == 0:
                model = PandasModel(posSearch)
                return model
            if len(fName) > 0 and len(lName) == 0:
                fnPlayers = posSearch.loc[posSearch['First Name'].str.contains(fName)]
                model = PandasModel(fnPlayers)
                return model
            if len(fName) == 0 and len(lName) > 0:
                lnPlayers = posSearch.loc[posSearch['Last Name'].str.contains(lName)]
                model = PandasModel(lnPlayers)
                return model
        return None

    def blank(self):
        blank = self.players.iloc[0:0]
        model = PandasModel(blank)
        return model

    def getTop(self, position):
        fiveList = [position]
        topFive = self.players.loc[f'{position}', ['First Name', 'Last Name']].head(5)
        for idx, row in topFive.iterrows():
            name = f"{row['First Name']} {row['Last Name']}"
            fiveList.append(name)

        return fiveList

    def removePlayer(self, *idx):
        self.df_proj.drop(idx, inplace=True)
        self.players.drop(idx, inplace=True)
        self.saveDF()

    def saveDF(self):
        self.df_proj.to_csv('Saved/df.csv', na_rep='', float_format='%.1f', header=True, index=True)


# class creates model to be used on QTableView in MainWindow.py
class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
