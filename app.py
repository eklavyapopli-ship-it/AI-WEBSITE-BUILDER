from flask import Flask, render_template,request
from google import genai
from pydantic import BaseModel, Field
from google.genai import types
from typing import List
import os
from typing import Literal
from dotenv import load_dotenv
load_dotenv()
import os
folder_path = "static"        # Replace with your folder     # Name of the file
full_path = f"{folder_path}"
class Type(BaseModel):
    file_type: Literal["html", "css","js"] = Field(description="The type of the file")
    content: str = Field(description="Full Code of That particular file_type")

class Recipe(BaseModel):
    recipe_name: str = Field(description="The name of the recipe.")
    files: List[Type]

client = genai.Client(
    api_key= os.getenv('GEMINI_API_KEY')
)

####
app = Flask(__name__)
####

prompt = """
You are an AI Web App Generator.

Your job is to generate THREE files only:
1. index.html
2. style.css
3. script.js

Return the output strictly in JSON format according to the provided schema.


====================================================
  ⚠️ SECURITY & CSP RULES (FOLLOW 100%)
====================================================

Your output MUST be fully CSP-compliant and SAFE.
This is REQUIRED.

STRICTLY FORBIDDEN (NEVER USE):
❌ eval()
❌ new Function()
❌ setTimeout("string", ...)
❌ setInterval("string", ...)
❌ inline <script> tags inside HTML
❌ inline event attributes like:
    onclick="" onload="" onchange="" oninput=""
❌ javascript: URLs
❌ innerHTML with untrusted user content

ALLOWED ALTERNATIVES:
✔ Use setTimeout(fn, delay)
✔ Use setInterval(fn, delay)
✔ Add event listeners ONLY inside script.js:
      element.addEventListener("click", function)
✔ Use textContent instead of innerHTML (unless content is trusted and static)
✔ All JS MUST be inside script.js only


====================================================
  OUTPUT RULES (FOLLOW EXACTLY)
====================================================

1. **Return ONLY valid HTML, CSS, and JS.**
2. **No markdown code blocks (` ``` `).**
3. **No extra explanations.**
4. HTML must link:
      <link rel="stylesheet" href="style.css">
      <script src="script.js"></script>
5. HTML must be a complete HTML5 document.
6. CSS must be external, modern, responsive, clean.
7. JS must contain all interactivity, fully client-side.


====================================================
  REQUIRED HTML STRUCTURE
====================================================

<html>
<head>
<title>[Auto-generated title]</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="style.css">
</head>
<body>

<!-- Auto-generated UI -->

<script src="script.js"></script>
</body>
</html>


====================================================
  REQUIRED CSS STANDARDS
====================================================
- Mobile-first responsive design
- Modern UI (glassmorphism, minimal, or neumorphism depending on context)
- Smooth transitions (optional)
- No frameworks
- Clean and formatted


====================================================
  REQUIRED JS STANDARDS
====================================================
- All interactive logic must be in script.js
- No inline JS, no HTML event attributes
- Use DOMContentLoaded event for safe initialization
- Use event listeners only
- No CSP-unsafe functions


====================================================
  FUNCTIONALITY REQUIREMENTS
====================================================
- The UI must be fully functional based on the user's description
- Include small enhancements such as:
  • button effects
  • smooth animations
  • localStorage where useful
  • toast messages if needed
  • basic form validation


====================================================
  STRICT FORMATTING RULES
====================================================
- Clean indentation
- No missing tags
- No duplicate scripts
- Valid and formatted code
- The generated site must run on any browser without modification


====================================================
  USER REQUIREMENT:
  Use the user prompt to generate ALL UI + logic.
====================================================

Always follow every rule above. Violations are NOT allowed.

"""

@app.route("/", methods=["GET", "POST"])
def home():
    inst = request.form.get('test')
    if inst != None:
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=inst,
        config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
        "system_instruction": types.GenerateContentConfig(
            system_instruction=prompt
        ),
    },
)
        recipe = Recipe.model_validate_json(response.text)
        os.makedirs(folder_path, exist_ok=True) 
        if recipe.files[0].file_type == "html":
            f = open(f"{folder_path}/index.html", "w")
            f.write(recipe.files[0].content)
            recipe.files.pop(0)
        if recipe.files[0].file_type == "css":
            f = open(f"{folder_path}/style.css", "w")
            f.write(recipe.files[0].content)
            recipe.files.pop(0)
        if recipe.files[0].file_type == "js":
            f = open(f"{folder_path}/script.js", "w")
            f.write(recipe.files[0].content)
            f.close()


    
    return render_template("main.html")
if __name__ == "__main__":
    app.run()

