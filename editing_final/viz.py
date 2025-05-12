from flask import Flask, request, send_from_directory, url_for
import pandas as pd

app = Flask(__name__, static_url_path='/', static_folder='')

def cc(x):
    return 'green' if x > 2 else 'red'

@app.route("/mask", methods=['GET', 'POST'])
def mask():
    f = request.args.get('f', type=str, default="focus")
    t = request.args.get('t', type=int, default=9)
    dist = request.args.get('dist', type=float, default=None)
    sn = request.args.get('sn', type=float, default=-1.0)
    mask = request.args.get('mask', type=str, default="True")
    q = request.args.get('Q', type=int, default=85)
    seed = request.args.get('seed', type=int, default=0)
    reg = request.args.get('reg', type=float, default=0.1)

    # Example data for visualization
    N = 100  # Number of samples
    C = 4   # Number of seeds
    df = pd.read_csv(f'local_descriptions_with_cat.csv')

    out = "<!DOCTYPE html><html><head>"
    out += "<style>"
    out += """
        table {
            width: 100%;
            border-collapse: collapse;
        }
        td {
            vertical-align: top;
            text-align: left;
            padding: 10px;
            border: 1px solid #ccc;
        }
        img {
            display: block;
            margin-bottom: 10px;
        }
        td span {
            display: block;
            word-wrap: break-word;
            white-space: normal;
            max-width: 256px;
        }
    """
    out += "</style>"
    out += "<link rel='stylesheet' type='text/css' href='" + url_for('static', filename='style.css') + "'>"
    out += "</head><body>"
    out += "<table>"
    for i in range(len(df)):
        if df.iloc[i, 5] != 'change':
            continue
        out += "<tr>"
        out += f"<td>"
        img_src = f'input/{i}.png'
        out += f"<img src='{img_src}' width='256' height='256'>"
        prompt = df.iloc[i, 2]
        out += f"<span><strong>Cap: </strong>{prompt}</span><br>"
        prompt = df.iloc[i, 3]
        out += f"<span><strong>Inst: </strong>{prompt}</span><br>"
        out += f"</td>"

        out += "<td>"
        img_src = f'0/{i}.png'
        out += f"<img src='{img_src}' width='256' height='256'>"
        score = df.iloc[i, 6]
        out += f"<span style='color:{cc(score)}'>bg:{score}</span>"
        score = df.iloc[i, 8]
        out += f"<span style='color:{cc(score)}'>text:{score}</span>"
        score = df.iloc[i, 10]
        out += f"<span style='color:{cc(score)}'>qual:{score}</span>"
        score = df.iloc[i, 12]
        out += f"<span style='color:{cc(score)}'>pref:{score}</span>"
        out += f"</td>"

        out += "<td>"
        img_src = f'1/{i}.png'
        out += f"<img src='{img_src}' width='256' height='256'>"
        score = df.iloc[i, 7]
        out += f"<span style='color:{cc(score)}'>bg:{score}</span>"
        score = df.iloc[i, 9]
        out += f"<span style='color:{cc(score)}'>text:{score}</span>"
        score = df.iloc[i, 11]
        out += f"<span style='color:{cc(score)}'>qual:{score}</span>"
        score = df.iloc[i, 13]
        out += f"<span style='color:{cc(score)}'>pref:{score}</span>"
        out += f"</td>"

        out += "</tr>"
    
    out += "</table>"
    out += "</body></html>"
    
    return out

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
