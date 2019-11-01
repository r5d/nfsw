# -*- coding: utf-8 -*-
#
#   SPDX-License-Identifier: ISC
#
#   Copyright (C) 2019 rsiddharth <s@ricketyspace.net>
#
#   This file is part of nfsw.
#

VENV_DIR=/usr/local/virtualenv/.nfsw
VENV_CMD=virtualenv-3
JSHINT=~/.npm-packages/bin/jshint

dunno:
	@echo "Give me somepin to make"

dev:
	pip install -r requirements.txt
.PHONY: dev


va:
	@echo ${VENV_DIR}/bin/activate
.PHONY: va


venv:
	rm -rf *.egg-info
	${SHELL} -c 'if [[ -d $(VENV_DIR) ]] then \
		rm -rf $(VENV_DIR); fi'
	${VENV_CMD} --clear --python=python3 $(VENV_DIR)
.PHONY: venv


jsh:
	${JSHINT} nfsw/static/io.js
	${JSHINT} nfsw/static/epilogue.js
.PHONY: jsh
