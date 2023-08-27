# OUTPUT ARTICLES

Outputs a list of articles posted on Qiita or Zenn in CSV format.

## Installation

Use the standard Python3 library [venv](https://docs.python.org/ja/3/library/venv.html).

```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
(.venv) $ python3 -m pip install -r requirements.txt
```

## Usage

```bash
# launch virtual environment
$ . .venv/bin/activate

# create Qiita articles CSV File
(.venv) $ python3 output_articles.py qiita user_id
# create Zenn articles CSV File
(.venv) $ python3 output_articles.py zenn user_id

# finish virtual environment
(.venv) $ deactivate
```

You can only make up to 60 requests per hour per IP address because you are not authenticated with [Qiita API v2](https://qiita.com/api/v2/docs).
