from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys
from datetime import datetime, timedelta


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "temporary/"

def CountTime():
    f = request.files['file']        
    filename = secure_filename(f.filename)
    f.save(app.config['UPLOAD_FOLDER'] + filename)
    content = open(app.config['UPLOAD_FOLDER']+filename,'r')
    flag = False
    total_hours = 0
    total_minutes = 0
    line_no = 0
    for line in content:
        line_no += 1
        if not flag and "time log" in line.lower():
            flag = True
            continue
        if flag:
            try:
                l = [i.strip("\n").strip(" ") for i in line.split("-")]
                if "/" in l[0]:
                    l[0] = ":".join(l[0].split(":")[1:]).strip(" ")
                l = [i.split(" ")[0] for i in l if "am" in i.split(" ")[0].lower() or "pm" in i.split(" ")[0].lower()]
                #print(l, end = " ")
                l[0] = datetime.strptime(l[0], "%I:%M%p")
                l[1] = datetime.strptime(l[1], "%I:%M%p")
                if l[0]>l[1]:
                    l[1] += timedelta(days = 1)
                time_diff = l[1] - l[0]
                mins = (time_diff).seconds/60
                total_hours += mins//60
                total_minutes += mins%60
            except Exception as e:
                print("Not able to parse line number:", line_no)
    total_hours += total_minutes//60
    total_minutes %= 60
    output="Total Time:"+str(int(total_hours))+" hrs "+str(int(total_minutes))+" mins"
    return output;





@app.route('/')
def upload_file():
    return render_template('index.html') 
    
@app.route('/display_output', methods = ['GET', 'POST'])
def parse():  
    if request.method == 'POST':
        return render_template('index.html',timer=CountTime())
    return render_template('index.html')
                    

if __name__ == '__main__':
    app.run(debug = True)
