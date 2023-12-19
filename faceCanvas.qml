import QtQuick 2.12

Item {
    id : root
    width:640
    height:480
    Canvas {
        id: mycanvas
        onPaint: {
            var x = root.width / 3;
            var y = root.height / 3;
            var radius = 20;
            var startAngle = (Math.PI / 180) * 270;
            var fullAngle = (Math.PI / 180) * (270 + 360);
            var ctx = getContext("2d");
            ctx.reset();
            ctx.fillStyle = Qt.rgba(0, 0, 0, 1);
            ctx.fillRect(0, 0, width, height);

            ctx.fillStyle = Qt.rgba(0, 0, 1, 1);
            ctx.beginPath();
            ctx.moveTo(x,y);
            ctx.arc(x, y, radius-1, startAngle, fullAngle);
            ctx.lineTo(x, y)
            ctx.fill()

            x = root.width - root.width/3 ;
            y = root.height /3;
            ctx.fillStyle = Qt.rgba(0, 0, 1, 1);
            ctx.beginPath();
            ctx.moveTo(x,y);
            ctx.arc(x, y, radius-1, startAngle, fullAngle);
            ctx.lineTo(x, y)
            ctx.fill()
        }
    }
}
