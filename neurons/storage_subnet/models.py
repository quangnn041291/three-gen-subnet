import base64

from pydantic import BaseModel


class StoredData(BaseModel):
    assets: str  # Generated 3D assets (base64 encoded).
    miner: str  # Miner hotkey.
    validator: str  # Validator hotkey.
    prompt: str  # Prompt used for generation.

    submit_time: int  # time.time_ns() returned from miner.
    signature: str  # Miner signature: b64encode(sign(f'{submit_time}{prompt}{validator.hotkey}{miner.hotkey}'))

    def to_base64(self) -> str:
        return base64.b64encode(self.json().encode(encoding="utf-8")).decode(encoding="utf-8")

    @staticmethod
    def from_base64(serialized: str) -> "StoredData":
        return StoredData.parse_raw(base64.b64decode(serialized.encode(encoding="utf-8")).decode(encoding="utf-8"))
