from flask import Blueprint, render_template

approximation_bp = Blueprint(
    'approximation',
    __name__,
    template_folder='../../frontend/templates/approximation',
    url_prefix='/approximation'
)

@approximation_bp.route('/')
def approximation_index():
    """
    Trang chính cho Xấp xỉ hàm số (chứa link tới các tab con).
    """
    return render_template('index.html')

@approximation_bp.route('/optimal-nodes')
def optimal_nodes():
    return render_template('optimal_nodes.html')

@approximation_bp.route('/lagrange')
def lagrange():
    return render_template('lagrange.html')

@approximation_bp.route('/newton')
def newton():
    return render_template('newton.html')

@approximation_bp.route('/central')
def central():
    return render_template('central.html')