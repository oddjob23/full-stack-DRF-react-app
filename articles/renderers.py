from core.renderers import UniversalJSONRenderer


class ArticleJSONRenderer(UniversalJSONRenderer):
    object_label = 'article'
    object_label_plural = 'articles'
