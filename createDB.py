import sqlite3
def createDB():
    #book store
    con=sqlite3.connect(database=r'bookInventory.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS inventory(store_name text, book_type text, email text, password text, contact_no text, address text, state text, city text, pin int)")
    con.commit()
#book details 
    #con=sqlite3.connect(database=r'bookRecord.db')
    #cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS bookRecordInventory(book_id, book_title, email, dept, subject, quantity)")
    #con.commit()
createDB()
