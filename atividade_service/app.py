from config import create_app
from controllers.atividade_controller import atividade_bp2

app = create_app()
app.register_blueprint(atividade_bp2, url_prefix='/atividades')

if __name__ == '__main__':
    app.run(host='localhost', port=5002)
