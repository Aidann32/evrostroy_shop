from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_category_sequence'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, help_text='Текст под товарами на странице категории. Например: «Межкомнатные и входные двери в Актобе…»', verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title',
            field=models.CharField(blank=True, help_text='Если пусто: «<Категория> в Актобе — купить в Еврострой»', max_length=255, verbose_name='SEO заголовок'),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.TextField(blank=True, verbose_name='SEO описание'),
        ),
    ]
