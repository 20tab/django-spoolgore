from setuptools import setup
setup(
    name='django-spoolgore',
    version='0.1',
    author='20Tab S.r.l.',
    author_email='info@20tab.com',
    description='A django EMAIL_BACKEND for enqueuing mail in the Spoolgore daemon.',
    url='https://github.com/20tab/django-spoolgore',
    packages=['spoolgore'],
)
