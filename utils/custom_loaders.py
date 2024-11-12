import re
from django.template.loaders.filesystem import Loader as FilesystemLoader
from django.template import TemplateDoesNotExist
from django.template.loaders.app_directories import Loader as AppDirectoriesLoader
from django.conf import settings


class CustomLoader:
    def __init__(self, *args, **kwargs):
        self.loaders = [
            FilesystemLoader(*args, **kwargs),
            AppDirectoriesLoader(*args, **kwargs),
        ]

    def get_template(self, template_name, *args, **kwargs):
        for loader in self.loaders:
            try:
                template = loader.get_template(template_name, *args, **kwargs)
                if settings.DEBUG is False:  # Check if in production mode
                    template_content = template.template.source
                    template_content = re.sub(
                        r"\{% static 'website_v2/([^']*)' %\}",
                        r"https://cdn.musfiqdehan.com/msa-v2/$1",
                        template_content,
                    )
                    template.template.source = template_content
                return template
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(template_name)

    def load_template(self, *args, **kwargs):
        return self.get_template(*args, **kwargs)

    def get_template_sources(self, *args, **kwargs):
        for loader in self.loaders:
            yield from loader.get_template_sources(*args, **kwargs)
