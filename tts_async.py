from gtts import gTTS
import Queue
import threading
import urllib2

def stub(*args):
    return None


def tts_async(text, output_file="tts.mp3", done=stub):
    # called by each thread

    def make_req(q, url):
        q.put(urllib2.urlopen(url).read())

        def _tts():
            return


    theurls = ["http://google.com", "http://yahoo.com"]

    q = Queue.Queue()

    for u in theurls:
        t = threading.Thread(target=get_url, args=(q, u))
        t.daemon = True
        t.start()

    s = q.get()
    print s
