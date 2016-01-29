{% from "supervisor/map.jinja" import supervisor with context %}


supervisor_service_dead:
  service.dead:
    - name: {{ salt['file.basename'](supervisor.service.installed.init_script_file) }}
    - enable: no
