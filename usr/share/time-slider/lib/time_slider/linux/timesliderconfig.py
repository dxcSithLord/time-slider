#!/usr/bin/python3
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#

import configparser
import sys
import time_slider.util as util

# Default config file name position
configfile = "/etc/time-slider/timesliderd.conf"

# Default values
default_properties = {
    'application/time-slider': {
        'zpool/emergency-level': 95,
        'zpool/critical-level': 90,
        'zpool/warning-level': 80,
        'zfs/sep': '_',
        'daemon/verbose': 'true',
        'state': 'online',
    },
    'system/filesystem/zfs/auto-snapshot:monthly': {
        'zfs/interval': 'months',
        'zfs/period': 1,
        'zfs/keep': 2,
        'state': 'online',
    },
    'system/filesystem/zfs/auto-snapshot:weekly': {
        'zfs/interval': 'days',
        'zfs/period': 7,
        'zfs/keep': 4,
        'state': 'online',
    },
    'system/filesystem/zfs/auto-snapshot:daily': {
        'zfs/interval': 'days',
        'zfs/period': 1,
        'zfs/keep': 6,
        'state': 'online',
    },
    'system/filesystem/zfs/auto-snapshot:hourly': {
        'zfs/interval': 'hours',
        'zfs/period': 1,
        'zfs/keep': 23,
        'state': 'online',
    },
    'system/filesystem/zfs/auto-snapshot:frequent': {
        'zfs/interval': 'minutes',
        'zfs/period': 15,
        'zfs/keep': 3,
        'state': 'online',
    },
}

class MyConfigParser(configparser.ConfigParser):
    def __init__(self):
        configparser.ConfigParser.__init__(self)

        for section, content in default_properties.items():
            if not self.has_section(section):
                self.add_section(section)
            for k,v in content.items():
                self.set(section, k, str(v))

class Config:
    def __init__(self):
        self.config = MyConfigParser()
        self.config.read(configfile)

    def get(self, section, option):
        try:
            result = self.config.get(section, option)
            util.debug('CONFIG: GET section %s, option %s with value %s\n' % (section, option, result), 1)
            return result
        except (configparser.NoOptionError, configparser.NoSectionError):
            util.debug('CONFIG: NOTFOUND section %s, option %s\n' % (section, option), 1)
            return ''

    def sections(self):
        return self.config.sections()

def configdump():
    MyConfigParser().write(sys.stdout)
