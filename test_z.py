from roboflow import Roboflow
rf = Roboflow(api_key="YLK6lMqxJmuCDufEJYAR")
project = rf.workspace("zheng-kaigw").project("luekemia-cells")
version = project.version(2)
dataset = version.download("coco-segmentation")
