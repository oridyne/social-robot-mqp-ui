import QtQuick 2.12
import QtQuick.Window 2.12
import QtGraphicalEffects 1.0

Window {
    id:window
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")
    Rectangle {
        width: animation.width; height: animation.height + 8

        AnimatedImage {
            id: animation;
            source: "qrc:/../../../../run/user/1000/doc/ab0dcc65/blink.gif"
            width: 400;
            height: 400;
            x: 120
            y: 40
        }
    }
}


