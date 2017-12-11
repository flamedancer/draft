import datetime
import subprocess

start = '2017-10-22'
end = '2016-09-18'

cmd = "spark-submit  --packages $MONGO_SPARK_CONNECTOR --master=spark://`hostname`:7077 `pwd`/src/welog/analyse/sem_kw.py {}"
cmd = "echo `hostname`{}"

def run():
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d') 
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d') 
    this_date = start_date
    while this_date >= end_date:
        this_date_str = str(this_date.date())
        now = datetime.datetime.now()
        print("start >>>>", this_date_str, str(now))
        subprocess.call(cmd.format(this_date_str) ,shell=True)
        
        print("end >>>> use time", (datetime.datetime.now() - now).total_seconds())
        this_date -= datetime.timedelta(days=1)
    

if __name__ == '__main__':
    run()
