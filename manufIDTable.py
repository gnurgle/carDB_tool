import sqlite3 as sql
import requests
import json
from fuzzywuzzy import process

def buildManfId():
	#connect to to DB
	con = sql.connect("base_car.db")
	con.row_factory = sql.Row
	con.text_factory = str
	cur = con.cursor()

	#Do create table here
	cur.execute("SELECT DISTINCT Make FROM Menu ORDER BY Make")

	rows = cur.fetchall()
	rowTxt = [rows[0][0]]

	for i in range(len(rows)):
		print(rows[i][0])
		rowTxt.append(rows[i][0])

	url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetMakesForVehicleType/car?format=json"
	r = requests.get(url)
	response = json.loads(r.content.decode())
	results = [response['Results'][0]['MakeName']]
	for i in range (1,response['Count'],1):
		results.append(response['Results'][i]['MakeName'])
	
	nhtsaList = results

	resMakeId = [response['Results'][0]['MakeId']]
	for i in range (1,response['Count'],1):
		resMakeId.append(response['Results'][i]['MakeId'])
	
	

	for i in range(len(rowTxt)):
		matchResult = (process.extractOne(nhtsaList[i], rowTxt, score_cutoff = 90))
		if not matchResult:
			print ("No Match found for " + nhtsaList[i])
		else:
			print (matchResult) 
			print ("for " + nhtsaList[i])
			print (matchResult[0])
			for j in range(len(rowTxt)):
				if rowTxt[j] == matchResult[0]:
					cur.execute("INSERT OR IGNORE INTO Manf (Make, MakeID) VALUES(?,?)",(rowTxt[j],resMakeId[i]))
					con.commit()
					print (rowTxt[j] + " is ID# " + str(resMakeId[i]))

def buildMakeId():

	#connect to to DB
	con = sql.connect("base_car.db")
	con.row_factory = sql.Row
	con.text_factory = str
	cur = con.cursor()

	cur.execute("SELECT Make,MakeId FROM Manf")
	rows = cur.fetchall()
	rowCheck = []
	for i in range(len(rows)):
		print(rows[i][0] + str(rows[i][1]))
		rowCheck.append([rows[i][0]])
	for i in range(len(rows)):
		print(rows[i][0] + str(rows[i][1]))
		rowCheck[i].append([rows[i][1]])

	for m in range(len(rows)):
		url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMakeId/" + str(*rowCheck[m][1]) + "?format=json"
		print(url)
		r = requests.get(url)
		response = json.loads(r.content.decode())
		results = [response['Results'][0]['Model_Name']]
		for i in range (1,response['Count'],1):
			results.append(response['Results'][i]['Model_Name'])
	
		nhtsaModelList = results
		
		resModelId = [response['Results'][0]['Model_ID']]
		for i in range (1,response['Count'],1):
			resModelId.append(response['Results'][i]['Model_ID'])
	
		cur.execute("SELECT DISTINCT Model FROM Menu where Make = ?",(rowCheck[m][0],))

		rows = cur.fetchall()
		rowTxt = [rows[0][0]]
		for i in range(len(rows)):
			print(rows[i][0])
			rowTxt.append(rows[i][0])


		for i in range(len(rowTxt)):
			matchResult = (process.extractOne(rowTxt[i], nhtsaModelList, score_cutoff=70))
			if not matchResult:
				print ("No Match found for " + rowTxt[i])
			else:
				print (matchResult) 
				print (" for " + rowTxt[i])
				print (matchResult[0])
				for j in range(len(nhtsaModelList)):
					if nhtsaModelList[j] == matchResult[0]:
						cur.execute("INSERT OR IGNORE INTO Model (Make, Model, ModelID) VALUES(?,?,?)",(rowCheck[m][0],rowTxt[i],resModelId[j]))
						con.commit()
						print (rowCheck[m][0] + " " + nhtsaModelList[j] + "is ID# " + str(resModelId[j]))


def test():
	#connect to to DB
	con = sql.connect("base_car.db")
	con.row_factory = sql.Row
	con.text_factory = str
	cur = con.cursor()

	cur.execute("SELECT Make,MakeId FROM Manf")
	rows = cur.fetchall()
	for i in range(len(rows)):
		print(rows[i][0] + str(rows[i][1]))
	print(rows)
	print("Done")

if __name__ == '__main__':
	buildMakeId()
	#test()
