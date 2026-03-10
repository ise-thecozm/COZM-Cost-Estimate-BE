import django.utils.timezone
import django.db.models.deletion
import django.db.models
import uuid
from django.db import migrations, models

try:
    from pgvector.django import VectorField
except ImportError:
    VectorField = None


def _add_vector_db(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return
    schema_editor.execute(
        "ALTER TABLE core_savedestimate "
        "ADD COLUMN IF NOT EXISTS embedding vector(768);"
    )
    schema_editor.execute("""
        CREATE TABLE IF NOT EXISTS core_marketinsightcache (
            id          bigserial PRIMARY KEY,
            country_code varchar(10)  NOT NULL,
            city_code    varchar(10)  NOT NULL,
            city_label   varchar(200) NOT NULL,
            currency     varchar(10)  NOT NULL,
            embedding    vector(768),
            data         jsonb        NOT NULL,
            created_at   timestamptz  NOT NULL DEFAULT now(),
            updated_at   timestamptz  NOT NULL DEFAULT now(),
            UNIQUE (country_code, city_code, currency)
        );
    """)
    schema_editor.execute(
        "CREATE INDEX IF NOT EXISTS core_marketinsightcache_embedding_idx "
        "ON core_marketinsightcache "
        "USING ivfflat (embedding vector_cosine_ops) WITH (lists = 10);"
    )


def _remove_vector_db(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return
    schema_editor.execute(
        "ALTER TABLE core_savedestimate "
        "DROP COLUMN IF EXISTS embedding;"
    )
    schema_editor.execute("DROP TABLE IF EXISTS core_marketinsightcache;")


def _embedding_field():
    if VectorField is not None:
        return VectorField(dimensions=768, null=True, blank=True)
    return models.JSONField(null=True, blank=True)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_enable_pgvector'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='savedestimate',
                    name='embedding',
                    field=_embedding_field(),
                ),
                migrations.CreateModel(
                    name='MarketInsightCache',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                        ('country_code', models.CharField(db_index=True, max_length=10)),
                        ('city_code', models.CharField(db_index=True, max_length=10)),
                        ('city_label', models.CharField(max_length=200)),
                        ('currency', models.CharField(db_index=True, max_length=10)),
                        ('embedding', _embedding_field()),
                        ('data', models.JSONField()),
                        ('created_at', models.DateTimeField(auto_now_add=True)),
                        ('updated_at', models.DateTimeField(auto_now=True)),
                    ],
                    options={
                        'unique_together': {('country_code', 'city_code', 'currency')},
                    },
                ),
            ],
            database_operations=[
                migrations.RunPython(_add_vector_db, _remove_vector_db),
            ],
        ),
    ]
