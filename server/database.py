import sqlite3,json,base64,uuid

class NoUserFound(Exception):
    pass

class UniqueUserConstrain(Exception):
    pass


class DB:
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        self.cur = self.conn.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS userAuth(username PRIMARY KEY,password)')
        self.cur.execute('CREATE TABLE IF NOT EXISTS usertableinfo(username PRIMARY KEY,table_number)')

    def getPass(self,username):
        self.cur.execute('SELECT password FROM userAuth where username = (?)',(username,))
        password = self.cur.fetchone()
        if password == None:
            raise NoUserFound ('User not registed')
        
        return password[0]

    def createUser(self,username,password):
        try:
            table_name = username + uuid.uuid4().hex
            self.cur.execute('INSERT INTO userAuth values(?,?)',(username,password))
            self.cur.execute('INSERT INTO usertableinfo values(?,?)',(username,table_name))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise UniqueUserConstrain
    
    def get_resources(self,username,date=None):
        usertable = sqlite3.connect("usertable.db")
        c = usertable.cursor()
        self.cur.execute('SELECT table_number FROM usertableinfo where username=(?)',(username,))
        table_name = self.cur.fetchone()[0]
        if date == None:
            c.execute('SELECT date FROM {}'.format(table_name))
            date = c.fetchall()
            print("=================================\n",date)
            dates =  [x[0] for x in date ]
            
            return dates
        elif date:
            c.execute('SELECT expenditure FROM (?) where date=(?)',(table_name,date))
            return c.fetchone()[0]
    
    def create_recource(self,username,date,expenditure):
        usertable = sqlite3.connect("usertable.db")
        c = usertable.cursor()
        self.cur.execute('SELECT table_number FROM usertableinfo where username=(?)',(username,))
        table_name = self.cur.fetchone()[0]
        c.execute("CREATE TABLE IF NOT EXISTS {}(date,expenditire)".format(table_name))
        insert =  "INSERT INTO {} values(?,?)".format(table_name)
        c.execute(insert,(date,expenditure))
        usertable.commit()





    
    def delete_resource(username,bill=None,month=None):
        pass

    # def update_resource(username)


    
    # def 

