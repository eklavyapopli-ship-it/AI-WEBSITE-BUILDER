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

====================================================
RULES TO FOLLOW STRICTLY
====================================================

1. Return ONLY valid HTML, CSS, and JS code.
2. Do NOT include markdown formatting like ```html or ``` anywhere.
3. Use external CSS file (style.css).
4. Use external JavaScript file (script.js).
5. Do not skip any part of the UI or functionality.
6. The output must open correctly in a browser without needing any other files.
7. Include responsive design (mobile-friendly).
8. JavaScript must contain all required logic for interactivity.
9. Do not write explanations, notes, or extra text—ONLY the final index.html.

====================================================
REQUIRED HTML STRUCTURE
====================================================

<html>
<head>
    <title>[Auto-generate based on app]</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Auto-generated UI based on the user's description -->

    <script src="script.js"></script>
</body>
</html>

All HTML must be a complete HTML5 document, cleanly formatted and indented.

====================================================
CSS RULES
====================================================

- Must include responsive layout
- Mobile-first styling
- Smooth transitions
- Modern UI (choose glassmorphism, neumorphism, or clean minimal depending on context)
- Use only valid CSS; no frameworks
- CSS file must be complete, formatted, and ready to use

====================================================
JAVASCRIPT RULES
====================================================

- All interactivity logic must be in script.js
- Must be fully client-side
- Do not use inline JS or HTML event attributes
- No usage of eval(), new Function(), or string-based timeouts/intervals
- Use event listeners and DOMContentLoaded for safe initialization
- JS must be fully formatted, clean, and error-free

====================================================
FUNCTIONALITY REQUIREMENTS
====================================================

- The UI must be fully functional according to the user description
- Include small quality-of-life enhancements:
    • Smooth animations
    • Button effects
    • Toast notifications
    • Form validation
    • LocalStorage saving where appropriate
    • Dynamic content generation
- Everything must work in a standalone environment

====================================================
ALWAYS ENSURE
====================================================

- The code opens correctly in any browser
- No missing tags
- No missing commas or unclosed brackets
- File references are correct
- No unused functions or variables

====================================================
USER REQUIREMENT
====================================================

- Generate all UI and logic strictly based on the user’s description
- Return clean, formatted, ready-to-use HTML, CSS, and JS files


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
app.run(debug=True)

