{% from "supervisor/map.jinja" import supervisor with context %}


include:
  - supervisor.service.installed
  - supervisor.service._supervisor_service_running_base

extend:
  supervisor_service_running:
    service.running: {{ supervisor.service.get('running', {}).get('state', [])|yaml }}
