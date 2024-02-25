from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMainWindow
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal, Slot
from rqt_gui_py.plugin import Plugin
from PIL import Image
from std_msgs.msg import String
import rospkg
import rospy
import os

class MyPlugin(Plugin):
    def __init__(self, context):
        super(MyPlugin, self).__init__(context)
        self.setObjectName('MyPlugin')

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                    dest="quiet",
                    help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print ('arguments: ', args)
            print ('unknowns: ', unknowns)

        gif_file = os.path.join(rospkg.RosPack().get_path('rqt_mypkg'), 'resource', 'blink.gif')
        # GUI initialization code 
        self._widget = ImagePlayer(gif_file, "Robot UI")
        print("UI instance created")
        self._widget.showMaximized()
        self.sub = rospy.Subscriber("/rqt_mypkg/mode", String, self.callback)

    def shutdown_plugin(self):
        self.sub.unregister()

    def callback(self, mode_d):
        print(mode_d.data)
        mode = str(mode_d.data)
        self._widget.change.emit(mode)


def smooth_gif_resize(gif, frameWidth, frameHeight):
    gif = Image.open(gif)
    gifWidth0, gifHeight0 = gif.size

    widthRatio = frameWidth / gifWidth0
    heightRatio = frameHeight / gifHeight0

    if widthRatio >= heightRatio:
        gifWidth1 = gifWidth0 * heightRatio
        gifHeight1 = frameHeight
        return gifWidth1, gifHeight1

    gifWidth1 = frameWidth
    gifHeight1 = gifHeight0 * widthRatio
    return gifWidth1, gifHeight1


class ImagePlayer(QWidget):
    change = Signal(str)
    
    def __init__(self, filename, title, parent=None):
        QWidget.__init__(self, parent)
        self.change.connect(self.changeGif)
        # Load the file into a QMovie
        self.movie = QtGui.QMovie(filename, QtCore.QByteArray(), self)
        gifSize = QtCore.QSize(*smooth_gif_resize(filename, 500, 500))
        self.movie.setScaledSize(gifSize)
        size = self.movie.scaledSize()
        self.setGeometry(300, 300, size.width(), size.height())
        self.setWindowTitle(title)
        # self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.movie_screen = QLabel()
        # Make label fit the gif
        self.movie_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.movie_screen.setAlignment(QtCore.Qt.AlignCenter)
        # self.movie_screen.setMaximumWidth(100)

        # Create the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.movie_screen)

        self.setLayout(main_layout)
        # Add the QMovie object to the label
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        # self.movie.setSpeed(100)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()

    @Slot(str) 
    def changeGif(self,mode):
        modes = ['angry', 'blink', 'neutral', 'smirk', 'surprise']
        if mode not in modes:
            print("Unrecognized Mode")
            return
        
        filename = mode + ".gif"
        gif_file = os.path.join(rospkg.RosPack().get_path('rqt_mypkg'), 'resource', filename)
        self.movie.stop()
        gifSize = QtCore.QSize(*smooth_gif_resize(gif_file, 500, 500))
        self.movie.setScaledSize(gifSize)
        self.movie.setFileName(gif_file)
        self.movie_screen.setMovie(self.movie)
        self.movie.start()
