import winreg
import datetime
import os
import numpy as np
from PIL import ImageGrab
from hashlib import md5
import cv2
import time
import tkinter as tk
import pyautogui
import tkinter.messagebox
pyautogui.FAILSAFE = False

suoyin=np.zeros((9,4),dtype=np.int32)
suoyin[0]=[2,4,8,1]
suoyin[1]=[2,4,8,1]
suoyin[2]=[5,10,16,1]
suoyin[3]=[5,10,16,1]
suoyin[4]=[3,5,8,0]
suoyin[5]=[0,0,0,0]
suoyin[6]=[0,0,0,0]
suoyin[7]=[12,16,24,0]
suoyin[8]=[6,8,12,0]

sj=[[[0,0,0,0,0,0] for i in range(4)] for i in range (9)]

sj[1][0]=[0,0,0.36,0.04,0.08,0.05]
sj[1][1]=[0,0,0.26,0.03,0.04,0.04]
sj[1][2]=[0,0,0.32,0.02,0.06,0.04]
sj[1][3]=[0,0,4.58,0.4,0.85,0.6]
sj[2][0]=[0.92,0,0.15,0.01,0.04,0.04]
sj[2][1]=[0.75,0,0.13,0.01,0.02,0.02]
sj[2][2]=[0.75,0,0.11,0.01,0.03,0.01]
sj[2][3]=[17.6,0,2.78,0.39,0.52,0.22]
sj[3][0]=[0,0.61,0.16,0.02,0.04,0.01]
sj[3][1]=[0,0.51,0.11,0.01,0.02,0.01]
sj[3][2]=[0,0.51,0.13,0.01,0.02,0.01]
sj[3][3]=[0,11.7,2.77,0.19,0.56,0.37]
sj[4][0]=[0.58,0.15,0.18,0.02,0.03,0.02]
sj[4][1]=[0.45,0.10,0.15,0.01,0.04,0.02]
sj[4][2]=[0.52,0.14,0.29,0.02,0.05,0.04]
sj[5][0]=[0,0,0.2,0,0.03,0.01]
sj[5][1]=[0,0,0.23,0.02,0.07,0.02]
sj[6][0]=[0.04,0.13,0.04,0,0.04,0.08]
sj[6][1]=[0.20,0.07,0.09,0,0.04,0]
sj[6][2]=[0.33,0.09,0.25,0.02,0.03,0.02]
sj[7][0]=[0,0,0.13,0.01,0.01,0.01]
sj[7][1]=[0.07,0.01,0.12,0.01,0.03,0.02]
sj[7][2]=[0.07,0.02,0.10,0.01,0.03,0.01]
sj[8][0]=[0,0,0.12,0.01,0.05,0]
sj[8][1]=[0,0,0.15,0.02,0.03,0.02]
sj[8][2]=[0,0,0.13,0,0.01,0]


z=[0,0,0,0,0,0]#为权重分配，金图到staag
qz=[[0] *4 for i in range (10)]#加权后计算得分
chuang_kou_zuo_biao=[0,0,0,0]



class pic(tk.Frame):
    weituowancheng=False
    home=[0.93,0.082]
    keyantubiao=[0.55,0.96]
    junbu=[0.3,0.5]
    if_run=False
    zuo_biao=np.zeros((10,2),dtype=np.int32)
    cishu=[0]*10  #第0个为截屏次数 #第一个为是否开始，开始后变为1
    start_time=0#时间戳
    rest_time=0
    ration=1
    if_tiaozhuan2=False
    if_tiaozhuan=False
    if_keyan=True
    if_weituo=True
    if_weituorun=False
    start_time2=0#时间戳
    rest_time2=0
    def tanchuang2(self):
        tc=tk.Tk()
        l=tk.Label(tc,text="20秒后将自动跳转,暂停后可点击继续",font=("微软雅黑",15))
        l.pack()
        tc.title("时间已到")
        tc.geometry("350x120")
        time1=time.time()
        def zidong():
            if(time.time()-time1)>21:
                self.if_tiaozhuan2=True
                tc.destroy()
            tc.after(1000,zidong)
        zidong()
        def liji():
            self.if_tiaozhuan2=True
            tc.destroy()
        b1=tk.Button(tc,text="立即前往",command=liji)
        b1.place(relx=0.2,rely=0.5)
        def zanting():
            self.if_tiaozhuan2=False
            tc.destroy()
        b2=tk.Button(tc,text="暂停",command=zanting)
        b2.place(relx=0.6,rely=0.5)
    def tanchuang(self):
        tc=tk.Tk()
        l=tk.Label(tc,text="30秒后将自动跳转,暂停后可点击继续",font=("微软雅黑",15))
        l.pack()
        tc.title("时间已到")
        tc.geometry("350x120")
        time1=time.time()
        def zidong():
            if(time.time()-time1)>31:
                self.if_tiaozhuan=True
                tc.destroy()
            tc.after(1000,zidong)
        zidong()
        def liji():
            self.if_tiaozhuan=True
            tc.destroy()
        b1=tk.Button(tc,text="立即前往",command=liji)
        b1.place(relx=0.2,rely=0.5)
        def zanting():
            self.if_tiaozhuan=False
            tc.destroy()
        b2=tk.Button(tc,text="暂停",command=zanting)
        b2.place(relx=0.6,rely=0.5)

    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.pack()
        def quanzhong():
            q=tk.Toplevel()
            q.geometry("600x700")
            q.title("权重设置")



            s=tk.Scale(q,label="金色蓝图",from_=1,to=5,orient=tk.HORIZONTAL,length=200,tickinterval=1,resolution=0.5)
            s.place(relx=0.05,rely=0)
            s2=tk.Scale(q,label="彩色蓝图",from_=1,to=40,orient=tk.HORIZONTAL,length=200,tickinterval=13,resolution=0.5)
            s2.place(relx=0.05,rely=0.13)
            s3=tk.Scale(q,label="金色装备图纸",from_=1,to=20,orient=tk.HORIZONTAL,length=200,tickinterval=6.5,resolution=0.5)
            s3.place(relx=0.05,rely=0.26)
            s4=tk.Scale(q,label="彩色装备图纸",from_=1,to=200,orient=tk.HORIZONTAL,length=200,tickinterval=40,resolution=0.5)
            s4.place(relx=0.05,rely=0.39)
            s5=tk.Scale(q,label="金火控雷达",from_=1,to=20,orient=tk.HORIZONTAL,length=200,tickinterval=6.5,resolution=0.5)
            s5.place(relx=0.05,rely=0.52)
            s6=tk.Scale(q,label="金博福斯staag",from_=1,to=20,orient=tk.HORIZONTAL,length=200,tickinterval=6.5,resolution=0.5)
            s6.place(relx=0.05,rely=0.65)
            cvar1=tk.IntVar()
            cb1=tk.Checkbutton(q,text="魔方解析1h，心智补全。此为最高优先级",variable=cvar1,onvalue=1,offvalue=0)
            cb1.place(relx=0.05,rely=0.8)
            cvar2=tk.IntVar()
            cb2=tk.Checkbutton(q,text="开启后将不做需要物资的科研,半小时科研不受影响",variable=cvar2,onvalue=1,offvalue=0)
            cb2.place(relx=0.5,rely=0.8)
            l3=tk.Label(q,text="目前不会选择有附加条件的科研项目")
            l3.place(relx=0.5,rely=0.6)
            def queding():
                z[0]=s.get()
                z[1]=s2.get()
                z[2]=s3.get()
                z[3]=s4.get()
                z[4]=s5.get()
                z[5]=s6.get()
                global qz
                for i in range(9):
                    for j in range(4):
                        for k in range(6):
                            qz[i][j]=qz[i][j]+sj[i][j][k]*z[k]
                if("1"==str(cvar1.get())):
                    qz[0][0]=1000
                    qz[0][3]=2000
                if("1"==str(cvar2.get())):
                    qz[2][0]=0
                    qz[2][1]=0
                    qz[2][2]=0
                    qz[3][0]=0
                    qz[3][1]=0
                    qz[3][2]=0
                    qz[4][0]=0
                    qz[4][1]=0
                    qz[4][2]=0
                np.save("1",np.array(qz))
                q.destroy()


            
            b=tk.Button(q,text="确定",width=8,command=queding)
            b.place(relx=0.1,rely=0.9)
        def jietu():
            self.cishu[0]=0
            def myevent(event,x,y,flag,param):
                if(event==cv2.EVENT_LBUTTONDOWN):
                    
                    if(self.cishu[0]==1):
                        self.zuo_biao[1]=[x,y]
                        self.cishu[0]+=1
                    if(self.cishu[0]==0):
                        self.zuo_biao[0]=[x,y]
                        self.cishu[0]+=1
            cv2.namedWindow("123")
            self.screenshot(2)
            a=cv2.imread("p/2.png")
            h,w,r=a.shape
            a=a[h//3:h]
            cv2.setMouseCallback("123",myevent)
            while self.cishu[0]!=2:
                cv2.imshow("123",a)
                cv2.waitKey(100)
                if self.cishu[0]==1:
                    cv2.circle(a,self.zuo_biao[0],1,(255,0,255),1,-1)
                if self.cishu[0]==2:
                    cv2.rectangle(a,self.zuo_biao[0],self.zuo_biao[1],(255,0,255),1)
                    cv2.imshow("123",a)
                    a=a[self.zuo_biao[0][1]+1:self.zuo_biao[1][1],self.zuo_biao[0][0]+1:self.zuo_biao[1][0]]
                    cv2.imwrite("p/2.png",a)
                    cv2.waitKey(1000)
                    cv2.destroyWindow("123")
                    
            cv2.waitKey(0)
        master.title("碧蓝程序")
        master.geometry("400x600")
        l=tk.Label(master,text="选择分辨率")
        l.place(relx=0.65,rely=0.2)
        tvar=tk.StringVar()
        l2=tk.Label(master, text="00:00:00",textvariable=tvar ,fg='black',font=("微软雅黑",40))
        tvar.set("00:00:00")
        l2.place(relx=0.29,rely=0.05)
        def gotoweituo():
            if self.if_tiaozhuan2:
                self.if_tiaozhuan2=False
                self.movetomoniqi()
                quick_move(self.home[0],self.home[1])
                pyautogui.click()
                pyautogui.click()
                time.sleep(0.3)
                pyautogui.click()
                time.sleep(0.3)
                pyautogui.click()
                quick_move(0.83,0.52)
                pyautogui.click()
                quick_move(0.67,0.85)
                pyautogui.click()
                quick_move(0.25,0.25)
                for i in range(20):
                    time.sleep(0.1)
                    pyautogui.click()
                for i in range(4):
                    quick_move(self.home[0],self.home[1])
                    pyautogui.click()
                    quick_move(0.83,0.52)
                    pyautogui.click()
                    quick_move(0.67,0.85)
                    pyautogui.click()
                    quick_move(0.25,0.6)
                    pyautogui.drag(0,-2000,0.5,button="left")
                    quick_move(0.25,0.88)
                    pyautogui.click()
                    quick_move(0.71,0.51)
                    pyautogui.click()
                    quick_move(0.84,0.51)
                    pyautogui.click()
                    time.sleep(0.1)
                pyautogui.hotkey("win","m")
            master.after(500,gotoweituo)

        def tiaozhuan():
            if(self.if_tiaozhuan):
                self.if_tiaozhuan=False
                self.movetomoniqi()
                self.movetokeyan()
                time.sleep(1)
                wt=self.get_time()
                if(wt[0]==0 and wt[1]==0 and wt[5]==0):
                    tk.messagebox.showwarning(title="错误",message="当前科研条件未完成或出现错误,请完成后重启程序")
                else:
                    cv2.waitKey(2000)
                    self.chanchujietu()
                    quick_move(0.5,0.7)
                    self.hanshu2()
            master.after(300,tiaozhuan)
        def runtime():
            if self.if_run:
                nowtime=self.rest_time-(time.time()-self.start_time)
                if nowtime>0:
                    if(self.if_keyan==1 and self.if_weituo==1):
                        if(self.weituowancheng):
                            if(nowtime>2000):
                                self.weituowancheng=False
                                self.set_weituo_time([0,0,2,5,0,0])
                    tvar.set(time_switch(nowtime))
                else:
                    tvar.set(0)
                    self.if_run=False
                    self.rest_time=0
                    self.start_time=0
                    self.tanchuang()
                    tiaozhuan()
            master.after(500,runtime)
        runtime()
        def runtime2():
            if self.if_weituorun:
                nowtime=self.rest_time2-(time.time()-self.start_time2)
                if nowtime<0:
                    self.if_weituorun=False
                    self.rest_time2=0
                    self.start_time2=0
                    self.tanchuang2()
                    gotoweituo()
                    if(self.if_keyan==0):
                        self.set_weituo_time([0,0,2,5,0,0])
                self.weituowancheng=True
            master.after(500,runtime2)
        runtime2()
        def ckck():
            self.ration=float(var.get())
        var=tk.StringVar()
        ck1=tk.Radiobutton(master,text="1080",variable=var,value="1",command=ckck)
        ck2=tk.Radiobutton(master,text="2k",variable=var,value="1.414",command=ckck)
        ck3=tk.Radiobutton(master,text="4k",variable=var,value="2",command=ckck)
        ck1.select()
        ck1.place(relx=0.65,rely=0.25)
        ck2.place(relx=0.65,rely=0.3)
        ck3.place(relx=0.65,rely=0.35)
        def keyan():
            self.if_keyan=not self.if_keyan
        kaiqikeyan=tk.Checkbutton(master,text="启动自动科研",command=keyan)
        def weituo():
            self.if_weituo=not self.if_weituo
        kaiqiweituo=tk.Checkbutton(master,text="启动自动委托",command=weituo)
        kaiqikeyan.select()
        kaiqiweituo.select()
        kaiqikeyan.place(relx=0.55,rely=0.5)
        kaiqiweituo.place(relx=0.55,rely=0.6)
        #s6=tk.Button(master,text="试验",width=12,command=self.tanchuang)
        #s6.place(relx=0.1,rely=0.1)
        s2=tk.Button(master,text="截取模拟器图标",width=12,command=jietu)
        s2.place(relx=0.3,rely=0.2)
        s3=tk.Button(master,text="设置权重",width=10,command=quanzhong)
        s3.place(relx=0.3,rely=0.3)
        s4=tk.Button(master,text="开始",width=6,command=self.zhuhanshu)
        s4.place(relx=0.3,rely=0.4)
        s7=tk.Button(master,text="查看产出",width=6,command=lambda : os.startfile("poic"))
        s7.place(relx=0.3,rely=0.6)
        def jixu():
            self.if_tiaozhuan=True
        s5=tk.Button(master,text="继续",width=6,command=jixu)
        s5.place(relx=0.3,rely=0.5)
            
    @classmethod
    def screenshot(self,name):
        im=ImageGrab.grab()
        s="p/"+str(name)+".png"
        im.save(s)
    
    

    def chanchujietu(self):
        cv2.waitKey(300)
        nowtime=get_beijin_time()
        im=ImageGrab.grab()
        s="poic/"+str(nowtime[0:13])+","+str(nowtime[14:16])+".png"
        im.save(s)

    def zhuhanshu(self):
        if self.cishu[1]==0:
            if(self.if_keyan==1 ):
                if(os.path.exists("p/2.png")):
                    if("yes"==tk.messagebox.askquestion(title="确认开始",message="开始后请勿移动鼠标,最小化模拟器窗口后操作完成")):
                        global qz
                        qz=np.load("1.npy")
                        self.hanshu2()
                    else:
                        return
                else:
                    tk.messagebox.showwarning(title="无图标",message="没有截图图标")
                    return
            if(self.if_keyan==0 and self.if_weituo==1):
                self.cishu[1]=1
                if("yes"==tk.messagebox.askquestion(title="确认开始",message="开始后请勿移动鼠标,最小化模拟器窗口后操作完成")):
                    self.set_weituo_time([0,0,0,0,0,0])
            if(self.if_keyan==0 and self.if_weituo==0):
                tk.messagebox.showwarning(title="错误",message="你想干嘛？")
        else:
            return
    

    def movetomoniqi(self):
        self.screenshot("first")
        background=cv2.imread("p/first.png",0)
        tubiao=cv2.imread("p/2.png",0)
        tubiaoh,tubiaow=tubiao.shape
        res=cv2.matchTemplate(background,tubiao,cv2.TM_SQDIFF_NORMED)
        min_value,max_value,min_location,max_location=cv2.minMaxLoc(res)
        x,y=min_location
        pyautogui.moveTo(x+tubiaow//2,y+tubiaoh//2,0.5)
        cv2.waitKey(500)
        pyautogui.click()

        self.screenshot("first")
        background=cv2.imread("p/first.png",0)
        pyautogui.moveTo(x+tubiaow//2,y+tubiaoh//2,0.5)
        cv2.waitKey(200)
        pyautogui.click()
        self.screenshot("second")
        moniqiground=cv2.imread("p/second.png",0)
        moniqi=cv2.bitwise_xor(moniqiground,background)
        r,img=cv2.threshold(moniqi,1,255,cv2.THRESH_BINARY)
        contours,h=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        pyautogui.moveTo(x+tubiaow//2,y+tubiaoh//2,0.5)
        cv2.waitKey(200)
        pyautogui.click()
        maxlist=[0,0,0,0,0]
        for zuobiao in contours:
            m_list=cv2.boundingRect(zuobiao)
            if(m_list[2]*m_list[3]>maxlist[4]):
                global chuang_kou_zuo_biao
                chuang_kou_zuo_biao=list(m_list)
                chuang_kou_zuo_biao[2]=int(chuang_kou_zuo_biao[2]*1.0236)
                for i in range(4):
                    maxlist[i]=m_list[i]
                maxlist[4]=m_list[2]*m_list[3]
        print(maxlist)
    def movetozhiding(self,x:int):
        quick_move(self.home[0],self.home[1])
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.click()
        quick_move(self.keyantubiao[0],self.keyantubiao[1])
        pyautogui.click()
        quick_move(self.junbu[0],self.junbu[1])
        pyautogui.click()
        for i in range(x):
            quick_move(0.65,0.5)
            pyautogui.click()
            pyautogui.click()
        quick_move(0.5,0.5)
        pyautogui.click()
        time.sleep(0.5)
        quick_move(0.38,0.82)
        pyautogui.click()
        time.sleep(1)
        atime=self.get_time()
        print(atime)
        time.sleep(3)
        wtime=self.get_time()
        if wtime[5]!=0:
            self.set_time(wtime)
            pyautogui.hotkey("win"+"m")
            return True
        elif atime[0]==9:
            quick_move(0.6,0.71)
            pyautogui.click()
            time.sleep(4)
            self.set_time(self.get_time())
            tubiao=cv2.imread("p/2.png",0)
            tubiaoh,tubiaow=tubiao.shape
            res=cv2.matchTemplate(background,tubiao,cv2.TM_SQDIFF_NORMED)
            min_value,max_value,min_location,max_location=cv2.minMaxLoc(res)
            x,y=min_location
            pyautogui.moveTo(x+tubiaow//2,y+tubiaoh//2,0.5)
            cv2.waitKey(500)
            pyautogui.click()
            pyautogui.moveRel(0,-tubiaoh*3,0.5)
            return True
        else:
            return False

    def movetokeyan(self):
        quick_move(self.home[0],self.home[1])
        pyautogui.click()
        quick_move(self.home[0]*0.96,self.home[1]*1.5)
        pyautogui.click()
        quick_move(self.home[0]*0.98,self.home[1]*1.2)
        pyautogui.click()
        quick_move(self.home[0],self.home[1])
        pyautogui.click()
        quick_move(self.keyantubiao[0],self.keyantubiao[1])
        pyautogui.click()
        quick_move(self.junbu[0],self.junbu[1])
        pyautogui.click()
        quick_move(0.5,0.5)
        pyautogui.click()
    def get_time(self):
        try:
            cv2.waitKey(1000)
            self.screenshot("third")
            third=cv2.imread("p/third.png",0)
            roi=third[realy(0.4):realy(0.48),realx(0.6):realx(0.7)]
            self.get_ration(roi)
            r,roi=cv2.threshold(roi,180,255,cv2.THRESH_BINARY)
            bg=np.array(roi,dtype=np.uint8)
            w,h=bg.shape
            listx=[]
            for i in range(h):
                xs=0
                for j in range(w):
                    xs+=bg.item(j,i)
                listx.append(xs)
            lix=[]
            ave=listx.copy()
            while 0 in ave:
                ave.remove(0)
            avn=np.mean(ave)//4
            for i in range(len(listx)):
                if listx[i] < avn:
                    listx[i]=0
            for i in range(len(listx)-1):
                if(listx[i]==0 and listx[i+1]!=0):
                    lix.append(i)
                if(listx[i]!=0 and listx[i+1]==0):
                    lix.append(i+1)
        
            i=0
            while i<len(lix):
                if (lix[i+1]-lix[i])<((lix[1]-lix[0])*0.4):
                    del lix[i+1]
                    del lix[i]
                i+=2
            atime=[9,0,0,0,0,0]
            for i in range(len(lix)//2):
                num=roi[:,lix[2*i]:lix[2*i+1]]
                #cv2.imshow("sdfsa",num)
                #cv2.waitKey(0)
                num=cv2.copyMakeBorder(num,10,10,30,30,cv2.BORDER_CONSTANT,value=0)
                minvalue=1
                for j in range(10):
                    name="number/"+str(j)+".png"
                    shu=cv2.imread(name,0)
                    shu=cv2.resize(shu,None,None,self.ration,self.ration)
                    cra,shu=cv2.threshold(shu,210,255,cv2.THRESH_BINARY)
                    #cv2.imshow("faa",shu)
                    #cv2.imshow("faas",num)
                    #cv2.waitKey(0)
                    res=cv2.matchTemplate(num,shu,cv2.TM_SQDIFF_NORMED)
                    minv,maxv,minl,maxl=cv2.minMaxLoc(res)
                    if(minv<minvalue):
                        minvalue=minv
                        atime[i]=j

            return atime
        except:
            return [9,0,0,0,0,0]

    def get_ration(self,bg):
        r=self.ration
        rs,bg=cv2.threshold(bg,190,255,cv2.THRESH_BINARY)
        n0=cv2.imread("number/0.png",0)
        ra,n0=cv2.threshold(n0,200,255,cv2.THRESH_BINARY)
        min_value=1
        rat=1
        for i in np.arange(0.5*r,1.2*r,0.01*r):
            zero=cv2.resize(n0,dsize=None,fx=i,fy=i)
            res=cv2.matchTemplate(bg,zero,cv2.TM_SQDIFF_NORMED)
            minv,maxv,minl,maxl=cv2.minMaxLoc(res)
            if(minv<min_value):
                min_value=minv
                rat=i
        self.ration=rat
        
    def hanshu2(self):
        self.cishu[1]=1
        self.movetomoniqi()
        self.movetokeyan()
        time.sleep(1)
        w_time=self.get_time()
        if(w_time[3]!=0 or w_time[4]!=0 or w_time[5]!=0):
            self.set_time(w_time)
            pyautogui.hotkey("win","m")
        elif(w_time[0]==0 and w_time[1]==0 and w_time[2]==0):
            tk.messagebox.showwarning(title="错误",message="当前科研任务未完成或出现错误,请完成后重启程序")
        else:
            qzlb=[]
            for i in range(5):
                qzlb.append(self.shibie())
                quick_move(0.65,0.5)
                pyautogui.click()
                pyautogui.click()
            sortlist=qzlb.copy()
            sortlist.sort()
            sortlist.reverse()
            for i in range(5):
                if(self.movetozhiding(qzlb.index(sortlist[i]))):
                    return
                else:
                    continue

    def set_time(self,w):
        self.rest_time=(w[0]*10+w[1])*3600+(w[2]*10+w[3])*60+w[4]*10+w[5]
        self.start_time=time.time()
        self.if_run=True

    def set_weituo_time(self,w):
        self.rest_time2=(w[0]*10+w[1])*3600+(w[2]*10+w[3])*60+w[4]*10+w[5]
        self.start_time2=time.time()
        self.if_weituorun=True

    def shibie(self):
        quanzhong=np.load("1.npy")
        time.sleep(1)
        self.screenshot("xmm")
        roi=cv2.imread("p/xmm.png",0)
        roi=roi[realy(0.17):realy(0.24),realx(0.25):realx(0.325)]
        r,roi=cv2.threshold(roi,200,255,cv2.THRESH_BINARY)
        roi=cv2.copyMakeBorder(roi,10,10,30,30,cv2.BORDER_CONSTANT,value=0)
        h,w=roi.shape
        listy=[]
        for i in range(h):
            shuzhi=0
            for j in range(w):
                shuzhi+=roi[i][j]
            listy.append(shuzhi)
        avn=np.mean(listy)
        i=0
        while i < len(listy):
            if listy[i]<avn:
                listy.remove(listy[i])
            else:
                i+=1
        file=os.listdir("xiangmuming")
        minvalue=1
        name=""
        for i in file:
            filename="xiangmuming/"+i
            moban=cv_imread(filename)
            moban=cv2.cvtColor(moban,cv2.COLOR_BGR2GRAY)
            gao=int(i[-6:-4])
            rat=len(listy)/gao
            moban=cv2.resize(moban,None,None,rat,rat)
            r,moban=cv2.threshold(moban,190,255,cv2.THRESH_BINARY)
            for g in np.linspace(0.8,1.2,11):
                copy=moban.copy()
                copy=cv2.resize(copy,None,None,g,g)
                #cv2.imshow("asxz",copy)
                #cv2.waitKey(0)
                ret=cv2.matchTemplate(roi,copy,cv2.TM_SQDIFF_NORMED)
                minv,asd,eaf,efs=cv2.minMaxLoc(ret)
            
                if (minv<minvalue):
                    minvalue=minv
                    name=i
        name=list(name)
        list.reverse(name)
        del name[0:6]
        list.reverse(name)
        name=''.join(name)
        resttime=self.get_time()
        xiabiao=-1
        if resttime[2]==3:
            xiabiao=resttime[1]*2+1
        else:
            xiabiao=resttime[1]*2
        global suoyin
        if name=="定向研发":
        
            cv2.waitKey(100)
            self.screenshot("tuzhi")
            tuzhi=cv2.imread("p/tuzhi.png")
            roi=tuzhi[realy(0.35):realy(0.6),realx(0.26):realx(0.4)]
            roi=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            roi=cv2.inRange(roi, np.array([15,50,50]),np.array([25,255,255]))
            roi=list(roi)
            if np.mean(roi)>10:
                firstnumber=2
                for i in range(4):
                    if suoyin[firstnumber][i]==xiabiao:
                        return quanzhong[firstnumber][i]
            else:
                firstnumber=3
                for i in range(4):
                    if suoyin[firstnumber][i]==xiabiao:
                        return quanzhong[firstnumber][i]

        if name=="魔方解析":
            firstnumber=0
            for i in range(4):
                if suoyin[firstnumber][i]==xiabiao:
                    return quanzhong[firstnumber][i]
        if name=="心智补全":
            firstnumber=0
            for i in range(4):
                if suoyin[firstnumber][i]==xiabiao:
                    return quanzhong[firstnumber][i]
        if name=="舰装解析":
            firstnumber=1
            for i in range(4):
                if suoyin[firstnumber][i]==xiabiao:
                    return quanzhong[firstnumber][i]
        if name=="资金募集":
            firstnumber=4
            for i in range(4):
                if suoyin[firstnumber][i]==xiabiao:
                    return quanzhong[firstnumber][i]
        if name=="基础研究":
            firstnumber=7
            for i in range(4):
                if suoyin[firstnumber][i]==xiabiao:
                    return quanzhong[firstnumber][i]
        if name=="试验品募集":
            return 0
        if name=="数据收集":
            return 0
        if name=="研究委托":
            return 0

def quick_move(x,y):
    print(chuang_kou_zuo_biao[0]+int(x*chuang_kou_zuo_biao[2]),chuang_kou_zuo_biao[1]+int(y*chuang_kou_zuo_biao[3]))
    pyautogui.moveTo(chuang_kou_zuo_biao[0]+int(x*chuang_kou_zuo_biao[2]),chuang_kou_zuo_biao[1]+int(y*chuang_kou_zuo_biao[3]),0.5)

def realx(x):
    return chuang_kou_zuo_biao[0]+int(x*chuang_kou_zuo_biao[2])
def realy(y):
    return chuang_kou_zuo_biao[1]+int(y*chuang_kou_zuo_biao[3])

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img

def get_id():#获取系统唯一标识码
    key = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        "SOFTWARE\\Microsoft\\Cryptography",0,
        winreg.KEY_READ | winreg.KEY_WOW64_64KEY
    )
    result = winreg.QueryValueEx(key, "MachineGuid")
    return result[0]

def get_beijin_time():
    try:
        url = 'https://beijing-time.org/'
        request_result = requests.get(url=url)
        if request_result.status_code == 200:
            headers = request_result.headers
            net_date = headers.get("date")
            gmt_time = time.strptime(net_date[5:25], "%d %b %Y %H:%M:%S")
            bj_timestamp = int(time.mktime(gmt_time) + 8 * 60 * 60)
            return datetime.datetime.fromtimestamp(bj_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as exc:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def signout():
    os._exit(0)

def h(t):
    t=t.encode("utf-8")
    return md5(t).hexdigest()[0:6]

def input_jihuoma():
    def if_right(window):
        t=get_beijin_time()[0:10]
        if( line.get()==str(h(t))):
            window.destroy()
            with open("1.txt","w") as first:
                first.write(h(get_id()))
                main()
        else:
            #print(str(h(t)))
            var.set("输入错误")
    tim=get_beijin_time()

    try:
        window=tk.Tk()
        window.title("激活码")
        window.geometry("300x200")
        line=tk.Entry(window,width=22)
        line.place(relx=0.3,rely=0.2)
        var=tk.StringVar()
        l=tk.Label(window,textvariable=var,font=("",15))
        var.set("请输入激活码")
        l.pack()
        confirm=tk.Button(window,text="确认",width=5,height=1,command=lambda : if_right(window))
        confirm.place(relx=0.3,rely=0.4)
        quit=tk.Button(window,text="退出",width=5,height=1,command=signout)
        quit.place(relx=0.6,rely=0.4)
        window.mainloop()
    except:
        print("error")

def time_switch(miaoshu):
    miaoshu=int(miaoshu)
    fir=str(miaoshu//3600)
    miaoshu=miaoshu%3600
    if((miaoshu//60)<10):
        sec="0"+str(miaoshu//60)
    else:
        sec=str(miaoshu//60)
    miaoshu=miaoshu%60
    if(miaoshu<10):
        thir="0"+str(miaoshu)
    else:
        thir=str(miaoshu)
    rt=fir+":"+sec+":"+thir
    return rt

def main():
    root=tk.Tk()
    shot=pic(master=root)
    shot.mainloop()

def start():
    
    with open("1.txt","a+") as first:
        first.seek(0,os.SEEK_SET)
        s=first.read()
        if(s!=h(get_id())):
            input_jihuoma() 
        else:
            main()

start()