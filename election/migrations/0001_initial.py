# Generated by Django 2.0.5 on 2020-08-14 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='avatars/')),
                ('full_name', models.CharField(max_length=70)),
                ('level', models.CharField(choices=[('level_400', 'Level 400'), ('level_300', 'Level 300'), ('level_200', 'Level 200'), ('level_100', 'Level 100')], default='level_100', max_length=30)),
                ('course_offering', models.CharField(choices=[('AREN', 'Agricultural Engineering'), ('BMEN', 'Biomedical Engineering'), ('CPEN', 'Computer Engineering'), ('FPEN', 'Food Processing Engineering'), ('MTEN', 'Materials Science & Engineering')], default='AREN', max_length=70)),
                ('bio', models.TextField(blank=True)),
                ('year', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('year', models.DateField()),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contestable', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='election.Election')),
            ],
        ),
        migrations.CreateModel(
            name='Queries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('email', models.CharField(max_length=30, verbose_name='query from')),
                ('subject', models.CharField(max_length=40, verbose_name='subject')),
                ('message', models.TextField(verbose_name='message')),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='date')),
            ],
            options={
                'verbose_name': 'Query',
                'verbose_name_plural': 'Queries',
                'ordering': ['-sent_at'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_at', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='election.Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=150, verbose_name='full name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('pass_code', models.CharField(blank=True, max_length=30, verbose_name='pass code')),
            ],
            options={
                'verbose_name': 'Voter',
                'verbose_name_plural': 'Voters',
                'ordering': ['full_name'],
            },
        ),
        migrations.AddField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='election.Voter'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='election.Position'),
        ),
    ]
