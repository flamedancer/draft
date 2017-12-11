import subprocess

def run(cmd):
    p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p1.wait()
    # print type(p1.stdout)

    for line in p1.stdout:
        print line
    print 'returncode code:', p1.returncode

if __name__ == '__main__':
    cmd = 'mysql -uguochen -p1111 -e "select sleep(3)";'
    cmd = 'lls -la'
    run(cmd)
