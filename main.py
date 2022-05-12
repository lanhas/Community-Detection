import sys

from PyQt5.QtWidgets import QApplication

from controller import DetecNetwork


def run_dection():
    app = QApplication(sys.argv)
    detec_network = DetecNetwork()
    detec_network.setWindowTitle('复杂社交网络社区检测')
    detec_network.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_dection()