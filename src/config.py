from pydantic import BaseModel, ConfigDict


class FileTypeConfig(BaseModel):
    suppress_extensions: list[str]


class CyantizeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    filetypes: FileTypeConfig
