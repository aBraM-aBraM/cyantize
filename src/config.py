from pydantic import BaseModel, ConfigDict


class CyantizeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    filetypes: dict[str, str]
