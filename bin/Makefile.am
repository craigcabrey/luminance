bin_SCRIPTS = luminance

EXTRA_DIST = \
	luminance.in
	$(NULL)

CLEANFILES = \
	$(bin_SCRIPTS)
	$(NULL)

luminance: luminance.in Makefile
	$(SED)						\
		-e s!\@pythondir\@!$(pythondir)!	\
		-e s!\@pyexecdir\@!$(pyexecdir)!	\
		< $< > $@
	chmod a+x $@

all-local: luminance
