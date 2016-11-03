from Skill import Skill
import wikipedia

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
        furb.say_sync("I didn't understand you", interrupt=True)

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


def all(furb):
    """

    :param furb: the Furb.Furb to apply them to
    :return:  array of skills to use
    """

    return [
        WikipediaSkill(furb),
        WikipediaProSkill(furb),
        Echo(furb),
        What(furb)
    ]