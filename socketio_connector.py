import logging
import uuid
from sanic import Blueprint, response
from socketio import AsyncServer
from typing import Optional, Text, Any
from gtts import gTTS

from rasa.core.channels.channel import InputChannel
from rasa.core.channels.channel import UserMessage, OutputChannel

import os
import time
import urllib
import speech_recognition as sr

logger = logging.getLogger(__name__)


def google_asr(audio_file):
    API_key = ""
    r = sr.Recognizer()
    with sr.WavFile(audio_file) as source:
        print("Say something!")
        audio = r.record(source)

    # Speech recognition using Google Speech Recognition
    start = time.time()
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = r.recognize_google(audio)
        print("You said: " + text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    end = time.time()
    print("Time taken:", end - start)
    return "Error"


class SocketBlueprint(Blueprint):
    def __init__(self, sio: AsyncServer, socketio_path, *args, **kwargs):
        self.sio = sio
        self.socketio_path = socketio_path
        super(SocketBlueprint, self).__init__(*args, **kwargs)

    def register(self, app, options):
        self.sio.attach(app, self.socketio_path)
        super(SocketBlueprint, self).register(app, options)


class SocketIOOutput(OutputChannel):

    @classmethod
    def name(cls):
        return "socketio"

    def __init__(self, sio, sid, bot_message_evt, message):
        self.sio = sio
        self.sid = sid
        self.bot_message_evt = bot_message_evt
        self.message = message

    async def _send_audio_message(self, socket_id, response, **kwargs: Any):
        # type: (Text, Any) -> None
        """Sends a message to the recipient using the bot event."""

        ts = time.time()
        OUT_FILE = str(ts) + '.wav'
        link = "http://localhost:8888/" + OUT_FILE

        language = 'en'
        voice = gTTS(text=response['text'], lang=language, slow=False)
        voice.save(OUT_FILE)

        # wav_norm = self.tts_predict(MODEL_PATH, response['text'], CONFIG, use_cuda, OUT_FILE)

        await self.sio.emit(self.bot_message_evt, {'text': response['text'], "link": link}, room=socket_id)

    async def send_text_message(self, recipient_id: Text, message: Text, **kwargs: Any) -> None:
        """Send a message through this channel."""

        await self._send_audio_message(self.sid, {"text": message})


class SocketIOInput(InputChannel):
    """A socket.io input channel."""

    @classmethod
    def name(cls):
        return "socketio"

    @classmethod
    def from_credentials(cls, credentials):
        credentials = credentials or {}
        return cls(credentials.get("user_message_evt", "user_uttered"),
                   credentials.get("bot_message_evt", "bot_uttered"),
                   credentials.get("namespace"),
                   credentials.get("session_persistence", False),
                   credentials.get("socketio_path", "/socket.io"),
                   )

    def __init__(self,
                 user_message_evt: Text = "user_uttered",
                 bot_message_evt: Text = "bot_uttered",
                 namespace: Optional[Text] = None,
                 session_persistence: bool = False,
                 socketio_path: Optional[Text] = '/socket.io'
                 ):
        self.bot_message_evt = bot_message_evt
        self.session_persistence = session_persistence
        self.user_message_evt = user_message_evt
        self.namespace = namespace
        self.socketio_path = socketio_path

    def blueprint(self, on_new_message):
        sio = AsyncServer(async_mode="sanic", cors_allowed_origins=[])
        socketio_webhook = SocketBlueprint(
            sio, self.socketio_path, "socketio_webhook", __name__
        )

        @socketio_webhook.route("/", methods=['GET'])
        async def health(request):
            return response.json({"status": "ok"})

        @sio.on('connect', namespace=self.namespace)
        async def connect(sid, environ):
            logger.debug("User {} connected to socketIO endpoint.".format(sid))
            print('Connected!')

        @sio.on('disconnect', namespace=self.namespace)
        async def disconnect(sid):
            logger.debug("User {} disconnected from socketIO endpoint."
                         "".format(sid))

        @sio.on('session_request', namespace=self.namespace)
        async def session_request(sid, data):
            print('This is session request')

            if data is None:
                data = {}
            if 'session_id' not in data or data['session_id'] is None:
                data['session_id'] = uuid.uuid4().hex
            await sio.emit("session_confirm", data['session_id'], room=sid)
            logger.debug("User {} connected to socketIO endpoint."
                         "".format(sid))

        @sio.on('user_uttered', namespace=self.namespace)
        async def handle_message(sid, data):

            output_channel = SocketIOOutput(sio, sid, self.bot_message_evt, data['message'])
            if data['message'] == "/get_started":
                message = data['message']
            else:
                ##receive audio
                received_file = 'output_' + sid + '.wav'

                urllib.request.urlretrieve(data['message'], received_file)
                path = os.path.dirname(__file__)

                message = google_asr(received_file)

                await sio.emit(self.user_message_evt, {"text": message}, room=sid)

            message_rasa = UserMessage(message, output_channel, sid,
                                       input_channel=self.name())
            await on_new_message(message_rasa)

        return socketio_webhook
