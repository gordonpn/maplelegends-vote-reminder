local failure_notification = {
  name: 'failure notification',
  image: 'plugins/slack',
  when: { status: ['failure'] },
  failure: 'ignore',
  settings: {
    channel: 'drone-ci',
    webhook: {
      from_secret: 'SLACK_WEBHOOK_URL',
    },
    template: |||
      Deploy failed
      Commit: <https://github.com/{{ repo.owner }}/{{ repo.name }}/commit/{{ build.commit }}|{{ truncate build.commit 8 }}>
      Branch: <https://github.com/{{ repo.owner }}/{{ repo.name }}/commits/{{ build.branch }}|{{ build.branch }}>
      Author: {{ build.author }}
      <{{ build.link }}|Visit build #{{build.number}} page ➡️>
    |||,
  },
};

local deploy = {
  kind: 'pipeline',
  type: 'docker',
  name: 'deploy',
  trigger: { event: ['custom'] },
  steps: [
    {
      name: 'deploy prod',
      image: 'docker:20.10.12',
      environment: {
        BOT_TOKEN: { from_secret: 'BOT_TOKEN' },
        MONGO_INITDB_DATABASE: { from_secret: 'MONGO_INITDB_DATABASE' },
        MONGO_INITDB_ROOT_PASSWORD: { from_secret: 'MONGO_INITDB_ROOT_PASSWORD' },
        MONGO_INITDB_ROOT_USERNAME: { from_secret: 'MONGO_INITDB_ROOT_USERNAME' },
        MONGO_NON_ROOT_PASSWORD: { from_secret: 'MONGO_NON_ROOT_PASSWORD' },
        MONGO_NON_ROOT_USERNAME: { from_secret: 'MONGO_NON_ROOT_USERNAME' },
      },
      volumes: [{
        name: 'dockersock',
        path: '/var/run/docker.sock',
      }],
      commands: [
        'apk update && apk --no-cache add bash curl docker-compose && curl --version && bash --version && docker-compose version',
        '/bin/bash /drone/src/docker/scripts/deploy.sh',
      ],
    },
    failure_notification,
  ],
  volumes: [{
    name: 'dockersock',
    host: { path: '/var/run/docker.sock' },
  }],
};

[deploy]
