# EstoqueSmart

Sistema web de controle de estoque para pequenas empresas, feito com **Python + Flask**.
Projeto acadêmico (Ciência da Computação – UVV).

## Funcionalidades

- Cadastro e login com senha criptografada (PBKDF2) e dois perfis: **admin** e **funcionário**
- Multiempresa: cada empresa tem um código de convite e só enxerga os próprios dados
- CRUD de **produtos** e **fornecedores** (apenas admin cria, edita e exclui)
- **Entradas e saídas** de estoque, com validação (quantidade inválida e saída maior que o estoque são bloqueadas)
- **Dashboard** com produtos em estoque crítico, movimentações do dia, receita e lucro
- **Histórico** de movimentações com filtro por data e produto
- Exportação de produtos em **CSV**
- Logs em arquivo e testes automatizados com **pytest**

## Tecnologias

Python 3 · Flask · Flask-SQLAlchemy · Flask-Login · SQLite · Jinja2 · HTML/CSS · pytest

## Como executar

```bash
git clone https://github.com/da6zin/estoquesmart-flask.git
cd estoquesmart-flask

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env            # Windows: copy .env.example .env
# edite o .env e defina uma SECRET_KEY

python app.py
```

Acesse http://127.0.0.1:5000, crie uma conta como **admin** (isso cria sua empresa e gera o
código de convite) e cadastre funcionários usando esse código.

## Testes

```bash
pytest
```

Os testes usam um banco SQLite em memória e não alteram os seus dados.

## Estrutura

```
app.py            fábrica da aplicação (create_app)
models.py         Usuario, Empresa, Produto, Fornecedor, Movimentacao
decorators.py     admin_required
routes/           blueprints: auth, dashboard, produtos, fornecedores, movimentacoes
templates/        páginas Jinja2
static/           CSS e logo
tests/            testes automatizados
```

## Prints

_(adicione aqui screenshots do dashboard e da lista de produtos, ex.: `docs/dashboard.png`)_
