# Welcome 👋
This is the public-facing API for my life. You can use it to consume
information about me or you can browse the code to see how I like to
build things.

## Objects
### Articles
Articles are my writing. They contain long-form string content with
thoughts and opinions by me. They usually have lots of spelling
mistakes, poor grammar and lots of "arm-waiving".

#### Endoints
| Route | Method | Protected? | Description |
| --- | --- | --- | --- |
| */articles/* | `GET` | 🔐 | Lists `published` articles. If auth is valid, will list all articles |