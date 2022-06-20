.DEFAULT: start
.PHONY: start docker-build docker-run -docker-build-run
CMD_DOCKER_BUILD := docker build --target development -t maplelegends_vote_reminder-proxy_server .
CMD_DOCKER_RUN := docker run -p 127.0.0.1:5000:5000 maplelegends_vote_reminder-proxy_server


start:
	export FLASK_APP=proxy_server && flask run

docker-build:
	$(CMD_DOCKER_BUILD)

docker-run:
	$(CMD_DOCKER_RUN)

docker-build-run:
	$(CMD_DOCKER_BUILD) && $(CMD_DOCKER_RUN)
