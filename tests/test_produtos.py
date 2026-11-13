from models import Usuario
from models import Produto
from extensions import db as _db
from tests.conftest import cria_empresa, cria_admin, login


def test_produto_requer_login(client):

    resposta = client.get("/produtos/")

    assert resposta.status_code in (302, 401)


def test_criar_produto(client, app):

    with app.app_context():
        empresa = cria_empresa()
        cria_admin(empresa)

    login(client)

    client.post(
        "/produtos/novo",
        data={
            "nome": "Notebook",
            "codigo": "NB001",
            "quantidade_atual": "10",
            "quantidade_minima": "2"
        },
        follow_redirects=True
    )

    with app.app_context():

        produto = Produto.query.filter_by(
            codigo="NB001"
        ).first()

        assert produto is not None
        assert produto.nome == "Notebook"


def test_listar_produtos(client, app):

    with app.app_context():

        empresa = cria_empresa()
        cria_admin(empresa)

        produto = Produto(
            empresa_id=empresa.id,
            nome="Mouse",
            codigo="M001"
        )

        _db.session.add(produto)
        _db.session.commit()

    login(client)

    resposta = client.get("/produtos/")

    assert resposta.status_code == 200
    assert b"Mouse" in resposta.data

def test_funcionario_nao_pode_criar_produto(client, app):
    with app.app_context():
        empresa = cria_empresa()
        func = Usuario(nome="Func", email="func@teste.com",
                       cargo="funcionario", empresa_id=empresa.id)
        func.set_senha("senha123")
        _db.session.add(func)
        _db.session.commit()

    client.post("/auth/login", data={"email": "func@teste.com", "senha": "senha123"})

    resposta = client.post(
        "/produtos/novo",
        data={"nome": "X", "codigo": "X1", "quantidade_atual": "1", "quantidade_minima": "1"},
    )

    assert resposta.status_code == 403
    with app.app_context():
        assert Produto.query.filter_by(codigo="X1").first() is None
