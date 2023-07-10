from pyVoIP.VoIP import VoIPPhone, InvalidStateError, CallState
import sys
import time
import wave
import subprocess

phonenumber = sys.argv[1]
pagetext = sys.argv[2]

text_str = pagetext + pagetext + pagetext + pagetext + pagetext + pagetext + pagetext + pagetext + pagetext + pagetext + pagetext + pagetext
text_str = text_str + text_str
text_str = text_str[:1000]
cmd_str = "pico2wave -w=/code/pyVoIP/page.wav '" + text_str + "'  > /dev/null 2>&1"
subprocess.run(cmd_str, shell=True)
cmd_str = "ffmpeg -y -i /code/pyVoIP/page.wav -ar 8000 -ac 1 -acodec pcm_u8 /code/pyVoIP/page-encoded.wav  > /dev/null 2>&1"
subprocess.run(cmd_str, shell=True)

sipserver = "voip.amsmaine.com"
sipport = 5060
sipuser = "5130"
sippass = "6lUeu0xRXVjvhrZ7"
retval = ""

def answer(call):
    try:
        call.answer()
        time.sleep(1)
        call.hangup()
    except InvalidStateError:
        pass
    except:
        call.hangup()

if __name__ == "__main__":
    phone = VoIPPhone(sipserver, sipport, sipuser, sippass, myIP="198.74.57.224", callCallback=answer)
    phone.start()
    call = phone.call(phonenumber)

    try:
        f = wave.open("/code/pyVoIP/page-encoded.wav", "rb")
        frames = f.getnframes()
        data = f.readframes(frames)
        f.close()

        stop = time.time() + (frames / 8000)  # frames/8000 is the length of the audio in seconds. 8000 is the hertz of PCMU.
        runonce = False

        while True:
            if call.state == CallState.ANSWERED:
                if runonce == False:
                    call.write_audio(data)
                    retval = True
                    runonce = True
            time.sleep(0.1)
            if time.time() > stop:
                break
            if call.state == CallState.ENDED:
                break
        call.hangup()
    except InvalidStateError:
        pass
    except:
        call.hangup()

    phone.stop()

    print(retval)
