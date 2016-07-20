resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --sourcedir=$(builddir) --generate-dependencies $(builddir)/resources.xml)

resources.gresource: resources.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) --sourcedir=$(builddir) $<

resourcedir = $(pkgdatadir)
resource_DATA = resources.gresource

icondir = $(pkgdatadir)/icons
icon_DATA = $(filter %.png,$(resource_files))

uidir = $(pkgdatadir)/ui
ui_DATA = $(filter %.ui,$(resource_files))

gsettings_SCHEMAS = com.craigcabrey.luminance.gschema.xml

gschemas.compiled: $(gsettings_SCHEMAS) Makefile
	$(AM_V_GEN) $(GLIB_COMPILE_SCHEMAS) $(builddir)

@GSETTINGS_RULES@

EXTRA_DIST = \
	$(hicolor_icon_files) \
	$(resource_files) \
	resources.xml \
	com.craigcabrey.luminance.gschema.xml \
	$(NULL)

CLEANFILES = \
	resources.gresource \
	*.valid \
	gschemas.compiled \
	$(NULL)

all-local: gschemas.compiled
