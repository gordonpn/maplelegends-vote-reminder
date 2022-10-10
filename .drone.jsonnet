local failure_notification(message) = {
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
      %(message)s
      Commit: <https://github.com/{{ repo.owner }}/{{ repo.name }}/commit/{{ build.commit }}|{{ truncate build.commit 8 }}>
      Branch: <https://github.com/{{ repo.owner }}/{{ repo.name }}/commits/{{ build.branch }}|{{ build.branch }}>
      Author: {{ build.author }}
      <{{ build.link }}|Visit build #{{build.number}} page ➡️>
    ||| % message,
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
    failure_notification('Deployment failed'),
  ],
  volumes: [{
    name: 'dockersock',
    host: { path: '/var/run/docker.sock' },
  }],
};

local project_workspace = 'projectworkspace';

local clone_workspace = {
  kind: 'pipeline',
  type: 'docker',
  name: 'clone workspace to host filesystem',
  trigger: { event: ['push'] },
  steps: [
    {
      name: 'clone workspace',
      image: 'alpine',
      environment: {
        GIT_DISCOVERY_ACROSS_FILESYSTEM: 1,
      },
      commands: [
        'apk update && apk --no-cache add bash git && git --version && bash --version',
        'git config --global --add safe.directory /home',
        'cd /home || exit 1',
        '[ -d ".git" ] && git fetch --all --prune && git reset --hard && exit 0',
        'git clone "${DRONE_GIT_HTTP_URL}" /home',
      ],
      volumes: [{
        name: project_workspace,
        path: '/home',
      }],
    },
    failure_notification('Cloning failed'),
  ],
  volumes: [{
    name: project_workspace,
    host: { path: '/mnt/share/docker/maplelegends_vote_reminder/workspace' },
  }],
};

[
  deploy,
  clone_workspace,
]
