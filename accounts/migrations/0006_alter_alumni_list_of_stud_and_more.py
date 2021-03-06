# Generated by Django 4.0.3 on 2022-03-24 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alumni_list_of_stud_alumni_list_of_stud_pend_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumni',
            name='list_of_stud',
            field=models.TextField(blank=True, default='', verbose_name='List of Student talked'),
        ),
        migrations.AlterField(
            model_name='alumni',
            name='list_of_stud_pend',
            field=models.TextField(blank=True, default='', verbose_name='List of Student request pending'),
        ),
        migrations.AlterField(
            model_name='company',
            name='job_desc',
            field=models.TextField(blank=True, default='', verbose_name='Job Description'),
        ),
        migrations.AlterField(
            model_name='company',
            name='list_of_students',
            field=models.TextField(blank=True, default='', verbose_name='List of Students applied'),
        ),
        migrations.AlterField(
            model_name='company',
            name='other_details',
            field=models.TextField(blank=True, default='', verbose_name='Some Other details(if any)'),
        ),
        migrations.AlterField(
            model_name='company',
            name='overview',
            field=models.TextField(blank=True, default='', verbose_name='Company Overview(to display on Company Page)'),
        ),
        migrations.AlterField(
            model_name='company',
            name='work_environ',
            field=models.TextField(blank=True, default='', verbose_name='Work Environment'),
        ),
        migrations.AlterField(
            model_name='student',
            name='list_of_alum',
            field=models.TextField(blank=True, default='', verbose_name='List of Alumni Talked'),
        ),
        migrations.AlterField(
            model_name='student',
            name='list_of_alum_pend',
            field=models.TextField(blank=True, default='', verbose_name='List of Alumni request pending'),
        ),
        migrations.AlterField(
            model_name='student',
            name='list_of_comp',
            field=models.TextField(blank=True, default='', verbose_name='List of Companies Applied'),
        ),
    ]
