import PyQt4,sys,os,glob,shutil,cv2
from PyQt4 import QtCore, QtGui,uic
import Face_Detection
import Find_Face
import sqlite3
import time
import ConfigParser

form_class=uic.loadUiType("abc.ui")[0]


class Ui_TabWidget(QtGui.QTabWidget,form_class):
    
    def __init__(self,parent=None):        
        QtGui.QTabWidget.__init__(self,parent)
        self.setupUi(self)
##        self.pushButton_7.clicked.connect(self.pushbutton_clicked)        
        self.pushButton_6.clicked.connect(self.addUser)         
        self.pushButton_4.clicked.connect(self.reset1)          
        self.pushButton_5.clicked.connect(self.reset2)          
        self.pushButton_8.clicked.connect(self.DeleteUser)        
        self.pushButton.clicked.connect(self.setSearchUserFileName)
        self.pushButton_3.clicked.connect(self.setSearchUser)
        self.radioButton.setChecked(True)
        self.lineEdit.setFocus()
        self.radioButton_3.setChecked(True)
        self.searchflag=1
        self.radioButton.clicked.connect(self.fn1)
        self.radioButton_2.clicked.connect(self.fn2)               
        self.groupBox_3.setEnabled(0)
        self.pushButton_8.setEnabled(0)
        self.pushButton_9.clicked.connect(self.openCam)
        self.pushButton_11.clicked.connect(self.closeCam)
        self.pushButton_12.clicked.connect(self.findfaceAt)
        self.pushButton_10.clicked.connect(self.markAttendance)
        self.pushButton_13.clicked.connect(self.calButton1)        
        self.pushButton_14.clicked.connect(self.calButton2)
        self.pushButton_15.clicked.connect(self.calButton3)        
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(('Database\DB\icons\window.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_16.clicked.connect(self.editNoOfFace)
        self.pushButton_17.clicked.connect(self.saveNoOfFace)
        self.pushButton_18.clicked.connect(self.selectFolder)
        self.setConfig()        
        self.pushButton_12.setEnabled(0)
        self.pushButton_10.setEnabled(0)
        self.pushButton_11.setEnabled(0)
        self.pushButton_18.setEnabled(1)
        self.bgBox.currentIndexChanged.connect(self.setBG)
        self.pushButton_13.setWindowIcon(self.icon)
        self.dateSize=[0,0,(9999,99,99)]
        self.light = QtGui.QGraphicsScene()        
        self.pushButton_21.clicked.connect(self.createFolder)
        self.pushButton_22.clicked.connect(self.openCam)
        self.pushButton_24.clicked.connect(self.clickPhoto)
        self.pushButton_23.clicked.connect(self.closeCam)
        


    def setBG(self):
        if(self.bgBox.currentIndex()!=0):
            self.BG.setText(str(self.bgBox.currentText()))
        else:
            self.BG.setText("")        

    def setConfig(self):
        config = ConfigParser.RawConfigParser()
        self.configFile="Database\DB\config.ini"
        config.read(self.configFile)
        self.noOfFace=int(str(config.get('info','noofface')))
        self.lineEdit_4.setText(str(self.noOfFace))
        self.lineEdit_4.setEnabled(0)
        self.pushButton_17.setEnabled(0)

    def editNoOfFace(self):
        self.lineEdit_4.setEnabled(1)
        self.pushButton_17.setEnabled(1)

    def saveNoOfFace(self):
        self.noOfFace=int(str(self.lineEdit_4.text()))
        config = ConfigParser.RawConfigParser()
        config.read(self.configFile)
        config.set('info','noofface',str(self.noOfFace))
        with open(self.configFile,'wb') as ConfigFileObject:
            config.write(ConfigFileObject)        
        self.lineEdit_4.setEnabled(0)
        self.pushButton_17.setEnabled(0)
        self.messageBox("Configuration has been Updated");   


    def pushbutton_clicked(self):                
        self.pushButton_18.setEnabled(1)
        self.openCam()
        
    def takePic(self):
        try:
            pic=self.frame
            self.mypath='temp'
            self.makemydir()
            file = "temp//attemp.jpg"
            cv2.imwrite(file, pic)
            self.lineEdit_3.setText(file)
            self.setrvalue()
            self.video_capture.release()
            cv2.destroyAllWindows()        
            self.pushButton_18.setEnabled(0)
            self.pushButton_12.setEnabled(0)
            self.pushButton_10.setEnabled(0)
            self.pushButton_11.setEnabled(0)            
            self.pushButton_9.setEnabled(1)
        except:
            self.messageBox("Open Camera First");

    def selectFolder(self):
        self.dirname=str(QtGui.QFileDialog.getExistingDirectory(self,"Select Folder of your ID"))
        self.lineEdit_3.setText(str(self.dirname))       


        
    def markAttendance(self):
        try:
            tableName=time.strftime("%Y%m%d")
            timeNow=time.strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect('Database\\DB\\EmpData.db')
            instring='INSERT INTO '+"'"+str(tableName)+"'"+'(EmpID,t) VALUES ('+str(self.foundId)+','+'"'+str(timeNow)+'"'+');'
            crstring= ('CREATE TABLE if not exists '+"'"+tableName+"'"+
                       '( SrNo INTEGER PRIMARY KEY AUTOINCREMENT, t TEXT,  EmpID INTEGER ,FOREIGN KEY (`EmpID`) REFERENCES MainInfo(EmpID));' ) 
            cur = conn.cursor()
            cur.execute(crstring)
            cur.execute(instring)
            conn.commit()
            self.textBrowser_2.clear()
            line='Attendance has been marked Successfully\nEmployee Id = '+str(self.foundId)
            self.pushButton_10.setEnabled(0)
            self.textBrowser_2.append(line)
            self.openLight(QtCore.Qt.green)
        except:
            self.messageBox("Open Camera First");
            self.openLight(QtCore.Qt.red)

    def findfaceAt(self):
        try:            
            pic=self.frame
            self.openLight(QtCore.Qt.blue)
            self.mypath='temp'
            self.makemydir()
            file = "temp//attemp.jpg"
            cv2.imwrite(file, pic)
            self.pushButton_10.setEnabled(0)
            if(Face_Detection.cropface(self.mypath,file,1)):
                self.foundId=Find_Face.searchImage(self.noOfFace)
                self.textBrowser_2.clear()
                if(self.foundId ==0):
                    line="Face has not found in Database , Search Again"
                    self.openLight(QtCore.Qt.red)
                else:
                    line='Face has been found\nEmployee Id = '+str(self.foundId)
                    self.pushButton_10.setEnabled(1)
                    self.openLight(QtCore.Qt.yellow)
            else:
                
                self.textBrowser_2.clear()
                line="Face has not found in Camera, search Again"
                self.openLight(QtCore.Qt.red)

            self.textBrowser_2.append(line)
        except:
            self.messageBox("Open Camera First");
            self.openLight(QtCore.Qt.red)

    def openLight(self,color):
        self.light.setForegroundBrush(QtGui.QBrush(color))        
        self.graphicsView_2.setScene(self.light)                
        

    def openCam(self):
        cascPath = 'haarcascade_frontalface_alt.xml'
        faceCascade = cv2.CascadeClassifier(cascPath)
        self.video_capture = cv2.VideoCapture(0)
        self.scene = QtGui.QGraphicsScene()
        self.rvalue=True        
        self.pushButton_12.setEnabled(1)        
        self.pushButton_9.setEnabled(0)        
        self.pushButton_11.setEnabled(1)
        self.openLight(QtCore.Qt.cyan)
        
        while self.rvalue:           
            ret, self.frame = self.video_capture.read()
            gray = cv2.cvtColor(self.frame, cv2.cv.CV_RGB2GRAY)
        
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            
            cv2.imshow('Video',self.frame)
            cv2.waitKey(1)
            
        
    def setrvalue(self):
        self.rvalue=False
            
    def closeCam(self):
        try:
            self.setrvalue()
            self.video_capture.release()
            cv2.destroyAllWindows()        
            self.textBrowser_2.clear()
            self.pushButton_12.setEnabled(0)
            self.pushButton_10.setEnabled(0)
            self.pushButton_11.setEnabled(0)            
            self.pushButton_9.setEnabled(1)
            self.openLight(QtCore.Qt.white)
            del self.frame
            del self.foundId
        except:
            pass
        

    def fn1(self):        
        self.groupBox_3.setEnabled(0)        
        self.groupBox_2.setEnabled(1)
        self.lineEdit.setFocus()
        self.searchflag=1
    
    def fn2(self):        
        self.groupBox_2.setEnabled(0)
        self.groupBox_3.setEnabled(1)
        self.lineEdit_2.setFocus()
        self.searchflag=2

    def reset1(self):
        try:
            self.lineEdit.clear()        
            self.lineEdit_2.clear()
            self.textBrowser.clear()
            self.scene.clear()
            self.pushButton_8.setEnabled(0)
        except:
            pass
        
    def reset2(self):                
        self.lineEdit_3.clear()
        self.Name.clear()
        self.id.clear()
        self.job.clear()
        self.con.clear()
        self.Fname.clear()
        self.BG.clear()
        self.Addr.clear()
        self.manager.clear()
        self.dep.clear()    
        self.cal1.clear()     
        self.cal2.clear()   
        self.cal3.clear()

    def DeleteUser(self):
        self.msgBox1=QtGui.QMessageBox()
        self.msgBox1.setWindowIcon(self.icon)
        self.msgBox1.setWindowTitle("    Alert   ")        
        quit_msg="Are you sure to Delete User Permanently ?"
        reply = self.msgBox1.question(self, 'Message', 
                     quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            try:
                shutil.rmtree('Database\\'+self.foundId)
                conn = sqlite3.connect('Database\DB\EmpData.db')
                cur = conn.cursor()
                id=self.foundId.split('s')[1]
                cur.execute('DELETE from MainInfo where Empid ='+id)
                conn.commit()
                self.msgBox1.setText("User has been deleted Successfully")
                self.reset1()
            except:
                self.msgBox1.setText("Errorr : User was not been deleted")
                
            self.msgBox1.exec_()            
            
        else:
            pass
       
        
        
    def makemydir(self):
        try:
            os.makedirs(self.mypath)
        except OSError:
            pass

    def messageBox(self,msg):
        self.msgBox2=QtGui.QMessageBox()
        self.msgBox2.setWindowIcon(self.icon)
        self.msgBox2.setWindowTitle("    Alert   ")
        self.msgBox2.setText(msg)
        self.msgBox2.exec_()
        return 0;

    def setSearchUser(self):
        try:
            self.textBrowser.clear()            
            self.pushButton_8.setEnabled(0)
            self.scene.clear()
        except:
            pass
        
        if(self.searchflag==1):
            if str(self.lineEdit.text())=='':
                f=self.messageBox("Select Image First");
                self.lineEdit.setFocus()
            else:
                
                self.mypath='temp'
                self.makemydir()
                if(Face_Detection.cropface(self.mypath,self.setSearchUserFile,1)):
                    self.foundId=Find_Face.searchImage(self.noOfFace)
                    if(self.foundId !=0):
                        f=1
                    else:
                        f=self.messageBox("No Emplyoee found in Database")
                        
                else:
                    f=self.messageBox("No Face found in Image")
                    
                    
        else:
            if str(self.lineEdit_2.text())=='':
                f=self.messageBox("Enter Employee Id");
                self.lineEdit_2.setFocus()
            else:
                self.foundId=int(str(self.lineEdit_2.text()))
                f=1

                    
        if(f==1):
            
            try:
                self.showText() 
                self.foundId='s'+str(self.foundId)
                self.image=glob.glob('Database\\'+self.foundId+ '/*.pgm')
                self.image=self.image[0]
                self.showImage()       
                self.pushButton_8.setEnabled(1)
            except:
                self.messageBox("No Emplyoee found in Database")

        

    def showText(self):
        conn = sqlite3.connect('Database\\DB\\EmpData.db')
        cur = conn.cursor()
        b=cur.execute('''SELECT * from MainInfo where EmpId=?''',(self.foundId,))
        c=b.fetchone()        
        line=('Id = '+str(c[0])+'\nName = '+c[1].encode("ascii")+'\nFather = '+c[2].encode("ascii")+
            '\nDOB = '+c[3].encode("ascii")+'\nGender = '+c[4].encode("ascii")+'\nBlood Group = '+c[5].encode("ascii")+
            '\nAddress = '+c[6].encode("ascii")+'\nProfile = '+c[7].encode("ascii")+'\nManager = '+c[8].encode("ascii")+
            '\nDepartment = '+c[9].encode("ascii")+'\nDate of Joining = '+c[10].encode("ascii")+
            '\nLast Working Day = '+c[11].encode("ascii")+'\nContact = '+c[12].encode("ascii") )
        self.textBrowser.append(line)      
                
        

    def showImage(self): 
        self.scene = QtGui.QGraphicsScene()
        self.scene.addPixmap(QtGui.QPixmap(self.image)) 
        self.graphicsView.setScene(self.scene)       
        

    def setSearchUserFileName(self):
        self.setSearchUserFile=str(QtGui.QFileDialog.getOpenFileName(self,"Select Image","","*.jpg"))
        self.lineEdit.setText(str(self.setSearchUserFile))
        

    
    def addUser(self):               
        self.sname=str(self.Name.text())
        self.sfname=str(self.Fname.text())
        self.seid=str(self.id.text())
        self.sbg=str(self.BG.text())
        self.sadr=str(self.Addr.toPlainText())
        self.sjob=str(self.job.text())
        self.sman=str(self.manager.text())
        self.sdep=str(self.dep.text())
        self.scon=str(self.con.text())      
        self.sdob = str(self.cal1.text())      
        self.sdoj = str(self.cal2.text())      
        self.sdow = str(self.cal3.text())
        if self.radioButton_3.isChecked():
            self.gen="Male"
        else:
            self.gen="Female"
        f=1
        if self.seid=='' or self.sname=='' or self.seid=='' or self.sfname=='' or self.sdob=='' or self.gen=='' or self.sbg=='' or  self.sadr=='':
            f=self.messageBox("Fill All The Deatails");
        if f==1 and (self.sjob=='' or self.sman=='' or self.sdep=='' or self.sdoj==''  or self.scon=='') :
            f=self.messageBox("Fill All The Deatails");
        if f==1 and str(self.lineEdit_3.text())=='':
            f=self.messageBox("Take a Picture first");
            self.lineEdit_3.setFocus()
        if f==1 and self.validateContact(self.scon):
            f=self.messageBox("Contact should be a Number of 10 Digits Exactly      ");
            self.con.setFocus()

        if f==1 and self.validateDate():
            f=self.messageBox("Date of Joining should greater than Date of Birth");
            self.cal2.setFocus()
            
        if f==1 and self.validateLWDtoDOB():
            f=self.messageBox("Last Working Day should greater than Date of Birth");
            self.cal3.setFocus()
            
        if f==1 and self.validateLWDtoDOJ():
            f=self.messageBox("Last Working Day should greater than Date of Joining");
            self.cal3.setFocus()
            
        ##Adding new values in Database start
        if(f==1):            
            conn = sqlite3.connect('Database\DB\EmpData.db')
            cur = conn.cursor()
            cur.execute('''INSERT INTO MainInfo(EmpId,EName,EFName,DOB,Gender,BG,Address,Profile,Manager,Department,Doj,LastDate,Contact)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );''',(self.seid,self.sname,self.sfname,self.sdob,self.gen,self.sbg,
                                                                  self.sadr,self.sjob,self.sman,self.sdep,self.sdoj,self.sdow,self.scon))        
            conn.commit()
            ##Adding new values in Database end
            
            self.mypath='Database\\'+'s'+str(self.seid)
            self.makemydir()
            self.newUserImagePath=str(self.lineEdit_3.text())
            Face_Detection.cropface(self.mypath,self.newUserImagePath,2)
            self.messageBox("New User has been added Successfully");
            self.reset2()

    def validateDate(self):
        if self.dateSize[1]>self.dateSize[0]:
            return False
        return True

    def validateLWDtoDOB(self):        
        if self.dateSize[2]>self.dateSize[0]:
            return False
        return True
    def validateLWDtoDOJ(self):
        if self.dateSize[2]>self.dateSize[1]:
            return False
        return True
        

    def validateContact(self,contact):
        if(len(contact)==10 and contact.isdigit()):
            return False
        return True        
            

    # calender buuton and function start
    def calButton1(self):
        self.calbox=self.cal1
        self.calender()
        
    def calButton2(self):
        self.calbox=self.cal2
        self.calender()
        
    def calButton3(self):
        self.calbox=self.cal3
        self.calender()
        
    def calender(self):
        self.dateWindow = QtGui.QWidget()
        self.cal = QtGui.QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.cal.clicked[QtCore.QDate].connect(self.showDate)
        self.hbox = QtGui.QHBoxLayout()        
        self.hbox.addWidget(self.cal)
        self.dateWindow.setLayout(self.hbox)
        self.dateWindow.setGeometry(200,200,200,200)
        self.dateWindow.setWindowTitle('Calendar')
        self.dateWindow.setWindowIcon(self.icon)
        self.dateWindow.show()

    def showDate(self, date):        
        self.calbox.setText(date.toString())
        if(self.calbox==self.cal1):
            self.dateSize[0]=date.getDate()
        if(self.calbox==self.cal2):
            self.dateSize[1]=date.getDate()
        if(self.calbox==self.cal3):
            self.dateSize[2]=date.getDate()
        self.dateWindow.close()
        
    # calender buuton and function end

    def createFolder(self):        
        self.seid=str(self.id_2.text())
        self.mypath='Student\\'+str(self.seid)
        self.makemydir()
        self.noOfPhoto=0        
        self.lineEdit_5.setText(str(self.noOfPhoto))
        self.pushButton_24.setEnabled(1)

    def clickPhoto(self):
        self.seid=str(self.id_2.text())
        pic=self.frame
        self.noOfPhoto=self.noOfPhoto+1  
        file = self.mypath+'\\'+str(self.noOfPhoto)+".jpg"
        cv2.imwrite(file, pic)
        self.lineEdit_5.setText(str(self.noOfPhoto))
        if(self.noOfPhoto==10):
            self.pushButton_24.setEnabled(0)      
        



app = QtGui.QApplication(sys.argv)
myWindow = Ui_TabWidget(None)
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap(('Database\DB\icons\window.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
myWindow.setWindowIcon(icon)
myWindow.show()
app.exec_()
