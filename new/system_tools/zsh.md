zshrc config for macos

```bash
   export PATH="$HOME/.brew/bin:$PATH"
  1 export PATH="$HOME/.brew/bin:$PATH"
  2 export HOMEBREW_NO_AUTO_UPDATE=1
  3 export PATH="/usr/local/mysql/bin:$PATH"
  4 export PATH=/usr/local/mongodb/bin:$PATH
  5 eval "$(/usr/local/bin/brew shellenv)"
  6 alias clear='clear; printf "^[[3J"' # set cmd + k to clear command
```

