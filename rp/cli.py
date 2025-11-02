import click

from .generator import create_project


@click.group()
def cli():
    """RP - Rapid Django Project Generator"""
    pass


@cli.command()
@click.argument("project_name")
@click.option("--folder", default=None, help="Custom folder name")
@click.option("--template", default="default", help="Template type")
def create(project_name, folder, template):
    """Create a new Django project from template"""

    click.echo(f"✨ Creating Django project: {project_name}")

    # Folder defaults to project_name if not specified
    target_folder = folder or project_name

    try:
        create_project(
            project_name=project_name, target_folder=target_folder, template=template
        )
        click.echo(f"✅ Project '{project_name}' created in '{target_folder}/'")
        click.echo(f"\nNext steps:")
        click.echo(f"  cd {target_folder}")
        click.echo(f"  python -m venv venv")
        click.echo(f"  .venv\\Scripts\\activate")
        click.echo(f"  pip install -r requirements.txt")
        click.echo(f"  python manage.py migrate")

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)


if __name__ == "__main__":
    cli()
