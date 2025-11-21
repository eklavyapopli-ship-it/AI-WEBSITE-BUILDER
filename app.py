from flask import Flask, render_template,request
from google import genai
from pydantic import BaseModel, Field
from google.genai import types
from typing import List, Optional
import os
import html
from typing import Union, Literal
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

### FOLLOW THESE RULES STRICTLY:
1. Return ONLY valid HTML, CSS AND JS code.
2. Do NOT include markdown formatting like ```html or ``` anywhere.
3. Use external CSS.
4. Use external JavaScript.
5. Do not skip any part of the UI or functionality.
6. The output must open correctly in a browser without needing any other files.
7. Include responsive design (mobile-friendly).
8. JavaScript must contain all required logic for interactivity.
9. Do not write explanations, notes, or extra text—ONLY the final index.html.

### STRUCTURE YOU MUST FOLLOW:
<html>
<head>
<title>[Auto-generate based on app]</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="style.css">
</head>
<body>
  <!-- Auto-generated UI based on the user's description -->
  
<script src="script.js">
</script>
</body>
</html>

### USER REQUIREMENT:
ALSO GIVE FORMATTED CODES, so that it gets easily stored without any errors
HTML RULES

Must be a complete HTML5 document.

Use this structure:

<html> <head> <title>[Auto-generate based on app]</title> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <link rel="stylesheet" href="style.css"> </head> <body> <!-- Auto-generated UI based on the user's requirement --> <script src="script.js"></script> </body> </html>

All UI must be generated based on user's description.

Code must be formatted, indented, and clean.

✅ CSS RULES

Must include:

Responsive layout

Mobile-first styling

Smooth transitions

Modern UI (glassmorphism, neumorphism, or clean minimal depending on context)

Use ONLY valid CSS—no frameworks.

File must be complete and formatted.

✅ JAVASCRIPT RULES

Must contain all interactivity logic required by the user.

Must be fully client-side (no backend).

Must not require any external libraries unless user specifies.

Must be fully formatted and free of errors.

✅ FUNCTIONALITY REQUIREMENTS

The UI must be fully functional according to user description.

Add small quality-of-life features (if they fit the project), such as:

Smooth animations

Button effects

Toast notifications

Form validation

LocalStorage saving

Dynamic content generation

Everything must work in a standalone environment.

✅ ALWAYS ENSURE

The code opens correctly in any browser.

No missing tags.

No missing commas.

No unclosed brackets.

File references are correct.

No unused functions or variables.
"""

@app.route("/", methods=["GET", "POST"])
def home():
    inst = request.form.get('test')
    if inst != None:
        inst = html.escape(inst)
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
