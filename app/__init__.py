from core.database import create_model, Field

__all__ = ['Version', 'Available']

Version = create_model(
        'versions',
        Field('version', Field.STR),
        Field('folder', Field.STR),
)

Available = create_model(
    'available',
    Field('ruby_version', Field.STR),
    Field('full_version', Field.STR),
    Field('url', Field.STR),
)

if __name__ == '__main__':
    v1 = Version()
    v1.id = 1
    v1.version = '1.0'
    v1.folder = 'D:/tools/ruby/'
    v1.save()
