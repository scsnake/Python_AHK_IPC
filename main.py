import os, sys
import ctypes
from time import sleep
import queue
import ahk
import threading
import json

def check_ahk():
    global queue_ind, queue_max
    q = ahk.get('q'+str(queue_ind+1))


    if q!='':

        print(q, queue_ind)

        try:
            js=json.loads(q)
            threading.Thread(target=parse_msg, args=[js]).start()
        except:
            pass
        finally:
            ahk.execute('q{}:=""'.format(queue_ind+1))
            queue_ind= (queue_ind+1) % queue_max

    threading.Timer(1.0, check_ahk).start()

def parse_msg(js):
    print(js)


ahk.start()  # Ititializes a new script thread
ahk.ready()  # Waits until status is True

txt='''
Send_WM_COPYDATA(Hwnd, dwData, lpData="") {
; dwData = Command
; cbData = String lenght
; lpData = String
	static WM_COPYDATA := 0x4A
	VarSetCapacity(COPYDATASTRUCT, 3*A_PtrSize, 0)
		,cbData := (StrLen(lpData) + 1) * (A_IsUnicode ? 2 : 1)
		,NumPut(dwData,  COPYDATASTRUCT, 0*A_PtrSize)
		,NumPut(cbData,  COPYDATASTRUCT, 1*A_PtrSize)
		,NumPut(&lpData, COPYDATASTRUCT, 2*A_PtrSize)
	
	SendMessage, WM_COPYDATA, 0, &COPYDATASTRUCT,, ahk_id %Hwnd%
	return ErrorLevel == "FAIL" ? false : true
}


On_WM_COPYDATA(wParam, lParam, msg, hwnd) {
; dwData = Command
; cbData = String lenght
; lpData = String
	global q
	dwData := NumGet(lParam+0, 0)
	,cbData := NumGet(lParam + A_PtrSize)
	,lpData := NumGet(lParam + 2*A_PtrSize)
	,str := StrGet(lpData)
	,put(str)
}

put(e){
	global
	if(++i>100)
		i:=1
	q%i%:=e
}

#Persistent
gui,Show,x-1 y-1 w1 h1 NA,pyPortal_GUI
OnMessage(0x4a, "On_WM_COPYDATA")

i:=0
,n:=1000

settimer,debug,50
return
debug:
tooltip % q%i% "," i 
return
'''

ahk.execute(txt)

queue_ind = 0
queue_max = 1000
threading.Timer(1.0, check_ahk).start()


while 1:
    sleep(1)
