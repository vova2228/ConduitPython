class Successfullgetarticle:
    status_code = 200
    expected_keys = ["articles", "slug", "title", "description", "body", "tagList", "createdAt",
                     "updatedAt", "favorited", "favoritesCount", "author", "username", "bio", "image", "following",
                     "articlesCount"]


class SuccessfullPostArticle:
    status_code = 200
    expected_keys = ["article", "slug", "title", "description", "body", "tagList", "createdAt",
                     "updatedAt", "favorited", "favoritesCount", "author", "username", "bio", "image", "following"]


class SuccessfullDeleteArticle:
    status_code = 204
    expected_text = ''
