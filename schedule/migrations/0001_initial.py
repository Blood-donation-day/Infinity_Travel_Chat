# Generated by Django 5.0 on 2023-12-17 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('place', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Planner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='DateEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateField()),
                ('description', models.TextField()),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='date_events', to='place.place')),
                ('period_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='date_events', to='schedule.periodevent')),
            ],
        ),
        migrations.AddField(
            model_name='periodevent',
            name='planner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='period_events', to='schedule.planner'),
        ),
    ]
