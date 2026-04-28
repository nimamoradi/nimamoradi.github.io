rm -rf output/ &&\
pelican -s pelicanconf.py &&\
cp CNAME output/ &&\
cp content/images/favicon.jpg output/ &&\
ghp-import output &&\
git push origin gh-pages --force