import logging
import os
import sys

from dotenv import load_dotenv
from flask import Flask, render_template

from extensions import db, login_manager
from models import Usuario
import routes.auth as auth_bp
import routes.dashboard as dashboard_bp
import routes.produtos as produtos_bp
import routes.movimentacoes as mov_bp
import routes.fornecedores as forn_bp

load_dotenv()


def create_app(test_config=None):
    """Application factory. `test_config` sobrescreve a configuração padrão (usado nos testes)."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("estoquesmart.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-inseguro-dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoquesmart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    app.logger.info("Aplicativo EstoqueSmart inicializado")

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Faça login para acessar o sistema.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    @app.errorhandler(403)
    def acesso_negado(e):
        return render_template('403.html'), 403

    app.register_blueprint(auth_bp.bp)
    app.register_blueprint(dashboard_bp.bp)
    app.register_blueprint(produtos_bp.bp)
    app.register_blueprint(mov_bp.bp)
    app.register_blueprint(forn_bp.bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
