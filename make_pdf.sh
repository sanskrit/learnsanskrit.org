#!/usr/bin/env sh

BASE="http://localhost:5000/guide"
wkhtmltopdf \
    cover "${BASE}/print/cover/" \
    toc \
    page "${BASE}/print/all/" \
        --header-line \
    out.pdf
