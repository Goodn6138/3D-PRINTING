from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="YLK6lMqxJmuCDufEJYAR"
)

result = CLIENT.infer(r"C:\Users\Admin\Downloads\blank-scope-export\training\image4_2.jpg.4v3nqh99.ingestion-f69c99576-dhxn4.jpg", model_id="wbc-6fwys/2")
