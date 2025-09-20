from pathlib import Path
import requests


def cdn_downloader(url:str, out_path:Path, parent_mkdir:bool=True):
    if not isinstance(out_path, Path):
        raise ValueError(f"{out_path} must be valid pathlib Path object")
    if parent_mkdir:
        out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(url)
        response.raise_for_status()
        out_path.write_bytes(response.content)
        return True
    except requests.RequestException as e:
        print(f"{url} download for {e}")
        return False