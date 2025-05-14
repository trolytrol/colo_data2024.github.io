from flask import Flask, render_template_string, url_for
import os

app = Flask(__name__, static_folder="/")

# --- CONFIG -----------------------------------------------------------------
# Names of the sub‑folders that hold the PNG files inside ``static/images``
# Adjust the list if you ever change the folder names.
FOLDERS = [
    "input",  # reference images
    "0", "1", "2", "3", "4", "5"  # generated / compared images
]

# Highest index you want to show (inclusive). 0‑based indexing is assumed.
MAX_INDEX = 200  # shows 0.png … 200.png (201 rows)
# ----------------------------------------------------------------------------

PAGE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Image Comparison Grid</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 1rem; }
    table { border-collapse: collapse; }
    th, td { border: 1px solid #ccc; padding: 4px; text-align: center; }
    img { max-width: 120px; height: auto; display: block; margin: 0 auto; }
    thead th { position: sticky; top: 0; background: #f7f7f7; }
    tbody tr:nth-child(even) { background: #fafafa; }
  </style>
</head>
<body>
  <h1>Image Grid (index 0–{{ max_index }})</h1>

  <table>
    <thead>
      <tr>
        <th>#</th>
        {% for folder in folders %}
          <th>{{ folder }}</th>
        {% endfor %}
      </tr>
    </thead>
    <tbody>
      {% for idx in range(max_index + 1) %}
        <tr>
          <td>{{ idx }}</td>
          {% for folder in folders %}
            <td>
              {% set rel_path = '{}/{}.png'.format(folder, idx) %}
              {% if file_exists(rel_path) %}
                <img src="{{ url_for('static', filename=rel_path) }}" alt="{{ folder }}_{{ idx }}">
              {% else %}
                <em>n/a</em>
              {% endif %}
            </td>
          {% endfor %}
        </tr>
      {% endfor %}
    </tbody>
  </table>

</body>
</html>
"""

def file_exists(rel_path: str) -> bool:
    """Helper for the Jinja template: does the PNG actually exist?"""
    return os.path.exists(os.path.join(app.static_folder, rel_path))


# Make the helper available inside Jinja templates
@app.context_processor
def inject_helpers():
    return dict(file_exists=file_exists)


@app.route("/")
def index():
    """Main page showing the full grid."""
    return render_template_string(
        PAGE_TEMPLATE,
        folders=FOLDERS,
        max_index=MAX_INDEX,
    )


if __name__ == "__main__":
    # Run with ``python app.py`` and navigate to http://localhost:5000/
    app.run(debug=True)
