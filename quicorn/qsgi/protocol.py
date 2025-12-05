from asyncio import Queue

from aioquic.asyncio import QuicConnectionProtocol

from aioquic.quic.events import QuicEvent, StreamDataReceived

from quicorn.logger import logger
from quicorn.qsgi.context import qsqi_queue_var


class QSGIProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def echo(self, event: StreamDataReceived) -> None:
        logger.debug(event)
        self._quic.send_stream_data(stream_id=event.stream_id, data=event.data)

    def quic_event_received(self, event: QuicEvent):
        queue: Queue = qsqi_queue_var.get()
        if isinstance(event, StreamDataReceived):
            queue.put_nowait(event)

            # stream: QuicStream = self._quic._streams.get(event.stream_id)
            # stream.sender.write(data=f'PONG | {extra}'.encode(), end_stream=True)
            # logger.info(f'STREAM: {stream}')
            # logger.info(f'SENDER: {stream.sender}')
            # logger.info(f'RECEIVER: {stream.receiver}')
