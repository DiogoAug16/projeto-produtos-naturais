# 🌿 Projeto Produtos Naturais 
Desenvolvimento de um e-commerce de produtos naturais utilizando Django, como projeto da disciplina de Programação Web.

## 📦 Tecnologias

- Python 3.x + Django (backend)

- SQLite (banco de dados local)

- JavaScript, HTML5, CSS3, SCSS (frontend)

- Arquivos extras:

  - requirements.txt – dependências do projeto

## 🚀 Iniciando o projeto (localmente)

**1.** Clone o repositório:

```bash
git clone https://github.com/DiogoAug16/projeto-produtos-naturais.git
```

**2.** Crie um ambiente virtual e ative-o:

```bash
python3 -m venv virtual
source virtual/bin/activate  # Linux
virtual\Scripts\activate     # Windows
```

**3.** Instale as dependências:

```bash
pip install -r requirements.txt
```

**4.** Execute as migrações:

```bash
python manage.py migrate
```

**5.** (Opcional) Crie um superusuário:

```bash
python manage.py createsuperuser
```

**6.** Inicie o servidor de desenvolvimento:

```bash
python manage.py runserver
```

**7.** Acesse a aplicação:

```http://127.0.0.1:8000/```

## ✅ Funcionalidades

- Cadastro e visualização de produtos naturais

- Navegação por categorias e departamentos

- Adição de itens ao carrinho e marcação de favoritos

- Admin disponível para gestão completa de produtos e categorias

## 🧩 Estrutura do Projeto

```bash
projeto-produtos-naturais/
├── .github/              # Configurações de CI/CD
├── carrinho/             # App: carrinho de compras
├── categoria/            # App: categorias de produtos
├── departamento/         # App: departamentos
├── favoritos/            # App: lista de favoritos
├── ferramentas/          # App: funções auxiliares
├── produto/              # App: produtos individuais
├── produtos_naturais/    # App: catálogo de produtos naturais
├── media/                # Uploads e fotos
├── templates/            # Templates Django
├── manage.py
├── requirements.txt
├── db.sqlite3
└── readme.md
```
