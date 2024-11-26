import ctypes
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception as e:
        print(f"Error: {e}")
        return False

# Kind of same thing from registryedit.py
def edit_registry_value(value_name, new_value):
    try:
        # Open the registry key
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", 0, winreg.KEY_SET_VALUE)

        # Set the registry value
        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, new_value)

        # Close the registry key
        winreg.CloseKey(key)

        print(f"Registry value '{value_name}' updated successfully.")
    except Exception as e:
        print(f"Error updating registry value: {e}")

# Apparently if __name__ thing is good coding practice so that this can't be run in another script
if __name__ == "__main__":
    if is_admin():
        # If running with administrative privileges, edit the registry value
        value_name = "EnableLUA"
        new_value = 0  # Replace with the desired new value
        edit_registry_value(value_name, new_value)
    else:
        print("Cannot edit registry value. Run the script with administrative privileges.")
