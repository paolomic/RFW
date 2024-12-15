import sqlite3
import time

def leggi_db(db_path):
    try:
        #mode=ro&immutable=1
        conn = sqlite3.connect(f'file:{db_path}?immutable=1', uri=True)
        cursor = conn.cursor()
        conn.execute('PRAGMA journal_mode=WAL')
        print("open ok")
        #conn.execute("insert into TESTT values(2)")

        #cursor.execute("SELECT COUNT(*) FROM FT_C_SECURITY_LIST")
        cursor.execute("SELECT COUNT(*) FROM TESTT where a < 2")
        print (cursor.fetchone()[0]) 
    
    except sqlite3.OperationalError:
        print("Database ERROR")
        return None

# Uso periodico
risultato = leggi_db('D:\\wsp_c\\127_28000_REM.wsp4_wrk\\DB\\MetaMarketDICT.db3')
