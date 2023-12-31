from PyQt5 import QtWidgets
from LoRaSim.gui.AddSimIntWindow import AddSimIntWindow


class SimIntervalsView(QtWidgets.QFrame):
    def __init__(self, simulator):
        super(SimIntervalsView, self).__init__()
        self.simulator = simulator
        self.initUI()

    def initUI(self):
        self.setLayout(QtWidgets.QVBoxLayout())
        self.title = self.createTitle()
        self.table = self.createIntTable()
        self.add_btn = self.createAddBtn()
        self.refreshIntTable()

        self.add_btn.setStyleSheet("background-color: #FFFFED")

    def createTitle(self):
        title = QtWidgets.QLabel()
        title.setText("Simulation intervals:")
        self.layout().addWidget(title)
        return title

    def createIntTable(self):
        tab = QtWidgets.QTableWidget()
        tab.setColumnCount(3)
        tab.setHorizontalHeaderLabels(['Start time (ms)', 'Duration (ms)', 'Model'])
        tab.horizontalHeader().setStretchLastSection(True)
        tab.resizeColumnsToContents()

        # orange sub menu
        tab.setStyleSheet("background-color:#E1F7F3 ;")

        self.layout().addWidget(tab)
        return tab

    def createAddBtn(self):
        add_btn = QtWidgets.QPushButton()
        add_btn.setText("+ Add interval")
        add_btn.clicked.connect(self.openAddSimIntWindow)
        self.layout().addWidget(add_btn)
        return add_btn

    def openAddSimIntWindow(self):
        dialog = AddSimIntWindow(self)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected = dialog.intView.selectedItems()
            if len(selected) < 1:
                self.showErrorMessage('No model was selected')
                return

            modelItem = dialog.intView.itemWidget(selected[0])
            duration_ms = dialog.durationSpinner.time().msecsSinceStartOfDay()
            if duration_ms <= 0:
                self.showErrorMessage('Please enter a valid time duration for the model')
                return

            self.addIntervalToSim(
                modelItem.model,
                duration_ms
            )
        else:
            print('Cancelled')
        dialog.deleteLater()

    def showErrorMessage(self, msg):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle("Error")
        dialog.setIcon(QtWidgets.QMessageBox.Critical)
        dialog.setText("Error:")
        dialog.setInformativeText(msg)
        dialog.exec_()

    def refreshIntTable(self):
        t = self.table
        t.clearContents()
        t.setRowCount(0)

        for i in self.simulator.getIntervals():
            row = t.rowCount()
            t.insertRow(row)
            t.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i.start_time)))
            t.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i.duration)))
            t.setItem(row, 2, QtWidgets.QTableWidgetItem(i.model.title))


    def addIntervalToSim(self, model, duration_ms):
        self.simulator.addInterval(model, duration_ms)
        self.refreshIntTable()
