import pkg.dbman as dbman
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html",
    plates=dbman.listplates()
    
    )

@app.route("/itemcreate", methods=['POST', 'GET'])
def itemcreate():
    xsize, ysize = dbman.platedata(request.form['plate'])
    return render_template("itemcreate.html",xsize=int(xsize),ysize=int(ysize),name=request.form['itemname'],plate=request.form['plate'])

@app.route("/create", methods=['POST', 'GET'])
def create():
    try:
        print("createing")
        if request.form['type'] == "plate":
            dbman.create("plates",request.form['platename'],request.form['xsize'],request.form['ysize'])
            return render_template("index.html",
        plates=dbman.listplates()
        )
    except:
        if request.args.get('type') == "item":
            dbman.create("items",request.args.get('name'),request.args.get('x'),request.args.get('y'),request.args.get('plate'))
        return render_template("index.html",plates=dbman.listplates())

@app.route("/search", methods=['POST', 'GET'])
def search():
    return render_template("search.html",results=dbman.lookup(request.form['search']))


@app.route("/render", methods=['POST', 'GET'])
def render():
    plate = dbman.getplate(request.args.get('result'))
    xt, yt = dbman.itemdata(request.args.get('result'))
    xsize, ysize = dbman.platedata(plate)
    return render_template("render.html",xsize=xsize,ysize=ysize,xt=xt,yt=yt,plate=plate,item=request.args.get('result'))

@app.route("/edit", methods=['POST', 'GET'])
def edit():
    request.args.get('item')

@app.route("/delete", methods=['POST', 'GET'])
def delete():
    print(request.args.get('item'))
    dbman.delete(request.args.get('item'),"item")
    return "<h1> deleted </h1>"

if __name__ == "__main__":
    app.run(debug=True)