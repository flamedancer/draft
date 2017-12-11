from ConfigParser import  ConfigParser
import subprocess
import sys
import re
import tempfile

temp = tempfile.TemporaryFile()

try:

    output = subprocess.check_output("ssh root@192.168.2.204 'cat /root/code/settings/.git/config'", shell=True)
except subprocess.CalledProcessError as e:
    print e.message
    sys.exit(1)

#giturl = ''
#for line in output.split('\n'):
#    line = line.strip()
#    if line.startswith('url'):
#        _, giturl = line.split('=', 1)
#        giturl = giturl.strip()
#        break

temp.write(output)
temp.seek(0)

cp = ConfigParser().read('../csnow/.git/config')



temp.close()



print(cp)
