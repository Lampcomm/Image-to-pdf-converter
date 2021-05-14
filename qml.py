import os
import sys
import imghdr
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from urllib.request import urlopen

class Actions(QObject):
    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot()
    def convert(self):
        pass

    @pyqtSlot(result=str)
    def addImg(self):
        pass
        # input_file = easygui.fileopenbox("Add image", "Converter", filetypes=["*.png"])
        # input_file.replace('\\', '/')
        # print(input_file)
        # # self._listOfImg.append("Images\\1.png")
        # self._listOfImg += ["Images/1.png", "Images/2.png", "Images/3.png"]
        # # self._listOfImg.append(input_file)
        # return self._listOfImg[self._imgIndex]

    @pyqtSlot(result=str)
    def deleteImg(self):
        if len(self._listOfImg) > 0:
            self._listOfImg.pop(self._imgIndex)
            self._imgIndex -= 1
            if self._imgIndex < 0:
                self._imgIndex = len(self._listOfImg) - 1
            if len(self._listOfImg) == 0:
                return self._noImgStr
            else:
                return self._listOfImg[self._imgIndex]
        else:
            return self._noImgStr

    # Получение следующего изображения из списка
    @pyqtSlot(result=str)
    def getNextImg(self):
        if len(self._listOfImg) > 0:
            self._imgIndex += 1
            if self._imgIndex >= len(self._listOfImg):
                self._imgIndex = 0

            return self._listOfImg[self._imgIndex]
        else:
            return self._noImgStr

    # Получение предыдущего изображения из списка
    @pyqtSlot(result=str)
    def getPrevImg(self):
        if len(self._listOfImg) > 0:
            self._imgIndex -= 1
            if self._imgIndex < 0:
                self._imgIndex = len(self._listOfImg) - 1
            return self._listOfImg[self._imgIndex]
        else:
            return self._noImgStr

    # Получение текущего изображения из списка
    @pyqtSlot(result=str)
    def getCurImg(self):
        if len(self._listOfImg) > 0:
            return self._listOfImg[self._imgIndex]
        else:
            return self._noImgStr

    # Добавление изображений в список выбранных изображений при их перетаскивание
    @pyqtSlot(list)
    def dropEvent(self, urlsList):
        self.addToListOfImg(urlsList)

    # Проверка списка url ссылок на то, что они являются изображениями
    @pyqtSlot(list, result=bool)
    def isImgList(self, urlsList):
        for i in urlsList:
            if i is None:
                continue

            if imghdr.what(None, urlopen(i).read()) is None:
                return False
        return True

    # Добавление списка изображение к текущему списку изображений
    def addToListOfImg(self, listOfImg):
        self._listOfImg += listOfImg

    # Индекс текущего выводимого изображения
    _imgIndex = 0

    # Список путей к все выбранным изображениям
    _listOfImg = []

    # Путь к изображению, выводимому по умолчанию
    _noImgStr = "Images/no-image.png"


if __name__ == "__main__":
    sys_argv = sys.argv
    sys_argv += ['--style', 'material']
    app = QGuiApplication(sys_argv)
    app.setWindowIcon(QIcon("Images/icon.png"))

    engine = QQmlApplicationEngine()

    actions = Actions()
    actions.addToListOfImg(["Images/1.png", "Images/2.png", "Images/3.png"])

    engine.rootContext().setContextProperty("actions", actions)
    engine.rootContext().setContextProperty("appPath", os.getcwd())
    engine.load("mainWindow.qml")

    engine.quit.connect(app.quit)

    sys.exit(app.exec_())
