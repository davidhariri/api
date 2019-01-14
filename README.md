# Welcome 👋
This is the [public-facing API](https://api.dhariri.com/) for my life. You can use it to consume
information about me or you can browse the code to see how I like to
build things.

# Set Up
```py
cat .env.example > .env
pipenv shell
pipenv install
flask run
```

# Documentation
## Posts
Posts are little thoughts or events. They can be private (access only by direct url) or public. They usually have text, but can have locations, media, reviews, links etc... See the fields below for more information.

| Field | Description |
| --- | --- |
| `id` | An auto-incremented id for this post |
| `date_created` | The date and time at which this post was created |
| `date_updated` | The date and time at which this post was last updated |
| `slug` | A token used for sharing a post |
| `comment` | A string explaining the event |
| `public` | Boolean field denoting whether this post has been published publicly. If this is false, only knowing the slug will reveal the post |
| `location_lat` | The GPS latitude of the post |
| `location_lon` | The GPS longitude of the post |
| `location_name` | The name of the location where this post was created |
| `review` | A review for the post out of 5 |
| `link_name` | A name of an attached link |
| `link_uri` | An attached link |
| `love_count` | A field denoting the number of times this post has been loved |
| `media` | A list of URLs with media attachments |
| `topics` | A list of topics that this event pertains to |
| `tweet_id` | The id of the corresponding Tweet |

### [/posts/](https://api.dhariri.com/posts/)

| Method | Parameters | Description |
| --- | --- | --- |
| POST | _None_ | Creates a Post object from the fields (see fields above) passed as JSON in the body of the request. Requires an authentication token as a header (`Authentication: Bearer <token>`) |
| GET | `?page=<int>`, `?size=<int>` | Lists Post objects that have their `public` field set to `true`.

### [/posts/\<slug\>](https://api.dhariri.com/posts/BFz1LIg/)

| Method | Parameters | Description |
| --- | --- | --- |
| GET | _None_ | Shows a post for the `slug` regardless of it's `public` field. If not found, a status of 404 will be returned.
| DELETE | _None_ | Deletes a Post object matching `slug`. Requires an authentication token as a header (`Authentication: Bearer <token>`) |

## Media
Media can be images or GIFs and upload to static.dhariri.com. This is essentially an upload endpoint with some optimization features. For example, GIFs are uploaded on their own, but return with an MP4 link and a poster image. Static images return with an optimized version as well. See fields below.

#### URL Naming
`url_optimized` contains some helpful information about the media embedded in the file name for aiding graceful loading of the media itself:

`<ASPECT_RATIO>_<AVG_COLOR_HEX>_<UUID><?.thumb|?.poster>.<jpeg|mp4>`

| Field | Description |
| --- | --- |
| `id` | An auto-incremented id for the media |
| `date_created` | The date and time at which the media was created |
| `date_updated` | The date and time at which the media was last updated |
| `uuid` | A unique id string used to identify the media |
| `media_type` | The type of media that was uploaded |
| `url` | The URL of the raw file that was uploaded. This could be called the "full size" or "large" media. |
| `url_optimized` | The URL of the optimized version of the file that was uploaded. This is what will be used most often. |
| `url_poster` | If the file uploaded is a GIF, this is a picture of the first frame of the optimized version. |
| `showcase` | A boolean for whether or not this media should be showcased. Useful for a photograph that's more of a "work of art". |
| `width` | The width of the original file |
| `height` | The height of the original file |
| `aspect` | The aspect ratio of the original file. This is embedded in the file name. |
| `shot_exposure` | The exposure of the image. Pulled from EXIF tags. |
| `shot_aperture` | The aperture as an f-stop of the image. Pulled from EXIF tags. |
| `shot_speed` | The ISO speed of the image. Pulled from EXIF tags. |
| `shot_focal_length` | The focal length of the lens which captured the image. Pulled from EXIF tags. |
| `camera_make` | The make of the camera which captured the image. Pulled from EXIF tags. |
| `average_color` | The average hex color in the image. |

### [/media/](https://api.dhariri.com/media/)

| Method | Parameters | Description |
| --- | --- | --- |
| POST | `?showcase=<bool>` | Creates a Media object from a `file` passed as `multipart/form-data` (see fields above). Requires an authentication token as a header (`Authentication: Bearer <token>`) |