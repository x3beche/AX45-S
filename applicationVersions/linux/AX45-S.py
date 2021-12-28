from PyQt6 import QtCore, QtGui, QtWidgets
from json import dump,dumps,load,loads
from base64 import b64decode,b64encode
from random import randint
from os import scandir
import sys

class Ui_AX45S(object):
    def f_encrypt(self, oW,nW,rtry):
        own,nwn=int(rtry[0][rtry[1].index(oW)]),int(rtry[0][rtry[1].index(nW)])
        if own>nwn: chc=94-own+nwn
        else: chc=nwn-own
        return rtry[1][chc-1]
    def f_decrypt(self, oW,nW,rtry):
        own,nwn=int(rtry[0][rtry[1].index(oW)]),int(rtry[0][rtry[1].index(nW)])
        if own+nwn>94: chc=own+nwn-94
        else: chc=nwn+own
        return rtry[1][chc-1]
    def axen_algorithm(self,text,keyNumber):
        a,rtry,final=self.keyComplier(keyNumber)[1],self.keyComplier(keyNumber)[0],''
        oW=rtry[1][ord(a[1])-32]
        for y in range(0,len(text)):
            self.step += 1
            self.progressBarUpdate()
            oW=self.f_encrypt(oW,text[y],rtry)
            final=final+oW
        return final
    def axde_algorithm(self,text,keyNumber):
        a,rtry,final=self.keyComplier(keyNumber)[1],self.keyComplier(keyNumber)[0],''
        oW=rtry[1][ord(a[1])-32]
        for y in range(0,len(text)):
            self.step += 1
            self.progressBarUpdate()
            nW=text[y]
            final=final+self.f_decrypt(oW,nW,rtry)
            oW=text[y]
        return final
    def axen(self, text,keyNumber):
        self.total = len(dumps({"data":text})[10:len(dumps({"data":text}))-2])*2
        self.progressBarUpdate()
        data = self.axen_algorithm(self.axen_algorithm(dumps({"data":text})[10:len(dumps({"data":text}))-2],keyNumber),keyNumber)
        self.step,self.total = 0, 100
        self.progressBarUpdate()
        return data
    def axde(self, text,keyNumber):
        self.total = len(dumps({"data":text})[10:len(dumps({"data":text}))-2])*2
        self.progressBarUpdate()
        data = loads('{"data": "'+self.axde_algorithm(self.axde_algorithm(text,keyNumber),keyNumber)+'"}')["data"]
        self.step,self.total = 0, 100
        self.progressBarUpdate()
        return data
    def keyComplier(self, fileNumber):
        fileName,keyList='key'+str(fileNumber)+'.ax',[[],[]]
        try:
            with open(fileName,"r",encoding="utf-8") as file: json_data=load(file)
            if json_data["algorithm"]=="AX45-S" and json_data["layer"] == 1:
                for x in range(1,len(json_data["key"].keys())+1): keyList[0].append(str(x)),keyList[1].append(json_data["key"][str(x)])
                return keyList, [keyList[0][0],keyList[1][0]]
            else:print("This key file is not compatible with this encryption")
        except:print("Wrong key format!")
    def keyAnalyzer(self, fileNumber):
        fileName ='key'+str(fileNumber)+'.ax'
        try:
            keyAnalyzerData = ""
            with open(fileName,"r",encoding="utf-8") as file: json_data=load(file)
            if json_data["algorithm"]=="AX45-S" and json_data["layer"] == 1:
                keyLabel = "Algorithm = {}\nLayer = {}".format(json_data["algorithm"], json_data["layer"])
                keyAnalyzerData = ""
                for x in range(1,95):
                    if x == 94:
                        return [keyAnalyzerData + "{} - {}".format(x, json_data["key"][str(x)]), keyLabel]
                    keyAnalyzerData = keyAnalyzerData + "{} - {}\n".format(x, json_data["key"][str(x)])
        except:print("Wrong key format!")
    def fileLister(self, direction):
        programFiles,extensions,files = ["desktop.ini","AX45-S.exe","keyConverterOldToNew.py","algorithms.py","AX45-S.py","ax45sEngine","keygenerator.py"],["ax","axen"],[]
        with scandir() as entries:
            if direction == "EN":
                for entry in entries:
                    if entry.name.rsplit(".")[-1] not in extensions and entry.name not in programFiles and len(entry.name.split(".")) >= 2 : files.append(entry.name)
                return files
            elif direction == "DE":
                for entry in entries:
                    if entry.name.rsplit(".")[-1] == "axen" and len(entry.name.split("."))>=3: files.append(entry.name)
                return files
            elif direction == "KEY":
                for entry in entries:
                    if entry.name.rsplit(".")[-1] == "ax" and len(entry.name.split("."))==2 :files.append(int(entry.name.replace("key","").split(".")[0]))
                return files
            else: return "Wrong direction!"
    def fileEN(self, fileInput,keynum):
        try:
            with open(fileInput,"rb") as file: data = self.axen(b64encode(file.read()).decode(),keynum)
        except: return False
        try:
            with open(fileInput+".axen","w") as file: file.write(data)
        except: return False
        return True
    def fileDE(self, fileInput,keynum):
        try:
            with open(fileInput,"r") as file: data = file.read()
        except: return False
        try:
            with open(fileInput.rsplit(".",1)[0],"wb") as file: file.write(b64decode(self.axde(data,keynum)))
        except: return False
        return True
    def keyGeneration(self):
        # entering values
        key, json_data, regularKey, randomFileNumber = {}, {}, [[],[]], randint(1,10**4)

        # this function generating numbers in random order in the range from 1 to 94
        def randomNumbers():
            randomNumberArray=[]
            while len(randomNumberArray)!=94:
                randomNumber=randint(1,94)
                if randomNumber not in randomNumberArray: randomNumberArray.append(randomNumber)
            return randomNumberArray

        # generating a random key by matching the irregularly
        # ordered set of numbers with the regularly ordered character set
        irregularKey=[[chr(x) for x in range(32,127)],randomNumbers()]

        # arranging the key in an orderly sequence to make it ready for use
        for x in range(1,95):
            for y in range(0,94):
                if x==irregularKey[1][y]: regularKey[1].append(x), regularKey[0].append(irregularKey[0][y])

        # arranging data in dictionary type
        for x in range(0,94): key.update({regularKey[1][x]:regularKey[0][x]})
        json_data.update({"algorithm":"AX45-S","layer":1,"key":key})

        # saving data in json format to file with .ax extension
        with open("key"+str(randomFileNumber)+".ax","w",encoding="UTF-8") as file: dump(json_data,file,ensure_ascii=False,indent=2)
        return "key"+str(randomFileNumber)+".ax"
    def setupUi(self, AX45S):
        AX45S.setObjectName("AX45S")
        AX45S.setWindowIcon(QtGui.QIcon("files/ax.ico"))
        AX45S.setFixedSize(662, 419)
        with open("files/theme.qss",'r') as f: AX45S.setStyleSheet(f.read())

        # Widgets
        self.KeySector = QtWidgets.QGroupBox(AX45S)
        self.KeySector.setGeometry(QtCore.QRect(460, 20, 191, 391))
        self.KeySector.setTitle("")
        self.KeySector.setObjectName("KeySector")
        self.keyMainInfo = QtWidgets.QTextEdit(self.KeySector)
        self.keyMainInfo.setEnabled(True)
        self.keyMainInfo.setGeometry(QtCore.QRect(10, 167, 171, 217))
        self.keyMainInfo.setReadOnly(True)
        self.keyMainInfo.setObjectName("keyMainInfo")
        self.keyElements = QtWidgets.QTextEdit(self.KeySector)
        self.keyElements.setEnabled(True)
        self.keyElements.setGeometry(QtCore.QRect(10, 116, 171, 45))
        self.keyElements.setReadOnly(True)
        self.keyElements.setObjectName("keyElements")
        self.widget = QtWidgets.QWidget(self.KeySector)
        self.widget.setGeometry(QtCore.QRect(10, 31, 171, 80))
        self.widget.setObjectName("widget")
        self.keySelectionUnit = QtWidgets.QVBoxLayout(self.widget)
        self.keySelectionUnit.setContentsMargins(0, 0, 0, 0)
        self.keySelectionUnit.setObjectName("keySelectionUnit")
        self.keySelectionTitle = QtWidgets.QLabel(self.widget)
        self.keySelectionTitle.setObjectName("keySelectionTitle")
        self.keySelectionUnit.addWidget(self.keySelectionTitle)
        self.keySelectionBox = QtWidgets.QComboBox(self.widget)
        self.keySelectionBox.setCurrentText("")
        self.keySelectionBox.setObjectName("keySelectionBox")
        self.keySelectionUnit.addWidget(self.keySelectionBox)
        self.keyScan = QtWidgets.QPushButton(self.widget)
        self.keyScan.setObjectName("keyScan")
        self.keySelectionUnit.addWidget(self.keyScan)
        self.progressBar = QtWidgets.QProgressBar(AX45S)
        self.progressBar.setGeometry(QtCore.QRect(11, 382, 441, 29))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.logTextEdit = QtWidgets.QTextEdit(AX45S)
        self.logTextEdit.setGeometry(QtCore.QRect(11, 286, 441, 91))
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setObjectName("logTextEdit")
        self.mainTab = QtWidgets.QTabWidget(AX45S)
        self.mainTab.setEnabled(True)
        self.mainTab.setGeometry(QtCore.QRect(11, 11, 441, 271))
        self.mainTab.setObjectName("mainTab")
        self.text_tab = QtWidgets.QWidget()
        self.text_tab.setObjectName("text_tab")
        self.encryptTextInput = QtWidgets.QPlainTextEdit(self.text_tab)
        self.encryptTextInput.setGeometry(QtCore.QRect(4, 5, 160, 231))
        self.encryptTextInput.setObjectName("encryptTextInput")
        self.decryptTextInput = QtWidgets.QPlainTextEdit(self.text_tab)
        self.decryptTextInput.setGeometry(QtCore.QRect(270, 5, 160, 231))
        self.decryptTextInput.setObjectName("decryptTextInput")
        self.encryptText = QtWidgets.QPushButton(self.text_tab)
        self.encryptText.setGeometry(QtCore.QRect(172, 80, 92, 41))
        self.encryptText.setObjectName("encryptText")
        self.decryptText = QtWidgets.QPushButton(self.text_tab)
        self.decryptText.setGeometry(QtCore.QRect(172, 130, 92, 41))
        self.decryptText.setObjectName("decryptText")
        self.mainTab.addTab(self.text_tab, "")
        self.file_tab = QtWidgets.QWidget()
        self.file_tab.setObjectName("file_tab")
        self.fileScanner = QtWidgets.QPushButton(self.file_tab)
        self.fileScanner.setGeometry(QtCore.QRect(330, 10, 101, 31))
        self.fileScanner.setObjectName("fileScanner")
        self.fileSelecter = QtWidgets.QComboBox(self.file_tab)
        self.fileSelecter.setGeometry(QtCore.QRect(10, 10, 311, 31))
        self.fileSelecter.setPlaceholderText("--- Files ---")
        self.fileSelecter.setObjectName("fileSelecter")
        self.decryptFile = QtWidgets.QPushButton(self.file_tab)
        self.decryptFile.setGeometry(QtCore.QRect(225, 50, 205, 41))
        self.decryptFile.setObjectName("decryptFile")
        self.encryptFile = QtWidgets.QPushButton(self.file_tab)
        self.encryptFile.setGeometry(QtCore.QRect(10, 50, 205, 41))
        self.encryptFile.setObjectName("encryptFile")
        self.mainTab.addTab(self.file_tab, "")
        self.key_tab = QtWidgets.QWidget()
        self.key_tab.setObjectName("key_tab")
        self.generateKey = QtWidgets.QPushButton(self.key_tab)
        self.generateKey.setGeometry(QtCore.QRect(10, 10, 205, 41))
        self.generateKey.setObjectName("generateKey")
        self.mainTab.addTab(self.key_tab, "")
        self.retranslateUi(AX45S)
        self.mainTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AX45S)
    def retranslateUi(self, AX45S):
        _translate = QtCore.QCoreApplication.translate
        AX45S.setWindowTitle(_translate("AX45S", "AX45-S"))
        #self.keyMainInfo.setText("")
        self.keyElements.setText("Select a key in the key selection section.")
        self.keySelectionTitle.setText(_translate("AX45S", "Key Selection :"))
        self.keySelectionBox.setPlaceholderText(_translate("AX45S", "--- Key Files ---"))
        self.keyScan.setText(_translate("AX45S", "Scan Key Files"))
        self.encryptText.setText(_translate("AX45S", "Encrypt\n  >>>"))
        self.decryptText.setText(_translate("AX45S", "Decrypt\n  <<<"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.text_tab), _translate("AX45S", "Text Operations"))
        self.fileScanner.setText(_translate("AX45S", "Scan Files"))
        self.decryptFile.setText(_translate("AX45S", "Decrypt Selected File"))
        self.encryptFile.setText(_translate("AX45S", "Encrypt Selected File"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.file_tab), _translate("AX45S", "File Operations"))
        self.generateKey.setText(_translate("AX45S", "Generate Key"))
        self.mainTab.setTabText(self.mainTab.indexOf(self.key_tab), _translate("AX45S", "Key Generation"))
        self.mainTab.setEnabled(True)
        self.info_color = "#FFD801"
        self.warning_color = "#ED2939"
        self.success_color = "#FF4CAF50"
        self.programInit()
    def logger(self,msg,status):
        if status == "INFO": self.logTextEdit.insertHtml(f'<font color={self.info_color}><strong>INFO :: </strong></font><font color="white">{msg}</font><br>')
        elif status == "WARNING": self.logTextEdit.insertHtml(f'<font color={self.warning_color}><strong>WARNING :: </strong></font><font color="white">{msg}</font><br>')
        elif status == "SUCCESS": self.logTextEdit.insertHtml(f'<font color={self.success_color}><strong>SUCCESS :: </strong></font><font color="white">{msg}</font><br>')
        self.logTextEdit.verticalScrollBar().setValue(self.logTextEdit.verticalScrollBar().maximum())
    def programInit(self):
        self.logTextEdit.insertHtml('<p>')
        self.logger("Algorithms imported successfully.", "SUCCESS")
        self.logger("Key scanning is complete, please select a key in the key selection section for using the text and file operation tabs. If you don't have any key you can create one of them in Key Generation tab.", "INFO")
        self.startup_msg=True
        self.keyLister()
        self.startup_msg=False
        self.text_tab.setEnabled(False)
        self.file_tab.setEnabled(False)
        self.fileListerFunc()
        self.encryptTextButton()
        self.decryptTextButton()
        self.fileOperationCheck()
        self.connections()
        self.step,self.total = 0, 100
        self.progressBarUpdate()
    def connections(self):
        # key operations
        self.keySelectionBox.currentTextChanged.connect(self.keyInfoMeta)
        self.keyScan.clicked.connect(self.keyLister)
        self.generateKey.clicked.connect(self.generateKeyFunc)

        # encryption & decryption algorithms
        self.encryptTextInput.textChanged.connect(self.encryptTextButton)
        self.decryptTextInput.textChanged.connect(self.decryptTextButton)
        self.encryptText.clicked.connect(self.encryptTextFunc)
        self.decryptText.clicked.connect(self.decryptTextFunc)
        self.encryptFile.clicked.connect(self.encryptFileFunc)
        self.decryptFile.clicked.connect(self.decryptFileFunc)
        self.fileScanner.clicked.connect(self.fileListerFunc)
        self.fileSelecter.currentTextChanged.connect(self.fileOperationCheck)
    def encryptTextButton(self):
        if self.encryptTextInput.toPlainText() == "": self.encryptText.setEnabled(False)
        else :
            if self.encryptText.isEnabled()==False: self.encryptText.setEnabled(True)
    def decryptTextButton(self):
        if self.decryptTextInput.toPlainText() == "": self.decryptText.setEnabled(False)
        else :
            if self.decryptText.isEnabled()==False: self.decryptText.setEnabled(True)
    def keyLister(self):
        self.keySelectionBox.clear()
        for i,key in enumerate(self.fileLister("KEY")):
            self.keySelectionBox.addItem("")
            self.keySelectionBox.setItemText(i, "key"+str(key)+".ax")
        self.text_tab.setEnabled(False)
        self.file_tab.setEnabled(False)
        self.keyMainInfo.setText("")
        self.keyElements.setText("Select a key in the key selection section.")
        if self.startup_msg == False: self.logger("Key scanning is complete, please select a key in the key selection section for using the text and file operation tabs.", "INFO")
    def fileListerFunc(self):
        self.fileSelecter.clear()
        for i,file_name in enumerate(self.fileLister("EN")+self.fileLister("DE")):
            self.fileSelecter.addItem("")
            self.fileSelecter.setItemText(i, file_name)
    def keyInfoMeta(self):
        if self.text_tab.isEnabled() and self.file_tab.isEnabled() : pass
        else:
            self.text_tab.setEnabled(True)
            self.file_tab.setEnabled(True)
        if self.keySelectionBox.currentText() != "":
            self.keyNumber = int(self.keySelectionBox.currentText().replace("key","").replace(".ax",""))
            keyInfoVariables = self.keyAnalyzer(self.keyNumber)
            self.keyMainInfo.setText(keyInfoVariables[0])
            self.keyElements.setText(keyInfoVariables[1])
            self.logger(f"{self.keySelectionBox.currentText()} imported successfully.", "INFO")
    def encryptTextFunc(self):
        if self.encryptTextInput.toPlainText() != "":
            try:
                data = self.axen(self.encryptTextInput.toPlainText(), self.keyNumber)
                self.decryptTextInput.setPlainText(data)
            except:
                self.decryptTextInput.setPlainText("")
                self.logger(f"Text and key didn't match for encryption.", "WARNING")
                self.alert("Warning", "Text and key didn't match for encryption, disagreement determined.")
    def decryptTextFunc(self):
        if self.decryptTextInput.toPlainText() != "":
            try:
                data = self.axde(self.decryptTextInput.toPlainText(), self.keyNumber)
                self.encryptTextInput.setPlainText(data)
            except:
                self.encryptTextInput.setPlainText("")
                self.logger(f"Text and key didn't match for decryption.", "WARNING")
                self.alert("Warning", "Text and key didn't match for decryption, disagreement determined.")
    def encryptFileFunc(self):
        file_name = self.fileSelecter.currentText()
        if file_name != "":
            state = self.fileEN(file_name, self.keyNumber)
            if state == True:
                self.logger(f"{file_name}.axen created.", "SUCCESS")
            else:
                self.logger(f"{file_name} and key didn't match for encryption.", "WARNING")
                self.alert("Warning", f"{file_name} and key didn't match for encryption, disagreement determined.")
    def decryptFileFunc(self):
        file_name = self.fileSelecter.currentText()
        if file_name != "":
            state = self.fileDE(file_name, self.keyNumber)
            if state == True:
                nf=file_name.replace(".axen","")
                self.logger(f"{nf} created.", "SUCCESS")
            else:
                self.logger(f"{file_name} and key didn't match for decryption.", "WARNING")
                self.alert("Warning", f"{file_name} and key didn't match for decryption, disagreement determined.")
    def generateKeyFunc(self):
        file_name = self.keyGeneration()
        self.logger(file_name+" generated.", "INFO")
        generatedKeyFileNumber = file_name.replace("key","").replace(".ax","")
    def alert(self,title,alert_msg):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(f"<p align='center'>{alert_msg}<br>")
        msg.setWindowIcon(QtGui.QIcon('files/alert.png'))
        with open("files/theme.qss",'r') as f: msg.setStyleSheet(f.read())
        msg.exec()
    def fileOperationCheck(self):
        if self.fileSelecter.currentText()[-5:] == ".axen":
            self.encryptFile.setEnabled(False)
            self.decryptFile.setEnabled(True)
        elif self.fileSelecter.currentText() == "":
            self.encryptFile.setEnabled(False)
            self.decryptFile.setEnabled(False)
        else:
            self.encryptFile.setEnabled(True)
            self.decryptFile.setEnabled(False)
    def progressBarUpdate(self):
        self.progressBar.setValue(int(self.step*100/self.total))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    AX45S = QtWidgets.QWidget()
    ui = Ui_AX45S()
    ui.setupUi(AX45S)
    AX45S.show()
    sys.exit(app.exec())
