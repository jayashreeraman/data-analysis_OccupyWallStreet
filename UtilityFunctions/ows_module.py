import dateutil.parser, datetime
import re



class OccupyWallStreet:
	def __init__(self, state, city, date, refNum):
		self.state = state
		self.city = city
		self.date = date
		self.refNum = refNum



##x = OccupyWallStreet('Maharashtra', 'Mumbai', '28-96-8523', '753')
##print(x.city)


def parse_date(d):
    x = dateutil.parser.parse(d)
    x = datetime.datetime.strftime(x, '%d-%m-%Y')
    print(x)

#parse_date("October 21, 1989")



