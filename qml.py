import os
import sys
import imghdr
import easygui
import pathlib
from PIL import Image
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSlot, QUrl
from urllib.request import urlopen

class Actions(QObject):
    def __init__(self):
        QObject.__init__(self)

    # Конвертация выбранных изображений в pdf
    @pyqtSlot(str)
    def convert(self, pathToFile):
        if self._listOfImg:
            pathToFile = QUrl(pathToFile).toLocalFile()
            images = []
            for i in self._listOfImg:
                url = QUrl()
                url.setUrl(i)

                if url.isLocalFile():
                    img = Image.open(url.toLocalFile())
                else:
                    img = Image.open(urlopen(i))

                if img.mode == "RGBA":
                    img = img.convert('RGB')
                images.append(img)

            images.pop(0).save(pathToFile, "PDF", append_images=images, save_all=True)


    @pyqtSlot()
    def addImg(self):
        input_file = easygui.fileopenbox("Add image", "Converter", filetypes=["*.png"], multiple=True)
        for i in input_file:
            self._listOfImg.append(pathlib.Path(i).as_uri())

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
        self._imgIndex = len(self._listOfImg) - 1

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
    # img = Image.open(r"D:\Users\dAxeponb\Pictures\IhxKCtQSRgnFYdWx.png")
    # img = img.convert('RGB')
    # img.save("test.pdf", "PDF", append_images=[], save_all=True)

    sys_argv = sys.argv
    sys_argv += ['--style', 'material']
    app = QGuiApplication(sys_argv)
    app.setWindowIcon(QIcon("Images/icon.png"))

    engine = QQmlApplicationEngine()

    actions = Actions()
    # actions.addToListOfImg(["Images/1.png", "Images/2.png", "Images/3.png"])

    engine.rootContext().setContextProperty("actions", actions)
    engine.rootContext().setContextProperty("appPath", os.getcwd())
    engine.load("mainWindow.qml")
    engine.quit.connect(app.quit)
    sys.exit(app.exec_())
