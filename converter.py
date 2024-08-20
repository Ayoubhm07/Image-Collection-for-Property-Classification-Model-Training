import os
import sys
from flask import Flask, request, send_file
from io import BytesIO

# Add the directory containing the Cairo DLL to the system path
dll_path = r'C:\msys64\mingw64\bin'
os.add_dll_directory(dll_path)
sys.path.append(dll_path)

# Import cairocffi directly to see if it resolves the loading issue
try:
    import cairocffi as cairo
except ImportError as e:
    print("Failed to import cairocffi:", e)
    sys.exit(1)

# After ensuring cairocffi can be imported, now import cairosvg
try:
    import cairosvg
except OSError as e:
    print("Failed to import cairosvg or load cairo:", e)
    sys.exit(1)

app = Flask(__name__)

@app.route('/convert-svg', methods=['POST'])
def convert_svg():
    svg_data = request.data
    png_output = BytesIO()
    try:
        cairosvg.svg2png(bytestring=svg_data, write_to=png_output)
    except Exception as e:
        print("Error converting SVG to PNG:", e)
        return "Error in conversion", 500

    png_output.seek(0)  # Rewind the file
    return send_file(png_output, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
