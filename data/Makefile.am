resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --sourcedir=$(builddir) --generate-dependencies $(builddir)/resources.xml)

resources.gresource: resources.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) --sourcedir=$(builddir) $<

resourcedir = $(pkgdatadir)
resource_DATA = resources.gresource

# hicolor icons
hicolor_icon16dir = $(datadir)/icons/hicolor/16x16/apps
hicolor_icon16_DATA = icons/hicolor/16x16/apps/luminance.png
hicolor_icon32dir = $(datadir)/icons/hicolor/32x32/apps
hicolor_icon32_DATA = icons/hicolor/32x32/apps/luminance.png
hicolor_icon48dir = $(datadir)/icons/hicolor/48x48/apps
hicolor_icon48_DATA = icons/hicolor/48x48/apps/luminance.png
hicolor_icon64dir = $(datadir)/icons/hicolor/64x64/apps
hicolor_icon64_DATA = icons/hicolor/64x64/apps/luminance.png
hicolor_icon128dir = $(datadir)/icons/hicolor/128x128/apps
hicolor_icon128_DATA = icons/hicolor/128x128/apps/luminance.png
hicolor_icon256dir = $(datadir)/icons/hicolor/256x256/apps
hicolor_icon256_DATA = icons/hicolor/256x256/apps/luminance.png
hicolor_icon_files = \
	$(hicolor_icon16_DATA) \
	$(hicolor_icon22_DATA) \
	$(hicolor_icon32_DATA) \
	$(hicolor_icon48_DATA) \
	$(hicolor_icon64_DATA) \
	$(hicolor_icon128_DATA) \
	$(hicolor_icon256_DATA)

install-data-hook: update-icon-cache
uninstall-hook: update-icon-cache

gtk_update_hicolor_icon_cache = gtk-update-icon-cache -f -t $(datadir)/icons/hicolor

update-icon-cache:
	@-if test -z "$(DESTDIR)"; then \
		echo "Updating GTK hicolor icon cache."; \
		$(gtk_update_hicolor_icon_cache); \
	else \
		echo "Icon cache not updated."; \
	fi

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
