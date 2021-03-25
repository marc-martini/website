from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, session
from flask_login import current_user, login_required
from datetime import datetime
from .plot import render_graph_histo, render_graph_comp
from .iex import histo_data, quote_data, logo, company_data, news
from .forms import Stock, CompStock
from .db_models import db, UserStock

# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/', methods=['GET'])
def home():
    """Homepage"""

    return render_template('main_home.html', current_user=current_user, title = 'Home')
