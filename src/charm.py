#!/usr/bin/env python3
# Copyright 2021 Ben
# See LICENSE file for licensing details.

"""Charm the service."""

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import ActiveStatus


logger = logging.getLogger(__name__)


class SnappassTestCharm(CharmBase):
    """Charm the service."""

    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.snappass_workload_ready, self._on_snappass_workload_ready)
        self.framework.observe(self.on.redis_workload_ready, self._on_redis_workload_ready)
        self._stored.set_default(
            snappass_workload_ready=False,
            redis_started=False,
        )

    def _on_snappass_workload_ready(self, event):
        logger.info('_on_snappass_workload_ready')
        self._stored.snappass_workload_ready = True
        if self._stored.redis_started:
            # Redis started first, start snappass server now
            self._start_snappass()

    def _start_snappass(self):
        logger.info('_start_snappass')
        container = self.unit.containers['snappass']
        container.add_layer('snappass', """
summary: snappass layer
description: snappass layer
services:
    snappass:
        override: replace
        summary: snappass service
        command: snappass
        default: start
""")
        container.autostart()
        self.unit.status = ActiveStatus('snappass started')

    def _on_redis_workload_ready(self, event):
        logger.info('_on_redis_workload_ready')
        container = event.workload
        container.add_layer('redis', """
summary: redis layer
description: redis layer
services:
    redis:
        override: replace
        summary: redis service
        command: redis-server
        default: start
""")
        container.autostart()
        self.unit.status = ActiveStatus('redis started')
        self._stored.redis_started = True

        if self._stored.snappass_workload_ready:
            # If snappass container is ready, start snappass server,
            # otherwise wait for _on_snappass_workload_ready event.
            self._start_snappass()


if __name__ == "__main__":
    main(SnappassTestCharm)
