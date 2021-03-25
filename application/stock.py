from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, session
from flask_login import current_user, login_required
from datetime import datetime
from .plot import render_graph_histo, render_graph_comp
from .iex import histo_data, quote_data, logo, company_data, news
from .forms import Stock, CompStock
from .db_models import db, UserStock

# Blueprint Configuration
stock_bp = Blueprint('stock_bp', __name__)


@stock_bp.route('/stock', methods=['GET'])
def stock_home():
    """Stock Homepage"""

    return render_template('stock_home.html', current_user=current_user, title = 'Stock_Home')



@stock_bp.route('/_stock_histo_graph')
@login_required
def histo_graph():

	rng = request.args.get('rng',0, type=str )

	sym = request.args.get('sym', 0 , type=str)

	stock_name = request.args.get('stock_name', 0 , type=str)

	graph_data = histo_data(sym, rng)

	if graph_data == None:
	    graph_error = "/static/graph_error"
	    return jsonify(graph=graph_error)
	else:
	    x_val = graph_data[0]
	    y_val = graph_data[1]

	    graph_img = render_graph_histo(x_val, y_val, rng, stock_name)

	    return jsonify(graph=graph_img)



@stock_bp.route("/stock_single", methods=["GET", "POST"])
@login_required
def single():
    """Request single stock data."""

    form = Stock()
    if form.validate_on_submit():

        symbol = form.symbol.data

        session[symbol] = {}

        # quote
        quote = quote_data(symbol)

        session[symbol]["quote"] = quote

        if quote == None:
            flash("must provide a valid stock symbol", 'warning')
            return redirect(url_for("stock_bp.single"))

        # Graph
        name = "{} ({})".format(quote['name'], quote['symbol'])

        rng = '1d'
        graph_data = histo_data(symbol, rng)
        x_val = graph_data[0]
        y_val = graph_data[1]
        graph_img = render_graph_histo(x_val, y_val, rng, name)

        #session[symbol]['1dgraphdata'] = graph_data

        # Logo
        comp_logo = logo(symbol)

        session[symbol]['logo'] = comp_logo

        # Company
        comp = company_data(symbol)

        session[symbol]['comp'] = comp

        news_source = news(symbol)
        for item in news_source:

            summ_full = item['summary'].replace("\\",'')
            item['summary'] = summ_full[:200] + "..."
            date_raw = int(item['datetime']) / 1000
            date_edit = datetime.fromtimestamp(date_raw).strftime("%m/%d/%Y, %H:%M:%S")
            item['datetime'] = date_edit


        for item in news_source:

            if item['lang'] != 'en':
                news_source.remove(item)

        return render_template('stock_index.html', symbol = symbol, graph=graph_img, logo=comp_logo, news=news_source, quote=quote, comp=comp, title = 'Stock_Graph')

    return render_template("stock_quote.html", form=form, title = "Stock_Quote")

@stock_bp.route('/_stock_comp_graph')
@login_required
def comp_graph():

	rng = request.args.get('rng',0, type=str )

	sym1 = request.args.get('sym1', 0 , type=str)

	name1 = request.args.get('stock_name1', 0 , type=str)

	sym2 = request.args.get('sym1', 0 , type=str)

	name2 = request.args.get('stock_name2', 0 , type=str)


	name3 = request.args.get('stock_name3', 0 , type=str)
	if name3 == 'None':
	    graph_data3 = None
	    name3 = None

	else:
	    sym3 = request.args.get('sym3', 0 , type=str)
	    graph_data3 = histo_data(sym3, rng)

	graph_data1 = histo_data(sym1, rng)
	graph_data2 = histo_data(sym2, rng)


	graph_img = render_graph_comp(graph_data1, graph_data2, graph_data3, name1, name2, name3, rng)

	return jsonify(graph=graph_img)


@stock_bp.route("/stock_compare", methods=["GET", "POST"])
@login_required
def compare():
    print(session)
    quotes_all = []
    symbols_all = []
    names = []
    comp_logo = []


    form = CompStock()
    if form.validate_on_submit():

        #input range for base graph on page load
        rng = '1d'

        # Company 1
        # get symbol from form
        symbol1 = form.symbol1.data
        # add to symbol list for html
        symbols_all.append(symbol1)
        # check if data in session
        if symbol1 in session:
            quote1 = session[symbol1]['quote']
            logo1 = session[symbol1]['logo']
            comp_logo.append(logo1)
            quotes_all.append(quote1)

        else:
            session[symbol1] = {}
            quote1 = quote_data(symbol1)

            if quote1 == None:
                flash("must provide a valid stock symbol for Company 1", 'warning')
                return redirect(url_for("stock_bp.compare"))

            session[symbol1]["quote"] = quote1
            quotes_all.append(quote1)
            logo1 = logo(symbol1)
            comp_logo.append(logo1)
            session[symbol1]["logo"] = logo1


        # Graph data for company 1
        name1 = "{} ({})".format(quote1['name'], quote1['symbol'])
        names.append(name1)

        graph_data1 = histo_data(symbol1, rng)


        # Company 2
        # get symbol from form
        symbol2 = form.symbol2.data
        # add to symbol list for html
        symbols_all.append(symbol2)
        # check if data in session
        if symbol2 in session:
            quote2 = session[symbol2]['quote']
            logo2 = session[symbol2]["logo"]
            comp_logo.append(logo2)
            quotes_all.append(quote2)

        else:
            session[symbol2] = {}
            quote2 = quote_data(symbol2)

            if quote2 == None:
                flash("must provide a valid stock symbol for Company 2", 'warning')
                return redirect(url_for("stock_bp.compare"))

            session[symbol2]["quote"] = quote2
            quotes_all.append(quote2)
            logo2 = logo(symbol2)
            comp_logo.append(logo2)
            session[symbol2]["logo"] = logo2

        # Graph data for company 2
        name2 = "{} ({})".format(quote2['name'], quote2['symbol'])
        names.append(name2)

        graph_data2 = histo_data(symbol2, rng)


        # Company 3 - set variables, check if inputed, if inputed get values else return None
        name3 = None
        graph_data3 = None
        logo3 = None
        number = 2

        # Company 3
        # get symbol from form
        symbol3 = form.symbol3.data
        # check if symbol 3 was inputted
        if symbol3:
            number = 3
            symbols_all.append(symbol3)

            # check if data in session
            if symbol3 in session:
                quote3 = session[symbol3]['quote']
                logo3 = session[symbol3]['logo']
                comp_logo.append(logo3)
                quotes_all.append(quote3)

            else:
                session[symbol3] = {}
                quote3 = quote_data(symbol3)

                if quote3 == None:
                    flash("must provide a valid stock symbol for Company 3", 'warning')
                    return redirect(url_for("stock_bp.compare"))

                session[symbol3]["quote"] = quote3
                quotes_all.append(quote3)
                logo3 = logo(symbol3)
                comp_logo.append(logo3)
                session[symbol3]["logo"] = logo3

            # Graph data for company 3
            name3 = "{} ({})".format(quote3['name'], quote3['symbol'])
            names.append(name3)

            graph_data3 = histo_data(symbol3, rng)


        # get Graph img for the comparison graph of 2/3 companies
        graph_img = render_graph_comp(graph_data1, graph_data2, graph_data3, name1, name2, name3, rng)

        # Return the comprison page with company data
        return render_template('stock_comparison.html', syms = symbols_all, graph=graph_img,
                                logo=comp_logo, quotes=quotes_all, num = number,
                                names = names, title = 'Stock_Comparison')

    return render_template("stock_compare.html", form=form, title = "Stock_Compare")



@stock_bp.route("/_stock_index", methods=["POST"])
@login_required
def index():

    if request.method == "POST":
        symbol = request.form.get('stock')

        # check if data in session
        if symbol in session:
            quote = session[symbol]['quote']
            try:
                comp_logo = session[symbol]['logo']
            except:
                comp_logo = logo(symbol)
                session[symbol]['logo'] = comp_logo
            try:
                comp = session[symbol]['comp']
            except (KeyError):
                comp = company_data(symbol)
                session[symbol]['comp'] = comp

        else:
            session[symbol] = {}
            quote = quote_data(symbol)
            comp_logo = logo(symbol)
            comp = company_data(symbol)

            session[symbol]["quote"] = quote
            session[symbol]['comp'] = comp
            session[symbol]['logo'] = comp_logo

        # Graph
        name = "{} ({})".format(quote['name'], quote['symbol'])

        rng = '1d'
        graph_data = histo_data(symbol, rng)
        x_val = graph_data[0]
        y_val = graph_data[1]
        graph_img = render_graph_histo(x_val, y_val, rng, name)

        news_source = news(symbol)
        for item in news_source:

            summ_full = item['summary'].replace("\\",'')
            item['summary'] = summ_full[:200] + "..."
            date_raw = int(item['datetime']) / 1000
            date_edit = datetime.fromtimestamp(date_raw).strftime("%m/%d/%Y, %H:%M:%S")
            item['datetime'] = date_edit


        for item in news_source:

            if item['lang'] != 'en':
                news_source.remove(item)



        return render_template('stock_index.html', symbol = symbol, graph=graph_img, logo=comp_logo, quote=quote, comp=comp, news=news_source, title = 'Stock_Graph')


@stock_bp.route("/_stock_add_stock_db")
@login_required
def add_stock():
    userid = current_user.id
    print(userid)
    sym = request.args.get('sym',0, type=str ).lower()
    name = request.args.get('name',0, type=str )

    sym_exist = UserStock.query.filter_by(userid = userid, symbol = sym).first()
    print(sym_exist)
    if sym_exist is None:
        new_sym = UserStock(symbol = sym,
        userid = userid,
        name = name,
        created = datetime.now())
        db.session.add(new_sym)
        db.session.commit()
        cat = "success"
        message = "Stock ({}) Successfully added to Track".format(name)
        return jsonify(cat=cat, message=message)

    cat = "warning"
    message = "Stock ({}) Already Tracked".format(name)
    return jsonify(cat=cat, message=message)


@stock_bp.route("/_stock_remove_stock_db")
@login_required
def remove_stock():
    userid = current_user.id

    sym = request.args.get('sym').lower()
    name = request.args.get('name')

    sym_exist = UserStock.query.filter_by(userid = userid, symbol = sym).first()

    db.session.delete(sym_exist)
    db.session.commit()

    flash("Stock Successfully removed from Tracking", 'success')
    return redirect(url_for("stock_bp.dashboard"))


@stock_bp.route("/stock_dashboard")
@login_required
def dashboard():

    userid = current_user.id

    stockquery = UserStock.query.filter_by(userid = userid).all()

    watch = []

    for stock in stockquery:
        date = stock.created.strftime("%m/%d/%Y")
        sym = stock.symbol.upper()
        name = stock.name
        watch.append({'date':date, 'symbol':sym, 'name':name})

    return render_template("stock_dashboard.html", current_user=current_user, watch = watch, title = 'Stock_Dashboard')


'''
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)
'''
