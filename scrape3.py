import urllib2
import mechanize
import cookielib
from bs4 import BeautifulSoup
import math
import re
import time
import os
import urllib
class FetchUrl():
	'''no
	lpgnores
	result['minpce']
	result['maxpce']
	result['minocv']
	result['maxocv'] 
	result['minsccd']
	result['maxsccd']
	result['noofresults']

	def __init__(self):
		no = 0
		lpgnores = 0
		result['minpce'] = 0
		result['maxpce'] = 0
		result['minocv'] = 0
		result['maxocv'] = 0
		result['minsccd'] = 0
		result['maxsccd'] = 0
		result['noofresults'] = 0'''

	def callFunctions(self):
		result = x.constructUrl()
		for j in range(0,100):
			result['minpce'] = str(j*(0.01))
			result['maxpce'] = str(j*(0.01)+0.01)
			print str(result['minpce'])
			j = j+1
			url = x.getUrl('1',result['minpce'],result['maxpce'],result['minocv'],result['maxocv'],result['minsccd'],result['maxsccd'],result['noofresults'])
                        retsoup = x.openUrl(url)
                        value = x.scrapeNum(retsoup)
			no = value['no']
			lpgnores = value['lpgnores']
			for i in range(1,no+1):
				#if i < 7:
				#	continue
				'''url = x.GetUrl(i,self.result['minpce'],self.result['maxpce'],self.result['minocv'],self.result['maxocv'],self.result['minsccd'],self.result['maxsccd'],self.result['noofresults'])'''
				url = x.getUrl(i,result['minpce'],result['maxpce'],result['minocv'],result['maxocv'],result['minsccd'],result['maxsccd'],result['noofresults'])
				retsoup = x.openUrl(url)
				if i == no:
					x.scrapeData(retsoup,(2*lpgnores))
				else:
					x.scrapeData(retsoup,40)
				print i
				i = i+1



        def constructUrl(self):
                print 'Please enter the required minimum and maximum values\n'
                minpce = raw_input('Enter the minimum PCE value,the least posiible value is 0.0: ')
                maxpce = raw_input('Enter the maximum PCE value,the highest possible value is 11.3: ')
                minocv = raw_input('Enter the minimum Open-Circuit Voltage value,the least posiible value is 0.0: ')
                maxocv = raw_input('Enter the maximum Open-Circuit Voltage value,the highest possible value is 2.18: ')
                minsccd = raw_input('Enter the minimum Short-Circuit Current Density value,the least posiible value is 0.0: ')
                maxsccd = raw_input('Enter the minimum Short-Circuit Current Density value,the highest possible value is 397.04: ')
                noofresults = raw_input('please enter the number of search results you want: ')
		return {'minpce':minpce, 'maxpce':maxpce, 'minocv':minocv, 'maxocv':maxocv, 'minsccd':minsccd,'maxsccd':maxsccd,'noofresults':noofresults}

	def getUrl(self,i,minpce,maxpce,minocv,maxocv,minsccd,maxsccd,noofresults):
		i = str(i)
		constructedurl = 'page='+i+'&'+'pce_min='+minpce+'&pce_max='+maxpce+'&voc_min='+minocv+'&voc_max='+maxocv+'&jsc_min='+minsccd+'&jsc_max='+maxsccd+'&e_homo_alpha_min=&e_homo_alpha_max=&e_lumo_alpha_min=&e_lumo_alpha_max=&e_gap_alpha_min=&e_gap_alpha_max=&smiles_str=&stoich_str=&mass_min=&mass_max=&results_number='+noofresults+'&search=Search'
		baseurl = 'https://cepdb.molecularspace.org/?'
                finalurl = baseurl + constructedurl
		return finalurl
			

        def openUrl(self, url):
                response = authenticate()
                soup = BeautifulSoup(response.get_data())
                return soup

	def scrapeData(self,soup,limit):
		try:
			links = []
			baseurl = 'https://cepdb.molecularspace.org'
			for tr in soup.find_all('tr'):
				for a in tr.find_all('a'):
					links.append(a.get('href'))
                    			i=0
			for link in links:
				url = baseurl + links[i]
				response = x.authenticate(url)
                        	i = i+2
                        	soup1 = BeautifulSoup(response.get_data())
				#smiles = (soup1.find(id = "smiles")).text
				properties = soup1.find_all("table",{"class":"single-results"})
				td = properties[0].find_all('td')
				smiles = td[1].text
				stoicform = td[4].text
				mass = td[6].text
				tables = soup1.find_all( "table", {"class":"CSSTableGenerator"} )
				td = tables[0].find_all('td')
				homo = td[0].text
				lumo = td[1].text
				ev = td[2].text
				td = tables[1].find_all('td')
				pce = td[0].text
				ocv = td[1].text
				sccd = td[2].text
				file = open('testrun.txt','a+') 
                        	unencoded_string = smiles + "," + stoicform + "," + mass+ "," + homo + "," + lumo + "," + ev + "," + pce + "," + ocv + "," + sccd + "\n"
                        	encoded_str = unicode.encode(unencoded_string, errors='ignore')
                        	file.write(encoded_str)
				if i == limit:
					break
		except urllib2.URLError:
			time.sleep(2)

	
	def scrapeNum(self,soup):
		#div =  soup.find_all("div",{"class":"pagination"})
		#a = div[0].find_all('a')
		#a.pop()
		#no = a.pop().text
		head = soup.find_all("h3",{"class":"page-subtitle"})
		total = map(int, re.findall('\d+', head[1].text))
		no = total[0]/20 + 1
		lpgnores = total[0]%20
		return {'lpgnores':lpgnores,'no':no,}
		
	

	def authenticate(self,url):
		br = mechanize.Browser()
                cj = cookielib.LWPCookieJar()
                br.set_cookiejar(cj)
                br.set_handle_equiv(True)
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.set_handle_robots(False)
                br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		br.open('https://cepdb.molecularspace.org/accounts/login')
                br.select_form(nr=0) #check yoursite forms to match the correct number
                br['login']='spoorthiravi' #use the proper input type=text name
                br['password']='Lipstick21' #use the proper input type=password name
                br.submit()
                response = br.open(url,timeout = 2000000.0)
		return response

x = FetchUrl()
x.callFunctions()


