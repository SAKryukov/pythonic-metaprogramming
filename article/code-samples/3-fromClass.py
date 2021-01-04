class NamedDictionary:

# ...

    # Not really needed, because any suitable class can be directly passed to Merge
    @classmethod
    def FromClass(cls, definitionSetClass):
        return cls.Merge(cls, definitionSetClass)

# ...
