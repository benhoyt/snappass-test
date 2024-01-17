# Copyright 2024 Ben Hoyt
# See LICENSE file for licensing details.

import scenario
from ops import pebble

from src.charm import SnappassTestCharm

SNAPPASS_LAYER = {
    "summary": "snappass layer",
    "description": "snappass layer",
    "services": {
        "snappass": {
            "override": "replace",
            "summary": "snappass service",
            "command": "snappass",
            "startup": "enabled",
        }
    },
}

REDIS_LAYER = {
    "summary": "redis layer",
    "description": "redis layer",
    "services": {
        "redis": {
            "override": "replace",
            "summary": "redis service",
            "command": "redis-server",
            "startup": "enabled",
        }
    },
}


def test_snappass_pebble_ready_redis_not_started():
    # Arrange
    ctx = scenario.Context(SnappassTestCharm)
    snappass_container = scenario.Container(
        name="snappass",
        can_connect=True,
    )
    redis_container = scenario.Container(
        name="redis",
        can_connect=True,
    )
    state = scenario.State(
        containers=[snappass_container, redis_container],
    )

    # Act
    out = ctx.run(snappass_container.pebble_ready_event, state)

    # Assert
    assert out.unit_status.name == "unknown"


def test_snappass_pebble_ready_redis_started():
    # Arrange
    ctx = scenario.Context(SnappassTestCharm)
    snappass_container = scenario.Container(
        name="snappass",
        can_connect=True,
    )
    redis_container = scenario.Container(
        name="redis",
        can_connect=True,
        layers={"redis": pebble.Layer(REDIS_LAYER)},
        service_status={"redis": pebble.ServiceStatus.ACTIVE},
    )
    state = scenario.State(
        containers=[snappass_container, redis_container],
    )

    # Act
    out = ctx.run(snappass_container.pebble_ready_event, state)

    # Assert
    assert out.unit_status.name == "active"
    assert "snappass started" in out.unit_status.message
    assert out.containers[0] == scenario.Container(
        name="snappass",
        can_connect=True,
        layers={"snappass": pebble.Layer(SNAPPASS_LAYER)},
        service_status={"snappass": pebble.ServiceStatus.ACTIVE},
    )


def test_snappass_pebble_ready_already_started():
    # Arrange
    ctx = scenario.Context(SnappassTestCharm)
    snappass_container = scenario.Container(
        name="snappass",
        can_connect=True,
        layers={"snappass": pebble.Layer(SNAPPASS_LAYER)},
        service_status={"snappass": pebble.ServiceStatus.ACTIVE},
    )
    redis_container = scenario.Container(
        name="redis",
        can_connect=True,
        layers={"redis": pebble.Layer(REDIS_LAYER)},
        service_status={"redis": pebble.ServiceStatus.ACTIVE},
    )
    state = scenario.State(
        containers=[snappass_container, redis_container],
    )

    # Act
    out = ctx.run(snappass_container.pebble_ready_event, state)

    # Assert
    assert out.unit_status.name == "unknown"
    assert out.containers[0] == scenario.Container(
        name="snappass",
        can_connect=True,
        layers={"snappass": pebble.Layer(SNAPPASS_LAYER)},
        service_status={"snappass": pebble.ServiceStatus.ACTIVE},
    )


def test_redis_pebble_ready_redis_already_started():
    # Arrange
    ctx = scenario.Context(SnappassTestCharm)
    snappass_container = scenario.Container(
        name="snappass",
        can_connect=True,
    )
    redis_container = scenario.Container(
        name="redis",
        can_connect=True,
        layers={"redis": pebble.Layer(REDIS_LAYER)},
        service_status={"redis": pebble.ServiceStatus.ACTIVE},
    )
    state = scenario.State(
        containers=[snappass_container, redis_container],
    )

    # Act
    out = ctx.run(redis_container.pebble_ready_event, state)

    # Assert
    assert out.unit_status.name == "unknown"


def test_redis_pebble_ready_redis_not_started():
    # Arrange
    ctx = scenario.Context(SnappassTestCharm)
    snappass_container = scenario.Container(
        name="snappass",
        can_connect=True,
        layers={"snappass": pebble.Layer(SNAPPASS_LAYER)},
        service_status={"snappass": pebble.ServiceStatus.ACTIVE},
    )
    redis_container = scenario.Container(
        name="redis",
        can_connect=True,
    )
    state = scenario.State(
        containers=[snappass_container, redis_container],
    )

    # Act
    out = ctx.run(redis_container.pebble_ready_event, state)

    # Assert
    assert out.unit_status.name == "active"
    assert "redis started" in out.unit_status.message
    assert out.containers[1] == scenario.Container(
        name="redis",
        can_connect=True,
        layers={"redis": pebble.Layer(REDIS_LAYER)},
        service_status={"redis": pebble.ServiceStatus.ACTIVE},
    )


def test_redis_pebble_ready_neither_started():
    # Arrange
    ctx = scenario.Context(SnappassTestCharm)
    snappass_container = scenario.Container(
        name="snappass",
        can_connect=True,
    )
    redis_container = scenario.Container(
        name="redis",
        can_connect=True,
    )
    state = scenario.State(
        containers=[snappass_container, redis_container],
    )

    # Act
    out = ctx.run(redis_container.pebble_ready_event, state)

    # Assert
    assert out.unit_status.name == "active"
    assert "snappass started" in out.unit_status.message
    assert out.containers[0] == scenario.Container(
        name="snappass",
        can_connect=True,
        layers={"snappass": pebble.Layer(SNAPPASS_LAYER)},
        service_status={"snappass": pebble.ServiceStatus.ACTIVE},
    )
    assert out.containers[1] == scenario.Container(
        name="redis",
        can_connect=True,
        layers={"redis": pebble.Layer(REDIS_LAYER)},
        service_status={"redis": pebble.ServiceStatus.ACTIVE},
    )
