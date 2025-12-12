import sqlite3
import os

db_path = 'sql_app.db'
if not os.path.exists(db_path):
    print('Database does not exist yet - will be created on first run')
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print('=== DATABASE SCHEMA ===')
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f'\nTable: {table_name}')
        cursor.execute(f'PRAGMA table_info({table_name})')
        columns = cursor.fetchall()
        for col in columns:
            print(f'  - {col[1]} ({col[2]})')
        
        cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
        count = cursor.fetchone()[0]
        print(f'  Records: {count}')
    
    print('\n=== DATA INTEGRITY CHECK ===')
    # Check for orphaned chats
    cursor.execute('SELECT COUNT(*) FROM chats')
    total_chats = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM chats WHERE user_id NOT IN (SELECT id FROM users)')
    orphaned_chats = cursor.fetchone()[0]
    
    print(f'Total chats: {total_chats}')
    print(f'Orphaned chats (no user): {orphaned_chats}')
    
    if total_chats > 0:
        print('\n=== SAMPLE CHAT RECORDS ===')
        cursor.execute('SELECT c.id, c.user_id, c.input_text, c.timestamp, u.email FROM chats c LEFT JOIN users u ON c.user_id = u.id LIMIT 5')
        for row in cursor.fetchall():
            print(f'Chat ID: {row[0]}, User ID: {row[1]}, User Email: {row[4]}, Timestamp: {row[3]}')
            print(f'  Input: {row[2][:50]}...')
    
    conn.close()
