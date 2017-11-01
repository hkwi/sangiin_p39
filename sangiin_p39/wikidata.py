import os
import io
import re
import time
import requests
import selenium.webdriver
import lxml.html
import rdflib
import csv

ns={}
for k,v in csv.reader(open(os.path.join(os.path.dirname(__file__), "ns.csv"))):
	globals()[k.upper()] = rdflib.Namespace(v)
	ns[k] = v

def run():
	w = rdflib.ConjunctiveGraph(store="SPARQLStore")
	w.store.endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
	res = w.query('''
	SELECT distinct ?p ?pLabel ?altName WHERE {
	  ?p p:P39 ?st .
	  ?st ps:P39 wd:Q14552828 .
	  ?p skos:altLable ?altName .
	  FILTER NOT EXISTS { ?p wdt:P31 wd:Q17362920 . }
	  FILTER NOT EXISTS { ?p wdt:P570 ?dead . }
	  
	  { FILTER NOT EXISTS { ?st pq:P582 ?end . } }
	  UNION
	  { ?st pq:P582 ?end . FILTER(?end > now()) }
	  
	  SERVICE wikibase:label { bd:serviceParam wikibase:language "ja". } 
	}
	''')
	name2q = {}
	def ez_set(name, qname):
		name = re.sub("[　 ]+", "", name)
		if qname == name2q.get(name, qname):
			name2q[name] = qname
		else:
			name2q[name] = "-"
	for r in res:
		ez_set(r["pLabel"], r["p"])
		ez_set(r["altName"], r["p"])
	
	dr = selenium.webdriver.PhantomJS()
	dr.get("http://www.sangiin.go.jp/japanese/joho1/kousei/giin/current/giinmei.htm")
	time.sleep(2)
	txt = io.StringIO(requests.get(dr.current_url).text)
	doc = lxml.html.parse(txt)
	
	found = set()
	for tr in doc.xpath('.//table[contains(@class,"議員一覧")]//tr'):
		txt = [t.strip() for t in tr.xpath('.//td[0]//text()') if t.strip()]
		if txt:
			name = re.sub("[　 ]+", "", txt.pop(0))
			found.add(qname[name])
	assert found == set(name2q.values())

if __name__=="__main__":
	run()
