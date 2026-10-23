from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_attribute_alter_brand_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['sequence', 'name'], 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AddField(
            model_name='category',
            name='sequence',
            field=models.PositiveIntegerField(default=2147483647, help_text='Чем меньше число, тем выше категория в списке', verbose_name='Порядок отображения'),
        ),
    ]
