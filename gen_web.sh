#!/bin/bash
rm -r build
rm -r docs
mkdir docs
pygbag --archive   ../leobrooklyn
cp -avr build/web/* docs