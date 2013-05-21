from django.core.files.storage import get_storage_class, FileSystemStorage

from storages.backends.s3boto import S3BotoStorage
from filebrowser_safe.storage import S3BotoStorageMixin, FileSystemStorageMixin

from mezzanine.conf import settings

from .common import upload_to_s3


class CachedS3BotoStorage(S3BotoStorageMixin, S3BotoStorage):
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class("compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name


StaticRootS3BotoStorage = lambda: CachedS3BotoStorage(location='')


MediaRootS3BotoStorage = lambda: CachedS3BotoStorage(location='media')


class ParallelS3Storage(FileSystemStorageMixin, FileSystemStorage):
    def _save(self, name, content):
        if settings.S3_URL:
            upload_to_s3(name, in_memory_file=content)
            return super(ParallelS3Storage, self)._save(name, content)
