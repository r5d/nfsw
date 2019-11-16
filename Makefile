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
PRD_WHEEL=nfsw-0.1.0.dev3-py3-none-any.whl

HTTPD_CONF=etc/httpd.conf
ACME_CONF=etc/acme-client.conf
UWSGI_INI=etc/uwsgi/nfsw.ini
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

prd-init:
	ssh root@${PRD_HOST} \\"echo 'https://cdn.openbsd.org/pub/OpenBSD' \
		> /etc/installurl \
	&& pkg_add -v git redis py3-virtualenv cowsay rsync \
	&& git config --global --add user.name rsiddharth \
	&& git config --global --add user.email s@ricketyspace.net \
	&& git -C /etc init \
	&& git -C /etc add . \
	&& git -C /etc commit -m 'Initial commit' \
.PHONY: prd-init


prd-httpd:
	scp ${HTTPD_CONF} root@${PRD_HOST}:/${HTTPD_CONF}

	ssh root@${PRD_HOST} \\"rcctl enable httpd \
		&& rcctl restart httpd \\"
.PHONY: prd-httpd


prd-acme:
	scp ${ACME_CONF} root@${PRD_HOST}:/${ACME_CONF}
.PHONY: prd-acme


prd-user:
	ssh root@${PRD_HOST} \\"useradd -v -c 'NFSW daemon' \
		-e 0 -L daemon -s /sbin/nologin \
		-d /var/empty _nfsw\\"
.PHONY: prd-user


prd-venv:
	ssh root@${PRD_HOST} \\"mkdir -p /usr/local/virtualenv/ &&  \
		${VENV_CMD} --clear --python=python3 \
		${VENV_DIR}-prd \
		&& chown -R _nfsw:wheel ${VENV_DIR}-prd \\"
.PHONY: prd-venv


prd-install:
	ssh root@${PRD_HOST} \\"mkdir -p /var/www/nfsw/wheel/\\"
	scp dist/${PRD_WHEEL} \
		root@${PRD_HOST}:/var/www/nfsw/wheel/
	ssh root@${PRD_HOST} \\". ${VENV_DIR}-prd/bin/activate \
		&& pip install /var/www/nfsw/wheel/${PRD_WHEEL} \
		&& chown -R _nfsw:wheel ${VENV_DIR}-prd \
		&& chown -R _nfsw:wheel /var/www/nfsw/ \\"
.PHONY: prd-install

prd-upgrade:
	ssh root@${PRD_HOST} \\"mkdir -p /var/www/nfsw/wheel/\\"
	scp dist/${PRD_WHEEL} \
		root@${PRD_HOST}:/var/www/nfsw/wheel/
	ssh root@${PRD_HOST} \\". ${VENV_DIR}-prd/bin/activate \
		&& pip install --upgrade /var/www/nfsw/wheel/${PRD_WHEEL} \
		&& chown -R _nfsw:wheel ${VENV_DIR}-prd \
		&& chown -R _nfsw:wheel /var/www/nfsw/ \\"
.PHONY: prd-upgrade


prd-initdb:
	ssh root@${PRD_HOST} \\". ${VENV_DIR}-prd/bin/activate \
		&& FLASK_APP=nfsw flask init-db \
		&& chown -R _nfsw:wheel ${VENV_DIR}-prd \\"
.PHONY: prd-initdb


prd-rcd:
	ssh root@${PRD_HOST} mkdir -p -m 755 /etc/uwsgi
	scp ${UWSGI_INI} root@${PRD_HOST}:/${UWSGI_INI}
	scp ${RC_D} root@${PRD_HOST}:/${RC_D}
	ssh root@${PRD_HOST} chmod 555 /${RC_D}
	ssh root@${PRD_HOST} chmod 444 /${UWSGI_INI}
	ssh root@${PRD_HOST} chown root:wheel /${RC_D}
.PHONY: prd-rcd

prd-rr:
	ssh root@${PRD_HOST} rcctl restart nfsw redis httpd
.PHONY: prd-reload


clean:
	rm -rf build/ dist/ nfsw.egg-info/
	find ./ -type d -name '__pycache__' -exec rm -rf {} +
.PHONY: clean
