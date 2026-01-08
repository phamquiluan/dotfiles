alias l="ls -1 --color=always"
alias ll="ls -l --color=always"
alias cl="clear"
alias vi="vim"
alias py="python"
# alias python="python3.12"
alias i="ipython3 --TerminalInteractiveShell.editing_mode=vi"
alias tm="tmux"
alias ta="tmux a -t"
alias jup="jupyter-lab"
alias pep8="watch -n 0.5 pycodestyle"
alias net="curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -"
alias ww="watch -n 0.3"

# for git
alias gs="git status ."
alias gd="git diff"
alias gb="git branch -a"
alias gl="git log --all --graph --pretty=format:'%C(auto)%h%C(auto)%d %s %C(dim white)(%aN, %ar)'"
alias gcm="git commit -m"
alias gpush="git push "

# for conda
alias ca="conda activate"

# tmux session completion for ta alias
_ta_complete() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local session
    COMPREPLY=()
    while IFS= read -r session; do
        if [[ "$session" == "$cur"* ]]; then
            COMPREPLY+=("$session")
        fi
    done < <(tmux list-sessions -F '#{session_name}' 2>/dev/null)
}
complete -F _ta_complete ta
