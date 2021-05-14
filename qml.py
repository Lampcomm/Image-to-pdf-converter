import sys
import imghdr
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QStringListModel, QUrl


# Класс с функциями, вызываемыми из qml
class Actions(QObject):
    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot()
    def convert(self):
        pass

    @pyqtSlot()
    def addImg(self):
        pass

    @pyqtSlot()
    def deleteImg(self):
        pass

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
        for i in urlsList:
            url = QUrl()
            url.setUrl(i)
            self._listOfImg.append(url.toLocalFile())

    # Проверка списка url ссылок на то, что они являются изображениями
    @pyqtSlot(list, result=bool)
    def isImgList(self, urlsList):
        for i in urlsList:
            if i is None:
                continue

            url = QUrl()
            url.setUrl(i)
            if not url.isLocalFile() or imghdr.what(url.toLocalFile()) is None:
                return False
        return True

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
    # actions.addToListOfImg(["Images/1.png", "Images/2.png", "Images/3.png"])

    engine.rootContext().setContextProperty("actions", actions)
    engine.load("mainWindow.qml")

    engine.quit.connect(app.quit)

    sys.exit(app.exec_())
