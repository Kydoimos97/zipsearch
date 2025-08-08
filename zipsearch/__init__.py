# Import actual fast classes for direct access
from .FastSearchEngine import FastSearchEngine
from .FastZipcode import FastZipcode

# Import backwards compatible classes
from .boilerplate import (
    SearchEngine,  # Now points to FastSearchEngine
    SimpleZipcode,  # Now points to FastZipcode
    ComprehensiveZipcode,  # Now points to FastZipcode
    ZipcodeTypeEnum,
    SORT_BY_DIST,
    DEFAULT_LIMIT
    )

# All exports
__all__ = [
    'SearchEngine',        # Backwards compatible (now fast)
    'SimpleZipcode',       # Backwards compatible (now fast)
    'ComprehensiveZipcode', # Backwards compatible (now fast)
    'ZipcodeTypeEnum',
    'SORT_BY_DIST',
    'DEFAULT_LIMIT',
    'FastSearchEngine',    # Direct access to fast version
    'FastZipcode',         # Direct access to fast dataclass
]

