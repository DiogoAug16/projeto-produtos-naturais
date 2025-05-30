# Generated by Django 5.2.1 on 2025-05-21 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_produto_esta_disponivel'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='promocao_disponivel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='produto',
            name='promocao_valor_porcentagem',
            field=models.DecimalField(decimal_places=0, max_digits=2, null=True),
        ),
    ]
