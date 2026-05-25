import sqlite3
from datetime import date


db_name = r"D:\Timer\Timer_data.db"


#Creates the database and tables if they don't exist.
def init_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_process TEXT,
            available_time INTEGER,
            gone_time INTEGER,
            date TEXT)''')

    cursor.execute('''SELECT COUNT(*) FROM tracker''')
    if cursor.fetchone()[0] == 0:
        today = date.today().isoformat()
        cursor.execute('''INSERT INTO tracker (target_process, available_time, gone_time, date)
                       VALUES ('', 0, 0, ?)''', (today,))
    
    conn.commit()
    conn.close()


#Retrieves the current settings from the database.
def get_data():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM tracker''')
    data = cursor.fetchall()
    conn.close()

    all_data = []
    for row in data:
        all_data.append({
            "target_process": row[1],
            "available_time": row[2],
            "gone_time": row[3],
            "date": row[4]
        })

    return all_data


#Updates the rules from the GUI.
def update_setting(target_process, available_time):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO tracker (target_process, available_time, gone_time, date)
                      VALUES (?, ?, 0, ?)''', (target_process, available_time, date.today().isoformat()))
    conn.commit()
    conn.close()


#Updates the daily used time and checks the current date.
def update_usage(gone_time, today_date, target_process):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''UPDATE tracker 
                      SET gone_time = ?, date = ? 
                      WHERE target_process = ?''', (gone_time, today_date, target_process))
    conn.commit()
    conn.close()

#Clears the database when the user clicks the clear button in the GUI. This will delete all entries and reset the auto-incrementing ID.
def clear_settings():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM tracker''')
    cursor.execute('''DELETE FROM sqlite_sequence WHERE name='tracker' ''')
    conn.commit()
    conn.close()

#Removes the process from the database when the user clicks the clear button in the GUI. This will delete the entry for the specific process and reset the auto-incrementing ID.
def clear_process(target_process):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM tracker WHERE target_process = ?''', (target_process,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()