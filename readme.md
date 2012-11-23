Get the length of each section for each revision in a Wikipedia article. The revisions are fetched five at a time from the [English Wikipedia API](en.wikipedia.org/w/api.php), so articles with a long history may take a while to load.

Web API available using [Bottle](http://bottlepy.org/docs/dev/) on port 8080.

## Revision info ##
```python
{
  "comment": "",            # Edit summary
  "length": 0,              # Total characters in the article
  "page_id": 0,             # Page ID
  "page_title": "",         # Page title
  "rev_id": 0,              # Current revision ID
  "rev_parent_id": 0,       # Parent revision ID
  "sections": [],           # List of section info
  "sha1": "",               # Hash of the revision text (useful for detecting reverts/undo edits)
  "tags": [],               # (Mostly unused)
  "time": "",               # Timestamp of the edit
  "time_delta": 0,          # Time since parent revision
  "user_id": 0,             # User ID
  "user_text": ""           # Username
}
````


## Section info ##
```python
{
  "depth": 1,       # Heading level
  "length": 0,      # No. of characters
  "length_diff": 0, # Length difference from parent revision
  "name": ""        # Title of section
}   
```

## Todo ##
 * Detect vandalism/reverts
 * More detail about revisions using [difflib](http://docs.python.org/2/library/difflib.html)
 * Save results in database?