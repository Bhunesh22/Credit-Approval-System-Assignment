# Generated by Django 4.2.8 on 2023-12-18 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('phone_number', models.IntegerField()),
                ('monthly_salary', models.IntegerField()),
                ('approved_limit', models.IntegerField()),
            ],
            options={
                'db_table': 'customer',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_id', models.IntegerField()),
                ('loan_amount', models.FloatField()),
                ('tenure', models.IntegerField()),
                ('interest_rate', models.FloatField()),
                ('monthly_installment', models.FloatField()),
                ('emis_paid_on_time', models.IntegerField(default=0)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customerLoan.customer')),
            ],
            options={
                'db_table': 'loan',
            },
        ),
    ]
