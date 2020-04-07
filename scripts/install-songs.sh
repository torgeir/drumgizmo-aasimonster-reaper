#!/bin/zsh
for p in **/*.h2song; do echo copying $p; cp $p ~/.hydrogen/data/songs; done