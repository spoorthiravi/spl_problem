import urllib2
import mechanize
import cookielib
from bs4 import BeautifulSoup
class FetchUrl():

	def CallFunctions(self):
		for i in range(1,6):
			url = x.ConstructUrl(i)
			retsoup = x.OpenUrl(url)
			x.ScrapeData(retsoup)


        def ConstructUrl(self,i):
                print 'Please enter the required minimum and maximum values\n'
                minpce = raw_input('Enter the minimum PCE value,the least posiible value is 0.0: ')
                maxpce = raw_input('Enter the maximum PCE value,the highest possible value is 11.3: ')
                minocv = raw_input('Enter the minimum Open-Circuit Voltage value,the least posiible value is 0.0: ')
                maxocv = raw_input('Enter the maximum Open-Circuit Voltage value,the highest possible value is 2.18: ')
                minsccd = raw_input('Enter the minimum Short-Circuit Current Density value,the least posiible value is 0.0: ')
                maxsccd = raw_input('Enter the minimum Short-Circuit Current Density value,the highest possible value is 397.04: ')
                noofresults = raw_input('please enter the number of search results you want: ')
		i = str(i)
		constructedurl = 'page='+i+'&'+'pce_min='+minpce+'&pce_max='+maxpce+'&voc_min='+minocv+'&voc_max='+maxocv+'&jsc_min='+minsccd+'&jsc_max='+maxsccd+'&e_homo_alpha_min=&e_homo_alpha_max=&e_lumo_alpha_min=&e_lumo_alpha_max=&e_gap_alpha_min=&e_gap_alpha_max=&smiles_str=&stoich_str=&mass_min=&mass_max=&results_number='+noofresults+'&search=Search'
		baseurl = 'https://cepdb.molecularspace.org/?'
                finalurl = baseurl + constructedurl
		print finalurl
		return finalurl
			

        def OpenUrl(self, url):
                br = mechanize.Browser()

        # Cookie Jar
                cj = cookielib.LWPCookieJar()
                br.set_cookiejar(cj)

                br.set_handle_equiv(True)
                br.set_handle_gzip(True)
                br.set_handle_redirect(True)
                br.set_handle_referer(True)
                br.set_handle_robots(False)

                #Follows refresh 0 but not hangs on refresh > 0
                br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

                br.open('https://cepdb.molecularspace.org/accounts/login')
                br.select_form(nr=0) #check yoursite forms to match the correct number
                br['login']='spoorthiravi' #use the proper input type=text name
                br['password']='Lipstick21' #use the proper input type=password name
                br.submit()
                response = br.open(url)
                soup = BeautifulSoup(response.get_data())
                #print(soup.prettify) 
                return soup

	def ScrapeData(self,soup):
		links = []
		baseurl = 'https://cepdb.molecularspace.org'
		for tr in soup.find_all('tr'):
			for a in tr.find_all('a'):
				#print a
				links.append(a.get('href'))
                    		i=0
		for link in links:
			url = baseurl + links[i]
			#print url
			
			br = mechanize.Browser()

                	cj = cookielib.LWPCookieJar()
                	br.set_cookiejar(cj)

                	br.set_handle_equiv(True)
                	br.set_handle_gzip(True)
                	br.set_handle_redirect(True)
                	br.set_handle_referer(True)
                	br.set_handle_robots(False)

                #Follows refresh 0 but not hangs on refresh > 0
                	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

                	br.open('https://cepdb.molecularspace.org/accounts/login')
                	br.select_form(nr=0) #check yoursite forms to match the correct number
                	br['login']='spoorthiravi' #use the proper input type=text name
                	br['password']='Lipstick21' #use the proper input type=password name
                	br.submit()
                	response = br.open(url)

			#htmlpg = OpenUrl(url)
			#print "open"
                        i = i+2
                        soup1 = BeautifulSoup(response.get_data())
			smiles = (soup1.find(id = "smiles")).text
			
			#print smiles
			tables = soup1.find_all( "table", {"class":"CSSTableGenerator"} )
			#table = soup1.find_all(lambda tag: tag.name=='table' and tag.has_key('class') and tag['class']=="CSSTableGenerator")
			#print tables
			
			td = tables[0].find_all('td')
			homo = td[0].text 
			lumo = td[1].text
			ev = td[2].text
			#print homo
			#print lumo
			#print ev
			td = tables[1].find_all('td')
                        pce = td[0].text
                        ocv = td[1].text
                        sccd = td[2].text
			#print pce
			#print ocv
			#print sccd
			file = open('data.txt','a+') 
                        encoded_str = homo + "," + lumo + "," + ev + "," + pce + "," + ocv + "," + sccd + "\n" 
			decoded_str = encoded_str.decode('utf-8')
			file.write(decoded_str)
				
		file.close()


x = FetchUrl()
x.CallFunctions()


