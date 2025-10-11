# app.py
from flask import Flask, render_template
from backend.routes.linear_algebra_routes import linear_algebra_bp

# Khởi tạo ứng dụng Flask
app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static')

# Đăng ký các Blueprints (các nhóm route)
app.register_blueprint(linear_algebra_bp)

@app.route('/')
def index():
    """
    Render trang chủ của ứng dụng.
    """
    return render_template('index.html')

if __name__ == '__main__':
    # Chạy ứng dụng ở chế độ debug
    # Trong môi trường production, hãy sử dụng một WSGI server như Gunicorn
    app.run(debug=True, port=5001)