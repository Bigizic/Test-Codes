```bash
lex@lexs-MBP Downloads % gh auth login
? Where do you use GitHub? GitHub.com
? What is your preferred protocol for Git operations on this host? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser

! First copy your one-time code: 03D8-8D62
Press Enter to open https://github.com/login/device in your browser...
✓ Authentication complete.
- gh config set -h github.com git_protocol https
✓ Configured git protocol
✓ Logged in as Bigizic
lex@lexs-MBP Downloads % gh release download v1.69.168 --repo brave/brave-browser --pattern "Brave-Browser-universal.dmg"
```
