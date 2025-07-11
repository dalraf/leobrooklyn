#!/bin/bash
pygbag --archive   ../leobrooklyn
[ -d "docs" ] || mkdir docs
cp -avr build/web/* docs