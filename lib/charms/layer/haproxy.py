import os
import subprocess

from charmhelpers.core import hookenv
from charmhelpers.core import host
from charmhelpers.core.templating import render


# The path and filename to render the configuration for the service.
ETC_HAPROXY_CONFIG = '/etc/haproxy/haproxy.cfg'
# The file in the templates directory to render for the service configuration.
TEMPLATE_NAME = 'haproxy.cfg'
# The service name to restart after a configuration change.
SERVICE_NAME = 'haproxy'


def configure(name, template, **kwargs):
    """Configure haproxy by rendering a jinja2 template, and restarting the
    service.
    Arguments:
    name: The name of the configuration rule to write.
    template: The name of the template file to use in the 'templates' directory
              of the charm.
    **kwargs: Additional dictionary items to append to the context that will
              show up in the template as variables.
    """
    if not template:
        template = TEMPLATE_NAME
    hookenv.status_set('maintenance',
                       'Configuring {} with {}'.format(SERVICE_NAME, template))
    context = {}
    context.update(hookenv.config())
    context['name'] = name
    context['bind_address'] = '0.0.0.0'
    context.update(**kwargs)

    if os.path.exists(ETC_HAPROXY_CONFIG):
        os.remove(ETC_HAPROXY_CONFIG)
    # Use charmhelpers to render a template from the 'templates' directory.
    render(source=template,
           target=ETC_HAPROXY_CONFIG,
           context=context)
    hookenv.log('Wrote {} config {} to {}'.format(SERVICE_NAME,
                                                  context,
                                                  ETC_HAPROXY_CONFIG))
    # Reload the haproxy service to get the configuration changes.
    reload()


def enable():
    """Enable the haproxy service so it starts at boot time."""
    # The haproxy package should be enabled by default, but make sure.
    hookenv.log('Enabling the {} service with systemctl'.format(SERVICE_NAME))
    # Systemd services can be enabled using the systemctl command.
    return_code = subprocess.call(['systemctl', 'enable', 'haproxy'])
    if return_code != 0:
        hookenv.log('Enabling haproxy failed {}.'.format(return_code))


def get_version():
    """Retrun a string with the version of software deployed to the system."""
    version_output = subprocess.check_output([SERVICE_NAME, '-v'])
    hookenv.log('Getting version from: {}'.format(version_output))
    version_array = version_output.split(b' ')
    version = ''
    if len(version_array) > 2:
        version = version_array[2]
    return version


def is_active():
    """Return True if this service is active as seen by systemctl."""
    return 0 == subprocess.call(['systemctl', 'is-active', SERVICE_NAME])


def is_enabled():
    """Return True if this system is enabled as seen by systemctl."""
    return 0 == subprocess.call(['systemctl', 'is-enabled', SERVICE_NAME])


def reload():
    """Reload the haproxy service on this host."""
    hookenv.log('Reloading the {} service on this host.'.format(SERVICE_NAME))
    host.service_reload(SERVICE_NAME)
