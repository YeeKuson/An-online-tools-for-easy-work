from flask import Blueprint

pdf_to_image_bp = Blueprint('pdf_to_image', __name__, url_prefix='/api/pdf-to-image')

from src.routes.pdf_to_image.routes import *
