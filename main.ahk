DetectHiddenWindows,On
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


send_WM_COPYDATA(hwnd:=WinExist("pyPortal_GUI ahk_class AutoHotkeyGUI"), 0, "test2")
