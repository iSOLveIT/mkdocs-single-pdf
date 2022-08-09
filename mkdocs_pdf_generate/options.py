import logging
from typing import Dict

from mkdocs.config import config_options
from mkdocs.config.base import Config

from .templates.template import Template
from .templates.filters.url import URLFilter


class Options(object):
    DEFAULT_MEDIA_TYPE = "print"

    config_scheme = (
        ("media_type", config_options.Type(str, default=DEFAULT_MEDIA_TYPE)),
        ("verbose", config_options.Type(bool, default=False)),
        ("enabled_if_env", config_options.Type(str)),
        ("theme_handler_path", config_options.Type(str)),
        ("author", config_options.Type(str, default=None)),
        ("author_logo", config_options.Type(str, default=None)),
        ("copyright", config_options.Type(str, default=None)),
        ("disclaimer", config_options.Type(str, default=None)),
        ("cover", config_options.Type(bool, default=True)),
        ("cover_title", config_options.Type(str, default=None)),
        ("cover_subtitle", config_options.Type(str, default=None)),
        ("custom_template_path", config_options.Type(str, default="templates")),
        ("toc", config_options.Type(bool, default=True)),
        ("toc_title", config_options.Type(str, default="Table of Contents")),
        ("toc_level", config_options.Type(int, default=2)),
        ("cover_images", config_options.Type(dict, default=None)),
    )

    def __init__(self, local_config, config, logger: logging):
        self.strict = True if config["strict"] else False
        self.verbose = local_config["verbose"]
        # user_configs in mkdocs.yml
        self._user_config: Config = config
        self.site_url = config["site_url"]

        # Author and Copyright
        self._author = local_config["author"]
        if not self._author:
            self._author = config["site_author"]

        self._copyright = local_config["copyright"]
        if not self._copyright:
            self._copyright = config["copyright"]

        self._disclaimer = local_config["disclaimer"]

        # Individual document type cover
        self._cover_images: Dict = local_config["cover_images"]

        # Cover
        self.cover = local_config["cover"]
        if self.cover:
            self._cover_title = (
                local_config["cover_title"]
                if local_config["cover_title"]
                else config["site_name"]
            )
            self._cover_subtitle = local_config["cover_subtitle"]

        # path to custom template 'cover.html' and 'custom.css'
        self.custom_template_path = local_config["custom_template_path"]

        # TOC and Chapter heading
        self.toc = local_config["toc"]
        if self.toc:
            self.toc_title = local_config["toc_title"]
            self.toc_level = local_config["toc_level"]

        # Theming
        self.theme_name = config["theme"].name
        self.theme_handler_path = local_config.get("theme_handler_path", None)
        if not self.theme_handler_path:
            # Read from global config only if plugin config is not set
            self.theme_handler_path = config.get("theme_handler_path", None)

        # Template handler(Jinja2 wrapper)
        self._template = Template(self, config)

        # Author Logo
        logo_path_filter = URLFilter(self, config)
        self.author_logo = local_config["author_logo"]
        if not self.author_logo:
            self.author_logo = config["theme"]["logo"]
        if isinstance(self.author_logo, str):
            self.author_logo = logo_path_filter(self.author_logo)

        # for system
        self._logger = logger

    @property
    def author(self) -> str:
        return self._author

    @property
    def copyright(self) -> str:
        return self._copyright

    @property
    def disclaimer(self) -> str:
        return self._disclaimer

    @property
    def cover_title(self) -> str:
        return self._cover_title

    @property
    def cover_subtitle(self) -> str:
        return self._cover_subtitle

    @property
    def user_config(self) -> Config:
        return self._user_config

    @property
    def cover_images(self) -> Dict:
        return self._cover_images

    @property
    def logger(self) -> logging:
        return self._logger

    @property
    def template(self) -> Template:
        return self._template
