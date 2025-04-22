import winreg

def read_registry_value(hive, subkey, value_name):
    try:
        # Open registry key
        key = winreg.OpenKey(hive, subkey)
        
        # Read registry value
        value, data_type = winreg.QueryValueEx(key, value_name)
        
        # Print the current value
        print(f"Current {value_name}: {value} (Data Type: {data_type})")
        
        # Close the registry key
        winreg.CloseKey(key)

        return value
    except Exception as e:
        print(f"Error reading registry value: {e}")
        return None

def write_registry_value(hive, subkey, value_name, value):
    try:
        # Open registry key with write access
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE)
        
        # Write registry value
        winreg.SetValueEx(key, value_name, 0, winreg.REG_DWORD, value)
        
        # Close the registry key
        winreg.CloseKey(key)

        # Errors here without running CMD as admin
        print(f"Updated {value_name} to: {value}")
    except Exception as e:
        print(f"Error writing registry value: {e}")


# Specify the registry path and value name
hive = winreg.HKEY_LOCAL_MACHINE
subkey = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
value_name = "EnableLUA"

# Read the current registry value
current_value = read_registry_value(hive, subkey, value_name)

# Toggle the value (0 to 1 or 1 to 0)
new_value = 1 if current_value == 0 else 0

# Write the updated value to the registry
# Erroring, need admin perms
write_registry_value(hive, subkey, value_name, new_value)

# Read the updated value
read_registry_value(hive, subkey, value_name)