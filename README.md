# Ward 

MacOS wrapper around a KERI agent.

[![keri version](https://img.shields.io/badge/KERI-0.6.6-green.svg)](https://pypi.org/project/keri/)
[![python version](https://img.shields.io/badge/python-3.10.4-blue.svg)](https://www.python.org/downloads/)

### Running locally
    pip install -r requirements.txt
    make build
    ./dist/ward.app/Contents/MacOS/ward

### Publishing

Requires an identifier and signing certificates configured in an Apple developer account.

    source venv/bin/activate
    export ward_signer="SIGNER_HASH"; make publish;

`SIGNER_HASH` should be of type `Developer ID Installer` and can be found by using:

    security find-identity -p basic -v

#### Useful links on building for macOS

* [Creating Distribution-Signed Code for Mac](https://developer.apple.com/forums/thread/701514#701514021)

* [Packaging Mac Software for Distribution](https://developer.apple.com/forums/thread/701581#701581021)

##### Icon Attribution
Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons"> Smashicons </a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>