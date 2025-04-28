from flask import Blueprint, render_template
from middleware.auth_middleware import stall_owner_required

stall_owner_bp = Blueprint('stall_owner', __name__)

@stall_owner_bp.route('/dashboard')
@stall_owner_required
def dashboard():
    # Display stall owner's stalls and orders
    return render_template('stall_owner/dashboard.html')