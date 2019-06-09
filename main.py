import sys

from PyQt5.QtGui import QImage, QPixmap, QImageReader
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
from PyQt5.Qt import QDir
from main_ui import Ui_DialogMain


class MainWindow(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_DialogMain()

        self.ui.setupUi(self)

        self.ui.searchPB.clicked.connect(self.search_start)
        self.ui.nextPB.clicked.connect(self.next_item)
        self.ui.previousPB.clicked.connect(self.previous_item)

        self.path = "/media/zjay/Datas/workspace/pyqt_picture_browser/movies"
        self.filters = []
        self.name = ""
        for i in QImageReader.supportedImageFormats():
            self.filters.append("*." + str(i, encoding='utf-8'))

        self.iter = None
        self.to_start_item()
        self.show_item()

    def to_start_item(self):
        self.iter = iter(QDir(self.path).entryList(QDir.Dirs | QDir.NoDotAndDotDot))
        try:
            self.name = next(self.iter)
        except StopIteration:
            self.name = ""

    def clear_content(self):
        while True:
            child = self.ui.contenLayout.takeAt(0)
            if child is None:
                break

            if child.widget():
                # 用于清除上一次显示的内容，没有这行，下一次的显示只是覆盖在上一次的显示之上
                child.widget().setParent(None)
            self.ui.contenLayout.removeItem(child)

    def show_item(self):
        self.clear_content()
        info_path = self.path + QDir.separator() + self.name
        self.ui.nameInfoLabel.setText(self.name)
        self.ui.locationINfoLabel.setText(info_path)

        for img in QDir(info_path).entryList(self.filters, QDir.Files):
            full_path = info_path + QDir.separator() + img
            label = QLabel(self.ui.contentWidget)
            self.ui.contenLayout.addWidget(label)
            qimg = QImage(full_path)
            label.setPixmap(QPixmap.fromImage(qimg))

    # def paintEvent(self, QPaintEvent):
        # painter = QPainter(self)
        # rc = self.ui.ContentWidget.frameRect()
        # rc.translate(self.ui.ContentWidget.pos())
        # painter.drawImage(rc, QImage(self.path + QDir.separator() + self.name))

    def search_start(self):
        pass

    def next_item(self):
        print("switch to next")
        try:
            self.name = next(self.iter)
        except StopIteration:
            print("catch StopIteration")
            self.to_start_item()

        print(self.path + QDir.separator() + self.name)

        self.show_item()
        # self.repaint()

    def previous_item(self):
        pass


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

