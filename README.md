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
| `_id` | An ObjectId corresponding to the Note's document in the DB |
| `created` | A timestamp corresponding to the date the object was created
| `updated` | A timestamp corresponding to the date the object was last updated
| `location` | A list of lat, lon coordinates of where this object was created

### Notes
Notes are little thoughts. They contain markdown about my life.

#### Fields
| Field | Description |
| --- | --- |
| `text` | Markdown string with the content of the note |
| `html` | html string of the text content |
| `public` | Boolean field denoting whether this note has been published (public) |
| `love_count` | Int field denoting the number of times this note has been loved |
| `slug` | A token used for sharing a note |

#### Endoints
| Route | Method | Description |
| --- | --- | --- |
| [**/notes/**](https://api.dhariri.com/notes/) | `GET` | Lists all public Notes |
| [**/notes/<note_id_or_slug>/**](https://api.dhariri.com/notes/599f3d98d9a23f00080fcd7f) | `GET` | Retrieve a single public or private note |