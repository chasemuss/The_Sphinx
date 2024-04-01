docker build -t the_sphinx .
docker tag the_sphinx chasemuss/the_sphinx
docker push chasemuss/the_sphinx
docker run -d chasemuss/the_sphinx