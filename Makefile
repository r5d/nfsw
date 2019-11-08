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
PRD_HOST=cygnus
PRD_WHEEL=nfsw-0.1.0.dev1-py3-none-any.whl
RC_D=etc/rc.d/nfsw

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


build:
	python setup.py bdist_wheel
.PHONY: build


prd-user:
	ssh root@${PRD_HOST} \\"useradd -v -c 'NFSW daemon' \
		-e 0 -L daemon -s /sbin/nologin \
		-d /var/empty _nfsw\\"
.PHONY: prov-user

prd-venv:
	ssh root@${PRD_HOST} \\"mkdir -p /usr/local/virtualenv/ &&  \
		${VENV_CMD} --clear --python=python3 \
		${VENV_DIR}-prd\\"
.PHONY: prd-venv

prd-install:
	ssh root@${PRD_HOST} \\"mkdir -p /var/www/nfsw/wheel/\\"
	scp dist/${PRD_WHEEL} \
		root@${PRD_HOST}:/var/www/nfsw/wheel/
	ssh root@${PRD_HOST} \\". ${VENV_DIR}-prd/bin/activate \
		&& pip install /var/www/nfsw/wheel/${PRD_WHEEL} \\"
.PHONY: prd-install

rcd:
	scp ${RC_D} root@${PRD_HOST}:/${RC_D}
	ssh root@${PRD_HOST} chmod 555 /${RC_D}
	ssh root@${PRD_HOST} chown root:wheel /${RC_D}
.PHONY: rcd


clean:
	rm -rf build/ dist/ nfsw.egg-info/
	find ./ -type d -name '__pycache__' -exec rm -rf {} +
.PHONY: clean
