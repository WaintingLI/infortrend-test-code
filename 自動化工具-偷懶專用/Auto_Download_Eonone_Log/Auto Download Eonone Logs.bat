chcp 65001

set /p scaleout_input=Please enter Eonone IP value (Ex: 172.24.128.150):

python auto_download_eonone_logs.py --ip %scaleout_input% 


pause