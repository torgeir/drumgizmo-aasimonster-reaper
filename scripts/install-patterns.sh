#!/bin/zsh
for p in **/*.h2pattern; do echo copying $p; cp $p ~/.hydrogen/data/patterns; done