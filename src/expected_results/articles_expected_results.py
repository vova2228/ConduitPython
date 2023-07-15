class SuccessfullGetArticle:
    status_code = [200, 201]
    expected_keys = ["articles", "slug", "title", "description", "body", "tagList", "createdAt",
                     "updatedAt", "favorited", "favoritesCount", "author", "username", "bio", "image", "following",
                     "articlesCount"]


class SuccessfullPostArticle:
    status_code = [200, 201]
    expected_keys = ["article", "slug", "title", "description", "body", "tagList", "createdAt",
                     "updatedAt", "favorited", "favoritesCount", "author", "username", "bio", "image", "following"]


class SuccessfullDeleteArticle:
    status_code = 204
    expected_text = ''


class SuccessfullAddToFavorites:
    status_code = 200
    expected_keys = ["article", "slug", "title", "description", "body", "tagList", "createdAt",
                     "updatedAt", "authorId", "author", "username", "bio", "image", "following",
                     "favoritedBy"]


class SuccessfullGetComments:
    status_code = 200
    expected_keys = ["comments", "id", "createdAt", "updatedAt", "body",
                     "author", "username", "bio", "image", "following"]


class SuccessfullPostComments:
    status_code = 200
    expected_keys = ["comment", "id", "createdAt", "updatedAt", "body",
                     "author", "username", "bio", "image", "following"]


class SuccessfullDeleteComments:
    status_code = 200
    expected_text = ''
