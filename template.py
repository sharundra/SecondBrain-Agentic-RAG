import os
from pathlib import Path

project_name = "app"

list_of_files = [

    f"{project_name}/__init__.py",
    f"{project_name}/core/__init__.py",
    f"{project_name}/core/config.py",  
    f"{project_name}/db/__init__.py",
    f"{project_name}/db/checkpointer.py",
    f"{project_name}/db/vector_store.py",
    f"{project_name}/graph/ingestion.py",
    f"{project_name}/tools/",
    ".env",
    "requirements.txt",
]


for filepath in list_of_files:
    fp = filepath
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if fp.endswith("/"):
        os.makedirs(filepath, exist_ok=True)
        continue
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at: {filepath}")