class SuccesfullGetArticle:
    status_code = 200
    expected_keys = ["articles", "slug", "title", "description", "body", "tagList", "createdAt",
                     "updatedAt", "favorited", "favoritesCount", "author", "username", "bio", "image", "following",
                     "articlesCount"]