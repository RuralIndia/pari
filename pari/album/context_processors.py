from mezzanine.conf import settings


def get_context_data(request):
        allow_comments = "true" if settings.ALLOW_COMMENTS_IN_TALKING_ALBUM else "false"
        return {"ALLOW_COMMENTS_IN_TALKING_ALBUM": allow_comments}
