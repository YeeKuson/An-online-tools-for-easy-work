from flask import Blueprint

pdf_to_ppt_bp = Blueprint('pdf_to_ppt', __name__, url_prefix='/api/pdf-to-ppt')

from src.routes.pdf_to_ppt.routes import *
