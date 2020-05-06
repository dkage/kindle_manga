import subprocess
from defines import *
from functions.misc import check_os_for_kindlegen


kindlegen_absolute_path = PROJECT_DIR + '/assets/libs/./' + check_os_for_kindlegen()

a = 'test'
a = subprocess.check_output(kindlegen_absolute_path).decode()

print(a)
