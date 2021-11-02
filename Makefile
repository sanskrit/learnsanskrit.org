lint:
	black .

local:
	python runserver.py

test:
	echo "No tests configured."

test_pdf:
	weasyprint "http://localhost:5000/guide/print-debug/" debug.pdf

prod_pdf:
	weasyprint "http://localhost:5000/guide/print/" tmp.pdf
	mv tmp.pdf lso/static/pdf/guide.pdf

deploy_web: test
	./production/deploy.sh

deploy_all: test prod_pdf deploy_web
