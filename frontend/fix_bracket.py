with open("src/components/Timetable.jsx", "r", encoding="utf-8") as f:
    c = f.read()
c = c.replace("Click 'Dashboard' -> 'Create New Schedule' to get started.", "Click Dashboard and Create New Schedule to get started.")
with open("src/components/Timetable.jsx", "w", encoding="utf-8") as f:
    f.write(c)
print("done")
