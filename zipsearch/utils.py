import json
from typing import Optional, List


def _decode_blob(blob_data: bytes) -> Optional[List[str]]:
    """Decode BLOB data (compressed JSON)."""
    if not blob_data:
        return None
    try:
        if blob_data.startswith(b'[') or blob_data.startswith(b'{'):
            return json.loads(blob_data.decode('utf-8'))
        import zlib
        decompressed = zlib.decompress(blob_data)
        return json.loads(decompressed.decode('utf-8'))
    except:
        return None
