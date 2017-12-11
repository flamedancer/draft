import subprocess

def run(cmd):
    p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    p1.wait()
    # print type(p1.stdout)

    for line in p1.stdout:
        print line
    print 'returncode code:', p1.returncode

if __name__ == '__main__':
    # cmd = 'curl -f -F "file=@2.txt"  192.168.2.201:8040/upload_file_meta'
    cmd = """mysql -uguochen -p1111  -e "
        BEGIN;
            use www;
            insert into name (`name`) values ('gg3');
            insert into name (`name1`, `name2`) values ('gg1');
            show databases;
        COMMIT;"
    """
    cmd = """mysql -uguochen -p1111  -e "
            use www;
            insert into name (`name`) values ('gg3');
            insert into name (`name1`, `name2`) values ('gg1');
            show databases;
          "
    """

    # cmd = 'curl 127.0.0.1'
    run(cmd)
