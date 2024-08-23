import argparse
import pandas as pd
from tqdm import trange, tqdm
from datetime import datetime
import random
import random
import uuid

def create_sql(args):
    f = open(args.output,'w')

    sql = '''DROP TABLE IF EXISTS game_level_event;
CREATE TABLE game_level_event (
    event_id VARCHAR(255), 
    player_id INT,
    create_at  timestamp without time zone,
    device_os VARCHAR(255),
    device_screen_resolution VARCHAR(255),
    language VARCHAR(255),
    country VARCHAR(255),
    level_count int,
    level_play_time int,
    level_result VARCHAR(255),
    total_step int,
    pre_coin int,
    left_coin int
);
'''

    f.write(sql)


    date_start = args.start
    date_end = args.end

    start_date = datetime.strptime(date_start, '%Y-%m-%d')
    end_date = datetime.strptime(date_end, '%Y-%m-%d')
    # 计算两个日期之间的天数差
    days_diff = (end_date - start_date).days
    rows = args.rows
    id_start = args.id_start

    player_id_list = list(range(id_start, id_start+rows))

    device_os = ['Android OS 14 / API-34 (UP1A.231005.007/S901BXXS7DWL1)', 'Android OS 13 / API-33 (TP1A.220624.014/A037MUBS5CWH1)', 'Android OS 12 / API-31 (SP1A.210812.016/S.1431865-111f8)', 'iOS 16.7.2', 'iOS 17.1.2', 'Android OS 7.0 / API-24 (HUAWEIBTV-L0J/C137B365)', 'Android OS 12 / API-31 (SP1A.210812.016/A025FXXU6CWE2)', 'Android OS 13 / API-33 (TP1A.220624.014/A145RXXS4AWK6)', 'Android OS 12 / API-31 (SP1A.210812.016/20231117.201803)', 'iOS 16.7.4', 'Android OS 11 / API-30 (RP1A.201005.001/1701398769000)', 'Android OS 11 / API-30 (RP1A.200720.011/1616571340)']
    device_screen_resolution = ['1080 x 2340 @ 120Hz', '720 x 1600 @ 60Hz', '720 x 1612 @ 60Hz', '750 x 1334 @ 60Hz', '1170 x 2532 @ 60Hz', '1600 x 2560 @ 60Hz', '1080 x 2408 @ 60Hz', '720 x 1600 @ 90Hz', '1284 x 2778 @ 60Hz', '800 x 1280 @ 60Hz']
    language = ['German', 'Spanish', 'English', 'Japanese', 'French', 'Russian']
    country = ['DE', 'EC', 'MX', 'US', 'JP', 'FR', 'RU', 'TH', 'CA']
    level_count = list(range(1,200))
    level_play_time = list(range(6,300))
    level_result = ['fail','pass','quit']
    total_step = list(range(6,300))
    pre_coin = list(range(10,300))
    left_coin = list(range(0,100))

    data = {
        'event_id':[str(uuid.uuid4())[:8] + str(uuid.uuid4())[:8] for _ in range(rows)],
        'player_id':[random.choice(player_id_list) for _ in range(rows)],
        'create_at': [pd.to_datetime(date_start) + pd.DateOffset(days=random.randint(0, days_diff +1)) for _ in range(rows)],
        'device_os': [random.choice(device_os) for _ in range(rows)],
        'device_screen_resolution': [random.choice(device_screen_resolution) for _ in range(rows)],
        'language': [random.choice(language) for _ in range(rows)],
        'country': [random.choice(country) for _ in range(rows)],
        'level_count': [random.choice(level_count) for _ in range(rows)],
        'level_play_time': [random.choice(level_play_time) for _ in range(rows)],
        'level_result': [random.choice(level_result) for _ in range(rows)],
        'total_step': [random.choice(total_step) for _ in range(rows)],
        'pre_coin': [random.choice(pre_coin) for _ in range(rows)],
        'left_coin': [random.choice(left_coin) for _ in range(rows)],
    }

    # 将数据转换为 Dataframe
    df = pd.DataFrame(data)

    print(df)

    for index, row in tqdm(df.iterrows()):
        sql = '''INSERT INTO game_level_event ( event_id , player_id, create_at, device_os, device_screen_resolution, language, country, level_count, level_play_time, level_result, total_step, pre_coin, left_coin) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});
'''.format(row['event_id'], row['player_id'],  str(row['create_at']), row['device_os'], row['device_screen_resolution'], row['language'],  row['country'],row['level_count'], row['level_play_time'], row['level_result'], row['total_step'],  row['pre_coin'],row['left_coin'])
        f.write(sql)

    f.close()


def init_args():
    parser = argparse.ArgumentParser(
        description="Create sample data for table game_level_event."
    )
    parser.add_argument(
        "--rows",
        "-r",
        type=int,
        default=30000,
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
        default='./game_level_event.sql',
        help="output sql file.",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = init_args()
    create_sql(args)
