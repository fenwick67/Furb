def default_test(text):
    return False

def default_handler(text):
    return ""

class Skill:
    def __init__(self, test=default_test, handle=default_handler):
        self.test=test
        self.handle=handle
        return

def handleSkills(skills,text):
    for skill in skills:
        if skill.test(text):
            skill.handle(text)
            break