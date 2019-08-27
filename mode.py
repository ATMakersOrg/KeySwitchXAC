class Mode(object):
    """Represents one of several interface modes"""

    BUTTON_PRESS=1
    DPAD_MOVE=2


    def __init__(self, name, color="#FFFFFF"):
        """Make an instance.
        :param string name: Name for reference and reporting
        :param string color: HEX code (hash optional) to light up on key presses on this mode
        """
        self.name=name
        self.color=color
        self.actions = {}

    def _addAction(self, switches, action):
        switchBits = 0x0
        if type(switches) is int:
            switchBits = 0x1 << switches
        elif isinstance(switches, (list, tuple)):
            for s in switches:
                sBits = 0x1 << s
                switchBits |= sBits
        self.actions[switchBits]= action

    def buttonPress(self, switches, buttonNum):
        self._addAction(switches, (Mode.BUTTON_PRESS, buttonNum))

    def dpadMove(self, switches, x, y):
        self._addAction(switches, (Mode.DPAD_MOVE, x, y))