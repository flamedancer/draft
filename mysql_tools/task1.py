from  sql_tool import *
# mysql config
db_config = {
    'host': 'rm-bp1e309j0mk9n0n08ro.mysql.rds.aliyuncs.com',
    'db': 'jiazb_test2',  # www
    'user': 'shendm',
    'passwd': 'Sdm@jiazb123',
    'charset': 'utf8mb4',
    'port': 3333,
}

init(db_config)


def run():
    now = datetime.datetime.now()
    aunt_info = select('t_user_aunt', ['id',  'skill'], {'role_id': 2})
    for id, skill in aunt_info: 
        need_up = 0
        if skill and '带小孩' in skill:
            skill += "|照顾小孩"
            need_up = 1
        if skill and '擦玻璃' in skill and '一般家务' not in skill:
            skill += "|一般家务"
            need_up = 1
        if need_up:
            update('t_user_aunt', {'id': id, 'skill': skill}, ['id'])
        result_info = select('t_address', ['latitude', 'longitude', 'city_id'], {'user_id': id, 'is_default': 'Y'})
        if not result_info:
            continue
        addr_info = result_info[0]
        print(addr_info)
                
          
        insert('t_aunt_service_type',
            {
                'aunt_id': id,
                'type': 'not-livein-nanny-multi',
                'state': 1,
                'latitude': addr_info[0],
                'longitude': addr_info[1],
                'add_time': now,
                'city_id': addr_info[2],
             }
        )



if __name__ == '__main__':
    run()


