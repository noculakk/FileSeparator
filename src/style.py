message_box = """
QMessageBox {
    background: qlineargradient( x1:1.4 y1:0, x2:0 y2:3 stop:0 #3E9479, stop:0.2  #152E4B);
    font: 12pt "Poppins";
}
QMessageBox QLabel {
    color: rgba(255, 255, 255, 0.85);
    padding: 15px 0 0 0;
}
QPushButton {
    color: rgba(255, 255, 255, 0.85);
    font: 12pt "Poppins";
    background: rgba(231, 245, 236, 0.14);
    border: 1px solid rgb(2, 0, 36, 0.2);
    border-radius: 4px;
    padding: 5px 10px;
}
QPushButton:hover {
    background: rgba(231, 245, 236, 0.54);
}
"""

central_widget = """
QWidget {
	font: 12pt "Poppins";
	color: rgba(255, 255, 255, 0.85)
}

#centralwidget {

    background: qlineargradient( x1:1.4 y1:0, x2:0 y2:3 stop:0 #3E9479, stop:0.2  #152E4B);
}


QLineEdit {
	background: rgba(231, 245, 236, 0.14);
	border: 1px solid rgb(2, 0, 36, 0.2);
	border-radius: 4px;
	
}

QPushButton {
	background: rgba(231, 245, 236, 0.14);
	border: 1px solid rgb(2, 0, 36, 0.2);
	border-radius: 4px;
}

QPushButton:hover {
	background: rgba(231, 245, 236, 0.54);
}

QComboBox {
	background: rgba(231, 245, 236, 0.14);
	border: 1px solid rgb(2, 0, 36, 0.2);
	border-radius: 4px;
}

QListView
{
background-color :#152E4B;
}
"""

group_box = """
#groupBox {
	border: 1px solid rgba(232, 240, 255, 0.1);
	border-radius: 1px;
	background: rgba(9, 16, 39, 0);
	margin: 10px 0;
}

#label_9 {
	background-color: #152E4B;
}

"""