#!/bin/zsh
for f in *bpm; do
  cd $f;
  for ff in *; do
    cd $ff;
    for fff in *; do
      cd $fff;
      for mid in *mid; do
        echo "processing $mid";
        python ~/Recording/MT\ power\ drum\ kit\ 2/midi2hydro_pattern.py "$mid" "$mid.h2pattern" "$ff"
      done
      cd ..;
    done
    cd ..;
  done
  cd ..;
done
