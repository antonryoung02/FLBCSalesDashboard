import os
import platform

#Deployment device (windows) and development device (apple)
#Paths are hardcoded to reflect location for each
if platform.system() == "Windows":
    DATE_FILE_MONTH_FORMAT = "%#m"
    BASE_DIR_PATH = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "FLBC 1.1.1", "Revenue and menu engineering data")
else:
    DATE_FILE_MONTH_FORMAT = "%-m"
    BASE_DIR_PATH = "/Users/antonyoung/Code/FLBCSalesDashboard/"

CONFIG_SHEET_NAME = "CONFIG"
DATA_FILENAME = "MENU ENGINEERING FLBC PBHS and CELLAR.xlsx"
