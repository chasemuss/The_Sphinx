git add .
git commit -m "General Update before Deployment"
git push

aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 800723880739.dkr.ecr.us-east-2.amazonaws.com
docker build -t the_sphinx .
docker tag the_sphinx:latest 800723880739.dkr.ecr.us-east-2.amazonaws.com/the_sphinx:latest
docker push 800723880739.dkr.ecr.us-east-2.amazonaws.com/the_sphinx:latest

terraform destroy
terraform init

terraform plan
terraform apply