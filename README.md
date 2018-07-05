# python-buildtools

A set of wepback or gulp-like buildtools.

Create a forgeconfig.py file in you project.

```python
from forge.plugins.forgecopy import copySrc
from forge.plugins.forgecompile import compileSrc
from forge.plugins.forgewatch import watchSrc
from forge.plugins.forgebuild import buildSrc
from forge.plugins.forgeeggify import eggifySrc

def watch(config):
    return watchSrc("./src", [buildSrc(config)])

def build(config):
    return buildSrc(config)

config = {
    "src": "./src",
    "dest": [
        "/some/path/to/destination1",
        "/some/path/to/destination2"  
    ],
    "plugins": [
        copySrc("copy/this/path/", "to/here"),
        copySrc({
            "./copy/this/file.py": "./to/here.py"
        }),
        compileSrc("compile/contents/of/this/path", "to/here"),
        eggifySrc(
            {
                "/compile/this/egg/setup.py" : "to/eggs"
            },
            config={
                "purge": True
            }
        )
    ]
}
```

Cd into your project directory and run forge like this:

```
python -m forge build
```

to build your project or

```
python -m forge watch
```

to rebuild on file change