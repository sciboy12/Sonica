def InitKaldi():
    import dragonfly
    # Init Kaldi engine
    global engine
    engine = dragonfly.get_engine("kaldi", model_dir='kaldi_model')

    # Call connect() now that the engine configuration is set.
    engine.connect()

    # Voice command rule combining spoken form and recognition processing.
    grammar = dragonfly.Grammar('grammar') # Create a grammar to contain the command rules

    return engine, grammar

class Speech:
    import pyttsx3
    def say(text, rate=230):
        import pyttsx3
        tts = pyttsx3.init()
        tts.setProperty('rate', rate)

        tts.say(text)
        tts.runAndWait()
        
    def kaldi_recognize():
        engine, grammar = utils.InitKaldi()

