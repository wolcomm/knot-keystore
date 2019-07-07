<!--description: A tool for safely archiving knot dnssec key material to azure. -->
[![PyPI](https://img.shields.io/pypi/v/knot-keystore.svg)](https://pypi.python.org/pypi/knot-keystore)
[![Build Status](https://travis-ci.com/wolcomm/knot-keystore.svg?branch=master)](https://travis-ci.com/wolcomm/knot-keystore)
[![codecov](https://codecov.io/gh/wolcomm/knot-keystore/branch/master/graph/badge.svg)](https://codecov.io/gh/wolcomm/knot-keystore)

# knot-keystore

A tool to safely backup the knot kasp-db directory.

## overview

```bash
usage: knot-keystore [-h] [--socket SOCKET]
                     [--plugins [{local,azure} [{local,azure} ...]]]
                     [--retrieve] [--config-file CONFIG_FILE] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --socket SOCKET, -s SOCKET
                        path to knotc control socket
  --plugins [{local,azure} [{local,azure} ...]], -p [{local,azure} [{local,azure} ...]]
                        select archival plugins
  --retrieve, -r        retrieve archive
  --config-file CONFIG_FILE, -c CONFIG_FILE
                        path to a configuration file
  -v                    increase output verbosity
```

- tries to find the kasp-db path by reading `knotd` config over the control
  socket.
- plugins:
  - create an xz-compressed archive and put it somewhere, safely encrypted (default)
  - retrieve and decrypt the stored archive, ready to restore to the kasp-db directory (with `--retrieve`)

## available plugins

- `local`: create an encrypted copy of the archive and write it to disk along
  with the encryption key. Mostly useful for testing.
- `azure`: write the archive to an Azure storage blob, first encrypting it using
  "client-side-encryption" with a KEK stored in Azure Key Vault.
