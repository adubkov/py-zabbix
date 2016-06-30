# -*- encoding: utf-8 -*-
#
# Copyright © 2014 Alexey Dubkov
#
# This file is part of py-zabbix.
#
# Py-zabbix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Py-zabbix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with py-zabbix. If not, see <http://www.gnu.org/licenses/>.

import logging


class NullHandler(logging.Handler):
    """Null logger handler.

    :class:`NullHandler` will used if there are no other logger handlers.
    """

    def emit(self, record):
        pass
