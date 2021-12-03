import dragonfly
#from dragonfly import Text
import sys
from functools import partial
import utils
##def utils():
##    def InitKaldi():
##        # Init Kaldi engine
##        global engine
##        engine = dragonfly.get_engine("kaldi", model_dir='kaldi_model')
##
##        # Call connect() now that the engine configuration is set.
##        engine.connect()
##
##        # Voice command rule combining spoken form and recognition processing.
##        grammar = dragonfly.Grammar('grammar') # Create a grammar to contain the command rules
##
##        return engine, grammar
##
##    class Speech:
##        def say(text, rate=230):
##            import pyttsx3
##            tts = pyttsx3.init()
##            tts.setProperty('rate', rate)
##
##            tts.say(text)
##            tts.runAndWait()
##            
##        def kaldi_recognize():
##            engine2, grammar = utils.InitKaldi()
#def AskSkill():
    
    
def LaunchSkill(text):
    global idle
    if not idle:
        import importlib
        try:
            print(text)
            module = importlib.import_module(text)
            module.main()
            ToIdle()
        except:
            ToIdle()
    
def ToIdle():
    global idle
    idle = True
    IdleState()
    
def IdleState():
    print("Idle")
    global engine
    global idle

    if not idle:
        idle = True
        
    engine.do_recognition()

def MenuState():
    global idle
    if idle:
        idle = False
    else:
        return

    print("Menu")
    engine.do_recognition()


# List of commands
class MappingRule(dragonfly.MappingRule):
    
    mapping = {"computer": dragonfly.Function(MenuState)}
    
##class MappingRule(dragonfly.MappingRule):
##    mapping = {"computer": dragonfly.Function(MenuState)}

class MenuRule(dragonfly.MappingRule):
    conjunctions = "if|when|where|whether|why|how"
    mapping = {
        "cancel": dragonfly.Function(lambda engine: ToIdle()),
        "what time is it": dragonfly.Function(LaunchSkill, skill="time.SpeakTime"),
        "open <skill>": dragonfly.Function(lambda skill: LaunchSkill(skill)),
        "ask <skill> "+conjunctions+" <cmd>": dragonfly.Function(lambda skill, cmd: AskSkill(skill, cmd))
    }

    extras = [
        dragonfly.Dictation("skill"),
        dragonfly.Dictation("cmd")
    ]
    
def main():
    # Init Kaldi engine
    global engine
    engine, grammar = utils.InitKaldi()
##    engine = dragonfly.get_engine("kaldi", model_dir='kaldi_model')
##
##    # Call connect() now that the engine configuration is set.
##    engine.connect()
##
##    # Voice command rule combining spoken form and recognition processing.
##    grammar = dragonfly.Grammar('grammar') # Create a grammar to contain the command rules 
##
    # Add the command rule to the grammar.
    grammar.add_rule(MappingRule())
    grammar.add_rule(MenuRule())
    grammar.load()
    
    sys.path.append("./skills")

    # Enter recognition loop
    print('Ready')

    global idle
    idle = True
    
    IdleState()
    
if __name__ == "__main__":
    main()
