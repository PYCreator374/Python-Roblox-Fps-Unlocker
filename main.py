import os
import json
import getpass
import psutil

# Get current user's folder path
current_user = getpass.getuser()
roblox_versions_path = rf'C:\Users\{current_user}\AppData\Local\Roblox\Versions'

# Function to find the Roblox version folder containing RobloxPlayerBeta.exe
def find_roblox_version():
    for version_folder in os.listdir(roblox_versions_path):
        version_path = os.path.join(roblox_versions_path, version_folder)
        if os.path.isdir(version_path):
            for file in os.listdir(version_path):
                if file.lower() == 'robloxplayerbeta.exe':
                    return version_path

    return None

# Function to modify FPS cap in ClientAppSettings.json
def modify_fps_cap(version_path, new_cap):
    client_settings_path = os.path.join(version_path, 'ClientSettings', 'ClientAppSettings.json')
    with open(client_settings_path, 'r+') as file:
        settings = json.load(file)
        settings["DFIntTaskSchedulerTargetFps"] = new_cap
        file.seek(0)
        json.dump(settings, file, indent=4)
        file.truncate()

# Function to check if Roblox is running
def is_roblox_running():
    for process in psutil.process_iter(['name']):
        if process.info['name'] == 'RobloxPlayerBeta.exe':
            return True
    return False

# User input for FPS cap
user_input = input("Enter FPS cap (or 'inf' for no cap): ")

# Check if user input is a valid integer or float
try:
    if user_input.lower() == 'inf':
        fps_cap = 5588562.0  # Set to specific value for no cap
    elif float(user_input) <= 5588562.0:
        fps_cap = int(user_input)
    elif float(user_input) >= 5588562.0:
        print("Roblox is unable to operate with a fps above 5588562.0")
except ValueError:
    print("Please do a number " + user_input + " Isnt a number")
    print("Doing 60 instead")
    fps_cap = 60

# Find Roblox version folder
roblox_version_folder = find_roblox_version()
if roblox_version_folder:
    # Apply FPS cap
    modify_fps_cap(roblox_version_folder, fps_cap)
    print("FPS cap set to:", fps_cap)

    # Check if Roblox is running
    if is_roblox_running():
        # Ask for permission to restart Roblox
        permission = input("Roblox needs to be restarted for changes to take effect. Restart now? (y/n): ")
        if permission.lower() == 'y':
            # Restart Roblox
            os.system("taskkill /f /im RobloxPlayerBeta.exe")
            print("Restarting Roblox")
            roblox_exe_path = os.path.join(roblox_version_folder, 'RobloxPlayerBeta.exe')
            os.startfile(roblox_exe_path)
            print("Roblox restarted.")
        else:
            print("Remember to restart Roblox for changes to take effect.")
else:
    print("Roblox version folder containing RobloxPlayerBeta.exe not found.")
