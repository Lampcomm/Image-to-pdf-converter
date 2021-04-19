import sys
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QStringListModel

class Actions(QObject):
    def __init__(self):
        QObject.__init__(self)
    
    @pyqtSlot()
    def converAll(self):
        pass

    @pyqtSlot(result=str)
    def getNextImg(self):
        if len(self._listOfImg) > 0:
            self._imgIndex += 1
            if self._imgIndex >= len(self._listOfImg):
                self._imgIndex = 0

            return self._listOfImg[self._imgIndex]
        else:
            return self._noImgStr

    @pyqtSlot(result=str)
    def getPrevImg(self):
        if len(self._listOfImg) > 0:
            self._imgIndex -= 1
            if self._imgIndex < 0:
                self._imgIndex = len(self._listOfImg) - 1
            return self._listOfImg[self._imgIndex]
        else:
            return self._noImgStr

    @pyqtSlot(result=str)
    def getCurImg(self):
        if len(self._listOfImg) > 0:
            return self._listOfImg[self._imgIndex]
        else:
            return self._noImgStr

    def addToListOfImg(self, listOfImg):
        self._listOfImg += listOfImg

    _imgIndex = 0
    _listOfImg = []
    _noImgStr = "Images/no-image.png"
   

if __name__ == "__main__": 
    sys_argv = sys.argv
    sys_argv += ['--style', 'material']
    app = QGuiApplication(sys_argv)
    app.setWindowIcon(QIcon("Images/icon.png"))
    
    engine = QQmlApplicationEngine()

    actions = Actions()
    actions.addToListOfImg(["1.png", "2.png", "3.png"])

    engine.rootContext().setContextProperty("actions", actions)
    engine.load("mainWindow.qml")

    engine.quit.connect(app.quit)

    sys.exit(app.exec_())