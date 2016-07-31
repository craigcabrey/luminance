AC_PREREQ([2.69])
AC_INIT([luminance],
        m4_esyscmd(echo -n `git describe --always --tags`),
        [https://github.com/craigcabrey/luminance/issues],
        [luminance],
        [https://craigcabrey.github.io/luminance/])

AM_INIT_AUTOMAKE([foreign])

AM_PATH_PYTHON([3.5])

GLIB_GSETTINGS

DESKTOP_SCHEMAS_REQUIRED_VERSION=3.18.0
GTK_REQUIRED_VERSION=3.18.0
PYGOBJECT_REQUIRED_VERSION=3.20.0

PKG_CHECK_MODULES([GSETTINGS_DESKTOP_SCHEMAS], [gsettings-desktop-schemas >= $DESKTOP_SCHEMAS_REQUIRED_VERSION])
PKG_CHECK_MODULES([GTK], [gtk+-3.0 >= $GTK_REQUIRED_VERSION])
PKG_CHECK_MODULES([PYGOBJECT3], [pygobject-3.0 >= $PYGOBJECT_REQUIRED_VERSION])

GLIB_COMPILE_RESOURCES=`$PKG_CONFIG --variable glib_compile_resources gio-2.0`
AC_SUBST(GLIB_COMPILE_RESOURCES)

AC_PROG_SED
AC_CONFIG_FILES([
  Makefile
  bin/Makefile
  data/Makefile
  luminance/Makefile
  luminance/views/Makefile
])

AC_OUTPUT
