#!/usr/bin/env python3
# Copyright 2021 Ben
# See LICENSE file for licensing details.

"""Charm the service."""

import logging
import os
import re

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import ActiveStatus


logger = logging.getLogger(__name__)


LAYER_RE = re.compile(r'\d{3}-.+\.yaml')


def add_layer(container_name, layer_yaml, layer_name='layer',
              layers_dir_format='/charm/containers/{}/pebble/layers'):
    layers_dir = layers_dir_format.format(container_name)
    os.makedirs(layers_dir, exist_ok=True)

    layers = sorted(n for n in os.listdir(layers_dir) if LAYER_RE.match(n))
    if layers:
        last = int(layers[-1].split('-', 1)[0])
        assert 1 <= last <= 999, last
    else:
        last = 0
    filename = os.path.join(layers_dir, '{:03}-{}.yaml'.format(last + 1, layer_name))

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(layer_yaml)

    logger.info('wrote layer to {}'.format(filename))


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
            self._start_snappass()

    def _start_snappass(self):
        logger.info('_start_snappass')
        container = self.unit.containers['snappass']
        add_layer('snappass', """
summary: snappass layer
description: snappass layer
services:
    snappass:
        override: replace
        summary: snappass service
        command: snappass
""")
        container.start('snappass')
        self.unit.status = ActiveStatus('snappass started')

    def _on_redis_workload_ready(self, event):
        logger.info('_on_redis_workload_ready')
        container = self.unit.containers['redis']
        add_layer('redis', """
summary: redis layer
description: redis layer
services:
    redis:
        override: replace
        summary: redis service
        command: redis-server
""")
        container.start('redis')
        self.unit.status = ActiveStatus('redis started')
        self._stored.redis_started = True

        if self._stored.snappass_workload_ready:
            self._start_snappass()


if __name__ == "__main__":
    main(SnappassTestCharm)
