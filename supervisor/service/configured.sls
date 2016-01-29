{% from "supervisor/map.jinja" import supervisor with context %}


{% set conf_file_exists = salt['file.file_exists'](supervisor.service.installed.conf_file) %}

{% if not conf_file_exists %}
supervisor_create_config_file:
  file.touch:
    - name: {{ supervisor.service.installed.conf_file }}
{% endif %}

supervisor_manage_service_configuration:
  file.blockreplace:
    - name: {{ supervisor.service.installed.conf_file }}
    - marker_start: '#-- service configuration zone start --#'
    - marker_end: '#-- service configuration zone end --#'
    - prepend_if_not_found: yes
    - source: salt://supervisor/service/templates/supervisord.conf.jinja
    - template: jinja
    - context:
        config: {{ supervisor.service.installed.config|yaml }}
{% if not conf_file_exists %}
    - require:
        - file: supervisor_create_config_file
{% endif %}
