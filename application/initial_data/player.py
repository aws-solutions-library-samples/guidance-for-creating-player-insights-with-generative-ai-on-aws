import argparse
import pandas as pd
from tqdm import trange, tqdm
from datetime import datetime
import random

def create_sql(args):
    f = open(args.output,'w')

    sql = '''DROP TABLE IF EXISTS player;
CREATE TABLE player (
    player_id INT,  
    name VARCHAR(255),
    email VARCHAR(255),
    regist_date DATE,
    region VARCHAR(100),
    device_model VARCHAR(100),
    retain_day_local INT,
    active_day_local INT,
    passed_level INT,
    coin INT,
    energy INT
);
'''

    f.write(sql)

    # 地区列表
    regions = ['USA', 'Japan', 'China', 'UK', 'France']
    devices = ['samsung SM-T585','HUAWEI Meta50','lenovo Lenovo K12 Note','iPhone14,8','samsung SM-X200','HUAWEI MAR-LX1B','iPad13,19','motorola moto g stylus (2022)','samsung SM-A217F','iPhone10,1','OPPO CPH2343,''ZTE Z7540']
    retain_day = list(range(1, 180))
    active_day = list(range(1, 180))
    passwd_level = list(range(1, 199))
    coin = list(range(3000,99999))
    energy = list(range(500,9999))


    date_start = args.start
    date_end = args.end

    start_date = datetime.strptime(date_start, '%Y-%m-%d')
    end_date = datetime.strptime(date_end, '%Y-%m-%d')
    # 计算两个日期之间的天数差
    days_diff = (end_date - start_date).days
    rows = args.rows
    id_start = args.id_start

    player_id_list = list(range(id_start, id_start+rows))

    data = {
        'player_id':player_id_list,
        'name': ['Player' + str(i) for i in range(1, rows+1)],
        'email': [f"player{i}@example.com" for i in range(1, rows+1)],
        'regist_date': [pd.to_datetime(date_start) + pd.DateOffset(days=random.randint(0, days_diff+1)) for _ in range(rows)],
        'region': [random.choice(regions) for _ in range(rows)],
        'device_model': [random.choice(devices) for _ in range(rows)],
        'retain_day_local': [random.choice(retain_day) for _ in range(rows)],
        'active_day_local': [random.choice(active_day) for _ in range(rows)],
        'passed_level':[random.choice(passwd_level) for _ in range(rows)],
        'coin':[random.choice(coin) for _ in range(rows)],
        'energy':[random.choice(energy) for _ in range(rows)]
    }

    # 将数据转换为 Dataframe
    df = pd.DataFrame(data)

    print(df)

    for index, row in tqdm(df.iterrows()):
        sql = '''INSERT INTO player (player_id,name,email, regist_date, region, device_model, retain_day_local, active_day_local, passed_level, coin, energy) VALUES ({}, '{}', '{}', '{}', '{}', '{}', {}, {}, {}, {}, {});
'''.format(row['player_id'], row['name'], row['email'], str(row['regist_date']), row['region'],  row['device_model'], row['retain_day_local'],row['active_day_local'],  row['passed_level'], row['coin'], row['energy'])

        # print(sql)
        f.write(sql)

    f.close()


def init_args():
    parser = argparse.ArgumentParser(
        description="Create sample data for table player."
    )
    parser.add_argument(
        "--rows",
        "-r",
        type=int,
        default=10000,
        help="Row number of the sample data.",
    )

    parser.add_argument(
        "--start",
        "-s",
        type=str,
        default="2024-01-01",
        help="from data.",
    )

    parser.add_argument(
        "--end",
        "-e",
        type=str,
        default="2024-09-30",
        help="end data.",
    )

    parser.add_argument(
        "--id_start",
        "-i",
        type=int,
        default=100001,
        help="id start from.",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default='./player.sql',
        help="output sql file.",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = init_args()
    create_sql(args)

