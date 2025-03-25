import base64
import logging
import tomlkit


def get_attributes_from_pyproject():
    try:
        with open("pyproject.toml", "r", encoding="utf-8") as pyproject:
            project_data = tomlkit.parse(pyproject.read())
            project_info = project_data["project"]
            toml_params = {
                "version": project_info["version"],  # type: ignore
                "name": project_info["name"],  # type: ignore
                "description": project_info["description"],  # type: ignore
            }
            return toml_params
    except Exception as e:
        logging.error(f"Error reading version from pyproject.toml: {e}")
        return {}
    

def b64_encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


def b64_decode_image(image_bytes):
    return base64.b64decode(image_bytes)

def load_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
        base64_string = b64_encode_image(image_bytes)
    return base64_string