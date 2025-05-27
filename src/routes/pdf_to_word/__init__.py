from flask import Blueprint

pdf_to_word_bp = Blueprint('pdf_to_word', __name__, url_prefix='/api/pdf-to-word')

from src.routes.pdf_to_word.routes import *
