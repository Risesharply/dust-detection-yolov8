




class A():


    def __init__(self):

        self.a = 'A'
        self.b = 'B'
        self.curr_feat = 24


    def print(self, feat):
        """Update features vector and smooth it using exponential moving average."""
        feat += feat
        self.curr_feat = feat


b = A()
c = A()
print(b.a)
print(c.b)
