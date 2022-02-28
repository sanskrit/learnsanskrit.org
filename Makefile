.PHONY: test


lint:
	black .

devserver:
	python runserver.py

test:
	py.test test

# Create a fast but incomplete PDF (for testing and previewing print styles)
test_pdf:
	weasyprint "http://localhost:5000/guide/print-debug/" debug.pdf

# Create a full PDF for /guide
guide_pdf:
	weasyprint "http://127.0.0.1:5000/guide/print/" tmp-guide.pdf
	mv tmp-guide.pdf lso/static/pdf/guide.pdf

# Create a full PDF for /vyakarana
vyakarana_pdf:
	weasyprint "http://127.0.0.1:5000/vyakarana/print/" tmp-vyakarana.pdf
	mv tmp-vyakarana.pdf lso/static/pdf/vyakarana.pdf

# Generate static web pages and deploy them to prod.
deploy_static: test
	# echo "deploys are disabled on this branch."
	./production/deploy.sh

# (WIP) Deploy the API server.
deploy_api: test
	./production/deploy_api_server.sh

# Build and deploy all site content.
deploy: test guide_pdf vyakarana_pdf deploy_static
