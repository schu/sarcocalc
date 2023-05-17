import csv
import io

from flask import Flask, render_template, request

from sarcoma_nomogram_survival import calc_5yos

app = Flask(__name__)

_csv_fieldnames = ('id', 'age', 'size', 'grading', 'histo')
_csv_fieldnames_out = _csv_fieldnames + ('5yos',)

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    output = io.StringIO()

    if request.method == 'POST':
        csv_incoming = request.form['csv']
        reader = csv.DictReader(csv_incoming.splitlines(), fieldnames=_csv_fieldnames,
                                delimiter=';')

        items = []
        for row in reader:
            if row['id'] == 'id':
                # ignore header line
                continue
            items.append(row)

        for i in items:
            i['5yos'] = calc_5yos(i['age'], i['size'], i['grading'], i['histo'])

        writer = csv.DictWriter(output, fieldnames=_csv_fieldnames_out, delimiter=';')
        writer.writeheader()
        writer.writerows(items)

    return render_template('index.html', output=output.getvalue())
