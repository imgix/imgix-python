try:
    # Python 3
    def b(s):
        return s.encode("latin-1")

except ImportError:
    # Python 2
    def b(s):
        return s
