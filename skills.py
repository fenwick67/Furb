from Skill import Skill
import wikipedia
import requests
import secrets
import math

def rint(n=0):
    # rounded int casting
    return int(round(float(n)))

def Echo(furb):

    def test(st):
        if "say" in st:
            return True
        return False

    def handle(st):
        furb.say_sync(str(st).replace("say","")+".", interrupt=True)

    return Skill(test=test,handle=handle)

def What(furb):
    def test(st):
        return True
    def handle(st):
        furb.say_sync("I don't know what to do with that.", interrupt=True)

    return Skill(test=test, handle=handle)


def WikipediaSkill(furb):

    def test(st):
        s = str(st)
        if "tell me about" in s:
            return True
        return False

    def handle(st):
        wikipedia.set_lang("simple")
        sum = wikipedia.summary(st.replace("tell me about",""), sentences=2)
        furb.say_sync(sum, interrupt=True)

    return Skill(test=test,handle=handle)

def WikipediaProSkill(furb):

    def test(st):
        s = str(st)
        if "tell me more about" in s:
            return True
        return False

    def handle(st):
        wikipedia.set_lang("en")
        sum = wikipedia.summary(st.replace("tell me more about",""), sentences=2)
        furb.say_sync(sum, interrupt=True)

    return Skill(test=test,handle=handle)

def WeatherSkill(furb):

    """
    Supports weather for now, today, tomorrow, this week

    """

    def test(s):
        if "weather" in s or "temperature" in s or "outside" in s:
            return True
        return False

    def handle(s):
        # always a GET to weather endpoint
        r = requests.get("https://api.darksky.net/forecast/"+secrets.darksky_key+"/"+secrets.lat_lon+"?exclude=hourly,minutely")
        if r.status_code < 200 or r.status_code >= 400:
            furb.say_sync("Sorry, I can't get the weather right now.")
            return
        j = r.json()

        if "week" in s:
            # weather for this week
            result=j[u"daily"][u"summary"]
            furb.say_sync("This week's weather: "+result)
            return

        elif "now" in s:
            result=j[u"currently"]
            say = "It is currently {0} and {1} degrees.  Chance of precipitation: {2} percent.".format(result[u"summary"],rint(result[u"temperature"]),rint(result[u"precipProbability"]))
            furb.say_sync(say)

        elif "today" in s:
            result = j[u"daily"][u"data"][0]
            say = "Today will be {0}, with a high of {1} and low of {2}.  Chance of precipitation: {3} percent.".format(
                result[u"summary"], rint(result[u"temperatureMax"]) ,rint(result[u"temperatureMin"]), rint(result[u"precipProbability"]))
            furb.say_sync(say)

        elif "tomorrow" in s:
            result = j[u"daily"][u"data"][1]
            say = "Tomorrow will be {0}, with a high of {1} and low of {2}.  Chance of precipitation: {3} percent.".format(
                result[u"summary"], rint(result[u"temperatureMax"]), rint(result[u"temperatureMin"]), rint(result[u"precipProbability"]))
            furb.say_sync(say)

        else:
            furb.say_sync("Sorry, try asking for the weather right now, for today, tomorrow, or this week.")

    return Skill(test=test,handle=handle)

def all(furb):
    """

    :param furb: the Furb.Furb to apply them to
    :return:  array of skills to use
    """

    return [
        WeatherSkill(furb),
        WikipediaSkill(furb),
        WikipediaProSkill(furb),
        Echo(furb),
        What(furb)
    ]
