import urllib2
import csv
import json
from BeautifulSoup import BeautifulSoup
import random

class ApartmentBuilding(object):
    def __init__(self, aptname, link, bedrooms, price, latitude, longitude, address, city, state, zipcode):
        self.aptname = aptname
        self.link = link
        self.bedrooms = bedrooms
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
    def __name__(self):
        return self.aptname

def writeCSV(aptlist):
    file_writer = csv.writer(open('allapts.csv', 'wb'))
    file_writer.writerow(['ApartmentName', 'Link', 'Bedrooms', 'Price', 'Latitude', 'Longitude', 'Address', 'City', 'State', 'Zipcode'])
    for j in aptlist:
        row = []
        row.append(j.aptname)
        row.append(j.link)
        row.append(j.bedrooms)
        row.append(j.price)
        row.append(j.latitude)
        row.append(j.longitude)
        row.append(j.address)
        row.append(j.city)
        row.append(j.state)
        row.append(j.zipcode)
        file_writer.writerow(row)

if  __name__ =='__main__':
	matchedlist =[]
	pagenum = 1
	while(True):
		request = urllib2.build_opener()
		url = 'http://www.forrent.com/results.php?pagenum=' + str(pagenum) + '&repost=true&flattened=latitude%3D47.604304%26longitude%3D-122.329722%26area_name%3DSeattle%252C%2BWA%26sbeds%3D99%26sbaths%3D99%26max_price%3DNo%2BLimit%26ssradius%3D-1%26amenities%255B56%255D%3D0%26amenities%255B44%255D%3D1%26amenities%255B91%255D%3D2%26amenities%255B38%255D%3D3%26main_field%3DSeattle%252C%2BWA%26search_type%3Dcitystate%26pagenum%3D12%26resultsPerPage%3D20%26sort_by%3Ddefault%26view_type%3Dlist%26page_type_id%3Dcity%26seed%3D218469106%26is_refined%3D1%26locale%3DLangEN'
		#'&repost=true&flattened=latitude%3D47.604304%26longitude%3D-122.329722%26area_name%3DSeattle%252C%2BWA%26sbeds%3D99%26sbaths%3D99%26max_price%3D850%26ssradius%3D30%26amenities%255B44%255D%3D0%26amenities%255B91%255D%3D1%26amenities%255B38%255D%3D2%26main_field%3DSeattle%252C%2BWA%26search_type%3Dcitystate%26pagenum%3D14%26resultsPerPage%3D40%26sort_by%3Ddefault%26view_type%3Dlist%26page_type_id%3Dcity%26seed%3D624539403%26is_refined%3D1%26locale%3DLangEN'
		returnedpage = request.open(url)
		objectlist = BeautifulSoup(returnedpage.read()).findAll("li", { "class" : "searchMatch hListing offer rent housing line sep" })
		if len(objectlist) == 0:
			break
		for aptbuilding in objectlist:
			try: 
				linkblock = aptbuilding.find('a', { "class" : "permalink" })
				apartmentname = linkblock['title'].encode('utf-8')
				link = linkblock['href'].encode('utf-8')
				bdrmsandprice = aptbuilding.find('div', { "class" : "unit size3of5" }).a.string.encode('utf-8').replace('  ', '').replace('\n', '').replace('\t', '')
				split = bdrmsandprice.split(' | ')
				bedrooms = split[0]
				price = split[1]
				aptpage = urllib2.build_opener()
				aptpage = aptpage.open(link)
				aptpage = BeautifulSoup(aptpage.read())
				locationinfo = aptpage.find("div", { "id" : "addressForMap" })
				lat = locationinfo.find('span', {'class' : 'lat hide'}).string.encode('utf-8')
				lon = locationinfo.find('span', {'class' : 'lon hide'}).string.encode('utf-8')
				address = locationinfo.find('span', {'class' : 'dBlock street-address'}).string.encode('utf-8')
				city = locationinfo.find('span', {'class' : 'locality'}).string.replace(',','').encode('utf-8')
				state = locationinfo.find('span', {'class' : 'region'}).string.encode('utf-8')
				zipcode = locationinfo.find('span', {'class' : 'postal-code'}).string.encode('utf-8')
			except TypeError:
				pass

			try:
				matchedlist.append(ApartmentBuilding(apartmentname, link, bedrooms, price, lat, lon, address, city, state, zipcode))
			except NameError:
				pass

		pagenum += 1

	writeCSV(matchedlist)
	#json.dumps(random.choice(matchedlist))