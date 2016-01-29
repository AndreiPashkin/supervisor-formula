{% from "supervisor/map.jinja" import supervisor with context %}


include:
  - supervisor.service.running
  - supervisor.processes._supervisor_process_running_base

{% set processes = {} %}

{% for name, options in supervisor.processes.running.items() %}
  {% do processes.update(
    {'program:' + name:  options.settings}
  ) %}
{% endfor %}

supervisord_manage_processes_configuration:
   file.blockreplace:
     - name: {{ supervisor.service.installed.conf_file }}
     - marker_start: '#-- processes configuration zone start --#'
     - marker_end: '#-- processes configuration zone end --#'
     - append_if_not_found: yes
     - source: salt://supervisor/service/templates/supervisord.conf.jinja
     - template: jinja
     - context:
         config: {{ processes }}
     - require:
       - pip: supervisor_python_package_installed

# Prepare user-defined state declarations for processes for merging them
# with default declaration
{% set extend = {} %}

{% for name, options in supervisor.processes.running.items() %}
{% set state = options.get('state', []) %}
{% do extend.update({
  'supervisor_process_{}_running'.format(name): {
    'supervisord.running': state
}}) %}
{% endfor %}

extend: {{ extend|yaml }}

supervisor_update_processes:
  cmd.run:
    - name: supervisorctl update
    - onchanges:
      - file: {{ supervisor.service.installed.init_script_file }}
      - file: {{ supervisor.service.installed.conf_file }}
    - require:
      - service: supervisor_service_running
