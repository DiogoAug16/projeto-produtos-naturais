# Generated by Django 5.2.1 on 2025-05-21 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_produto_promocao_disponivel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='promocao_valor_porcentagem',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=2),
        ),
    ]
