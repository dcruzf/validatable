import sys

if sys.version_info < (3, 7):
    from typing import GenericMeta, TupleMeta

    typing_meta = (GenericMeta, TupleMeta)

    def get_type(t):
        return t._gorg.mro()[1]


elif sys.version_info < (3, 9):
    from typing import _GenericAlias  # type: ignore[attr-defined]
    from typing import _VariadicGenericAlias  # type: ignore[attr-defined]

    typing_meta = (_GenericAlias, _VariadicGenericAlias)

    def get_type(t):
        return t.__origin__


else:
    from typing import _GenericAlias  # type: ignore[attr-defined]
    from typing import _SpecialGenericAlias  # type: ignore[attr-defined]
    from typing import _TupleType  # type: ignore[attr-defined]

    typing_meta = (_GenericAlias, _SpecialGenericAlias, _TupleType)

    def get_type(t):
        return t.__origin__
