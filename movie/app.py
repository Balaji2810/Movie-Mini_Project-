from flask import Flask ,render_template
from bs4 import BeautifulSoup
import re 
import requests
import codecs
import pandas as pd
import html
import mysql.connector




mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="moviename"
)

mycursor = mydb.cursor()




fdata = pd.read_csv(r'genlang.txt', sep=" ", header=None)
imgurl=  pd.read_csv(r'dataimg.txt', sep=" ", header=None)
data=pd.read_csv('tmdb.csv')




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
	f=imgurl[[0,4]][imgurl[0].isin(list)]
	s=f.values.tolist()
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

app = Flask(__name__)



@app.route('/')
def index():
	
	mlist=movielistimg()
	return render_template('home.html',movies=mlist)
	
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


@app.route('/movie/<string:name>/similar/<string:gen>')
def similar(name,gen):
	gen=gen.split('$')
	a=fdata[0][fdata[2].isin(gen)]
	a=a.unique()
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




app.run(debug=True)