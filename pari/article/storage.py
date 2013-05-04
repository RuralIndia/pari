from django.core.files.storage import get_storage_class

from storages.backends.s3boto import S3BotoStorage


class CachedS3BotoStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class("compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name


StaticRootS3BotoStorage = lambda: CachedS3BotoStorage(location='')


MediaRootS3BotoStorage = lambda: CachedS3BotoStorage(location='media')
