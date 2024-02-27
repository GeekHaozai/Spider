import ddddocr

ocr = ddddocr.DdddOcr()  # import_onnx_path="myproject_0.984375_139_13000_2022-02-26-15-34-13.onnx", charsets_path="charsets.json")

with open('test.png', 'rb') as f:
    image_bytes = f.read()

res = ocr.classification(image_bytes)
print(res)
