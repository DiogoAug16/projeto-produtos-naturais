# Generated by Django 5.1.7 on 2025-07-04 21:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("produto", "0006_alter_produto_imposto"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="imposto",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=2
            ),
        ),
        migrations.AlterField(
            model_name="produto",
            name="promocao_valor_porcentagem",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=0, max_digits=2
            ),
        ),
    ]
