from models import Empresa, Usuario
from extensions import db as _db
from tests.conftest import cria_empresa, cria_admin

def test_cadastro_admin_cria_empresa(client, app):

    client.post(
        "/auth/cadastro",
        data={
            "nome": "João",
            "email": "joao@teste.com",
            "senha": "123456",
            "confirmar": "123456",
            "cargo": "admin",
            "nome_empresa": "Minha Empresa"
        },
        follow_redirects=True
    )

    with app.app_context():

        usuario = Usuario.query.filter_by(
            email="joao@teste.com"
        ).first()

        assert usuario is not None
        assert usuario.cargo == "admin"

        empresa = _db.session.get(
            Empresa,
            usuario.empresa_id
        )

        assert empresa.nome == "Minha Empresa"


def test_login_funciona(client, app):

    from tests.conftest import cria_empresa, cria_admin, login

    with app.app_context():
        empresa = cria_empresa()
        cria_admin(empresa)

    resposta = login(client)

    assert resposta.status_code == 200


def test_logout(client, app):

    from tests.conftest import cria_empresa, cria_admin, login

    with app.app_context():
        empresa = cria_empresa()
        cria_admin(empresa)

    login(client)

    resposta = client.get(
        "/auth/logout",
        follow_redirects=True
    )

    assert resposta.status_code == 200

def test_login_com_senha_errada_falha(client, app):
    with app.app_context():
        cria_admin(cria_empresa())

    resposta = client.post(
        "/auth/login",
        data={"email": "admin@teste.com", "senha": "errada"},
        follow_redirects=True,
    )

    assert b"incorretos" in resposta.data


def test_login_nao_redireciona_para_site_externo(client, app):
    with app.app_context():
        cria_admin(cria_empresa())

    resposta = client.post(
        "/auth/login?next=//site-malicioso.com",
        data={"email": "admin@teste.com", "senha": "senha123"},
    )

    assert resposta.status_code == 302
    assert "site-malicioso" not in resposta.headers["Location"]


def test_cadastro_com_email_duplicado_e_recusado(client, app):
    with app.app_context():
        cria_admin(cria_empresa())

    client.post(
        "/auth/cadastro",
        data={
            "nome": "Outro", "email": "admin@teste.com", "senha": "abcdef",
            "confirmar": "abcdef", "cargo": "admin",
        },
        follow_redirects=True,
    )

    with app.app_context():
        assert Usuario.query.filter_by(email="admin@teste.com").count() == 1
