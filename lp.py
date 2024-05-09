import os
import click
from app import create_app, db
from app.models import User, Topic, Comment, MailList, InfoModel, Category

app = create_app(os.getenv('FLASK_CONFIG') or 'test')
app = create_app(test_config=None)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Topic=Topic, Comment=Comment, MailList=MailList, InfoModel=InfoModel)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
