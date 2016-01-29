{% from 'supervisor/map.jinja' import supervisor with context %}


include:
  - supervisor.service.configured

supervisor_python_package_installed:
  pip.installed:
    - name: supervisor {{ supervisor.service.installed.version }}

supervisor_manage_init_script:
  file.managed:
    - name: {{ supervisor.service.installed.init_script_file }}
    - source: {{ supervisor.service.installed.init_script_source }}
    - template: jinja
    - user: root
    - group: root
    - mode: 755
    - context:
        supervisor: {{ supervisor|yaml }}
    - require:
        - pip: supervisor_python_package_installed
