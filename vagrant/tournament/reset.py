import psycopg2
import sys

def resetTable(table_name):
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    try:
        c.execute("DROP TABLE " + table_name)
        DB.commit()
        DB.close()
        print 'Table ' + str(table_name) + ' dropped with no errors'
    except:
        DB.close()
        print "Unexpected error:", sys.exc_info()

def deleteMatches():
    """Remove all the match records from the database."""
    resetTable('match_record')


def deletePlayers():
    """Remove all the player records from the database."""
    resetTable('players')
    
deletePlayers()
deleteMatches()