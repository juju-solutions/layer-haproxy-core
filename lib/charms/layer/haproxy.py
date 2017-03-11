from charmhelpers.core.templating import render
from charmhelpers.core import hookenv
from charmhelpers.core import host

import os


ETC_HAPROXY_CONFIG = '/etc/haproxy/haproxy.cfg'


def configure(template, **kwargs):
    """Configure haproxy using a jinja2 template.
    Arguments:
    template: The name of the template to use in the 'templates' directory of
              the charm.
    **kwargs: Additional dicttionary items to append to template variables
              exposed through the site.toml
    """
    hookenv.status_set('maintenance',
                       'Configuring haproxy with {}'.format(template))

    context = {}

    context.update(hookenv.config())
    context.update(**kwargs)

    if os.path.exists(ETC_HAPROXY_CONFIG):
        os.remove(ETC_HAPROXY_CONFIG)
    # Use charmhelpers to render the template from the 'templates' directory.
    render(source=template,
           target=ETC_HAPROXY_CONFIG,
           context=context)
    hookenv.log('Wrote haproxy config {} to {}'.format(context, template),
                'info')
    # Reload the haproxy service.
    host.service_reload('haproxy')
