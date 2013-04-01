# $Id: Makefile,v 1.6 2008/10/29 01:01:35 ghantoos Exp $
#
LBLUE_ON = \033[0;36m
GREEN_ON = \033[0;32m
OFF = \033[m

DOXYGEN=`which doxygen`
PYTHON=`which python`
DESTDIR=/
PROJECT=sipptam

all:
	@echo "$(GREEN_ON)make localshop.indigital$(OFF) - sdist to the localshop.indigital"
	@echo "$(GREEN_ON)make test$(OFF) - Run the test environment"
	@echo "$(GREEN_ON)make doc$(OFF) - Create associated documentation (doxygen/LaTeX)"
	@echo "$(GREEN_ON)make source$(OFF) - Create source package"
	@echo "$(GREEN_ON)make install$(OFF) - Install on local system"
	@echo "$(GREEN_ON)make buildrpm$(OFF) - Generate a $(LBLUE_ON)rpm$(OFF) package"
	@echo "$(GREEN_ON)make builddeb$(OFF) - Generate a $(LBLUE_ON)deb$(OFF) package"
	@echo "$(GREEN_ON)make clean$(OFF) - Get rid of scratch and byte files"

localshop.indigital:
	python setup.py register -r indigital sdist upload -r indigital

test:
	python /usr/local/lib/python2.6/dist-packages/tam/tests/main.py

doc:
	cd doc; $(DOXYGEN) doxygen.conf

source:
	$(PYTHON) setup.py sdist $(COMPILE)

install:
	$(PYTHON) setup.py install --root $(DESTDIR) $(COMPILE)

buildrpm:
	$(PYTHON) setup.py bdist_rpm --post-install=rpm/postinstall --pre-uninstall=rpm/preuninstall

builddeb:
	# build the source package in the parent directory
	# then rename it to project_version.orig.tar.gz
	#	$(PYTHON) setup.py sdist $(COMPILE) --dist-dir=../ --prune
	$(PYTHON) setup.py sdist $(COMPILE) --dist-dir=../ 
	rename -f 's/$(PROJECT)-(.*)\.tar\.gz/$(PROJECT)_$$1\.orig\.tar\.gz/' ../*
	# build the package
	dpkg-buildpackage -i -I -rfakeroot

clean:
	find . -type f -name "*.pyc" -exec rm -f '{}' \;
	find . -type f -name "*~" -exec rm -f '{}' \;
	$(PYTHON) setup.py clean
	$(MAKE) -f $(CURDIR)/debian/rules clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete
