from flask import (
    current_app,
    render_template,
    request,
    Blueprint
)
from twilio.twiml.voice_response import (
    Dial,
    VoiceResponse
)


koned = Blueprint('koned', __name__, url_prefix='/koned')


@koned.route('/')
def koned_home():
    current_app.logger.debug('Loaded /koned')
    return render_template('koned.html')


@koned.route('/incoming', methods=['GET', 'POST'])
def vota_vastu():
    """
    Docs: https://www.twilio.com/docs/voice/twiml/play#attributes-digits
    """
    response = VoiceResponse()
    caller = request.values.get('From')
    current_app.logger.info(f'Receiving call from: {caller}')
    allowlist = current_app.config.get('CALL_ALLOW_LIST', [])
    if caller not in allowlist:
        current_app.logger.info('Denying call that is not in allowlist...')
        response.reject()
    else:
        current_app.logger.info('Caller is in allowlist...')
        dial = Dial()
        dial.number(',1,,9,,')
        response.say('This is an automated reception channel. Please hold.')
        response.play(digits='ww1wwwww9')
        response.append(dial)
    current_app.logger.debug(f'Replying with {response}')
    return str(response)
