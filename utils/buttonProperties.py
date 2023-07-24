class ButtonProperties:
    def __init__(self, assigned_key, note,sound_to_play):
        self._assigned_key = assigned_key
        self._note = note
        self._sound_to_play = sound_to_play

    @property
    def assigned_key(self):
        return self._assigned_key

    @property
    def note(self):
        return self._note

    @property
    def sound_to_play(self):
        return self._sound_to_play
