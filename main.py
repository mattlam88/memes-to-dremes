import sys

from PySide2.QtWidgets import QApplication

from views.dashboard import Dashboard


def main():
    app = QApplication(sys.argv)
    view = Dashboard()
    view.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
