 #!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def resetTable(table_name): 
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    print 'DROP TABLE ' + str(table_name)
    try:
        c.execute("DROP TABLE " + str(table_name))
        DB.commit()
        DB.close()
        print 'Table ' + str(stable_name) + 'dropped with no errors'
    except:
        DB.close()
        print 'error'
    print 'dropped'

resetTable('matches')