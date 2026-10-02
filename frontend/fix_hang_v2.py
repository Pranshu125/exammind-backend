with open("src/components/UploadComponent.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("src/components/UploadComponent.jsx", "w", encoding="utf-8") as f:
    for line in lines:
        if "const storageRef = ref(storage" in line:
            continue
        if "await uploadBytes(storageRef" in line:
            continue
        f.write(line)
print("done")
