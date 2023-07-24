class ButtonTimerProperties:
    def __init__(self, assigned_key, function):
        self._assigned_key = assigned_key
        self._function = function

    @property
    def assigned_key(self):
        return self._assigned_key

    @property
    def function(self):
        return self._function
