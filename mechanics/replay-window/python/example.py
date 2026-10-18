class ReplayWindow:
    def __init__(self,width=64):
        if width<=0: raise ValueError("nonpositive window")
        self.width=width; self.highest=-1; self.bits=0
    def accept(self,sequence):
        if type(sequence) is not int or sequence<0: return False
        if sequence>self.highest:
            shift=sequence-self.highest
            # Avoid allocating a huge integer for an attacker-chosen jump.
            self.bits=0 if shift>=self.width else (self.bits<<shift)&((1<<self.width)-1)
            self.bits|=1; self.highest=sequence; return True
        age=self.highest-sequence
        if age>=self.width or self.bits&(1<<age): return False
        self.bits|=1<<age; return True
