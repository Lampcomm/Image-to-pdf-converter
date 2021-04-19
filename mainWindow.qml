import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    id: win

    Material.theme: Material.Dark
    Material.accent: Material.Purple

    visible: true
    width: 640
    height: 480

    title: "Image to pdf converter"

    Button {
        id: btnConvertAll
        text: "Convert All"
        width: 130
        height: 50

        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 5
        anchors.bottomMargin: 5

        onClicked: {
            actions.converAll()
        }
    }

    Image {
        property color btnColor: Qt.rgba(26 / 255, 29 / 255, 50 / 255, 0.3)

        id: img
        width: parent.width - 10
        height: parent.height - 100
        
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 5
        anchors.topMargin: 5

        Text {
            text: "Selcet an image"
            anchors.centerIn: parent
            color: "white"
            font.pixelSize: 20
            z: -1
        }

        source: actions.getCurImg()

        Rectangle {
            id: nextImgBtn

            width: 40
            height: parent.height

            anchors.right: parent.right
            anchors.top: parent.top

            
            color: nextBtnMsArea.containsPress ? Qt.darker(img.btnColor, 3) : img.btnColor

            Text {
                text: ">"
                anchors.centerIn: parent
                color: "white"
                font.pixelSize: 25
            }

            MouseArea {
                id: nextBtnMsArea
                anchors.fill: parent

                onClicked: {
                    img.source = actions.getNextImg()
                }
            }
        }

        Rectangle {
            id: prevImgBtn

            width: 40
            height: parent.height

            anchors.left: parent.left
            anchors.top: parent.top

            color: prevBtnMsArea.containsPress ? Qt.darker(img.btnColor, 3) : img.btnColor

            Text {
                text: "<"
                anchors.centerIn: parent
                color: "white"
                font.pixelSize: 25
            }

            MouseArea {
                id: prevBtnMsArea
                anchors.fill: parent

                onClicked: {
                    img.source = actions.getPrevImg()
                }
            }
        }
    }
}