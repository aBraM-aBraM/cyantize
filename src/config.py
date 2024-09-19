from pydantic import BaseModel, ConfigDict


class FileTypeConfig(BaseModel):
    filetypes: dict[str, str]


class CyantizeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    filetypes: FileTypeConfig
