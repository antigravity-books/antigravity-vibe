import shutil
import os

src1 = r"c:\Users\USER\OneDrive\Desktop\Project\vibe_coding_antigravity\ch6_4\양식\실습양식.pptx"
src2 = r"c:\Users\USER\OneDrive\Desktop\Project\vibe_coding_antigravity\ch6_4\placeholders.json"

dest_dir = r"c:\Users\USER\.gemini\antigravity\skills\generate_pptx_skill\resources"
os.makedirs(dest_dir, exist_ok=True)

shutil.copy2(src1, os.path.join(dest_dir, "실습양식.pptx"))
shutil.copy2(src2, os.path.join(dest_dir, "placeholders.json"))
print("Successfully copied resources")
