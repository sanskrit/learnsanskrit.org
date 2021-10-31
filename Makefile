lint:
	black .

local:
	python runserver.py

test:
	echo "No tests configured."

deploy: test
	./production/deploy.sh
