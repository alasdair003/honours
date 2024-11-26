# wireg lets Python use the Windows registry API
import winreg

def read_registry_value(hive, subkey, value_name):
    try:
        # Open registry key
        key = winreg.OpenKey(hive, subkey)
        
        # Read registry value
        value, data_type = winreg.QueryValueEx(key, value_name)
        
        # Print the result
        print(f"{value_name}: {value} (Data Type: {data_type})")
        
        # Close the registry key
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error reading registry value: {e}")

# Specify the registry path and value name
hive = winreg.HKEY_LOCAL_MACHINE

# Set the desired value to EnableLUA
subkey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
value_name = "EnableLUA"

# Read the registry value
read_registry_value(hive, subkey, value_name)