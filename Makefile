SHELL := /bin/zsh
DIR = $(shell pwd)

clean:
	rm -rf build dist

build: clean
	echo $(shell git rev-parse --short HEAD) > version
	pyinstaller --clean --noconfirm main.spec

run: build
	./dist/ward.app/Contents/MacOS/ward

package:
	pushd dist; \
	productbuild --identifier $(WARD_IDENT) --sign $(WARD_INSTALLER) --component ward.app /Applications ward.pkg

noterize:
	pushd dist; \
	xcrun notarytool submit ward.pkg --keychain-profile $(WARD_IDENT) --wait

staple:
	pushd dist; \
	xcrun stapler staple ward.pkg

publish: build package noterize staple

.PHONY: build-ward
build-ward:
	pushd ward; \
	@docker build -f ../images/ward.dockerfile --tag gleif/ward .

