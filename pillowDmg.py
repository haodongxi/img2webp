
import sys
from PyQt6.QtWidgets import (QWidget, QLabel,
        QLineEdit, QApplication,QPushButton,QListWidget,QCheckBox)
from PyQt6 import QtCore
from compress import CompressUtil
import requests
import json
import os

class QEventHandler(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.DragEnter:
            event.accept()
        if event.type() == QtCore.QEvent.Type.Drop:
            md = event.mimeData()
            if md.hasUrls():
            	# 此处md.urls()的返回值为拖入文件的file路径列表，即支持多文件同时拖入；
            	# 此处默认读取第一个文件的路径进行处理，可按照个人需求进行相应的修改
                url = md.urls()[0]
                obj.setText(url.toLocalFile())
                return True
        return super().eventFilter(obj, event)


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.start = False
        self.compress = CompressUtil()
        self.initUI()


    def initUI(self):

        margin_x = 10
        margin_y = 10

        self.input_lbl = QLabel(self)
        self.input_lbl.setText('')
        input_qle = QLineEdit(self)
        input_tip = QLabel(self)
        input_tip.move(margin_x,0)
        input_tip.setText('请输入图片的文件夹路径')
        input_qle.setGeometry(margin_x,40,200,30)
        input_qle.setAcceptDrops = True
        input_qle.installEventFilter(QEventHandler(self))
        input_qle.setPlaceholderText('可拖拽/输入')
        self.input_lbl.move(margin_x, 80)
        input_qle.textChanged[str].connect(self.input_onChanged)

        
        self.output_lbl = QLabel(self)
        self.output_lbl.setText('')
        output_qle = QLineEdit(self)
        output_tip = QLabel(self)
        output_tip.move(margin_x,120)
        output_tip.setText('请输入压缩完图片的文件夹输出路径')
        output_qle.setGeometry(margin_x,160,200,30)  
        output_qle.setAcceptDrops = True
        output_qle.installEventFilter(QEventHandler(self))
        output_qle.setPlaceholderText('可拖拽/输入')
        self.output_lbl.move(margin_x, 200)
        output_qle.textChanged[str].connect(self.output_onChanged)

        self.cb1 = QCheckBox('是否上传',self)


        btn = QPushButton('开始', self)
        btn.resize(btn.sizeHint())
        btn.move(160, 230)
        btn.clicked.connect(self.start_click)
        
        self.cb1.move(btn.frameGeometry().right()+10,235)


        self.error_tip = QLabel(self)
        self.error_tip.move(margin_x,260)

        self.name_list = QLabel(self)
        self.name_list.move(margin_x,280)
        self.name_list.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.url_list = QLabel(self)
        self.url_list.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)

        self.setGeometry(300, 300, 350, 400)
        self.setWindowTitle('图片压缩工具')
        self.show()

    def input_onChanged(self, text):
        self.input_lbl.setText(text)
        self.input_lbl.adjustSize()

    def output_onChanged(self, text):
        self.output_lbl.setText(text)
        self.output_lbl.adjustSize()

    def start_click(self):
        if self.start != True:
            self.error_tip.setText('')
            self.start = True
            self.compress.compress(self.input_lbl.text(),self.output_lbl.text(),self.finish_callback)
    def finish_callback(self,error,result_list=[],abs_path_list=[]):
        self.start = False
        if error != None and error != '':
            self.error_tip.setText(error)
            self.error_tip.adjustSize()
        else:
            url_list = []
            if self.cb1.checkState() == QtCore.Qt.CheckState.Checked:
                for path in abs_path_list:
                    url = self.upload_action(path)
                    if url == None:
                        self.error_tip.setText('上传报错')
                        self.error_tip.adjustSize()
                        return
                    else:
                        url_list.append(url)
                
            self.error_tip.setText('任务完成')
            self.error_tip.adjustSize()
            if len(result_list) != 0:
                self.name_list.setText(''.join(result_list))
                self.name_list.adjustSize()
            if len(url_list) != 0:
                self.url_list.setText('\n'.join(url_list))

            self.url_list.adjustSize()    
            self.url_list.move(10,self.name_list.geometry().bottom()+10)    
            self.adjustSize()
            self.setGeometry(self.geometry().left(),self.geometry().top(),self.geometry().width(),self.geometry().height() + 40)
    def upload_action(self,filePath):
        fsize = os.path.getsize(filePath)
        file = open(filePath, 'rb')
        #上传图片代码
        return None    

def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
