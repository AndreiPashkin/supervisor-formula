{% from "supervisor/map.jinja" import supervisor with context %}


{% for name, options in supervisor.processes.running.items() %}
supervisor_process_{{ name }}_running:
  supervisord.running:
    - name: {{ name }}
    - conf_file: {{ supervisor.service.installed.conf_file }}
    - require:
      - service: supervisor_service_running
      - file: supervisord_manage_processes_configuration
      - cmd: supervisor_update_processes
{% endfor %}
