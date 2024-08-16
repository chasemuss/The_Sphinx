docker build -t the_sphinx .
docker tag the_sphinx the_sphinx
docker run -d the_sphinx