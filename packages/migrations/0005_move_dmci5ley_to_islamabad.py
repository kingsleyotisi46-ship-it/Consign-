from django.db import migrations


def move_shipment_to_islamabad(apps, schema_editor):
    Package = apps.get_model('packages', 'Package')
    TrackingHistory = apps.get_model('tracking', 'TrackingHistory')

    package = Package.objects.filter(tracking_number='DFX-DMCI5LEY').first()
    if not package:
        return

    package.status = 'in_transit'
    package.save(update_fields=['status', 'updated_at'])
    TrackingHistory.objects.get_or_create(
        package=package,
        location='Islamabad, Pakistan',
        defaults={
            'status': 'In Transit',
            'latitude': 33.6844,
            'longitude': 73.0479,
            'notes': 'Package moved to Islamabad and is continuing to Lahore, Pakistan',
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_activate_dmci5ley'),
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(move_shipment_to_islamabad, migrations.RunPython.noop),
    ]
