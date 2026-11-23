#!/bin/zsh
# Files tracks downloaded from Suno into audio/ under the ids her site uses.
# Run from anywhere. Safe to re-run; it only copies.
set -u
AUD="$HOME/Projects/followkellie.github.io/audio"
mkdir -p "$AUD"
filed=0

match_id () {
  local n="${1:l}"
  case "$n" in
    *glitch*growth*)                     print "108f79a7" ;;
    *sign*on*the*line*vaudeville*|*sign*on*the*line*116*) print "6f60b69d" ;;
    *sign*on*the*line*spatial*|*sign*on*the*line*digital*) print "dc9aa87d" ;;
    *sign*on*the*line*)                  print "6f60b69d" ;;
    *signed*and*prayed*)                 print "1875425a" ;;
    *can*t*fall*off*the*floor*|*cant*fall*off*the*floor*) print "9e612e7c" ;;
    *wisdom*or*trauma*)                  print "52266d37" ;;
    *loneliness*killing*people*)         print "c30d26a7" ;;
    *)                                   print "" ;;
  esac
}

for f in "$HOME/Downloads"/*.(mp3|m4a|wav|flac)(Nom); do
  base="${f:t}"
  id="$(match_id "$base")"
  [[ -z "$id" ]] && continue
  ext="${f:e:l}"
  cp "$f" "$AUD/$id.$ext"
  print "filed  $base  ->  audio/$id.$ext"
  filed=$((filed+1))
done

print ""
if (( filed == 0 )); then
  print "Nothing matched in ~/Downloads. Looking for names containing:"
  print "  glitch...growth / sign on the line / can't fall off the floor"
  print "  wisdom or trauma / signed and prayed / loneliness...killing people"
else
  print "$filed filed. Now in audio/:"
  for id in 108f79a7 6f60b69d 9e612e7c 52266d37 dc9aa87d 1875425a c30d26a7; do
    for g in "$AUD/$id".*(Nom); do print "  ${g:t}  $(du -h "$g" | cut -f1)"; done
  done
fi
