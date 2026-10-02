with open("src/components/ProfileView.jsx", "r", encoding="utf-8") as f:
    content = f.read()

btn_code = """<div className="relative z-10 self-start md:self-end pb-2">
          <Link to="/settings" className="btn-base bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 px-4 py-2 rounded-xl flex items-center gap-2 font-medium shadow-sm transition-all">
            <Settings size={18} /> Edit Profile
          </Link>
        </div>"""

if btn_code in content:
    content = content.replace(btn_code, "")
    with open("src/components/ProfileView.jsx", "w", encoding="utf-8") as f:
        f.write(content)
print("done")
