# `global_app`

Script allows to run crawler, process files, get statics and run extra methods

**Installation**:

```console
$ pip install -r requirements.txt
$ python main.py --help
```

**Usage**:

```console
$ python main.py [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

It's better to go with this order. 
First crawl than process. After that whatever you want...

* `crawl`: Crawl process is time-consuming.
* `process-crawler-file`: Process the file prepared by scrapy crawler.
* `get-stats`: Get statistics from processed files.
* `get-orphans`: Get orphans that is internal urls with 404...
* `plot-graph`: Get plot_name.png file from graph.
* `shortest-path`: Shows shortest path between urls if exists.

## `python main.py crawl`

Crawl process is time consuming. Be patient.
Logging is enabled, that you can see the process is ongoing.
Crawler skips redirects 301,302

:param filename: Filename without extension
:param crawl: Extra confirmation
:param override_file: Overrides existing file
:return: None

**Usage**:

```console
$ python main.py crawl [OPTIONS] [FILENAME]
```

**Arguments**:

* `[FILENAME]`: Filename without extension  [default: global_app_spider]

**Options**:

* `--crawl / --no-crawl`: The crawl process may take some longer time  [default: False]
* `--override-file / --no-override-file`: Overrides existing crawler file  [default: False]
* `--help`: Show this message and exit.

## `python main.py get-orphans`

Get orphans that is internal urls with 404 errors.
Not checking external links.

:param filename: Filename without extension
:return: None

**Usage**:

```console
$ python main.py get-orphans [OPTIONS] [FILENAME]
```

**Arguments**:

* `[FILENAME]`: Filename without extension  [default: global_app_spider]

**Options**:

* `--help`: Show this message and exit.

## `python main.py get-stats`

Get statistics from processed files.

:param filename: Filename without extension
:return: None

**Usage**:

```console
$ python main.py get-stats [OPTIONS] [FILENAME]
```

**Arguments**:

* `[FILENAME]`: Filename without extension  [default: global_app_spider]

**Options**:

* `--help`: Show this message and exit.

## `python main.py plot-graph`

Get plot_name.png file from graph.
Better plots one can create with for example cytoscape.org/cytoscape.js

:param plot_name: Name file without extension with plot
:param filename: Filename without extension
:return: None

**Usage**:

```console
$ python main.py plot-graph [OPTIONS] PLOT_NAME [FILENAME]
```

**Arguments**:

* `PLOT_NAME`: Filename without extension  [required]
* `[FILENAME]`: Filename without extension  [default: global_app_spider]

**Options**:

* `--help`: Show this message and exit.

## `python main.py process-crawler-file`

Process the file prepared by scrapy crawler.

:param filename: Filename without extension
:return: None

**Usage**:

```console
$ python main.py process-crawler-file [OPTIONS] [FILENAME]
```

**Arguments**:

* `[FILENAME]`: Filename without extension  [default: global_app_spider]

**Options**:

* `--help`: Show this message and exit.

## `python main.py shortest-path`

Shows shortest path between urls if exists.

:param from_node: Starting url
:param to_node: Destination url
:param filename: Filename without extension
:return: None

**Usage**:

```console
$ python main.py shortest-path [OPTIONS] FROM_NODE TO_NODE [FILENAME]
```

**Arguments**:

* `FROM_NODE`: Starting url   [required]
* `TO_NODE`: Destination url  [required]
* `[FILENAME]`: Filename without extension  [default: global_app_spider]

**Options**:

* `--help`: Show this message and exit.
