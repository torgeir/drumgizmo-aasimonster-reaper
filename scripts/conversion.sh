#!/bin/zsh
for f in midi/*; do
  (cd $f &&
  for ff in *; do
    (cd $ff &&
    for fff in *; do
      (cd $fff && 
      for mid in *mid; do
        echo "processing $mid";
        ../../../../midi2hydro_pattern.py "$mid" "$mid.h2pattern" "$ff"
      done
    )
    done
    )
  done
  )
done
