pelican -s pelicanconf.py &&\
cp CNAME output/ &&\
ghp-import output &&\
git push origin gh-pages --force