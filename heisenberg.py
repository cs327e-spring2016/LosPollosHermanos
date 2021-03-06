from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql


preseason =["Fri 10/23","Tue 10/20","Mon 10/19","Wed 10/14","Mon 10/12","Sat 10/10","Thu 10/8","Tue 10/6"]

def dbase_init():
	# database connection: add your own passwd
	conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='jfh71293.,', db='data_scraper')
	cur = conn.cursor()


	# tables wiped 
	cur.execute("DROP TABLE IF EXISTS Data")
	cur.execute("create table Data (id_pk INT not null, game_fk INT, player_fk INT, minutes INT, fg_made INT, fg_attempted INT, three_made INT, three_attempted INT, free_made INT, free_attempted INT, rebounds INT, assists INT, blocks INT, steals INT, fouls INT, turnovers INT, points INT, outcome varchar(1), PRIMARY KEY (id_pk))")
	cur.execute("DROP TABLE IF EXISTS Player")
	cur.execute("create table Player (id_pk INT not null, first varchar(25), last varchar(25), age INT, PRIMARY KEY (id_pk))")
	cur.execute("DROP TABLE IF EXISTS Games")
	cur.execute("create table Games ( id_pk INT not null, opponent_fk varchar(25), date varchar(25), bulls_points INT, opp_points INT, outcome varchar(1), PRIMARY KEY (id_pk))")

	return cur, conn


def scrape(player_array, cur):
	global globalid_num
	global game_id
	global oppo_bool
	global data_id

	pIDS=[6430,2528354,3192,1708,3113587,996,3986,2284101,2528588,6459,6460,3224,3064482,3456,2528353]
	tracking=0

	id_num = 0
	globalid_num = 0
	game_id = 0
	oppo_bool = False
	data_id = 0
	# iterate over roster
	for plyer in range(1,(len(player_array)+1)):
		LRID= pIDS[tracking]
		LRID= str(LRID)

		game_id = 0


		ayer = player_array[plyer-1]
		ayer = ayer.split("-")

		player = player_array[plyer-1]

		# scrape begins
		html = urlopen("http://espn.go.com/nba/player/gamelog/_/id/"+LRID)
		bsObj = BeautifulSoup(html.read(), "html.parser")
		tracking+=1


		s = (bsObj.findAll("ul", {"class":"player-metadata floatleft"}))
		t = s[0].findAll("li")
		j = t[1].findAll("span")
		f = t[0].getText()
		y = len(f) - 1
		x = y - 2
		age = int(f[x:y])
		playr = player.split("-")

		id_num += 1
		first = playr[0].capitalize()
		last = playr[1].capitalize()
		cur.execute('insert into Player values ("%s","%s","%s","%s")' % (plyer,first,last,age))		

		
		# iterate over nba teams
		for v in range(1,31):
			odd(v, bsObj, playr, player, ayer, cur, plyer)
			even(v, bsObj, playr, player, ayer,cur, plyer)

		print("Player: ", ayer[0].capitalize(), ayer[1].capitalize(),"is done!")


def odd(v, bsObj, playr, player, ayer,cur, plyer):
	global data_id
	global game_id
	global dates
	dates = [0]*82
	xy=0
	v = str(v)
	st1 = (bsObj.findAll("tr", {"class":"oddrow team-46-"+v}))


	for i in range(len(st1)):


		obj = st1[i].findAll("td")
		playr = player.split("-")
		
		#date
		date = obj[0].getText()
		if date in preseason:
			continue
		if date in dates:
			continue

		game_id += 1
		data_id += 1

		dates[xy]=date
		xy+=1

		#opponent
		opp = obj[1].getText()
		opponent = opp[2:]
		#score
		q = obj[2].findAll("a")
		score = q[0].getText()
		Fscore= score.split("-")

		bulls = Fscore[0]
		opts = Fscore[1]
		#outcome
		wl = obj[2].findAll("span")
		outcome = wl[0].getText()
		#minutes
		minu = obj[3].getText()

		x = obj[4].getText().split("-")
		fg_made = x[0]
		fg_attempted = x[1]

		x = obj[6].getText().split("-")
		three_made = x[0]
		three_attempted = x[1]

		x = obj[8].getText().split("-")
		free_made = x[0]
		free_attempted = x[1]

		rebounds = obj[10].getText()

		assists = obj[11].getText()

		blocks = obj[12].getText()

		steals = obj[13].getText()

		fouls = obj[14].getText()

		turnovers = obj[15].getText()

		points = obj[16].getText()
		
		if plyer == 1:
			cur.execute('insert into Games values (%s,"%s","%s","%s","%s", "%s")' % (game_id, opponent , date, bulls, opts, outcome))
		cur.execute('insert into Data values ("%s",%s,%s,"%s", "%s", "%s","%s","%s","%s", "%s" ,"%s", "%s", "%s","%s","%s","%s", "%s", "%s")' % (data_id, game_id ,plyer, minu, fg_made, fg_attempted, three_made, three_attempted, free_made, free_attempted, rebounds, assists, blocks, steals, fouls, turnovers, points, outcome ))
	# end of scrape


def even(v, bsObj, playr, player, ayer,cur, plyer):
	global data_id
	global game_id

	xy = 0
	v = str(v)
	st2 = (bsObj.findAll("tr", {"class":"evenrow team-46-"+v}))


	for i in range(len(st2)):
		obj = st2[i].findAll("td")
		playr = player.split("-")
		#date
		date = obj[0].getText()
		if date in preseason:
			continue
		if date in dates:
			continue

		game_id += 1
		data_id += 1
		dates[xy]=date
		xy+=1
		#opponent
		opp = obj[1].getText()
		opponent = opp[2:]
		#score
		q = obj[2].findAll("a")
		score = q[0].getText()
		Fscore= score.split("-")

		bulls = Fscore[0]
		opts = Fscore[1]
		#outcome
		wl = obj[2].findAll("span")
		outcome = wl[0].getText()
		#minutes
		minu = obj[3].getText()

		x = obj[4].getText().split("-")
		fg_made = x[0]
		fg_attempted = x[1]

		x = obj[6].getText().split("-")
		three_made = x[0]
		three_attempted = x[1]

		x = obj[8].getText().split("-")
		free_made = x[0]
		free_attempted = x[1]

		rebounds = obj[10].getText()

		assists = obj[11].getText()

		blocks = obj[12].getText()

		steals = obj[13].getText()

		fouls = obj[14].getText()

		turnovers = obj[15].getText()

		points = obj[16].getText()

		if plyer == 1:
			cur.execute('insert into Games values (%s,"%s","%s","%s","%s", "%s")' % (game_id, opponent , date, bulls, opts, outcome))
		cur.execute('insert into Data values ("%s",%s,%s,"%s", "%s", "%s","%s","%s","%s", "%s" ,"%s", "%s", "%s","%s","%s","%s", "%s", "%s")' % (data_id, game_id ,plyer, minu, fg_made, fg_attempted, three_made, three_attempted, free_made, free_attempted, rebounds, assists, blocks, steals, fouls, turnovers, points, outcome ))
	# end of scrape

					
	

def query_interface (cur, conn):
	select=''
	table='' 
	whre='' 
	groupAns=''
	# custom query interface
	start = input("Ready to start querying?(yes/no) ")

	colNames=[]

	if start.lower() != "yes":
		print("BYE!")
		cur.close()
		conn.commit()
		conn.close()
		stop = True
		return stop

	print("GREAT!")
	print()

	c = True
	# iterate until correct table name is specified
	while c == True:
		print("Tables: Player, Data, Games")
		print()
		table = input("What table would you like to query? ")
		print("Thanks!")
		print()

		if (table.lower() == "player"):
			print("Table", table.capitalize(), "has: id_pk , first , last ,and age for each player")
			print()
			# user inputs what columns they'd like to see
			select = input("What would you like to select(use commas to separate values)? ")
			select2 = select.split(",")
			print(select)
			c = False
		elif (table.lower() == "data"):
			print("Table", table.capitalize(), "has: outcome, id_pk , game_fk , player_fk , minutes  , fg_made , fg_attempted , three_made , three_attempted , free_made , free_attempted , rebounds , assists , blocks , steals , fouls , turnovers ,  points for each Player in each Game played")
			print()
			select = input("What would you like to select(use commas to separate values)? ")
			select2 = select.split(",")
			print(select)
			c = False
		elif (table.lower() == "games"):
			print("Table", table.capitalize(), "has: outcome, id_pk , opponent_fk , date , and score for each game")
			print()
			select = input("What would you like to select(use commas to separate values)? ")
			select2 = select.split(",")
			print(select)
			c = False
		else:
			print("Seems like your spelling may be incorrect, lets try again.")
			c = True
	print()
	# user input WHERE clause
	whereQ = input("Want to use filter out data(yes/no) ")
	print()
	if whereQ.lower() == "yes":
		print("What conditions would you like to add(ex first = 'jimmy', age >= 20)?")
		print()
		whre = input("WHERE: ")

		print()

	#ask user groupBy
	groupQ = input("Want to use group by?: (yes/no) ")
	print()
	if groupQ.lower() == "yes":
		print("What would you like to group by?")
		print()
		groupAns = input("GROUP BY: ")

		print()



	# user validation of custom query
	print("Is this the query you'd like to run?")
	print()
	table = table.capitalize()
	if whereQ.lower() == "yes":
		if groupQ.lower()=="yes":
			print("SELECT", select, "FROM",table, "WHERE", whre, "GROUP BY", groupAns)
		else:
			print("SELECT", select, "FROM",table, "WHERE", whre)
	else:
		if groupQ.lower()=="yes":
			print("SELECT", select, "FROM",table, "GROUP BY", groupAns)
		else:
			print("SELECT", select, "FROM",table)
	print()
	statement = input("(yes/no): ")
	print()
	# sql query construction and output
	if (statement.lower() == "yes"):
		if whereQ.lower() == "yes":
			if groupQ.lower()=="yes":
				hfg = cur.execute('SELECT %s FROM %s WHERE %s GROUP BY %s' % (select, table, whre, groupAns))
			else:
				hfg = cur.execute('SELECT %s FROM %s WHERE %s' % (select, table, whre))
		else:
			if groupQ.lower()=="yes":
				hfg = cur.execute('SELECT %s FROM %s GROUP BY %s' % (select, table, groupAns))
			else:
				hfg = cur.execute('SELECT %s FROM %s' % (select, table))
			
		p = cur.fetchall()
		print()

		
		for x in select2:
			print(x[:4],end="\t")
	
		print()
		for row in p:
			for y in row:
				print(y,end="\t")
			print()

	print()
	print()
	query_interface(cur, conn)


def some_or_all ():

	player_array = ["jimmy-butler", "cameron-bairstow", "aaron-brooks", "mike-dunleavy", "cristiano-felicio", "pau-gasol", "taj-gibson", "justin-holidy", "doug-mcdermott", "nikola-mirotic", "e'twaun-moore", "joakim-noah", "bobby-ports", "derrick-rose", "tony-snell"]
	else_arry_ver = input("Would you like to input all payers or custom select players to import(all/some)? ")
	if else_arry_ver.lower().replace(" ", "") == "some":
		print()
		new_array = input("Type the names of the players youd like to import separated by a comma. (ex jimmy butler , aaron brooks) ")
		new_array = new_array.replace(", ", ",")
		new_array = new_array.replace(" ,", ",")
		new_array = new_array.replace(" ", "-")
		new_array = new_array.split(",")
		player_array = []
		player_array = new_array
	return player_array


def main():

	print("Starting to scrape...")
	print('...')


	cur, conn = dbase_init()

	player_array = some_or_all()


	print("Chicago Bulls Roster: ")

	scrape(player_array, cur)
	
	print()

	stop = query_interface(cur, conn)
	if stop == True:
		return

	# close database connection
	#cur.close()
	#conn.commit()
	#conn.close()

main()