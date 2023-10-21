# Generated by Django 4.2.5 on 2023-10-21 01:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GeneratedMelody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('melody', models.FileField(upload_to='melodies/')),
                ('average_ratings', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('generation', models.PositiveIntegerField(default=1)),
                ('duration', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_rating', models.ManyToManyField(to='ga.evaluation')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GeneticAlgorithmInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('population_size', models.PositiveIntegerField()),
                ('num_generations', models.PositiveIntegerField()),
                ('num_selected', models.PositiveIntegerField()),
                ('num_children', models.PositiveIntegerField()),
                ('crossover_probability', models.FloatField()),
                ('mutation_probability', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='MusicalRepresentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_signature', models.CharField(max_length=5)),
                ('scale_signature', models.CharField(max_length=10)),
                ('tempo', models.PositiveIntegerField()),
                ('has_back_track', models.BooleanField()),
                ('uses_arp_or_scale', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='GeneratedMusic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generation_number', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('duration', models.FloatField(default=0.0)),
                ('img', models.ImageField(default='img/default.jpg', upload_to='img/')),
                ('ga_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ga.geneticalgorithminfo')),
                ('melodies', models.ManyToManyField(to='ga.generatedmelody')),
                ('musical_representation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ga.musicalrepresentation')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='evaluation',
            name='melody',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ga.generatedmelody'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='evaluation',
            unique_together={('user', 'melody')},
        ),
    ]
