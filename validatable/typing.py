import sys


if sys.version_info < (3, 7):
    from typing import GenericMeta, TupleMeta

    typing_meta = (GenericMeta, TupleMeta)

    def get_type(t):
        return t.mro()[1]


elif sys.version_info < (3, 9):
    from typing import _GenericAlias

    typing_meta = (_GenericAlias,)

    def get_type(t):
        return t.mro()[0]


else:
    from typing import _GenericAlias, _SpecialGenericAlias

    typing_meta = (_GenericAlias, _SpecialGenericAlias)

    def get_type(t):
        return t.mro()[0]
