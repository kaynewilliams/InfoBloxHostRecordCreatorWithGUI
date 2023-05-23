import sys
from infoblox_client import connector
from infoblox_client import objects
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import qdarkstyle
from PyQt5.QtGui import QIcon

app = QApplication(sys.argv)
palette = QPalette()
palette.setColor(QPalette.Window, QColor(255, 255, 255))
palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
palette.setColor(QPalette.Base, QColor(240, 240, 240))
palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
palette.setColor(QPalette.Text, QColor(0, 0, 0))
palette.setColor(QPalette.Button, QColor(255, 255, 255))
palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
app.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.host_records = []
        self.setWindowTitle("Infoblox Host Record Creator")
        self.setGeometry(100, 100, 500, 550)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setWindowIcon(QIcon('icon.png'))
        

        self.host_label = QLabel("Enter a host name (or 'q' to quit):", self)
        self.host_label.move(50, 50)
        self.host_label.setFixedWidth(400)
        self.host_input = QLineEdit(self)
        self.host_input.move(50, 80)
        self.host_input.resize(400, 30)

        self.ipaddr_label = QLabel("Enter the IP address for this host:", self)
        self.ipaddr_label.move(50, 120)
        self.ipaddr_label.setFixedWidth(400)
        self.ipaddr_input = QLineEdit(self)
        self.ipaddr_input.move(50, 150)
        self.ipaddr_input.resize(400, 30)

        self.comment_label = QLabel("Enter a comment for this record:", self)
        self.comment_label.move(50, 190)
        self.comment_label.setFixedWidth(400)
        self.comment_input = QTextEdit(self)
        self.comment_input.move(50, 220)
        self.comment_input.resize(400, 100)

        self.username_label = QLabel("Enter username:", self)
        self.username_label.move(50, 340)
        self.username_label.setFixedWidth(400)
        self.username_input = QLineEdit(self)
        self.username_input.move(50, 370)
        self.username_input.resize(400, 30)

        self.password_label = QLabel("Enter password:", self)
        self.password_label.move(50, 410)
        self.password_label.setFixedWidth(400)
        self.password_input = QLineEdit(self)
        self.password_input.move(50, 440)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.resize(400, 30)

        self.submit_btn = QPushButton("Submit", self)
        self.submit_btn.move(200, 480)
        self.submit_btn.clicked.connect(self.submit)

    def submit(self):
        host_name = self.host_input.text()
        if host_name == 'q':
            self.close()
            return
        ipaddr = self.ipaddr_input.text()
        comment = self.comment_input.toPlainText()
        self.host_records.append({'host_name': host_name, 'ipaddr': ipaddr, 'comment': comment})
        self.host_input.setText("")
        self.ipaddr_input.setText("")
        self.comment_input.setPlainText("")

        opts = {}
        opts['host'] = "(IB IP)"
        opts['username'] = self.username_input.text()
        opts['password'] = self.password_input.text()
        conn = connector.Connector(opts)

        for i in self.host_records:
            host_ip = objects.IP.create(ip=i['ipaddr'])
            hostRecord = objects.HostRecord.create(conn, name=i['host_name'], ip=host_ip, comment=i['comment'])
            print(hostRecord)
        self.username_input.setText("")
        self.password_input.setText("")

window = MainWindow()
window.show()
sys.exit(app.exec_())