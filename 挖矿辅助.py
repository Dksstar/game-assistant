import cv2
import numpy 
import win32gui, win32ui, win32con,win32api
from win32con import KEYEVENTF_KEYUP
import time
import random

def jieping():
    #获取后台窗口的句柄，注意后台窗口不能最小化
    hWnd = win32gui.FindWindow(0,'辉煌') #窗口的类名
    #获取句柄窗口的大小信息
    left, top, right, bottom = win32gui.GetWindowRect(hWnd)
    width = right - left
    height = bottom - top
    #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    #创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    #创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    #创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
    #获取位图信息
    bmpInfo =saveBitMap.GetInfo()
    img = numpy.frombuffer(saveBitMap.GetBitmapBits(True), dtype = numpy.uint8)
    #内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd,hWndDC)
    #图片格式转换
    img=img.reshape(bmpInfo['bmHeight'], bmpInfo['bmWidth'], 4)
    return img
    
def 更换锄头():
    templ = cv2.imread(r"D:\rxcq\chutou.bmp")
    height, width, c = templ.shape
    #按照标准相关系数匹配
    res = cv2.matchTemplate(img, templ, cv2.TM_CCOEFF_NORMED)
    thresthold=0.9
    loc = numpy.where(res >= thresthold)
    if len(loc[0])!=0:
        print('有锄头！')
    else: 
        print('没有锄头!')
        temp1_bb = cv2.imread(r"D:\rxcq\chutou_bb.bmp")
        height, width, c = temp1_bb.shape
        #按照标准相关系数匹配
        res = cv2.matchTemplate(img, temp1_bb, cv2.TM_CCOEFF_NORMED)
        thresthold=0.7
        loc = numpy.where(res >= thresthold)
        for pt in zip(*loc[::-1]): 
            right_bottom = (pt[0] + width, pt[1] + height)
            cv2.rectangle(img, pt, right_bottom, (0, 255, 0), 1) #所有匹配的物品逐个画框
            time.sleep(random.uniform(1,3)) 
            #鼠标移动到制定坐标（瞬移位置）
            win32api.SetCursorPos(pt)
            
            time.sleep(random.uniform(1,3)) 
            #背包中找到锄头，双击更换锄头
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            break
        print('锄头更换完毕！')    

def 矿石比对(pic):
    #templ = cv2.imread(r"D:\rxcq\" + pic +".bmp") #斜杠有误
    templ = cv2.imread("D:/rxcq/" + pic +".bmp")
    height, width, c = templ.shape
    #按照标准相关系数匹配
    res = cv2.matchTemplate(img, templ, cv2.TM_CCOEFF_NORMED)
    thresthold=0.9
    loc = numpy.where(res >= thresthold)
    unused.extend(zip(*loc[::-1]))

def 丢弃矿石(x,y):
    #丢弃矿石命令
    time.sleep(random.uniform(1,3)) 
    win32api.SetCursorPos((x,y))  #可以加上偏移
    time.sleep(random.uniform(1,3)) 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    time.sleep(random.uniform(1,3)) 
    win32api.SetCursorPos((433,155))
    time.sleep(random.uniform(1,3))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
img = jieping()  
img = numpy.array(img)
img=cv2.cvtColor(img,cv2.COLOR_BGRA2BGR)
更换锄头()
unused =[]  #废矿总表

矿石比对("tiekuang")
矿石比对("tongkuang")
矿石比对("yinkuang")
random.shuffle(unused)  #打乱顺序

for x, y in unused: 
    #cv2.rectangle(img, (x,y),(x+25,y+25), (0, 255, 0), 1) #所有匹配的物品逐个画框
    丢弃矿石(x,y)
    #break

#cv2.imshow("img", img)
#cv2.waitKey()
#cv2.destroyAllWindows()








    

