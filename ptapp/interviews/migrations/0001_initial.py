# Generated by Django 2.0.7 on 2018-07-17 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tests', '0002_auto_20180717_1907'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testunit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.TestUnit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interview', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interviews.Interview')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Question')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.Answer')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interviews.Reply')),
            ],
        ),
    ]
