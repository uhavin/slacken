import asyncio
import logging

from pyee import BaseEventEmitter
from fastapi.encoders import jsonable_encoder


class NamedEventEmitter(BaseEventEmitter):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        return BaseEventEmitter.__init__(self, *args, **kwargs)


events = NamedEventEmitter(name="events")
actions = NamedEventEmitter(name="actions")
commands = NamedEventEmitter(name="commands")


def emit(emitter, event, payload):
    jsonable = jsonable_encoder(payload)
    log = logging.getLogger(__name__)
    log.info(f"Emitting '{event}' using emitter '{emitter.name}'")
    log.debug(jsonable)

    async def _emit_async(emitter, event, payload):
        emitter.emit(event, jsonable)

    loop = asyncio.get_event_loop()
    loop.create_task(_emit_async(emitter, event, payload))
