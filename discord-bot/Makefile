.DEFAULT: start
.PHONY: start docker-build docker-run -docker-build-run
CMD_DOCKER_BUILD := docker build -t maplelegends_vote_reminder-discord_bot .
CMD_DOCKER_RUN := docker run maplelegends_vote_reminder-discord_bot

start:
	poetry run python ./discord_bot/app.py

docker-build:
	$(CMD_DOCKER_BUILD)

docker-run:
	$(CMD_DOCKER_RUN)

docker-build-run:
	$(CMD_DOCKER_BUILD) && $(CMD_DOCKER_RUN)
