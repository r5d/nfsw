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

PRD_HOST=vela
PRD_WHEEL=nfsw-0.1.0.dev4-py3-none-any.whl

ACME_CONF=etc/acme-client.conf
UWSGI_INI=etc/uwsgi/nfsw.ini
RC_D=etc/rc.d/nfsw

NGINX_DIR=etc/nginx
NEWSYSLOG=etc/newsyslog.conf

SSH_PUB=lyra.pub

TB=bin/tball
TB_CNF=etc/tball
CRON=cron/root

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
	&& pkg_add -I -v git redis py3-virtualenv cowsay \
			rsync-3.1.3-iconv nginx bash \
	&& git config --global --add user.name rsiddharth \
	&& git config --global --add user.email s@ricketyspace.net \
	&& git -C /etc init \
	&& git -C /etc add . \
	&& git -C /etc commit -m 'Initial commit' \
	&& useradd -v -c 'NFSW daemon' \
		-e 0 -L daemon -s /sbin/nologin \
		-d /var/empty _nfsw \
	&& git -C /etc add . \
	&& git -C /etc commit -m 'Add _nfsw user'\\"
.PHONY: prd-init


prd-nginx:
	rsync -a ${NGINX_DIR}/ \
		root@${PRD_HOST}:/${NGINX_DIR}
	rsync -a ${NEWSYSLOG} \
		root@${PRD_HOST}:/${NEWSYSLOG}
	ssh root@${PRD_HOST} \\"rcctl enable nginx \
		&& rcctl restart nginx \
		&& git -C /etc add nginx rc.conf.local\\"
.PHONY: prd-nginx


prd-acme:
	rsync ${ACME_CONF} root@${PRD_HOST}:/${ACME_CONF}
.PHONY: prd-acme


prd-venv:
	ssh root@${PRD_HOST} \\"mkdir -p /usr/local/virtualenv/ &&  \
		${VENV_CMD} --clear --python=python3 \
		${VENV_DIR}-prd \
		&& chown -R _nfsw:wheel ${VENV_DIR}-prd \\"
.PHONY: prd-venv


prd-install:
	ssh root@${PRD_HOST} \\"mkdir -p /var/www/nfsw/wheel/\\"
	rsync dist/${PRD_WHEEL} \
		root@${PRD_HOST}:/var/www/nfsw/wheel/
	ssh root@${PRD_HOST} \\". ${VENV_DIR}-prd/bin/activate \
		&& pip install /var/www/nfsw/wheel/${PRD_WHEEL} \
		&& chown -R _nfsw:wheel ${VENV_DIR}-prd \
		&& chown -R _nfsw:wheel /var/www/nfsw/ \\"
.PHONY: prd-install

prd-upgrade:
	ssh root@${PRD_HOST} \\"mkdir -p /var/www/nfsw/wheel/\\"
	rsync dist/${PRD_WHEEL} \
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


prd-config:
	ssh root@${PRD_HOST} \\"echo \"SECRET_KEY=b'`openssl rand -hex 16`'\" \
		> ${VENV_DIR}-prd/var/nfsw-instance/config.py\\"
.PHONY: prd-config

prd-rcd:
	ssh root@${PRD_HOST} mkdir -p -m 755 /etc/uwsgi
	rsync ${UWSGI_INI} root@${PRD_HOST}:/${UWSGI_INI}
	rsync ${RC_D} root@${PRD_HOST}:/${RC_D}
	ssh root@${PRD_HOST} \\"chmod 555 /${RC_D} \
		&& chmod 444 /${UWSGI_INI} \
		&& chown root:wheel /${RC_D} \
		&& rcctl enable nfsw redis \
		&& rcctl restart nfsw redis \
		&& git -C /etc add rc.conf.local rc.d/nfsw uwsgi/\\"
.PHONY: prd-rcd

prd-rr:
	ssh root@${PRD_HOST} rcctl restart nfsw redis httpd
.PHONY: prd-reload


prd-sk:
	rsync ssh/${SSH_PUB} root@${PRD_HOST}:~/.ssh/
	ssh root@${PRD_HOST} \\"cat ~/.ssh/${SSH_PUB} \
		>> ~/.ssh/authorized_keys\\"
.PHONY: prd-sk

prd-tb:
	rsync -a ${TB} root@${PRD_HOST}:/usr/local/bin/tball
	rsync -a ${TB_CNF} root@${PRD_HOST}:/${TB_CNF}
	rsync -a ${CRON} root@${PRD_HOST}:~/.cron
	ssh root@${PRD_HOST} \\"mkdir -p \
			/var/backups/nfsw/instance \
		&& crontab ~/.cron \
		&& git -C /etc add tball\\"
.PHONY: prd-tb

clean:
	rm -rf build/ dist/ nfsw.egg-info/
	find ./ -type d -name '__pycache__' -exec rm -rf {} +
.PHONY: clean
