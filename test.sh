export NVM_DIR="$HOME/.nvm"
[ -s "/opt/homebrew/opt/nvm/nvm.sh" ] && \. "/opt/homebrew/opt/nvm/nvm.sh"  # This loads nvm

# function parse_git_branch() {
#     git branch 2> /dev/null | sed -n -e 's/^\* \(.*\)/[\1]/p'
# }

# COLOR_DEF=$'\e[0m'
# COLOR_USR=$'\e[38;5;243m'
# COLOR_DIR=$'\e[38;5;197m'
# COLOR_GIT=$'\e[38;5;39m'
# setopt PROMPT_SUBST
# export PROMPT='${COLOR_DIR}%~ ${COLOR_GIT}$(parse_git_branch)$'`

# Load version control information
autoload -Uz vcs_info
precmd() { vcs_info }

# Format the vcs_info_msg_0_ variable
zstyle ':vcs_info:git:*' formats '%F{cyan}[%b]%f'
 
# Set up the prompt (with git branch name)
setopt PROMPT_SUBST
PROMPT='%n in %F{red}${PWD/#$HOME/~}%f ${vcs_info_msg_0_}> '
