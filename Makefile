YAJL_VERSION=2.0.4
YAJL_BUILD_FOLDER=vendor/yajl/build/yajl-$(YAJL_VERSION)

UNAME_S:=$(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	YAJL_SRC_LIBNAME=libyajl.$(YAJL_VERSION).dylib
	YAJL_DST_LIBNAME=libyajl.dylib
else
	YAJL_SRC_LIBNAME=libyajl.so.$(YAJL_VERSION)
	YAJL_DST_LIBNAME=libyajl.so
endif

clean:
	rm -rf dist build

vendor/yajl:
	mkdir -p vendor
	cd vendor; git clone https://github.com/lloyd/yajl
	cd vendor/yajl; git checkout $(YAJL_VERSION)
	cd vendor/yajl; git apply ../yajl-symbols.patch

vendor/yajl/build/yajl-$(YAJL_VERSION): vendor/yajl
	cd vendor/yajl; ./configure
	cd vendor/yajl; make distro

jsonstream/$(YAJL_DST_LIBNAME): vendor/yajl/build/yajl-$(YAJL_VERSION)
	cp $(YAJL_BUILD_FOLDER)/lib/$(YAJL_SRC_LIBNAME) jsonstream/$(YAJL_DST_LIBNAME)

bundle: jsonstream/$(YAJL_DST_LIBNAME)

unbundle:
	rm -f jsonstream/$(YAJL_DST_LIBNAME)

wheel: bundle
	python setup.py bdist_wheel
