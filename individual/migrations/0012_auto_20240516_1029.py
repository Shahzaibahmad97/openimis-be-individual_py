# Generated by Django 3.2.25 on 2024-05-16 10:29

import core.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion

from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('individual', '0011_auto_20240131_1015'),
    ]

    operations = [
        migrations.RunSQL(
            sql=(
                """
                IF (SELECT SERVERPROPERTY('EngineEdition')) = 5 BEGIN
                    IF EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='individualdatasourceupload' 
                               AND column_name='individual') 
                    BEGIN
                        ALTER TABLE individualdatasourceupload DROP COLUMN individual;
                    END
                END
                """ if settings.MSSQL else """
                DO $$
                BEGIN
                    IF EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='individualdatasourceupload' 
                               AND column_name='individual') THEN
                        ALTER TABLE individualdatasourceupload DROP COLUMN individual;
                    END IF;
                END $$;
                """
            ),
            reverse_sql=migrations.RunSQL.noop
        ),
        migrations.RunSQL(
            sql=(
                """
                IF (SELECT SERVERPROPERTY('EngineEdition')) = 5 BEGIN
                    IF EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='historicalindividualdatasourceupload' 
                               AND column_name='individual') 
                    BEGIN
                        ALTER TABLE historicalindividualdatasourceupload DROP COLUMN individual;
                    END
                END
                """ if settings.MSSQL else """
                DO $$
                BEGIN
                    IF EXISTS (SELECT 1 FROM information_schema.columns 
                               WHERE table_name='historicalindividualdatasourceupload' 
                               AND column_name='individual') THEN
                        ALTER TABLE historicalindividualdatasourceupload DROP COLUMN individual;
                    END IF;
                END $$;
                """
            ),
            reverse_sql=migrations.RunSQL.noop
        ),
        migrations.AlterField(
            model_name='group',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='json_ext',
            field=models.JSONField(blank=True, db_column='Json_ext', default=dict),
        ),
        migrations.AlterField(
            model_name='groupindividual',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='groupindividual',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='groupindividual',
            name='json_ext',
            field=models.JSONField(blank=True, db_column='Json_ext', default=dict),
        ),
        migrations.AlterField(
            model_name='historicalgroup',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalgroup',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalgroup',
            name='json_ext',
            field=models.JSONField(blank=True, db_column='Json_ext', default=dict),
        ),
        migrations.AlterField(
            model_name='historicalgroupindividual',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalgroupindividual',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalgroupindividual',
            name='json_ext',
            field=models.JSONField(blank=True, db_column='Json_ext', default=dict),
        ),
        migrations.AlterField(
            model_name='historicalindividual',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalindividual',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalindividual',
            name='json_ext',
            field=models.JSONField(blank=True, db_column='Json_ext', default=dict),
        ),
        migrations.AlterField(
            model_name='historicalindividualdatasource',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalindividualdatasource',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalindividualdatasource',
            name='validations',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='historicalindividualdatasourceupload',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalindividualdatasourceupload',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalindividualdatasourceupload',
            name='error',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='historicalindividualdatauploadrecords',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='historicalindividualdatauploadrecords',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='json_ext',
            field=models.JSONField(blank=True, db_column='Json_ext', default=dict),
        ),
        migrations.AlterField(
            model_name='individualdatasource',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='individualdatasource',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='individualdatasource',
            name='individual',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='individual.individual'),
        ),
        migrations.AlterField(
            model_name='individualdatasource',
            name='upload',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='individual.individualdatasourceupload'),
        ),
        migrations.AlterField(
            model_name='individualdatasource',
            name='validations',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individualdatasourceupload',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='individualdatasourceupload',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='individualdatasourceupload',
            name='error',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='individualdatauploadrecords',
            name='date_created',
            field=core.fields.DateTimeField(db_column='DateCreated', default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='individualdatauploadrecords',
            name='date_updated',
            field=core.fields.DateTimeField(db_column='DateUpdated', default=datetime.datetime.now, null=True),
        ),
    ]
