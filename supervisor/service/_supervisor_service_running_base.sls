{% from "supervisor/map.jinja" import supervisor with context %}


supervisor_service_running:
  service.running:
    - name: {{ salt['file.basename'](supervisor.service.installed.init_script_file) }}
    - enable: yes
    - require:
      - file: {{ supervisor.service.installed.init_script_file }}
      - file: supervisor_manage_service_configuration
    - watch:
      - file: {{ supervisor.service.installed.init_script_file }}
      - file: supervisor_manage_service_configuration
