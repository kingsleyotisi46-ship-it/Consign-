from django.db import migrations


def activate_shipment(apps, schema_editor):
    Package = apps.get_model('packages', 'Package')
    TrackingHistory = apps.get_model('tracking', 'TrackingHistory')

    package = Package.objects.filter(tracking_number='DFX-DMCI5LEY').first()
    if not package or package.status != 'pending':
        return

    package.status = 'in_transit'
    package.save(update_fields=['status', 'updated_at'])
    TrackingHistory.objects.create(
        package=package,
        status='In Transit',
        location='Bangkok, Thailand',
        notes='Shipment departed origin and is in transit to Lahore, Pakistan',
    )


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0003_add_country_fields'),
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(activate_shipment, migrations.RunPython.noop),
    ]
