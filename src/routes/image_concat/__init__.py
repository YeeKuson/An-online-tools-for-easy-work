from flask import Blueprint

image_concat_bp = Blueprint('image_concat', __name__, url_prefix='/api/image-concat')

from src.routes.image_concat.routes import *
