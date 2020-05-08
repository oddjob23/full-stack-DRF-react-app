from django.apps import AppConfig


class ArticleAppsConfig(AppConfig):
    name = 'articles'
    label = 'articles'
    verbose_name = 'Articles'

    def ready(self):
        import articles.signals


default_app_config = 'articles.ArticleAppsConfig'
