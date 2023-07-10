from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import time
import wave

sipserver = "voip.amsmaine.com"
sipport = 5060
sipuser = "5130"
sippass = "6lUeu0xRXVjvhrZ7"

def answer(call):
    try:
        f = wave.open('page-encoded.wav', 'rb')
        frames = f.getnframes()
        data = f.readframes(frames)
        f.close()

        call.answer()
        call.write_audio(data)

        while call.state == CallState.ANSWERED:
            dtmf = call.get_dtmf()
            if dtmf == "1":
                # Do something
                call.hangup()
            elif dtmf == "2":
                # Do something else
                call.hangup()
            time.sleep(0.1)
    except InvalidStateError:
        pass
    except:
        call.hangup()

if __name__ == '__main__':
    phone = VoIPPhone(sipserver, sipport, sipuser, sippass, myIP="198.74.57.224", callCallback=answer)
    phone.start()
    input('Press enter to disable the phone')
    phone.stop()
