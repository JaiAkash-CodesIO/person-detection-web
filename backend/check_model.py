import onnxruntime as ort

session = ort.InferenceSession("models/best.onnx")

print("===== INPUTS =====")
for inp in session.get_inputs():
    print(f"Name : {inp.name}")
    print(f"Shape: {inp.shape}")
    print(f"Type : {inp.type}")
    print()

print("===== OUTPUTS =====")
for out in session.get_outputs():
    print(f"Name : {out.name}")
    print(f"Shape: {out.shape}")
    print(f"Type : {out.type}")
    print()