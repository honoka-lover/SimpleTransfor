import os
import sys

from PySide2 import QtGui
from PySide2.QtCore import Slot, QFile, QDir, QIODevice
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QDialog, QLabel, QTextEdit, QHBoxLayout, QGridLayout, QFileDialog,
                               QMainWindow, QMessageBox)

from translate import Translate


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.results=''
        # Create widgets
        self.setWindowTitle('小咪翻译器')
        self.label1=QLabel("原句")
        self.label2 = QLabel('译文')
        self.button = QPushButton("翻\n译")
        self.edit1 = QTextEdit()
        self.edit2 = QTextEdit()
        self.button2=QPushButton('文件翻译')
        self.label3=QLineEdit('字数:')

        self.label3.setReadOnly(1)
        font=QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label2.setFont(font)

        self.edit1.setMinimumSize(400,500)
        self.button.setMaximumSize(50,100)
        self.edit2.setMinimumSize(400, 500)
        # Create layout and add widgets
        layout = QGridLayout()
        layout.addWidget(self.label1,1,1)
        layout.addWidget(self.label2,1,3)
        layout.addWidget(self.button,2,2)
        layout.addWidget(self.edit1,2,1)
        layout.addWidget(self.edit2,2,3)
        layout.addWidget(self.button2,3,3)
        layout.addWidget(self.label3,3,1)
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.transition)
        self.button2.clicked.connect(self.fileTrans)

    def transition(self):
        text = self.edit1.toPlainText()
        if text=='':
            return
        self.trans = Translate(text)
        self.results=self.trans.trans()
        if self.results=='':
            self.edit2.setText('翻译失败')
        self.edit2.setText(self.results)
        self.label3.setText('字数: '+str(len(text)))


    def fileTrans(self):
        curPath = QDir.currentPath()
        dlgTitle = "打开一个文件"
        filter = '文本文件(*.txt);;所有文件(*.*)'
        aFileName = QFileDialog.getOpenFileName(self,dlgTitle,curPath,filter)
        file=open(aFileName[0],encoding='gbk')
        lines=file.readlines()
        for line in lines:
            self.results+=str(line)
        #print(self.results)
        self.edit1.setText(self.results)
        self.transition()

    def closeEvent(self, event):
        # message为窗口标题
        # Are you sure to quit?窗口显示内容
        # QtGui.QMessageBox.Yes | QtGui.QMessageBox.No窗口按钮部件
        # QtGui.QMessageBox.No默认焦点停留在NO上
        reply = QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?",
                                        QMessageBox.Yes |
                                        QMessageBox.No,
                                        QMessageBox.No)
        # 判断返回结果处理相应事项
        if reply == QMessageBox.Yes:
            self.trans.close()
            event.accept()
        else:
            event.ignore()



if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec_())