import requests
import sqlite3 as sql
import xml.etree.ElementTree as ET

def import_data():
	#build DB
	setup_db()
	
	#URLs for govt data
	baseUrl = 'http://www.fueleconomy.gov/ws/rest/vehicle/menu/'
	makeUrl = "make?year="		#<year>
	modelUrl = "model?year="	#<year>&make=<make>
	engineUrl = "options?year="	#<year>&make=<make>&model=<model>
	
	#access avaliable years
	currUrl = baseUrl + 'year'
	
	#Fetch XML data
	ret = requests.get(currUrl)
	root = ET.fromstring(ret.content)
	
	for menuItem in root.findall('menuItem'):
		txt_year = menuItem.find('text').text
		
		#Access avaliable Makes by year
		response_make = requests.get(baseUrl + makeUrl + txt_year)
		root_make = ET.fromstring(response_make.content)
		
		for menuItem in root_make.findall('menuItem'):
			txt_make = menuItem.find('text').text
			
			#Access avaliable Models by make by year
			response_model = requests.get(baseUrl + modelUrl + txt_year + "&make=" + t2h(txt_make))
			root_model = ET.fromstring(response_model.content)
			
			for menuItem in root_model.findall('menuItem'):
				txt_model = menuItem.find ('text').text
				
				#Access avaliable Engines by model, by make, by year
				response_engine = requests.get(baseUrl + engineUrl + txt_year + "&make=" + t2h(txt_make) + "&model=" + t2h(txt_model))
				root_engine = ET.fromstring(response_engine.content)
				for menuItem in root_engine.findall('menuItem'):
					txt_engine = menuItem.find('text').text
					
					#Check if no gas Engine listed (in case of EV), replace w "Electric"
					if not txt_engine:
						txt_engine = "Electric"
					#Print Item recieved
					print (txt_year + " " + txt_make + " " + txt_model + " " + txt_engine)	
					#Write to DB
					add_entry(txt_year,txt_make,txt_model,txt_engine)
					
#text to http compatible
def t2h(string):
	return (string.replace(' ', "%20"))

#Write to database
def add_entry(year, make, model, engine):
	#Connect to DB
	con = sql.connect("base_car.db")
	cur=con.cursor()

	#insert values into DB, Ignore Duplicates
	cur.execute("INSERT OR IGNORE INTO Menu (Year, Make, Model, Engine) VALUES(?,?,?,?)",(year,make,model,engine) )
	try :
		con.commit()
	except sql.Error:
		print (txt_year + " " + txt_make + " " + txt_model + " " + txt_engine + "failed")

	con.close()

#setup Database
def setup_db():
	con = sql.connect("base_car.db")
	
	con.execute('CREATE TABLE Menu (Year INT, Make CHAR(50), Model CHAR(50), Engine CHAR(50), PRIMARY KEY(Year, Make, Model, Engine))')
	con.close()

#Run as main if appliciable
if __name__ == '__main__':
	import_data()

