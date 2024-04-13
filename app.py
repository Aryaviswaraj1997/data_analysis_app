from flask import Flask, request, render_template, jsonify
import pandas as pd
import io
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

def plot_to_html_img(figure):
    """Converts matplotlib plot to HTML img tag."""
    buf = BytesIO()
    figure.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    return f'<img src="data:image/png;base64,{image_base64}" />'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    df=0
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file:
                df = pd.read_csv(file)
        else:
            data = request.form['data']
            data = io.StringIO(data)
            df = pd.read_csv(data)

        # Generate summary statistics and a histogram
        result_stats = df.describe().to_html()
        plt.figure()
        df.hist()
        plt.tight_layout()
        plot_html_img = plot_to_html_img(plt.gcf())
        plt.close()
        
        return render_template('results.html', tables=result_stats, plot_img=plot_html_img)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
