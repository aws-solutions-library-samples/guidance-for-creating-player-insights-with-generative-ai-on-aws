import argparse
import pandas as pd
from tqdm import trange, tqdm
from datetime import datetime
import random
import random
import uuid

def create_sql(args):
    f = open(args.output,'w')

    sql = '''DROP TABLE IF EXISTS payment;
CREATE TABLE payment (
    payment_id VARCHAR(255),
    player_id INT ,
    product_id VARCHAR(255),
    product_count INT,
    price_usd double precision,
    status INT,
    create_at  timestamp without time zone,
    update_at  timestamp without time zone
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
    product_type = ['coin_100', 'coin_300', 'coin_500', 'diamond_1', 'diamond_5','diamond_10']
    product_count = list(range(1,5))
    price_usd = ['11.99', '1.99', '54.99', '11.99', '7.99', '54.99', '0.99', '19.99', '19.99', '1.99', '1.99', '14.99', '1.99', '99.99', '29.99', '1.99', '0.99', '1.99', '14.99', '7.99', '11.99', '0.99', '0.99', '1.99']
    status = [0,1,2]



    data = {
        'payment_id':[str(uuid.uuid4())[:8] + str(uuid.uuid4())[:8] for _ in range(rows)],
        'player_id':[random.choice(player_id_list) for _ in range(rows)],
        'product_id': [random.choice(product_type) for _ in range(rows)],
        'product_count': [random.choice(product_count) for _ in range(rows)],
        'price_usd': [random.choice(price_usd) for _ in range(rows)],
        'status': [random.choice(status) for _ in range(rows)],
        'create_at': [pd.to_datetime(date_start) + pd.DateOffset(days=random.randint(0, days_diff+1)) for _ in range(rows)],
        'update_at': [pd.to_datetime(date_start) + pd.DateOffset(days=random.randint(0, days_diff+1)) for _ in range(rows)]
    }

    # 将数据转换为 Dataframe
    df = pd.DataFrame(data)
    df['update_at'] = df['create_at']

    print(df)

    for index, row in tqdm(df.iterrows()):
        sql = '''INSERT INTO payment ( payment_id, player_id, product_id, product_count, price_usd, status, create_at, update_at) VALUES ({}, {}, {}, {}, {}, {}, {}, {});
'''.format(row['payment_id'], row['player_id'], row['product_id'], row['product_count'], row['price_usd'],  row['status'], str(row['create_at']),str(row['update_at']))
        f.write(sql)
    f.close()


def init_args():
    parser = argparse.ArgumentParser(
        description="Create sample data for table payment."
    )
    parser.add_argument(
        "--rows",
        "-r",
        type=int,
        default=8000,
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
        default='./payment.sql',
        help="output sql file.",
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = init_args()
    create_sql(args)
