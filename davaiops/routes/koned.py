from flask import (
    current_app,
    render_template,
    Blueprint
)
from twilio.twiml.voice_response import (
    Dial,
    VoiceResponse,
    Number
)


koned = Blueprint('koned', __name__, url_prefix='/koned')


@koned.route('/')
def koned_home():
    return render_template('koned.html')


@koned.route('/incoming', methods=['GET', 'POST'])
def vota_vastu():
    """
    Docs: https://www.twilio.com/docs/voice/twiml/play#attributes-digits
    """
    response = VoiceResponse()
    response.say('This is an automated reception channel. Please hold.')
    response.play(digits='ww1w9')
    return str(response)
