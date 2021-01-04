class Functor:
    def __call__(self):
        result = type(str(), (), {})
        result.a = 1
        result.b = 2
        def init(self):
            self.c = 3
            self.d = 4
        result.__init__ = init
        return result

res = Functor()
res = res()
inst = res()
print(res.a)