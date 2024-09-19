from pydantic import BaseModel


class CyantizeState(BaseModel):
    processed_file_count: int = 0


g_state = CyantizeState()
