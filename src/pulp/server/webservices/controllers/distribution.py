#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2010 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.

import logging

import web

from pulp.server.api.distribution import DistributionApi
from pulp.server.webservices.controllers.base import JSONController
from pulp.server.webservices.role_check import RoleCheck

# globals ---------------------------------------------------------------------

api = DistributionApi()
log = logging.getLogger('pulp')

# controllers -----------------------------------------------------------------

class Distributions(JSONController):

    @JSONController.error_handler
    @RoleCheck(admin=True)
    def GET(self):
        """
        List all available distributions.
        @return: a list of all available distributions
        """
        distributions = api.distributions()

        return self.ok(distributions)

class Distribution(JSONController):

    @JSONController.error_handler
    @RoleCheck(admin=True)
    def GET(self, id):
        """
        Look up distribution by id.
        @param id: distribution id
        @return: distribution info
        """
        # implement filters
        return self.ok(api.distribution(id))

    @JSONController.error_handler
    @RoleCheck(admin=True)
    def PUT(self):
        """
        Create a new errata
        @return: errata that was created
        """
        distribution_data = self.params()
        distribution = api.create(distribution_data['id'],
                                  distribution_data['description'],
                                  distribution_data['relative_path'],
                                  distribution_data.get('files', []))
        return self.created(distribution['id'], distribution)

    def POST(self):
        # REST dictates POST to collection, and PUT to specific resource for
        # creation, this is the start of supporting both
        return self.PUT()

    @JSONController.error_handler
    @RoleCheck(admin=True)
    def DELETE(self):
        """
        @return: True on successful deletion of distribution
        """
        return self.ok(api.delete(id))
# web.py application ----------------------------------------------------------

URLS = (
    '/$', 'Distributions',
    '/([^/]+)/$', 'Distribution',
)

application = web.application(URLS, globals())
