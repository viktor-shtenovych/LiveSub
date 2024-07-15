from flask import Blueprint, render_template
from flask_socketio import emit
from app import socketio
import azure.cognitiveservices.speech as speechsdk

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_transcription')
def start_transcription(data):
    print("Received start_transcription event")
    speech_key = "5728a1a9467d4ebb9aeb75a573736ee6"
    service_region = "eastus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    def process_result(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized Speech: ", evt.result.text)
            emit('transcription', {'text': evt.result.text})
        elif evt.result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized")
            emit('transcription', {'text': 'No speech could be recognized'})
        elif evt.result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = evt.result.cancellation_details
            print("Recognition canceled: ", cancellation_details.reason)
            emit('transcription', {'text': 'Recognition canceled: {}'.format(cancellation_details.reason)})

    speech_recognizer.recognized.connect(process_result)
    speech_recognizer.start_continuous_recognition()

    emit('status', {'message': 'Transcription started'})
    print("Transcription started")

    def stop_recognition():
        print("Stopping recognition")
        speech_recognizer.stop_continuous_recognition()

    # To stop the recognition after a certain period, use this line
    # socketio.sleep(30)  # Stop after 30 seconds for demo purposes
    # stop_recognition()
