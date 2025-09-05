chcp 65001

set /p reason_for_overtime=Please enter Reason for overtime (Ex: AI(Phase2.5)(PVR Verify)):

python Apply_for_overtime_pay.py --reason "%reason_for_overtime%"


pause