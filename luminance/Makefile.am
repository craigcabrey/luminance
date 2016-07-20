SUBDIRS = views

BUILT_SOURCES = __init__.py

luminancedir = $(pkgpythondir)

luminance_PYTHON = application.py \
                   __init__.py

__init__.py: __init__.py.in
	$(SED)					\
		-e 's|@datadir[@]|$(pkgdatadir)|g' \
		-e 's|@version[@]|$(VERSION)|g' \
		< $< > $@
