import sqlite3
from datetime import datetime
import os

END_TIME = datetime.fromisoformat('2024-10-19T12:00:00')
END_UID_LIMIT = 2800

# 创建并连接到SQLite数据库（如果数据库不存在会自动创建）
def create_db():
    # 数据库文件名为 your_database.db
    db_directory = 'db'
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)

    connection = sqlite3.connect('db/llm.db')
    
    # 获取游标对象，用来执行SQL语句
    cursor = connection.cursor()

    # 创建表结构
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_question_limit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid INTEGER NOT NULL,
        date TEXT NOT NULL,  
        question_count INTEGER DEFAULT 0,
        UNIQUE(uid, date)  
    )
    ''')

    # 提交事务并关闭连接
    connection.commit()
    connection.close()

# 数据库连接配置
def get_db_connection():
    connection = sqlite3.connect('db/llm.db')
    connection.row_factory = sqlite3.Row  # 返回字典样式的行
    return connection

# 检查和更新用户的提问次数
def check_and_update_question_count(uid, limit):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        if datetime.today() > END_TIME:
            if uid > END_UID_LIMIT:
                return False, 0
            today = 'game_end'
        else:
            today = datetime.today().strftime('%Y-%m-%d') 

        # 查询今天该uid的提问次数
        cursor.execute("SELECT question_count FROM user_question_limit WHERE uid=? AND date=?", (uid, today))
        result = cursor.fetchone()

        if result:
            question_count = result['question_count']
            if question_count >= limit:
                return False, 0
            else:
                # 更新提问次数
                cursor.execute("UPDATE user_question_limit SET question_count = question_count + 1 WHERE uid=? AND date=?", (uid, today))
        else:
            question_count = 0
            # 没有记录，插入新数据
            cursor.execute("INSERT INTO user_question_limit (uid, date, question_count) VALUES (?, ?, ?)", (uid, today, 1))

        connection.commit()
        return True, limit - (question_count+1)
    finally:
        connection.close()

