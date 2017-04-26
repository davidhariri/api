# Welcome 👋
This is the [public-facing API](https://api.dhariri.com/) for my life. You can use it to consume
information about me or you can browse the code to see how I like to
build things.

## Objects
### Base
Base objects are what all my objects inherit from. They just provide some convenience fields and methods.

#### Fields
| Field | Description |
| --- | --- |
| `_id` | An ObjectId corresponding to the Article's document in the DB |
| `created` | A timestamp corresponding to the date the object was created
| `updated` | A timestamp corresponding to the date the object was last updated

### Articles
Articles are my writing. They contain long-form markdown about my thoughts.

#### Fields
| Field | Description |
| --- | --- |
| `title` | A string article title |
| `content` | Markdown string with the content of the article |
| `published` | Boolean field denoting wether this article has been published (public) |
| `shared` | Boolean field denoting wether this article has been shared (private, link accesible with `share_handle`) |
| `love_count` | Int field denoting the number of times this article has been loved |
| `read_count` | Int field denoting the number of times this article has been read |
| `share_handle` | A UUID token used for sharing an article before it's been `published` |
| `slug` | A human-readable, unique, URL-safe string for more conveniently accessing a published article |

#### Endoints
| Route | Method | Authenticated | Description |
| --- | --- | --- | --- |
| **/articles/** | `GET` | 🔑 | Lists all Articles with all fields |
| **/articles/** | `GET` | None | Lists all `published` Articles with some [fields removed](/routes/articles.py#L50)  |