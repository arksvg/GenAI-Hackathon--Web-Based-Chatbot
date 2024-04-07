from flask import Flask, redirect, url_for, request , render_template
import data
from flask import Flask, render_template, request, send_file
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import io


app = Flask(__name__, template_folder="templates")
@app.route('/admin',methods=["GET", "POST"])
def success():
    if request.method == 'POST':
        # Process form data when the request method is POST
        tag = request.form['tag']
        pattern = request.form['pattern']
        res = request.form['res']
        value = data.insertData(tag, pattern, res)
        print(value)

        # Render the 'admin.html' template for both GET and POST requests
        return render_template('admin.html')

    # Render the 'admin.html' template for GET requests
    return render_template('admin.html')
@app.route('/', methods=["GET", "POST"])
def login():
    # if(request.method == 'POST'):
    #     tag = request.form['tag']
    #     pattern = request.form['pattern']
    #     res = request.form['res']
    #     value = data.insertData(tag, pattern, res)
    #     print(value)
        # return redirect(url_for('login'))
        return render_template('index.html')

    # else:
    #     tag = request.args.get('tag')
    #     pattern = request.args.get('pattern')
    #     res = request.form.get('res')
    #     value = data.insertData(tag, pattern, res)

    #     print(value)
    #     # return redirect(url_for('login'))
    #     return render_template('index.html')

@app.route('/files', methods=["GET", "POST"])
def files():
    
    if request.method == "POST":
        file = request.files['file']
        data.excelToJson(file)
    return render_template('upload.html')
    # return redirect(url_for('admin'))

@app.route('/web-scrape')
def index():
    return render_template('web.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    website_url = request.form['url']
    scraped_data = scrape_website(website_url)

    if scraped_data:
        excel_data = save_to_excel(scraped_data)
        return send_file(
            io.BytesIO(excel_data),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            download_name='output.xlsx',
            as_attachment=True
        )
    else:
        return "Failed to scrape data."

def scrape_website(url):
    response = urllib.request.urlopen(url)

    if response.getcode() == 200:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        data = list(set(element.get_text(strip=True) for element in soup.find_all(
            ['p', 'h1', 'h2', 'h3', 'li', 'span', 'a', 'div', 'strong', 'em', 'b']) if element.get_text(strip=True)))

        return data
    else:
        print(f"Failed to retrieve data from {url}")
        return None

def save_to_excel(data):
    df = pd.DataFrame({'Data': data})
    excel_data = io.BytesIO()
    with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    excel_data.seek(0)
    return excel_data.getvalue()


if __name__ == "__main__":
    app.run(debug=True, port=5002)