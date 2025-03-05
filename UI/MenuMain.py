from tkinter import *  # 引入模块
from playsound import playsound
from tkinter.messagebox import *
import threading
import time

import pygame

from UI import Info

ImgNum = int(time.time()) % 4
def main():
    class voiceOpera():
        def __init__(self):
            self.BGM = 0
            self.voice = 0.5
            self.changeVoice_FirstTime = True
            self.l = 0
            music_start =  False

        def changeVoice(self,event):
            print('changeVoice')
            if self.changeVoice_FirstTime:
                self.BGM = bgm.Get_voice()
                canvas.coords(vr3, 188, 155, bgm.Get_voice() * 1000 + 128, 195)
                canvas.coords(vr4, 188, 255, self.voice * 1000 + 118, 295)
                self.changeVoice_FirstTime = False
            pic.PicShow(False)
            for i in Info.uiList:
                canvas.itemconfigure(i['Num'], state='hidden')

            canvas.itemconfigure('vt1',state = 'normal')
            print("SHOW")

            if 148 <= event.x <= 1273 and 155 <= event.y <= 195:
                self.l = event.x
                if event.x - 188 <= 0:
                    self.l = 188
                elif event.x - 1178 >= 0:
                    self.l = 1178
                bgm.BGM_voice((self.l - 188) / 1000)
                canvas.coords(vr3, 188, 155, self.l, 195)

            if 148 <= event.x <= 1273 and 255 <= event.y <= 295:
                self.l = event.x
                if event.x - 188 <= 0:
                    self.l = 188
                elif event.x - 1178 >= 0:
                    self.l = 1178
                self.voice = (self.l - 188) / 1000
                canvas.coords(vr4, 188, 255, self.l, 295)
            print(self.BGM, "+", self.voice)

            if 533 <= event.x <= 633 and 480 <= event.y <= 520:  # 确定键
                self.changeVoice_FirstTime = True
                canvas.itemconfigure('vt1', state='hidden')

                pic.PicShow(True)

                for i in Info.uiList:
                    canvas.itemconfigure(i['Num'], state='normal')
                return 0
            elif 733 <= event.x <= 833 and 480 <= event.y <= 520:  # 取消键
                self.changeVoice_FirstTime = True
                bgm.BGM_voice(self.BGM)
                canvas.itemconfigure('vt1', state='hidden')

                pic.PicShow(True)

                for i in Info.uiList:
                    canvas.itemconfigure(i['Num'], state='normal')
                return 0
            else:  # 循环
                return 1

        def HighLine(self,event):
            print('HighLine')

            if 533 <= event.x <= 633 and 480 <= event.y <= 520:
                canvas.itemconfigure(vt3, fill='white')  # 重设显示文本颜色
            elif 733 <= event.x <= 833 and 480 <= event.y <= 520:#取消键
                canvas.itemconfigure(vt4, fill='white')  # 重设显示文本颜色
            elif 148 <= event.x <= 1273 and 255 <= event.y <= 295:
                canvas.itemconfigure(vt1,fill = 'white')
                canvas.itemconfigure(vr2, outline='white')
                canvas.itemconfigure(vr4, fill='white',outline='white')
            elif 148 <= event.x <= 1273 and 155 <= event.y <= 195:
                canvas.itemconfigure(vt2, fill='white')
                canvas.itemconfigure(vr1, outline='white')
                canvas.itemconfigure(vr3, fill='white',outline='white')
            else:
                canvas.itemconfigure(vt1, fill = 'grey')
                canvas.itemconfigure(vt2, fill = 'grey')
                canvas.itemconfigure(vt3, fill = 'grey')
                canvas.itemconfigure(vt4, fill = 'grey')
                canvas.itemconfigure(vr1, outline = 'grey')
                canvas.itemconfigure(vr2, outline = 'grey')
                canvas.itemconfigure(vr3, fill = 'grey',outline = 'grey')
                canvas.itemconfigure(vr4, fill = 'grey',outline = 'grey')
            return

    def Voice():
        playsound("Music/哲♂学经典语录 - 1.16791305-33-34.wav")
        return
    def Voice1():
        playsound("Music/WU♂ - 1.164538002205-0-0 (1).wav")
        return

    class ShuBiaoKongZhi():
        def __init__(self):
            self.ret=0
        global ReturnNum
        menuNumNow = 0
        ts = threading.Thread(target=Voice1)

        def getReturnNum(self):
            return self.ret

        def MenuChoose(self,event):

            if self.menuNumNow == 0:
                self.Menu1(event)

            elif self.menuNumNow == 1:
                self.Menu2(event)
                print("Menu2")

            else:
                self.menuNumNow = 0
            return

        def MenuKickChoose(self,event):  # 鼠标经过响应函数
            print('Kick',self.menuNumNow)
            if self.menuNumNow == 0:
                self.MenuKick1(event)
            elif self.menuNumNow == 1:
                self.MenuKick2(event)

        def MenuKick1(self,event):
            self.ret = 0
            if 200 <= event.x <= 250 and 490 <= event.y <= 510:  # bean
                #self.ts.start()
                print("bean")
                self.ret = 1
                root.destroy()
            elif 265 <= event.x <= 345 and 490 <= event.y <= 510:  # plane
                #self.ts.start()
                print("plane")
                self.ret = 2
                root.destroy()
            elif 355 <= event.x <= 435 and 490 <= event.y <= 510:  # tank
                #self.ts.start()
                print("tank")
                self.ret = 3
                root.destroy()
            elif 445 <= event.x <= 550 and 490 <= event.y <= 510:  # craft
                #self.ts.start()
                print("craft")
                self.ret = 4
                root.destroy()
            elif 200 <= event.x <= 250 and 540 <= event.y <= 565:  # tank
                #self.ts.start()
                self.menuNumNow = voiceopera.changeVoice(event)
                print("voice")
            elif 270 <= event.x <= 323 and 540 <= event.y <= 565:  # background
                #self.ts.start()
                print("background")
                ChangeImg()
            elif 340 <= event.x <= 450 and 540 <= event.y <= 565:  # BGM
                #self.ts.start()
                print("BGM")
                bgm.BGM_change()

            elif 200 <= event.x <= 360 and 570 <= event.y <= 610:  # exit
                #self.ts.start()
                if askyesnocancel(title='退出', message='是否确定退出？'):
                    print("Exit")
                    self.ret = -1
                    root.destroy()


        def MenuKick2(self,event):
            self.menuNumNow = voiceopera.changeVoice(event)
            return

        def Menu1(self,event):
            music_start = True
            if 200 <= event.x <= 550 and 450 <= event.y <= 510:  # 开始游戏
                canvas.itemconfigure(Info.uiList[Info.start]['Num'], fill='white')  # 重设显示文本颜色
                if 200 <= event.x <=250 and 490 <= event.y <= 510:
                    canvas.itemconfigure(Info.uiList[Info.bean]['Num'], fill='white')  # 重设显示文本颜色
                elif 265 <= event.x <= 345 and 490 <= event.y <= 510:
                    canvas.itemconfigure(Info.uiList[Info.craft]['Num'], fill='white')  # 重设显示文本颜色
                elif 355 <= event.x <= 435 and 490 <= event.y <= 510:
                    canvas.itemconfigure(Info.uiList[Info.tank]['Num'], fill='white')  # 重设显示文本颜色
                elif 445 <= event.x <=550 and 490 <= event.y <= 510:
                    canvas.itemconfigure(Info.uiList[Info.plane]['Num'], fill='white')  # 重设显示文本颜色
                else:
                    for i in range(3,7):
                        canvas.itemconfigure(Info.uiList[i]['Num'], fill=Info.uiList[i]['color'])

            elif 200 <= event.x <= 450 and 520 <= event.y <= 565:#设置
                canvas.moveto(Info.uiList[Info.seting]['Num'], 200, 500)#
                for i in range(3,7):
                    canvas.moveto(Info.uiList[i]['Num'], -100, 490)#
                for i in range(7,10):
                    canvas.moveto(Info.uiList[i]['Num'], (200 + (i - 7) * 70), 540)
                    canvas.itemconfigure(Info.uiList[1]['Num'], fill='white')  # 重设显示文本颜色

                if 200 <= event.x <= 250 and 540 <= event.y <= 565:
                    canvas.itemconfigure(Info.uiList[Info.voice]['Num'], fill='white')  # 重设显示文本颜色
                elif 270 <= event.x <= 323 and 540 <= event.y <= 565:
                    canvas.itemconfigure(Info.uiList[Info.background]['Num'], fill='white')  # 重设显示文本颜色
                elif 340 <= event.x <= 450 and 540 <= event.y <= 565:
                    canvas.itemconfigure(Info.uiList[Info.backMusic]['Num'], fill='white')  # 重设显示文本颜色
                else:
                    for i in range(7,10):
                        canvas.itemconfigure(Info.uiList[i]['Num'], fill=Info.uiList[i]['color'])


            elif 200 <= event.x <= 360 and 570 <= event.y <= 610:
                canvas.itemconfigure(Info.uiList[2]['Num'], fill='white')  # 重设显示文本颜色

            else:
                music_start = False
                for i in Info.uiList:
                    canvas.itemconfigure(i['Num'],fill = i['color'])

                canvas.moveto(Info.uiList[Info.seting]['Num'], 200, 525)

                canvas.moveto(Info.uiList[Info.bean]['Num'], 200, 490)
                canvas.moveto(Info.uiList[Info.craft]['Num'], 265, 490)
                canvas.moveto(Info.uiList[Info.tank]['Num'], 355, 490)
                canvas.moveto(Info.uiList[Info.plane]['Num'], 445, 490)

                canvas.moveto(Info.uiList[Info.voice]['Num'], -100, 490)
                canvas.moveto(Info.uiList[Info.background]['Num'], -100, 490)
                canvas.moveto(Info.uiList[Info.backMusic]['Num'], -100, 490)
                return

            if music_start == False:
                ts = threading.Thread(target=Voice)
                ts.start()
                music_start = True

        def Menu2(self,event):
            voiceopera.HighLine(event)
            return

    class BGM():
        def __init__(self):
            self.BGM_list = ["treasure.mp3","Keil Generic Keygen.mp3","Dance.wav"]
            self.Num = int(time.time()%3)
            self.file = r"UI\\Music\\"+ self.BGM_list[self.Num]  # 音乐的路径
            self.stop = True
            self.change = False
            self.voice = 0.2

            pygame.mixer.init()  # 初始化
            pygame.mixer.music.set_volume(0.2)

        def BGM_start(self):
            while self.stop:
                if self.change:
                    pygame.mixer.music.stop()
                    self.change = False
                if not pygame.mixer.music.get_busy():
                    if self.Num >= 3:
                        self.Num = 0
                    self.file = r"UI\\Music\\" + self.BGM_list[self.Num]  # 音乐的路径
                    self.track_s = pygame.mixer.music.load(self.file)  # 加载音乐文件
                    pygame.mixer.music.play()  # 开始播放音乐流

        def BGM_change(self):
            self.Num += 1
            self.change = True

        def BGM_voice(self,voice):
            self.voice = voice
            pygame.mixer.music.pause()
            pygame.mixer.music.set_volume(self.voice)
            pygame.mixer.music.unpause()  # 开始播放音乐流

        def Get_voice(self):
            return self.voice

        def BGM_stop(self):
            self.stop = False
            pygame.mixer.music.stop()

    def setupMenu():
        Num_List = 0
        for i in Info.uiList:
            Info.uiList[Num_List]['Num'] = canvas.create_text(i['place_x'], i['place_y'], text = i['text'], font = i['fontInfo'], fill =  i['color'])
            canvas.moveto(Info.uiList[Num_List]['Num'], i['place_x'], i['place_y'])
            Num_List += 1

    def ChangeImg():
        global ImgNum
        ImgNum += 1
        if ImgNum == 4:
            ImgNum = 0
        canvas.itemconfigure(bakImg, image = bgList[ImgNum])

    class PIC():
        def __init__(self):
            Draw1 = canvas.create_image(200, 200, image=pic1,tag = 'draw')
            Draw2 = canvas.create_image(1100, 200, image=pic2,tag = 'draw')
            Draw3 = canvas.create_image(1100, 415, image=pic3,tag = 'draw')
            Draw4 = canvas.create_image(1100, 600, image=pic4,tag = 'draw')

        def PicShow(self,n):# True -> normal  False -> hidden
            if n:
                canvas.itemconfigure('draw',state = 'normal')
            else:
                canvas.itemconfigure('draw',state = 'hidden')


    root = Tk()  # 创建Tk控件
    root.geometry('1366x768+200+100')  # 设置窗口大小及位置
    root.title('GameBox')  # 设置窗口标题

    canvas = Canvas(root, highlightthickness=0)  # 创建Canvas控件，并设置边框厚度为0
    canvas.place(width=1366, height=768)  # 设置Canvas控件大小及位置

    bgList = [PhotoImage(file='UI/PIC/aa2.png'), PhotoImage(file='UI/PIC/1142727.png'),
              PhotoImage(file='UI/PIC/114.png'), PhotoImage(file='UI/PIC/1024.png')]

    pic1 = PhotoImage(file='UI/PIC/POwer (2).png')
    pic2 = PhotoImage(file='UI/PIC/R-C (1).png')
    pic3 = PhotoImage(file='UI/PIC/toner.png')
    pic4 = PhotoImage(file='UI/PIC/Dio1.png')


    bakImg = canvas.create_image(683, 384, image=bgList[ImgNum])  # 添加背景图片

    pic = PIC()
    bgm = BGM()
    voiceopera = voiceOpera()
    shubiaocaozuo = ShuBiaoKongZhi()
    setupMenu()

    vt1 = canvas.create_text(125, 275, text="Voice", font=('等线', 25, 'bold'), fill='grey', tags="vt1")
    vt2 = canvas.create_text(125, 175, text=" BGM", font=('等线', 25, 'bold'), fill='grey', tags="vt1")
    vt3 = canvas.create_text(583,500,  text="确定", font=('等线', 25, 'bold'), fill='grey', tags="vt1")
    vt4 = canvas.create_text(783,500,  text="取消", font=('等线', 25, 'bold'), fill='grey', tags="vt1")
    vr1 = canvas.create_rectangle(183, 150, 1183, 200, outline='grey', tags="vt1")
    vr2 = canvas.create_rectangle(183, 250, 1183, 300, outline='grey', tags="vt1")
    vr3 = canvas.create_rectangle(188, 255, 0, 295, fill='grey', outline='white', tags="vt1")
    vr4 = canvas.create_rectangle(188, 155, 0, 195, fill='grey', outline='white', tags="vt1")



    canvas.itemconfigure('vt1',state = 'hidden')

    canvas.bind('<Button-1>', lambda event: shubiaocaozuo.MenuKickChoose(event))  # 关联鼠标点击事件
    canvas.bind('<Motion>', lambda event: shubiaocaozuo.MenuChoose(event))  # 关联鼠标经过事件

    t_BGM = threading.Thread(target = bgm.BGM_start)
    t_BGM.start()

    root.mainloop()  # 窗口进入消息事件循环
    bgm.BGM_stop()

    return shubiaocaozuo.getReturnNum()