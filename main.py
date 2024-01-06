import numpy as np
from PySide6.QtWidgets import QApplication, QPushButton

import Lsystems.Lsystem

QApplication()
QPushButton()

if __name__ == "__main__":
    test = Lsystems.Lsystem.LSystem(rules = ["F FLFRRFLF", "L LF"], keywords = (("F", '4'), "B", "L", "R", ''))
    arr = np.zeros((len(test.keywords), len(max(test.keywords, key = len))), dtype = np.str_)
    for index, item in enumerate(test.keywords):
        for jndex, jtem in enumerate(item):
            arr.itemset((index, jndex), jtem)
    print(arr)
    print(test)
