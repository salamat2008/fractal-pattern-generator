from PySide6.QtWidgets import QApplication, QPushButton

import Lsystems.Lsystem

QApplication()
QPushButton()

if __name__ == "__main__":
    test = Lsystems.Lsystem.LSystem(rules = ["F FLFRRFLF", "L LF"], keywords = (("F", '4'), "B", "L", "R", ''))
    print(test)
