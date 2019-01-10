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
| `id` | An automatically incremented number that is unique to this record |
| `created` | A timestamp corresponding to the date the object was created
| `updated` | A timestamp corresponding to the date the object was last updated

### Posts
Posts are little thoughts. They contain events in my life.

#### Fields
| Field | Description |
| --- | --- |
| `slug` | A token used for sharing a post |
| `comment` | A string explaining the event |
| `public` | Boolean field denoting whether this post has been published publicly. If this is false, only knowing the slug will reveal the post |
| `location_latitude` | The latitude of the post |
| `location_longitude` | The longitude of the post |
| `location_name` | The name of the location |
| `review` | A review for the post out of 5 |
| `link_name` | A name of an attached link |
| `link_uri` | An attached link |
| `love_count` | A field denoting the number of times this post has been loved |
| `media` | A list of URLs with media attachments |
| `topics` | A list of topics that this event pertains to |
| `tweet_id` | The id of the corresponding Tweet |


#### Endoints
| Route | Method | Description |
| --- | --- | --- |
| [**/posts/**](https://api.dhariri.com/posts/) | `GET` | Lists all public posts |
| [**/posts/<post_slug_str>/**](https://api.dhariri.com/posts/xxxxxxx/) | `GET` | Retrieve a single public or private post |
