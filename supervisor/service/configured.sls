{% from "supervisor/map.jinja" import supervisor with context %}


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
