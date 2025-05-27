from flask import Blueprint

image_resize_bp = Blueprint('image_resize', __name__, url_prefix='/api/image-resize')

from src.routes.image_resize.routes import *
