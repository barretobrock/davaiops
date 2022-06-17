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
    dial = Dial()
    dial.number(',,1,,9,,,,')
    response = VoiceResponse()
    response.say('This is an automated reception channel. Please hold.')
    response.play(digits='ww1wwwww9')
    response.append(dial)
    return str(response)
