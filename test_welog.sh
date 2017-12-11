start="2017-10-22"
end="2016-09-18"

delta="0"
this_day=$(date -d "-${delta} days" '+%Y-%m-%d')
while [ "${this_day}" != "${end}" ]; do
    echo ${this_day} 
    # spark-submit  --packages $MONGO_SPARK_CONNECTOR --master=spark://`hostname`:7077 `pwd`/src/welog/analyse/sem_kw.py ${this_day} 
    delta=$(($delta + 1))
    this_day=$(date -d "-${delta} days" '+%Y-%m-%d')
done

    
