# ai.ie reel — your three steps (then say "go")

1. Create the GitHub account. https://github.com/signup — username: followkellie (free; ai-ie is taken). Use any email you like.
2. Make the key and copy it. Click Run on this line (it makes a key file and copies the public half to your clipboard):
   ssh-keygen -t ed25519 -C "followkellie github" -f ~/.ssh/id_ed25519_aiie -N "" -q && pbcopy < ~/.ssh/id_ed25519_aiie.pub && echo copied
   Then paste it at https://github.com/settings/ssh/new (title: Mac) and click Add.
3. Create the empty repo. https://github.com/new — name it exactly: followkellie.github.io — Public — Create (nothing else).

Then tell me "go". I push the reel; the page appears at https://followkellie.github.io within a minute or two.

DONE 2026-11-03. Live: https://followkellie.github.io
