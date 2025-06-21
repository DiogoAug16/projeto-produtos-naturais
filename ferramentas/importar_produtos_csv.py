import pandas as pd
from produto.models import Produto
from categoria.models import Categoria

df = pd.read_csv('dados/produtos.csv')

for _, row in df.iterrows():
    try:
        categoria = Categoria.objects.get(categoria_nome=row['categoria'])
        
        Produto.objects.create(
            produto_nome=row['produto_nome'],
            descricao=row['descricao'],
            slug=row['slug'],
            categoria=categoria,
            imposto=row['imposto'],
            preco=row['preco'],
            estoque=row['estoque'],
            esta_disponivel=bool(row['esta_disponivel']),
            promocao_disponivel=bool(row['promocao_disponivel']),
            promocao_valor_porcentagem=row['promocao_valor_porcentagem']
        )
        print(f"✔ Produto '{row['produto_nome']}' criado com sucesso.")
    except Categoria.DoesNotExist:
        print(f"⚠ Categoria '{row['categoria']}' não encontrada. Ignorado.")
    except Exception as e:
        print(f"❌ Erro ao criar '{row['produto_nome']}':", e)
