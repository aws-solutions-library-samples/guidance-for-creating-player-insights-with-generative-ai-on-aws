
bulk_questions = [
    # 1. 下面是Sample QA对的例子
    {"question": "近14日，玩家的人均游戏场次，以及人均胜利场次？",
     "sql": '''
    SELECT
        ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT player_id), 2) AS avg_plays_per_player,
        ROUND(SUM(CASE WHEN level_result = 'pass' THEN 1 ELSE 0 END) * 1.0 / COUNT(DISTINCT player_id), 2) AS avg_wins_per_player
    FROM
        game_level_event
    WHERE
        create_at >= DATEADD(day, -14, CURRENT_DATE);
    '''}
]

for q in bulk_questions:
    # 2. 请修改profile_name和Data Profile name一致
    q['profile'] = '<profile_name>'

custom_bulk_questions = {
    'custom': bulk_questions
}