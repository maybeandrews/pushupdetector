from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QRadioButton, QPushButton, QVBoxLayout, QButtonGroup)
import os
import cv2

# This file handles all the leaderboards stuff and can be imported into main.py to be used

class PlayerInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.gender = 'Male'

        # Create the window layout
        self.setWindowTitle("PLAYER INFO")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()

        # Label to guide the user
        label = QLabel("Enter Name")
        layout.addWidget(label)

        # Text field for the user to input their name
        self.text_field = QLineEdit(self)
        layout.addWidget(self.text_field)

        # Radio buttons for gender selection
        self.male_radio = QRadioButton("Male")
        self.male_radio.setChecked(True)
        self.female_radio = QRadioButton("Female")

        # Grouping the radio buttons
        self.gender_group = QButtonGroup()
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)

        layout.addWidget(self.male_radio)
        layout.addWidget(self.female_radio)

        # Submit button
        submit_button = QPushButton("Submit", self)
        submit_button.clicked.connect(self.get_text)
        layout.addWidget(submit_button)

        self.setLayout(layout)

    def get_text(self):
        # Get the name from the text field and the selected gender
        self.name = self.text_field.text()
        self.gender = 'Male' if self.male_radio.isChecked() else 'Female'
        self.close()

    def get_player_info(self):
        self.exec()
        return [self.name, self.gender]


def input_details():
    app = QApplication([])

    # Create and show the player info window
    window = PlayerInfoWindow()
    window.show()

    # Start the application loop
    app.exec()

    return [window.name, window.gender]


def write_into_file(val):
    """Players listed sorted by the number of pushups
       Creating two files because a new player can't be inserted in the lines in between
       So reading from one file and writing to another is done"""
    
    # Opening files
    file2 = open("/Users/andrews/Desktop/file2.txt", "w")
    file1 = open("/Users/andrews/Desktop/file1.txt", "r")
    contents = file1.readlines()

    flag1 = 0  # Flag to track if player was inserted

    try:
        for content in contents:
            first_pipe = content.find("|")
            second_pipe = content.rfind("|")

            p_name = content[:first_pipe]
            p_count = int(content[second_pipe + 1:-1])

            # Check for name duplication
            if not flag1 and p_name == val[0]:
                flag1 = 1
                if int(val[2]) >= p_count:
                    file2.write(f"{val[0]}|{val[1]}|{val[2]}\n")
                    continue

            if not flag1 and int(val[2]) >= p_count:
                file2.write(f"{val[0]}|{val[1]}|{val[2]}\n")
                flag1 = 1

            file2.write(content)

        if not flag1:
            file2.write(f"{val[0]}|{val[1]}|{val[2]}\n")

    finally:
        file2.close()
        file1.close()

        os.remove("/Users/andrews/Desktop/file1.txt")
        os.rename("/Users/andrews/Desktop/file2.txt", "/Users/andrews/Desktop/file1.txt")


def read_from_file():
    file1 = open("/Users/andrews/Desktop/file1.txt", 'r')
    contents = file1.readlines()

    mlst, flst = [], []

    for content in contents:
        first_pipe = content.find("|")
        second_pipe = content.find("|", first_pipe + 1, -1)
        from_file = content[first_pipe + 1:second_pipe]

        if from_file == "Male":
            if len(mlst) < 16:
                mlst.append(content)
        else:
            if len(flst) < 16:
                flst.append(content)

        if len(mlst) == 15 and len(flst) == 15:
            break

    return mlst, flst
    file1.close()


def out_list(pipestring):
    first_pipe = pipestring.find("|")
    second_pipe = pipestring.rfind("|")

    p_name = pipestring[:first_pipe]
    p_count = int(pipestring[second_pipe + 1:-1])

    return [p_name, p_count]

