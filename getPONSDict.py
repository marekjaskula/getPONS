import os
from lxml import html
import requests
import sys
import re
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Programik tworzy listę słów w formacie Quizlet, SuperMemo QA oraz strone internetową (html) do wstawienia
# składnia   python getPONS3.py SŁOWO SŁOWNIK JĘZYK_WYSZUKIWANIA
# USAGE:  python getPONS4.py speak enpl en
# USAGE:  python getPONS4.py szukaj depl pl
# frpl / depl / 


OufFileName=sys.argv[1]			# szukany wyraz
Dict=str(sys.argv[2])			# słownik
SearchLang=str(sys.argv[3])		# język wyszukiwania 


# OUT_FILE = u'index.html'
OUT_FILE = str(OufFileName) + '_' + Dict + '.html'						# nazwa pliku html
QuizletFile = open(OufFileName + '_' + Dict+ "_Quizlet.txt", 'wb')		# nazwa pliku Quizlet
QAFile = open(OufFileName + '_' + Dict+  "_QA.txt", 'wb')				# nazwa pliku Q&A


out_file = open(OUT_FILE, 'wb')

def main():
	if len(sys.argv)>=3: 			
		# print('Wybrane slowo:' + sys.argv[1])	
		link = requests.get('https://pl.pons.com/t%C5%82umaczenie?q=' + sys.argv[1] + '&l='+Dict+'&in='+SearchLang+'&lf='+SearchLang)
		source = link.content
		tree = html.fromstring(link.text)
		soup = BeautifulSoup(source, 'lxml')	
		  
		# kod nagłówka HTMLA
		html_head = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="pl-pl" lang="pl-pl" dir="ltr" >
		<head>
			<meta http-equiv="content-type" content="text/html; charset=utf-8" />
		</head><body>"""
		
		#kod zamknięcia HTMLA
		html_tail ="""</body>
		</html>"""
		
		
		out_file.write(html_head.encode())
		# count=0
		out_file.write("\r\n<table table-layout:fixed; width:700px>".strip('\n').encode('utf-8')+ "\r\n".encode('utf-8'))
		for dls in soup.find_all("div", id=re.compile('^A'+Dict+'.*')):
				
			for tr in dls.find_all("dl"):
				translated = tr.dt.div.div.text
				DTword = tr.dd.div.div.text
				
				# tworzenie pliku HTML	
				out_file.write("<tr>".strip('\n').encode('utf-8'))
				out_file.write("<td align=""left"" style=""font-weight:normal"">".strip('\n').encode('utf-8') + translated.strip('\n').encode('utf-8') + "</td>".strip('\n').encode('utf-8') + "\t".strip('\n').encode('utf-8')+ "<td align=""left"" style=""font-weight:bold"">".strip('\n').encode('utf-8') + DTword.strip('\n').encode('utf-8')  + "</td>".strip('\n').encode('utf-8'))
				out_file.write("</tr>".strip('\n').encode('utf-8'))
				out_file.write('\r\n'.encode('utf-8'))
								
				# tworzenie pliku QUIZLET	
				QuizletFile.write(translated.strip('\n').encode('UTF-8') + "\t".strip('\n').encode('utf-8') + DTword.strip('\n').encode('utf-8'))
				QuizletFile.write('\r\n'.encode('utf-8'))
				
				# tworzenie pliku SUPERMEMO
				QAFile.write("Q: ".encode('UTF-8') + translated.strip('\n').encode('UTF-8') + "\r\n".encode('utf-8') + "A: ".strip('\n').encode('utf-8') + DTword.strip('\n').encode('utf-8'))
				QAFile.write('\r\n\r\n'.encode('utf-8'))
				
				# count=count+1
		# out_file.write("________________________________________________".encode('utf-8'))
		
		
		# przyklady z zakładki EXAMPLES z PONSa
		for dls in soup.find_all(id=re.compile("results-tab-examples")):
			# print(dls)
			for tr in dls.find_all("dl", id=re.compile('T'+Dict+'.*')):
				# print(tr)
				# translated = tr.dt.div.div.text
				# DTword = tr.dd.div.div.text
				translatedDT = tr.dt.div.div.span.text
				wordDD = tr.dd.div.div.text
			
				# print(translatedDT + '\t' +wordDD)
			
			# # # tworzenie pliku HTML	
				out_file.write("<tr>".strip('\n').encode('utf-8'))
				out_file.write("<td align=""left"" style=""font-weight:normal"">".strip('\n').encode('utf-8') + translatedDT.strip('\n').encode('utf-8') + "</td>".strip('\n').encode('utf-8') + "\t".strip('\n').encode('utf-8')+ "<td align=""left"" style=""font-weight:bold"">".strip('\n').encode('utf-8') + wordDD.strip('\n').encode('utf-8')  + "</td>".strip('\n').encode('utf-8'))
				out_file.write("</tr>".strip('\n').encode('utf-8'))
				out_file.write('\r\n'.encode('utf-8'))
							
				# tworzenie pliku QUIZLET	
				QuizletFile.write(translatedDT.strip('\n').encode('UTF-8') + "\t".strip('\n').encode('utf-8') + wordDD.strip('\n').encode('utf-8'))
				QuizletFile.write('\r\n'.encode('utf-8'))
			
				# tworzenie pliku SUPERMEMO
				QAFile.write("Q: ".encode('UTF-8') + translatedDT.strip('\n').encode('UTF-8') + "\r\n".encode('utf-8') + "A: ".strip('\n').encode('utf-8') + wordDD.strip('\n').encode('utf-8'))
				QAFile.write('\r\n\r\n'.encode('utf-8'))
			
				# count=count+1
				# print("COUNT = " + str(count))
		
		
		
		
		# zakończ tabelę ze słownictwem w pliku HTML
		out_file.write("</table>".strip('\n').encode('utf-8')+ "\r\n".encode('utf-8')) 
		
		# dopisz kody zamknięcia htmla
		out_file.write(html_tail.encode())
		
		# ZAMKNIJ PLIKI 
		out_file.close()	
		QuizletFile.close()	
		QAFile.close()	
		
		
		print(u'Zapis do plików zakończony.')			
	else:
		print('Nie podano słowa') 	

		
		
if __name__ == '__main__':
	main()