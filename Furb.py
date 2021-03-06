import pyglet
import speech_recognition as sr
from gtts import gTTS
import pyttsx

import threading
import os
import time
# from RPi.GPIO import GPIO

def stub(*args):
    return None

class Furb():
    """
    Furb's main loop looks like this:
    * listen
    * test skills
    * use the skill that matches first
    * run the skill's "handle" function
        => skill's handle function does whatever, eventually returns to give control back to loop

    """

    def enqueue_media(self, media_source, interrupt=False):
        if self.player.source is not None and interrupt is False:
            self.player.queue(media_source)
            return    # don't interrupt play in progress
        else:
            if self.player.playing:
                self.player.queue(media_source)
                self.player.next_source()
            else:
                self.player.queue(media_source)
                self.player.play()


    def set_interval(self, function=stub, interval=1.0):
        """
        Add a task to the pyglet event loop

        :param function: the function to call
        :param interval: the interval at which to call it (Seconds)
        :return: None
        """

        pyglet.clock.schedule_interval(function,interval)

    def run(self):

        def _handle(speech):
            for skill in self.skills:
                if skill.test(speech):
                    skill.handle(speech)
                    break

        while(True):

            # wait for activation
            while(True):
                if self.poll_activation():
                    break
                else:
                    time.sleep(100)

            self.greet()

            r = sr.Recognizer()
            with sr.Microphone(sample_rate=44100) as source:
                print("listening")
                audio = r.listen(source)
                try:
                    print("processing")
                    what_i_said = r.recognize_google(audio)
                    print("Google Speech Recognition: " + what_i_said)
                    _handle(what_i_said)
                except sr.UnknownValueError:
                    self.what()
                    print("Google Speech Recognition could not understand your audio")
                except sr.RequestError as e:
                    self.what()
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))


    def say_sync(self, text, interrupt=False):
        self.speech_thread = threading.Thread(
            target=self._say_thread_2,
            kwargs={"text":text, "interrupt":interrupt},
        )
        self.speech_thread.run()

    def _say_thread(self,text="default text.",interrupt=False):
        print("GONNA SAY "+text)
        self.speech_lock.acquire()
        tts = gTTS(text=text, lang="en-us")
        tts.save("output_tts.mp3")
        # speech = pyglet.media.load('output_tts.mp3', streaming=False)
        os.system("vlc --play-and-exit output_tts.mp3")
        print("I SAID IT")
        self.speech_lock.release()

    def _say_thread_2(self,text="default",interrupt=False):
        print(u"GONNA SAY " + text)
        # get text in ASCII
        t=text.encode('ascii', 'replace').replace('"','\"')

        self.speech_lock.acquire()
        os.system('espeak -g 2 -p 50 "{0}"'.format(t))
        print("I SAID IT")
        self.speech_lock.release()

    def __init__(self):
        print("WA")
        self.player = pyglet.media.Player()
        self.player.play()
        self.speech_thread = None
        self.speech_lock = threading.Lock()

        self.pyglet_thread=threading.Thread(target=pyglet.app.run)

    # Stuff below this is ripe for overriding

    def greet(self):
        # overwrite this if you'd like
        self.say_sync("coo coo",False)

    def what(self):
        self.say_sync("Sorry, I didn't understand that.",False)

    def poll_activation(self):
        """
        poll activation circuit (button, piezo etc)

        polls every 100ms

        if you need faster activation, start your own thread and poll on your own

        :return: True when button is pushed
        """

        return True
