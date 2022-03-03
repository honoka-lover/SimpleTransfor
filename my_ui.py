import os
import re
import sys
from functools import partial

from PySide2 import QtGui
from PySide2.QtCore import Slot, QFile, QDir, QIODevice
from PySide2.QtGui import QFont
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QDialog, QLabel, QTextEdit, QHBoxLayout, QGridLayout, QFileDialog,
                               QMainWindow, QMessageBox, QComboBox)

from translate import Translate


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.results=''
        self.trans = Translate()
        # Create widgets
        self.setWindowTitle('小咪翻译器')
        self.label1=QLabel("原句")
        self.label2 = QLabel('译文')
        self.button = QPushButton("翻\n译")
        self.edit1 = QTextEdit()
        self.edit2 = QTextEdit()
        self.button2=QPushButton('文件翻译')
        self.label3=QLineEdit('字数:')
        self.button4=QPushButton('test')
        self.list=QComboBox()
        self.list.addItems(['auto','英中','中英','日中','中日'])
        self.selectList={0:['gbk','gbk'],1:['gbk','gbk'],2:['gbk','gbk'],3:['cp932','gbk'],4:['gbk','cp932']}

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
        layout.addWidget(self.list,3,2)
        #layout.addWidget(self.button4)
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.transition)
        self.button2.clicked.connect(self.fileTrans)
        #self.button4.clicked.connect(self.switch)


    def transition(self):
        text = self.edit1.toPlainText()  
        if text == '':
            return
        self.trans.read_src(text)
        self.results=self.trans.trans()
        if self.results == '':
            self.edit2.setText('翻译失败')
        self.edit2.setText(self.results)
        self.label3.setText('字数: '+str(len(text)))
        #print(self.trans.src)


    def fileTrans(self):
        curPath = QDir.currentPath()
        dlgTitle = "打开一个文件"
        filter = '文本文件(*.txt);;所有文件(*.*)'
        aFileName = QFileDialog.getOpenFileName(self,dlgTitle,curPath,filter)
        file = open(aFileName[0], encoding=self.selectList[self.switch()][0])
        lines = file.readlines()
        src = ''
        for line in lines:
            src += str(line)
        #print(self.results)
        self.edit1.setText(src)
        self.transition()
        #print(aFileName[0])
        fname = re.search(r'(.*)\.(.*?)$', aFileName[0])
        self.saveFile(fname.group(1)+'[translation].'+fname.group(2),self.results)
        file.close()


    def switch(self):
        return self.list.currentIndex()


    def saveFile(self,filename,string):
        f=open(filename,'w',encoding='utf-8')
        f.write(string)
        f.close()

    def closeEvent(self, event):
        if hasattr(self,'trans'):
            self.trans.close()
        '''# message为窗口标题
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
            if hasattr(self,'trans'):
                self.trans.close()
            event.accept()
        else:
            event.ignore()
'''





if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()

    # Run the main Qt loop
    sys.exit(app.exec_())