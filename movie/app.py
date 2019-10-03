from flask import Flask ,render_template
from bs4 import BeautifulSoup
import re 
import requests
import codecs
import pandas as pd
import html
import mysql.connector #pip install mysql-connector-python



#pip install mysql-connector-python
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="moviename"
)

mycursor = mydb.cursor()




fdata = pd.read_csv(r'genlang.txt', sep=" ", header=None)
imgurl=  pd.read_csv(r'dataimgn.txt', sep=" ", header=None)
data=pd.read_csv('tmdb.csv')
sim=pd.read_csv("t2.csv")



def cleanupString(string):
    string = urllib2.unquote(string).decode('utf8')
    return HTMLParser.HTMLParser().unescape(string).encode(sys.getfilesystemencoding())

def plot(url):
	
	a=requests.get(url)
	html=a.text
	c=html.find('<h2><span class="mw-headline" id="Plot">')
	if(c!=-1):
		temp=html[c+4:]
		c=temp.find('<h2>')
		temp=temp[:c]
		c=temp.find('<p>')
		temp=temp[c:]
		plot=temp
	else:
		plot='not found'
	s=plot
	s= re.sub(r'<(.|\n)*?>', '', s)
	replaced = re.sub(r'&#91;\d&#93;', '', s)
	return replaced

def movielistimg():
	l=[]
	fr = codecs.open('dataimg.txt','r','utf-8')
	for i in range(4792):
		a=fr.readline().split()
		l.append(a)
	return l
def imgbyname(list):
	#f=imgurl[[0,4]][imgurl[0].isin(list)]
	f=imgurl[[0,4]]
	list=pd.DataFrame(list)
	list.columns=['movie']
	f.columns=['movie','url']
	#print(list.head(10))
	#print(f.head(10))
	fs=pd.merge(list,f,on='movie',how='inner')
	#print(fs.head(10))
	s=fs.values.tolist()
	return s

def moviebygen(name):
		a=fdata[0][fdata[2]==name]
		a=a.unique()
		b=imgbyname(a)
		return b

def moviebylang(name):
		a=fdata[0][fdata[1]==name]
		a=a.unique()
		b=imgbyname(a)
		return b


def movieinfo(name):
	
	a=imgurl[[2,3,4]][imgurl[0]==name]
	for i in a[3]:
		u1=i
	for i in a[4]:
		u2=i
	for i in a[2]:
		gen=i.split('@')
	b=fdata[1][fdata[0]==name]
	lg=[]
	for i in b:
		if i not in lg:
			lg.append(i)
	
	gen.remove('')
	plt=plot(u1)
	img=u2
	# name, img, plot, gen, lang,
	return [name,img,plt,gen,lg]

def srt(s):
  return s[1]
def simmovie(name):
  #s2=sim.fillna(0)  
  s=sim[name].sum()
  d=[]
  for i in sim.columns[1:]:
    sm=(sim[name]*sim[i]).sum()/s
    d.append([i.replace(' ','_'),sm])
  d=sorted(d,key=srt,reverse=True)
  d= [item for sublist in d for item in sublist]
  #k=d.find(0)
  #for i in d[:19:2]:
  # print(i)
  return d[::2]



app = Flask(__name__)



@app.route('/')
def index():
	
	mlist=movielistimg()
	return render_template('home.html',movies=mlist,test="Balaji")
	
@app.route('/movie/<string:name>/')
def info(name):
	infomovie=movieinfo(name)
	return render_template('movieinfo.html',list=infomovie)


@app.route('/genre/<string:name>/')
def gen(name):
	mlist=moviebygen(name)
	return render_template('home.html',movies=mlist)

@app.route('/lang/<string:name>/')
def lang(name):
	mlist=moviebylang(name)
	return render_template('home.html',movies=mlist)


@app.route('/movie/<string:name>/similar/')
def similar(name):
	name=name.replace('_',' ')
	a=simmovie(name)
	#a=a.unique()
	b=imgbyname(a)
	
	
	
	return render_template('home.html',movies=b)

@app.route('/searchbox/<string:name>')
def searchbox(name):
	mycursor.execute("SELECT * FROM movies where name like '"+name+"%' limit 5")
	myresult = mycursor.fetchall()
	d=[]
	for i in myresult:
		d.append(''.join(i))
	
		
	
	return render_template('search.html',nm=d)

@app.route('/test')
def test():
	n=[['apple','car','bike'],'orange','banana','mango']
	return render_template('test.html',name=n)


app.run(debug=True,host='0.0.0.0',port='5000')