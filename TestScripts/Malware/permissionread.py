# ctypes lets this mess with functions from C and to work with DLLs
# Need it for IsUserAnAdmin
import ctypes

# Keep this as function and display stuff later, might reuse
def is_admin():
    try:
        # Check if the script is running with admin perms
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

    except Exception as e:
        print(f"Error: {e}")
        return False

if is_admin():
    print("Running with administrative privileges.")
else:
    print("Not running with administrative privileges.")
