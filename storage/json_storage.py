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
        if not self.file_path.exists():
            return[]
        with open(self.file_path,"r", encoding="utf-8") as file:
            return json.load(file) 
        


    def save(self,data:list[dict[str,Any]]) -> None:
        with self.file_path.open("w",encoding="utf-8") as file:
            json.dump(data,file,indent=2)
