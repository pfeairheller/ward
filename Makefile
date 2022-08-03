DIR = $(shell pwd)

clean:
	rm -rf build dist ward.pkg

build: clean
	pyinstaller --clean --noconfirm main.spec

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
