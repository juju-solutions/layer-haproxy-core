#!/usr/bin/env python3

# Copyright 2015 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess

from charms.apt import queue_install
from charms.reactive import when, when_not, set_state
from charms.reactive import data_changed
from charmhelpers.core import hookenv
from charmhelpers.core import unitdata
from charmhelpers.contrib.charmsupport import nrpe

from charms.layer import haproxy


@when_not('apt.installed.haproxy')
def install_haproxy():
    queue_install(['haproxy'])


@when('apt.installed.haproxy')
@when_not('haproxy.enabled')
def enable():
    """Ensure the software starts automatically on this system."""
    enable_haproxy()
    set_state('haproxy.enabled')


@when('apt.installed.haproxy')
def set_application_version():
    """Get the version of software deployed to the system."""
    version_string = subprocess.check_output(['haproxy', '-v'])
    version_array = version_string.split(b' ')
    if len(version_array) > 2:
        hookenv.application_version_set(version_array[2])


@when('haproxy.enabled', 'reverseproxy.available')
def update_reverseproxy_config(reverseproxy):
    """Get all the services and update the configuration to point to them."""
    services = reverseproxy.services()
    if data_changed('reverseproxy.services', services)
        for service in services:
            hookenv.log('{} has a unit {}:{}'.format(services['service_name'],
                                                     host['hostname'],
                                                     host['port']))

        haproxy.configure('haproxy.cfg',
                          services=services,
                          port=hookenv.config('port'))


def enable_haproxy():
    """Enable the haproxy service at boot time."""
    # Systemd services can be enabled using the systemctl command.
    return_code = subprocess.call(['systemctl', 'enable', 'haproxy'])
    if return_code != 0:
        hookenv.log('Enabling haproxy failed {}.'.format(return_code))
