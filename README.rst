==================
supervisor-formula
==================

A formula that installs and configures Supervisor_ service
and processes hosted by it.

.. _Supervisor: http://supervisord.org/

.. note::

    See the full `Salt Formulas installation and usage instructions
    <http://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html>`_.


Compatibility
=============

+--------------------+--------------------+--------------------+
| OS name            | OS release         | SaltStack release  |
+====================+====================+====================+
| Ubuntu             | 14.04 (Trusty)     | 2016.3 (Boron)     |
|                    |                    | 2015.8 (Beryllium) |
|                    |                    | 2015.5 (Lithium)   |
+--------------------+--------------------+--------------------+

Available states
================

.. contents::
    :local:

``supervisor.service.configured``
--------------------------------
Configures the service.

``supervisor.service.installed``
--------------------------------
Installs the service.

``supervisor.service.running``
--------------------------------
Launches the service.

``supervisor.processes.running``
-------------------------------
Adds processes to Supervisor.
