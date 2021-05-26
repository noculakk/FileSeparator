import sys
from src.file_separator import FileSeparator, FileSeparatorOptions, DateDirFormat, Parser

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from src.file_separator_error import *
import style


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        def on_browse_base_dir():
            self.lineEdit_base_dir.setText(QFileDialog.getExistingDirectory(MainWindow, 'Wybierz folder'))

        def on_browse_target_dir():
            self.lineEdit_target_dir.setText(QFileDialog.getExistingDirectory(MainWindow, 'Wybierz folder'))

        def on_run():
            # Parsing extensions
            try:
                extensions = Parser.extensions_to_list(
                    self.lineEdit_extensions.text()) if self.checkBox_extensions.isChecked() else []
            except ValueError as ve:
                msg = QMessageBox()
                msg.setIconPixmap(QPixmap("warning.png"))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowIcon(QIcon("minilogo.png"))
                msg.setStyleSheet(style.message_box)
                msg.setText('Rozszerzenia podane w błędnym formacie \n akceptowalne: np.  .png, .jpg, .pdf')
                msg.setWindowTitle('Błąd')
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return

            if self.radioButton_sizes.isChecked():
                try:
                    size_format = Parser.sizes_to_int(self.lineEdit_sizes.text())
                    date_format = None
                    is_cr_date = False
                except ValueError as ve:
                    msg = QMessageBox()
                    msg.setIconPixmap(QPixmap("warning.png"))
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setWindowIcon(QIcon("minilogo.png"))
                    msg.setStyleSheet(style.message_box)
                    msg.setText('Parsowanie rozmiarów pliku nie powiodło się. Akceptowalne rozmiary: B, KB, MB, GB, '
                                '\nPowinny być rozdzielone spacją między \nwartością, a jednostką,'
                                ' \nakceptowalne: np. 10 MB, 20 MB, 1 GB')
                    msg.setWindowTitle('Błąd')
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    return

            elif self.radioButton_cr_date.isChecked():
                date_format = DateDirFormat(self.comboBox_cr_date.currentIndex())
                is_cr_date = True
                size_format = None


            else:
                date_format = DateDirFormat(self.comboBox_md_date.currentIndex())
                is_cr_date = False
                size_format = None

            fso = FileSeparatorOptions(
                base_dir=self.lineEdit_base_dir.text(),
                target_dir=self.lineEdit_target_dir.text(),
                extensions=extensions,
                by_date_order=date_format,
                by_size_order=size_format,
                by_creation_date=is_cr_date,
                make_empty_dir=self.checkBox_empty_folders.isChecked(),
                remove_org_files=self.checkBox_rm_old_files.isChecked()

            )
            print(fso)

            try:
                FileSeparator.run(fso)
            except DirectoryNotExistError:
                msg = QMessageBox()
                msg.setIconPixmap(QPixmap("warning.png"))
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowIcon(QIcon("minilogo.png"))
                msg.setText('Nie wybrano folderu źródłowego lub docelowego!')
                msg.setWindowTitle('Błąd')
                msg.setStyleSheet(style.message_box)
                msg.exec_()
                return
            except EmptyFilesListError:
                msg = QMessageBox()
                msg.setIconPixmap(QPixmap("info.png"))
                msg.setText('Brak plików do sortowania')
                msg.setWindowTitle('Informacja')
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowIcon(QIcon("minilogo.png"))
                msg.setStyleSheet(style.message_box)
                msg.exec_()
                return
            except Exception as e:
                msg = QMessageBox()
                msg.setIconPixmap(QPixmap("warning.png"))
                msg.setText('Wystąpił błąd systemu\n' + str(e))
                msg.setWindowTitle('Błąd')
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setWindowIcon(QIcon("minilogo.png"))
                msg.setStyleSheet(style.message_box)
                msg.exec_()
                return

            msg = QMessageBox()
            msg.setIconPixmap(QPixmap("ok.png"))
            msg.setText('Program zakończono powodzeniem')
            msg.setWindowIcon(QIcon("minilogo.png"))
            msg.setWindowTitle('Hurra')
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setStyleSheet(style.message_box)
            msg.exec_()

        def default_settings():
            self.lineEdit_base_dir.setText('')
            self.lineEdit_target_dir.setText('')
            self.lineEdit_sizes.setText('np. 10 MB, 100 MB')
            self.lineEdit_extensions.setText('.jpg, .png')
            self.comboBox_cr_date.setCurrentIndex(0)
            self.comboBox_md_date.setCurrentIndex(0)
            self.checkBox_extensions.setChecked(False)
            self.checkBox_empty_folders.setChecked(False)
            self.checkBox_rm_old_files.setChecked(False)
            self.radioButton_cr_date.setChecked(True)

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 690)
        MainWindow.setMaximumSize(960, 690)
        MainWindow.setMinimumSize(960, 690)

        MainWindow.setWindowIcon(QIcon("minilogo.png"))
        MainWindow.setWindowTitle("FileSeparator")

        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(style.central_widget)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 250, 901, 281))
        self.groupBox.setStyleSheet(style.group_box)
        self.groupBox.setTitle(u"")

        self.checkBox_extensions = QCheckBox(self.groupBox)
        self.checkBox_extensions.setObjectName(u"checkBox_extensions")
        self.checkBox_extensions.setGeometry(QRect(10, 50, 361, 21))

        self.label_category = QLabel(self.groupBox)
        self.label_category.setObjectName(u"label_category")
        self.label_category.setGeometry(QRect(10, 105, 226, 16))
        self.label_other_options = QLabel(self.groupBox)
        self.label_other_options.setObjectName(u"label_other_options")
        self.label_other_options.setGeometry(QRect(380, 110, 126, 16))

        self.radioButton_cr_date = QRadioButton(self.groupBox)
        self.radioButton_cr_date.setChecked(True)
        self.radioButton_cr_date.setObjectName(u"radioButton_cr_date")
        self.radioButton_cr_date.setGeometry(QRect(10, 140, 151, 16))

        self.comboBox_cr_date = QComboBox(self.groupBox)
        self.comboBox_cr_date.addItem("")
        self.comboBox_cr_date.addItem("")
        self.comboBox_cr_date.addItem("")
        self.comboBox_cr_date.setObjectName(u"comboBox_cr_date")
        self.comboBox_cr_date.setGeometry(QRect(180, 130, 131, 31))

        self.radioButton_sizes = QRadioButton(self.groupBox)
        self.radioButton_sizes.setObjectName(u"radioButton_sizes")
        self.radioButton_sizes.setGeometry(QRect(10, 220, 82, 16))

        self.lineEdit_sizes = QLineEdit(self.groupBox)
        self.lineEdit_sizes.setObjectName(u"lineEdit_sizes")
        self.lineEdit_sizes.setGeometry(QRect(110, 210, 201, 31))
        self.lineEdit_sizes.setReadOnly(False)

        self.checkBox_empty_folders = QCheckBox(self.groupBox)
        self.checkBox_empty_folders.setObjectName(u"checkBox_empty_folders")
        self.checkBox_empty_folders.setGeometry(QRect(380, 140, 226, 17))
        self.checkBox_rm_old_files = QCheckBox(self.groupBox)
        self.checkBox_rm_old_files.setObjectName(u"checkBox_rm_old_files")
        self.checkBox_rm_old_files.setGeometry(QRect(380, 170, 241, 17))

        self.lineEdit_extensions = QLineEdit(self.groupBox)
        self.lineEdit_extensions.setObjectName(u"lineEdit_extensions")
        self.lineEdit_extensions.setGeometry(QRect(380, 44, 261, 31))
        self.lineEdit_extensions.setReadOnly(False)

        self.radioButton_md_date = QRadioButton(self.groupBox)
        self.radioButton_md_date.setObjectName(u"radioButton_md_date")
        self.radioButton_md_date.setGeometry(QRect(10, 180, 161, 16))

        self.comboBox_md_date = QComboBox(self.groupBox)
        self.comboBox_md_date.addItem("")
        self.comboBox_md_date.addItem("")
        self.comboBox_md_date.addItem("")
        self.comboBox_md_date.setObjectName(u"comboBox_md_date")
        self.comboBox_md_date.setGeometry(QRect(180, 170, 131, 31))
        self.comboBox_md_date.setAutoFillBackground(False)

        self.label_options = QLabel(self.groupBox)
        self.label_options.setObjectName(u"label_options")
        self.label_options.setGeometry(QRect(20, 0, 61, 24))

        font = QFont()
        font.setFamily(u"Poppins")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)

        self.label_options.setFont(font)
        self.label_options.setStyleSheet(u"#label_9 {\n"
                                         "	background-color: #152E4B;\n"
                                         "}")

        self.pushButton_run = QPushButton(self.centralwidget)
        self.pushButton_run.setObjectName(u"pushButton_run")
        self.pushButton_run.setGeometry(QRect(740, 570, 171, 31))
        self.pushButton_run.clicked.connect(on_run)

        self.pushButton_default_set = QPushButton(self.centralwidget)
        self.pushButton_default_set.setObjectName(u"pushButton_default_set")
        self.pushButton_default_set.setGeometry(QRect(390, 570, 311, 31))
        self.pushButton_default_set.clicked.connect(default_settings)

        self.label_base_dir = QLabel(self.centralwidget)
        self.label_base_dir.setObjectName(u"label_base_dir")
        self.label_base_dir.setGeometry(QRect(30, 100, 241, 21))

        self.label_target_dir = QLabel(self.centralwidget)
        self.label_target_dir.setObjectName(u"label_target_dir")
        self.label_target_dir.setGeometry(QRect(30, 160, 171, 31))

        self.lineEdit_base_dir = QLineEdit(self.centralwidget)
        self.lineEdit_base_dir.setObjectName(u"lineEdit_base_dir")
        self.lineEdit_base_dir.setGeometry(QRect(200, 90, 511, 31))
        self.lineEdit_base_dir.setReadOnly(True)

        self.pushButton_base_dir = QPushButton(self.centralwidget)
        self.pushButton_base_dir.setObjectName(u"pushButton_base_dir")
        self.pushButton_base_dir.setGeometry(QRect(740, 90, 171, 31))
        self.pushButton_base_dir.clicked.connect(on_browse_base_dir)

        self.lineEdit_target_dir = QLineEdit(self.centralwidget)
        self.lineEdit_target_dir.setObjectName(u"lineEdit_target_dir")
        self.lineEdit_target_dir.setGeometry(QRect(200, 160, 511, 31))
        self.lineEdit_target_dir.setReadOnly(True)

        self.pushButton_target_dir = QPushButton(self.centralwidget)
        self.pushButton_target_dir.clicked.connect(on_browse_target_dir)
        self.pushButton_target_dir.setObjectName(u"pushButton_target_dir")
        self.pushButton_target_dir.setGeometry(QRect(740, 160, 171, 31))

        self.label_title = QLabel(self.centralwidget)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setGeometry(QRect(-10, 0, 971, 71))
        self.label_title.setStyleSheet(u"QLabel {\n"
                                       "	\n"
                                       "	font: 57 22pt \"Poppins Medium\";\n"
                                       "	background-color: rgb(2, 0, 36, 0.2)\n"
                                       "}")

        self.label_logo = QLabel(self.centralwidget)
        self.label_logo.setObjectName(u"label_logo")
        self.label_logo.setGeometry(QRect(10, 0, 171, 71))
        self.label_logo.setPixmap(QPixmap("logo.png"))

        self.label_title_text = QLabel(self.centralwidget)
        self.label_title_text.setObjectName(u"label_title_text")
        self.label_title_text.setGeometry(QRect(18, 30, 251, 31))

        font1 = QFont()
        font1.setFamily(u"Poppins")
        font1.setPointSize(24)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setWeight(50)

        self.label_title_text.setFont(font1)
        self.label_title_text.setStyleSheet(u"font: 24pt \"Poppins\";\n"
                                            "letter-spacing: 1.15px;")

        self.label_upper_border = QLabel(self.centralwidget)
        self.label_upper_border.setObjectName(u"label_upper_border")
        self.label_upper_border.setGeometry(QRect(20, 80, 901, 131))
        self.label_upper_border.setStyleSheet(u"	border: 1px solid rgba(232, 240, 255, 0.1);\n"
                                              "	border-radius: 1px;")

        MainWindow.setCentralWidget(self.centralwidget)
        self.label_upper_border.raise_()
        self.groupBox.raise_()
        self.pushButton_run.raise_()
        self.pushButton_default_set.raise_()
        self.label_base_dir.raise_()
        self.label_target_dir.raise_()
        self.lineEdit_base_dir.raise_()
        self.pushButton_base_dir.raise_()
        self.lineEdit_target_dir.raise_()
        self.pushButton_target_dir.raise_()
        self.label_title.raise_()
        self.label_logo.raise_()
        self.label_title_text.raise_()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("FileSeparator")
        self.checkBox_extensions.setText(
            QCoreApplication.translate("MainWindow", u"Ogranicz sortowanie do rozszerze\u0144 plik\u00f3w:", None))
        self.label_category.setText(QCoreApplication.translate("MainWindow", u"Kategoria segregowania:", None))
        self.label_other_options.setText(QCoreApplication.translate("MainWindow", u"Pozosta\u0142e opcje:", None))
        self.radioButton_cr_date.setText(QCoreApplication.translate("MainWindow", u"Data utworzenia", None))
        self.comboBox_cr_date.setItemText(0, QCoreApplication.translate("MainWindow", u"Dzie\u0144", None))
        self.comboBox_cr_date.setItemText(1, QCoreApplication.translate("MainWindow", u"Miesi\u0105c", None))
        self.comboBox_cr_date.setItemText(2, QCoreApplication.translate("MainWindow", u"Rok", None))

        self.radioButton_sizes.setToolTip(QCoreApplication.translate(
            "MainWindow",
            u"Foldery b\u0119d\u0105 tworzone dla kolejnych przedzia\u0142\u00f3w rozmiarowych plik\u00f3w",
            None))

        self.radioButton_sizes.setText(QCoreApplication.translate("MainWindow", u"Rozmiar pliku", None))
        self.lineEdit_sizes.setText(QCoreApplication.translate("MainWindow", u"np. 10MB, 100MB", None))
        self.checkBox_empty_folders.setText(QCoreApplication.translate("MainWindow", u"Tw\u00f3rz puste foldery", None))
        self.checkBox_rm_old_files.setText(
            QCoreApplication.translate("MainWindow", u"Usu\u0144 pliki w starym folderze", None))
        self.lineEdit_extensions.setText(QCoreApplication.translate("MainWindow", u".jpg, .png", None))
        self.radioButton_md_date.setText(QCoreApplication.translate("MainWindow", u"Data modyfikacji", None))
        self.comboBox_md_date.setItemText(0, QCoreApplication.translate("MainWindow", u"Dzie\u0144", None))
        self.comboBox_md_date.setItemText(1, QCoreApplication.translate("MainWindow", u"Miesi\u0105c", None))
        self.comboBox_md_date.setItemText(2, QCoreApplication.translate("MainWindow", u"Rok", None))

        self.label_options.setText(QCoreApplication.translate("MainWindow", u"  Opcje ", None))
        self.pushButton_run.setText(QCoreApplication.translate("MainWindow", u"Uruchom", None))
        self.pushButton_default_set.setText(
            QCoreApplication.translate("MainWindow", u"Przywr\u00f3\u0107 ustawienia domy\u015blne", None))
        self.label_base_dir.setText(QCoreApplication.translate("MainWindow", u"Katalog \u017arod\u0142owy:", None))
        self.label_target_dir.setText(QCoreApplication.translate("MainWindow", u"Katalog docelowy:", None))
        self.lineEdit_base_dir.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.pushButton_base_dir.setText(QCoreApplication.translate("MainWindow", u"Wybierz", None))
        self.lineEdit_target_dir.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.pushButton_target_dir.setText(QCoreApplication.translate("MainWindow", u"Wybierz", None))
        self.label_title.setText("")
        self.label_logo.setText("")
        self.label_title_text.setText(QCoreApplication.translate("MainWindow", u"FileSeparator", None))
        self.label_upper_border.setText("")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    w = QMainWindow()
    win.setupUi(w)
    w.show()

    sys.exit(app.exec_())
