"""
demonstrate python usage for command line tool, machine setup
# install python36
# pip-3.6 install pipenv
# pip-3.6 install –upgrade pip

% pipenv --three
% pipenv install boto3
% pipenv install click
% pipenv install -d ipython

% pipenv shell
…..
Then run
"""

import boto3
import click

session = boto3.session.Session()
s3 = session.resource('s3')

@click.group()
def cli():
    "Python Click Demo"
    pass


@cli.command('list')
def list_buckets():
    """
    List the S3 buckets
    """
    for bucket in s3.buckets.all():
        print(bucket)




@cli.command('dir')
@click.argument('bucket')
def list_objects(bucket):
    """
    List the S3 bucket contents
   """
    for obj in s3.Bucket(bucket).objects.all():
        #print(dir(obj))
        print(obj.key)


if __name__ == '__main__':
    cli()
