with open("src/components/Timetable.jsx", "r", encoding="utf-8") as f:
    c1 = f.read()

c1 = c1.replace(
    'className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-1 rounded-md border border-blue-100"',
    'className="inline-block text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-1 rounded-md border border-blue-100 leading-relaxed"'
)

c1 = c1.replace(
    'className="text-xs font-bold uppercase tracking-wider text-purple-600 bg-purple-50 px-2 py-1 rounded-md border border-purple-100"',
    'className="inline-block text-xs font-bold uppercase tracking-wider text-purple-600 bg-purple-50 px-2 py-1 rounded-md border border-purple-100 whitespace-nowrap"'
)

with open("src/components/Timetable.jsx", "w", encoding="utf-8") as f:
    f.write(c1)

with open("src/components/SyllabusTracker.jsx", "r", encoding="utf-8") as f:
    c2 = f.read()

c2 = c2.replace(
    '<div className="flex items-center gap-2 mb-1.5">',
    '<div className="flex flex-wrap items-center gap-2 mb-1.5">'
)
c2 = c2.replace(
    'className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded"',
    'className="inline-block text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded leading-relaxed"'
)
c2 = c2.replace(
    'className="text-xs font-bold uppercase tracking-wider text-purple-600 bg-purple-50 px-2 py-0.5 rounded"',
    'className="inline-block text-xs font-bold uppercase tracking-wider text-purple-600 bg-purple-50 px-2 py-0.5 rounded leading-relaxed"'
)

with open("src/components/SyllabusTracker.jsx", "w", encoding="utf-8") as f:
    f.write(c2)

print("done")
