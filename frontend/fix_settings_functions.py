import re

with open("src/components/SettingsView.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports Update
content = content.replace(
    "import { updateProfile, updatePassword } from 'firebase/auth';",
    "import { updateProfile, updatePassword, deleteUser, linkWithPopup, GoogleAuthProvider, GithubAuthProvider } from 'firebase/auth';"
)

# 2. Add handlers for Export, Delete, and Link
handlers_code = """  const handleImageUpload = async (e) => {"""
new_handlers = """  const handleExportData = async () => {
    try {
      const docRef = doc(db, 'users', currentUser.uid);
      const snap = await getDoc(docRef);
      const data = snap.exists() ? snap.data() : { profile: formData };
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `exammind_backup_${currentUser.uid}.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      alert('Error exporting data: ' + err.message);
    }
  };

  const handleDeleteAccount = async () => {
    if (window.confirm("WARNING: This will permanently delete your account and all associated data. This action CANNOT be undone. Are you absolutely sure?")) {
      try {
        await deleteUser(currentUser);
      } catch (err) {
        alert("Failed to delete account. For security reasons, you may need to sign out and sign back in before deleting your account.\\n\\nError: " + err.message);
      }
    }
  };

  const handleLinkAccount = async (providerName) => {
    try {
      let provider;
      if (providerName === 'google') provider = new GoogleAuthProvider();
      if (providerName === 'github') provider = new GithubAuthProvider();
      
      await linkWithPopup(currentUser, provider);
      alert(`Successfully linked ${providerName} account!`);
      await currentUser.reload();
    } catch (err) {
      alert(`Failed to link ${providerName} account: ` + err.message);
    }
  };

  const handleImageUpload = async (e) => {"""
content = content.replace(handlers_code, new_handlers)

# 3. Attach handlers to JSX
# Replace Link Google
content = content.replace(
    """<button type="button" className="text-sm font-bold text-blue-600 hover:underline">Link</button>""",
    """<button type="button" onClick={() => handleLinkAccount('google')} className="text-sm font-bold text-blue-600 hover:underline">Link</button>""",
    1 # Only first one (Google)
)
# Replace Link Github
content = content.replace(
    """<button type="button" className="text-sm font-bold text-blue-600 hover:underline">Link</button>""",
    """<button type="button" onClick={() => handleLinkAccount('github')} className="text-sm font-bold text-blue-600 hover:underline">Link</button>""",
    1 # Second one (Github)
)
# Replace Export
content = content.replace(
    """<button type="button" onClick={() => alert('Exporting data...')} className="bg-gray-100 text-gray-800 px-6 py-3 rounded-xl font-bold shadow-sm hover:bg-gray-200 transition-colors flex items-center gap-2">""",
    """<button type="button" onClick={handleExportData} className="bg-gray-100 text-gray-800 px-6 py-3 rounded-xl font-bold shadow-sm hover:bg-gray-200 transition-colors flex items-center gap-2">"""
)
# Replace Delete
content = content.replace(
    """<button onClick={() => alert('Delete account triggered. Require confirmation modal.')} className="bg-red-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-red-700 flex items-center gap-2 transition-colors shadow-sm">""",
    """<button onClick={handleDeleteAccount} className="bg-red-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-red-700 flex items-center gap-2 transition-colors shadow-sm">"""
)

with open("src/components/SettingsView.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
