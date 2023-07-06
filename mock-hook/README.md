# mock-hook


## install

* 打包

```bash
> python3.9 -m poetry build
```

* 安装

```bash
> python3.9 -m pip install ./dist/mock_hook-0.1.1-py3-none-any.whl
```

* 卸载

```bash
> python3.9 -m pip uninstall mock_hook
```

## Used

* `copycat` cli tools.

```
> copycat --help
Usage: copycat [OPTIONS]

  Copycat CLI.

Options:
  -h, --hook TEXT      hook function file.
  -q, --request TEXT   request data file.
  -s, --response TEXT  response data file.
  --help               Show this message and exit.
```
