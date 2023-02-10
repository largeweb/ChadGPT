import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextBrowser
from PyQt5.QtGui import QPixmap, QTextCursor
from PyQt5.QtCore import Qt

import os
import openai
openai.organization = "org-r8hqgbSkNNa8LHOzUpsJ91Ua"
openai.api_key = "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"  # supply your API key however you choose
openai.Model.list()

class MainWindow(QMainWindow):
    fullMessage = ""
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a label to display the image
        self.label = QLabel(self)
        pixmap = QPixmap('C:\\Users\\matt\\projects\\ChadGPT\\chad.png')
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        # Create a text input field
        self.text_input = QTextEdit(self)
        self.text_input.setFixedHeight(40)
        self.text_input.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border: none;")

        # Create a send button with a border around it
        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet("border: 1px solid black;")
        self.send_button.setStyleSheet("padding: 3px;")
        # self.send_button.setStyleSheet("height: 100px;")
        self.send_button.clicked.connect(self.send_message)

        # Create a reset button
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setStyleSheet("border: 1px solid black;")
        self.reset_button.setStyleSheet("padding: 3px;")
        # self.reset_button.setStyleSheet("height: 100px;")
        self.reset_button.clicked.connect(self.reset_chat)

        # Create a layout for the text input and buttons
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.reset_button)

        # Create a widget to hold the text input and buttons
        input_widget = QWidget(self)
        input_widget.setLayout(input_layout)
        input_widget.setFixedHeight(40)
        input_widget.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 5px;")

        # Create a text browser to display the chat messages
        self.chat_browser = QTextBrowser(self)
        self.chat_browser.setStyleSheet("background-color: transparent;")
        self.chat_browser.hide()

        # Create a layout for the input widget and chat browser
        layout = QVBoxLayout()
        layout.addWidget(input_widget)
        layout.addWidget(self.chat_browser)

        # Create a widget to hold the layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Set the window size to the size of the image
        self.setFixedSize(pixmap.width(), pixmap.height())

        # Add the label as a child widget of the central widget
        central_widget.layout().addWidget(self.label)

        # Set the window title
        self.setWindowTitle("Chad GPT")

        # Show the window
        self.show()

    def send_message(self):
        # Get the message from the text input field
        message = self.text_input.toPlainText()

        # add to full message
        MainWindow.fullMessage += "User: " + message + ". Chad: "

        # Clear the text input field
        self.text_input.clear()

        # Add the message to the chat browser
        self.chat_browser.show()
        self.chat_browser.append("You: " + message)

        # Get the response from GPT-3
        response = self.get_response(MainWindow.fullMessage)

        # Add the response to the chat browser
        self.chat_browser.append("Chad: " + response)

        # Scroll the chat browser to the bottom
        self.chat_browser.verticalScrollBar().setValue(self.chat_browser.verticalScrollBar().maximum())

    def reset_chat(self):
        # Clear the chat browser
        self.chat_browser.clear()
        self.chat_browser.hide()
        # set full message to empty
        MainWindow.fullMessage = ""

    def get_response(self, message):
        # set full message
        # message += "User: " + message + ". Chad: "
        print(message)
        # Get the response from GPT-3
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            temperature=0.9,
            max_tokens=150,
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0.6,
            # stop=["\n", " Human:", " AI:"]
        )

        # Return the response
        print(response["choices"][0]["text"])

        # add to full message
        MainWindow.fullMessage += response["choices"][0]["text"] + ". User: "

        return response["choices"][0]["text"]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())