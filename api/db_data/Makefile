# Unprefixed verbs from Dr. Dhaval Patel
# Missing passives, prefixes, sanAdyanta
dhaval_verbs:
	wget https://github.com/drdhaval2785/SanskritVerb/raw/master/generatedforms/verbforms.tar.gz
	tar -xzvf verbforms.tar.gz
	rm verbforms.tar.gz
	mv generatedforms20062016.xml dhaval-verbs.xml

# Monier-Williams Sanskrit-English Dictionary, 1899
# https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/web/webtc/download.html
mw_data:
	wget https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/downloads/mwxml.zip
	unzip mwxml.zip
	mv xml/mw.xml monier-williams.xml
	rm -R xml/
	rm mwxml.zip
