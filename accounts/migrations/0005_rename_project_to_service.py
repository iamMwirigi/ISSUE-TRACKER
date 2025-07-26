# Generated manually to handle Project to Service transition

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_issue_assigned_to_alter_issue_status'),
    ]

    operations = [
        # Rename the table from accounts_project to accounts_service
        migrations.RenameModel(
            old_name='Project',
            new_name='Service',
        ),
        
        # Update the foreign key in Issue model
        migrations.RenameField(
            model_name='issue',
            old_name='project',
            new_name='service',
        ),
        
        # Add new fields to Issue model
        migrations.AddField(
            model_name='issue',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.office'),
        ),
        migrations.AddField(
            model_name='issue',
            name='attachments',
            field=models.FileField(blank=True, null=True, upload_to='issue_attachments/'),
        ),
        
        # Rename title field to type
        migrations.RenameField(
            model_name='issue',
            old_name='title',
            new_name='type',
        ),
        
        # Update related_name for reporter field
        migrations.AlterField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reported_issues', to='accounts.user'),
        ),
    ] 