docker stop nvr_speecher
docker rm nvr_speecher
docker build -t nvr_speecher .
docker run -d \
 -it \
 --name nvr_speecher \
 --net=host \
 --env-file ../.env_nvr \
 -v $HOME/creds:/speecher/creds \
 nvr_speecher
