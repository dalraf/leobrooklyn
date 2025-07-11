#!/bin/bash
mkdir docs
pygbag --archive   ../leobrooklyn
cp -avr build/web/* docs