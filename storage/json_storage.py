import json
from pathlib import Path
from typing import Any

class JSONStorage:
    def __init__(self, file_path: Path) -> None:
        self.file_path=file_path
        self.file_path.parent.mkdir(parents=True,exist_ok=True)

        if not self.file_path.exists():
            self.save([])

    def load(self) -> list[dict[str,Any]]:
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data=json.load(file) 

        except json.JSONDecoderError:
            raise ValueError(f"Invalid JSON format") from exc

        if not isinstance(data,list):
            raise ValueError(f"Invalid data format: expected a list of dictionaries")

        if not all(isinstance(item,dict)for item in data):
            raise ValueError(f"Each item in the list must be a dictionary")  

        return data

    def save(self,data:list[dict[str,Any]]) -> None:
        with self.file_path.open("w",encoding="utf-8") as file:
            json.dump(data,file,indent=4)
