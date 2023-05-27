# Import required modules
from flask import Flask, request, render_template, redirect, abort, send_from_directory
from feature import *
import json



# Initialize Flask app
app = Flask(__name__)

# Homepage route
@app.route("/")
def index():
    return redirect("/Laptop")

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

# Error Page 
@app.errorhandler(400)
def bad_request(e):
    static_url = app.static_url_path
    css_url = f"{static_url}/400.css"
    return render_template('400.html', css_url = css_url), 400

@app.errorhandler(403)
def error_forbidden(e):
    static_url = app.static_url_path
    css_url = f"{static_url}/403.css"
    return render_template('403.html', css_url = css_url), 403

@app.errorhandler(404)
def page_not_found(e):
    static_url = app.static_url_path
    css_url = f"{static_url}/404.css"
    return render_template('404.html', css_url = css_url), 404

@app.errorhandler(405)
def method_not_allowed(e):
    static_url = app.static_url_path
    css_url = f"{static_url}/405.css"
    return render_template('405.html', css_url = css_url), 405

@app.errorhandler(408)
def request_timeout(e):
    static_url = app.static_url_path
    css_url = f"{static_url}/408.css"
    return render_template('408.html', css_url = css_url), 408

@app.errorhandler(500)
def internal_server_error(e):
    static_url = app.static_url_path
    css_url = f"{static_url}/500.css"
    return render_template('500.html', css_url = css_url), 500  # Internal Server Error

@app.errorhandler(503)
def  service_unavailable(e):
    static_url = app.static_url_path
    css_url = f"{static_url}/503.css"
    return render_template('503.html', css_url = css_url), 503


# Category Page
@app.route("/<table_name>")
def category(table_name):
    if table_name not in allow_path:
        abort(404)

    return render_template("categoryPage.html", 
                           parameters = get_parameters(table_name), 
                           table_name = table_name,
                           productType = NAME[table_name],
                           productDescription = DESCRIPTION[table_name])


@app.route("/filterProduct", methods = ["POST"])
def filterProduct():
    table_name = request.args.get("c")
    if table_name == None:
        abort(404)

    product_per_page = 20
    page_index = request.args.get('page', default = 1, type = int)
    sort_type = request.args.get("sort", default = 1, type = int)

    filters = {}
    try:
        filters = request.json
    except:
        print('get filter failed')
    
    return json.dumps(filter_product(
        table_name = table_name,
        page_index = page_index,
        product_per_page = product_per_page,
        sort_type = sort_type,
        filters = filters
    ))


@app.route("/search", methods=['GET', 'POST'])
def search():
    name = str(request.form.get('search'))
    if not name or name == None or name == "None":
        name = request.args.get("name", default = 'None', type = str)
        
    return render_template("searchProduct.html", name = name)


@app.route("/searchProduct", methods = ["POST"])
def searchProduct():
    product_per_page = 20
    page_index = request.args.get('page', default = 1, type = int)
    sort_type = request.args.get("sort", default = 1, type = int)

    name = ''
    try:
        name = request.json
    except:
        print('get name failed')
    if not name or name == None or name == 'None':
        name = request.args.get("name", default = 'None', type = str)
    
    return json.dumps(search_product(
        name = name,
        page_index = page_index,
        product_per_page = product_per_page,
        sort_type = sort_type,
    ))


@app.route("/product/<table_name>", methods = ["GET"])
def productDetail(table_name):
    if table_name == None or table_name not in allow_path:
        abort(404)

    index = request.args.get('id', type = int)
    if not index:
        abort(403)
    
    static_url = app.static_url_path
    css_url_product = f"{static_url}/productDetail.css"
    css_url_index = f"{static_url}/style.css"
    css_url_mobile = f"{static_url}/mobile.css"

    product, listproduct = findProductById(table_name, index)
    return render_template(
        "productDetail.html",
        css_url_product = css_url_product,
        css_url_index = css_url_index,
        css_url_mobile = css_url_mobile,
        table_name = table_name,
        product = product,
        listproduct = listproduct,
        SHOP = SHOP,
    )


if __name__ == '__main__':
    app.run()