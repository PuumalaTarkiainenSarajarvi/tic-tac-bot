import mysql.connector

mydb = mysql.connector.connect(
    host=" ",
    user=" ",
    passwd=" "
)

mycursor = mydb.cursor()
mycursor.execute("USE tictacbot")

def limitListSize():

    sql = ('SELECT nickname, win_time FROM high_score '
           'JOIN session_memory '
           'ON session_memory.session_memory_id = high_score.session_memory_id '
           'WHERE high_score.session_memory_id = 1 '
           'ORDER BY win_time ASC')
    
    mycursor.execute(sql)
    result = mycursor.fetchall()
    
    if len(result) > 10:
        sql = ('SET SQL_SAFE_UPDATES = 0')
        mycursor.execute(sql)

        sql = ('DELETE h FROM high_score h JOIN '
               '(SELECT max(win_time) AS max_win_time FROM high_score) x '
               'ON h.win_time = x.max_win_time')
        
        mycursor.execute(sql)

        mydb.commit()

def getHighScores():

    limitListSize()

    sql = ('SELECT nickname, win_time FROM high_score '
           'JOIN session_memory '
           'ON session_memory.session_memory_id = high_score.session_memory_id '
           'WHERE high_score.session_memory_id = 1 '
           'ORDER BY win_time ASC')
    
    mycursor.execute(sql)
    result = mycursor.fetchall()

    for x in result:
        print(x)

    print(len(result))

    return result

def insertHighScore(name, time):

    sql = ('INSERT INTO high_score(session_memory_id, nickname, win_time) '
           'VALUES(1, %s, %s)')
    
    val = (name, time) 
    
    mycursor.execute(sql, val)
    print(mycursor.lastrowid)

    mydb.commit()

    limitListSize()

#insertHighScore("TESTAUS2", 16)
#getHighScores()
