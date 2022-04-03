import sys
import pygame
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QMainWindow, QApplication, QGridLayout, 
                             QWidget, QLayout)


class PopUpWindow(QMainWindow):
    """A class used to represent a popup window.

    This window shows whenever the game ends.
    Two push buttons are displayed inside.
    The user can replay or quit the game.

    Attributes
    ----------
    abalone: Abalone (required)
        Abalone board
    central_widget: QWidget
        Central widget
    h_box: QHBoxLayout
        Horizontal box to hold the two push buttons
    pbutton_replay: QPushButton
        Push button used to replay the game
    pbutton_quit: QPushButton:
        Push button used to quit the game

    Methods
    -------
    reset_game(self) [connected to pbutton_replay] -> None
        Calls the reset_game() method of the Abalone object
    set_run_game(self) -> None:
        Sets the attribute run_game to False
    get_run_game(self) -> bool:
        Returns the attribute run_game        
    """

    # Constructor
    # -----------
    def __init__(self, abalone):
        super().__init__()
        self.abalone = abalone
        self.setWindowTitle("Play again/Quit game?")
        self.setFixedHeight(100)
        self.setFixedWidth(290)
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.h_box = QtWidgets.QHBoxLayout(self.central_widget)
        self.pbutton_replay = QtWidgets.QPushButton(text="Replay")
        self.pbutton_replay.clicked.connect(self.reset_game)
        self.pbutton_replay.setFixedHeight(80)
        self.pbutton_quit = QtWidgets.QPushButton(text="Quit Game")
        self.pbutton_quit.clicked.connect(self.set_run_game)
        self.pbutton_quit.setFixedHeight(80)
        self.h_box.addWidget(self.pbutton_replay)
        self.h_box.addWidget(self.pbutton_quit)
        self.run_game = True

    # Methods
    # -------
    @QtCore.pyqtSlot()
    def reset_game(self) -> None:
        self.abalone.reset_game()
        self.close()

    @QtCore.pyqtSlot()
    def set_run_game(self) -> None:
        self.run_game = False

    def get_run_game(self) -> bool:
        return self.run_game


def main():
    pass

if __name__ == "__main__":
    main()
