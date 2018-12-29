import mysql.connector
import codecs

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="moviename"
)

mycursor = mydb.cursor()



file = codecs.open('dataimg.txt','r','utf-8')

a=file.readlines();

k=0;

for i in a:
	m=str(i)
	l=list(map(str,m.split()))
	name=l[0].replace('_',' ')
	print(k,name)	
	#mycursor.execute('insert into movies values(\''+name+'\');')
	print('insert into movies values(\''+name+'\')')
	sql = "INSERT INTO movies (name) VALUES (%(name)s)"
	val = {"name":name}
	print(val)
	mycursor.execute(sql, val)
	k+=1

mydb.commit()
'''
 
mycursor.execute("SELECT * FROM movies limit 5")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)
'''  