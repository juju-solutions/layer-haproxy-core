#!/usr/bin/env python3

from charms.apt import queue_install
from charms.reactive import when, when_not, set_state, remove_state
from charms.reactive.helpers import data_changed
from charmhelpers.core import hookenv

from charms.layer import haproxy

# The file in the templates directory to render when writing the haproxy.cfg.
TEMPLATE_NAME = 'haproxy.cfg'


@when_not('apt.installed.haproxy')
def install_haproxy():
    """Install haproxy and any other required software for this layer."""
    queue_install(['haproxy'])


@when('apt.installed.haproxy')
def application_version_set():
    """Get the version of software deployed on this system."""
    hookenv.application_version_set(haproxy.get_version())


@when('apt.installed.haproxy')
@when_not('haproxy.enabled')
def enable():
    """Ensure the software starts automatically on this system."""
    haproxy.enable()
    set_state('haproxy.enabled')


@when('apt.installed.haproxy')
def status_update():
    """Report the status of the haproxy service."""
    enabled = 'disabled'
    if haproxy.is_enabled():
        enabled = 'enabled'
    else:
        remove_state('haproxy.enabled')
    active = 'inactive'
    if haproxy.is_active():
        active = 'active'
        set_state('haproxy.active')
    else:
        remove_state('haproxy.active')
    message = 'HAProxy is {} and {}'.format(enabled, active)
    hookenv.status_set('active', message)


@when('haproxy.enabled', 'reverseproxy.available')
def configure_reverseproxy(reverseproxy):
    """Get all the services and update the configuration with each host."""
    services = reverseproxy.services()
    relation_changed = data_changed('reverseproxy', services)
    config_changed = data_changed('config', hookenv.config())
    # Only when the relation or config data changes, render a new template.
    if relation_changed or config_changed:
        hookenv.log('The relation or configuration data has changed.')
        # Replace slashes in unit name with dash for a configuration safe name.
        unit_name = hookenv.local_unit().replace('/', '-')
        hookenv.log('{} is a reverse proxy.'.format(unit_name))
        for service in services:
            hosts = service['hosts']
            for host in hosts:
                hookenv.log('{} has a unit {}:{}'.format(
                    service['service_name'],
                    host['hostname'],
                    host['port']))
        # Render a haproxy config template with services from this relation.
        haproxy.configure(unit_name, haproxy.TEMPLATE_NAME, services=services)


@when('config.changed.port')
def configure_port():
    """The port has changed, close old port and open a new one."""
    previous_port = hookenv.config().previous('port')
    if previous_port:
        hookenv.close_port(previous_port)
    hookenv.open_port(hookenv.config('port'))


@when('website.available')
def configure_website(website):
    """Implement the provides website contract by sending configured port."""
    website.configure(port=hookenv.config('port'))
