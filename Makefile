SHELL := /bin/zsh
DIR = $(shell pwd)

clean:
	rm -rf build dist

build: clean
	pyinstaller --clean --noconfirm main.spec

run: build
	./dist/ward.app/Contents/MacOS/ward

package:
	pushd dist; \
	productbuild --identifier $(ward_ident) --sign $(ward_signer) --component ward.app /Applications ward.pkg

noterize:
	pushd dist; \
	xcrun notarytool submit ward.pkg --keychain-profile $(ward_ident) --wait

staple:
	pushd dist; \
	xcrun stapler staple ward.pkg

publish: build package noterize staple
