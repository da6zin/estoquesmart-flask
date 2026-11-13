from models import Empresa
from models import Produto
from extensions import db as _db
from tests.conftest import cria_empresa, cria_admin, login


def test_entrada_aumenta_estoque(client, app):

    with app.app_context():

        empresa = cria_empresa()
        cria_admin(empresa)

        produto = Produto(
            empresa_id=empresa.id,
            nome="Teclado",
            codigo="T001",
            quantidade_atual=10
        )

        _db.session.add(produto)
        _db.session.commit()

        pid = produto.id

    login(client)

    client.post(
        f"/movimentacoes/registrar/{pid}",
        data={
            "tipo": "entrada",
            "quantidade": "5"
        },
        follow_redirects=True
    )

    with app.app_context():

        produto = _db.session.get(
            Produto,
            pid
        )

        assert produto.quantidade_atual == 15


def test_saida_diminui_estoque(client, app):

    with app.app_context():

        empresa = cria_empresa()
        cria_admin(empresa)

        produto = Produto(
            empresa_id=empresa.id,
            nome="Monitor",
            codigo="MON01",
            quantidade_atual=10
        )

        _db.session.add(produto)
        _db.session.commit()

        pid = produto.id

    login(client)

    client.post(
        f"/movimentacoes/registrar/{pid}",
        data={
            "tipo": "saida",
            "quantidade": "3"
        },
        follow_redirects=True
    )

    with app.app_context():

        produto = _db.session.get(
            Produto,
            pid
        )

        assert produto.quantidade_atual == 7

def _cria_produto(app, quantidade=10, codigo="X001", empresa=None):
    with app.app_context():
        if empresa is None:
            empresa = cria_empresa()
            cria_admin(empresa)
        produto = Produto(
            empresa_id=empresa.id,
            nome="Item",
            codigo=codigo,
            quantidade_atual=quantidade,
        )
        _db.session.add(produto)
        _db.session.commit()
        return produto.id


def test_saida_maior_que_estoque_e_bloqueada(client, app):
    pid = _cria_produto(app, quantidade=3)
    login(client)

    client.post(
        f"/movimentacoes/registrar/{pid}",
        data={"tipo": "saida", "quantidade": "5"},
        follow_redirects=True,
    )

    with app.app_context():
        assert _db.session.get(Produto, pid).quantidade_atual == 3


def test_quantidade_invalida_nao_altera_estoque(client, app):
    pid = _cria_produto(app, quantidade=10)
    login(client)

    for valor in ("0", "-2", "abc"):
        client.post(
            f"/movimentacoes/registrar/{pid}",
            data={"tipo": "entrada", "quantidade": valor},
            follow_redirects=True,
        )

    with app.app_context():
        assert _db.session.get(Produto, pid).quantidade_atual == 10


def test_nao_movimenta_produto_de_outra_empresa(client, app):
    with app.app_context():
        outra = Empresa(nome="Outra", codigo_convite="OUTRA123")
        _db.session.add(outra)
        _db.session.commit()
        outra_id = outra.id
    pid = _cria_produto(app, quantidade=10, codigo="Z9", empresa=_EmpresaRef(outra_id))

    with app.app_context():
        empresa = cria_empresa()
        cria_admin(empresa)
    login(client)

    resposta = client.post(
        f"/movimentacoes/registrar/{pid}",
        data={"tipo": "entrada", "quantidade": "5"},
    )

    assert resposta.status_code == 404
    with app.app_context():
        assert _db.session.get(Produto, pid).quantidade_atual == 10


class _EmpresaRef:
    """Objeto mínimo só com id, para reutilizar o helper acima."""
    def __init__(self, id):
        self.id = id
