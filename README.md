Build image:  
`docker build -f docker/ylab_test.Dockerfile -t ylab_test .`

Run project (docker-compose required to run the project):  
`docker-compose -f docker/docker-compose.yml up --force-recreate`

The swagger specification:  
https://app.swaggerhub.com/apis/kovalevvjatcheslav/ylab/1.0.0