local docker_pipeline = {
  kind: 'pipeline',
  type: 'docker',
};

local exec_pipeline = {
  kind: 'pipeline',
  type: 'exec',
};

local notification(message) = docker_pipeline {
  name: 'notification %(message)s' % message,
  steps: [{
    name: 'notification',
    image: 'plugins/slack',
    failure: 'ignore',
    settings: {
      channel: 'drone-ci',
      webhook: {
        from_secret: 'SLACK_WEBHOOK_URL',
      },
      template: |||
        %(message)s
        {{ uppercasefirst build.event }} on branch {{ build.branch }} from repo {{repo.name}}
        <{{ build.link }}|Visit build #{{build.number}} page ➡️>
      ||| % { message: message },
    },
  }],
};

[
  notification('build started'),
  notification('build finished'),
]
