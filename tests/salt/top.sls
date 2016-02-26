base:
  '*':
    - supervisor.service.installed
    - supervisor.service.configured
    - supervisor.service.running
    - supervisor.service.dead
    - supervisor.processes.running
