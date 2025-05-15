from pathlib import Path
project_root = Path(__file__).resolve().parent
project_root = str(project_root).replace("\\","/")

images_dir = project_root +"/downloads/images"
xmls =project_root +"/downloads/xmls"
output = project_root +"/output"
crop_dir = project_root +"/crop_image"