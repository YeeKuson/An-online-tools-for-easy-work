from flask import Blueprint

word_to_pdf_bp = Blueprint('word_to_pdf', __name__, url_prefix='/api/word-to-pdf')

from src.routes.word_to_pdf.routes import *
