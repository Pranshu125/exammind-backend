with open("src/components/UploadComponent.jsx", "r", encoding="utf-8") as f:
    content = f.read()

import re

old_footer = """             {Object.keys(extractedTopics).length > 0 && (
               <div className="mt-10 pt-6 border-t border-gray-200 flex justify-end">
                 <button 
                   onClick={handleGenerateMasterPlan}
                   disabled={generatingPlan}
                   className="btn-primary py-3 px-8 text-base shadow-md disabled:opacity-50 flex items-center"
                 >
                   {generatingPlan ? <><Loader2 className="animate-spin mr-2" size={20}/> Generating AI Schedule...</> : <><Sparkles className="mr-2" size={20}/> Generate Master Schedule</>}
                 </button>
               </div>
             )}"""

new_footer = """             <div className="mt-10 pt-6 border-t border-gray-200 flex flex-col items-end">
                 {Object.keys(extractedTopics).length === 0 && (
                     <p className="text-sm text-gray-500 mb-2">Extract topics for at least one subject above to generate your plan.</p>
                 )}
                 <button 
                   onClick={handleGenerateMasterPlan}
                   disabled={generatingPlan || Object.keys(extractedTopics).length === 0}
                   className="btn-primary py-3 px-8 text-base shadow-md disabled:opacity-50 flex items-center transition-all"
                 >
                   {generatingPlan ? <><Loader2 className="animate-spin mr-2" size={20}/> Generating AI Schedule...</> : <><Sparkles className="mr-2" size={20}/> Generate Master Schedule</>}
                 </button>
             </div>"""

content = content.replace(old_footer, new_footer)

with open("src/components/UploadComponent.jsx", "w", encoding="utf-8") as f:
    f.write(content)

print("done")
