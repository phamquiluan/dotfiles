" general config
syntax on
set nocompatible
set number
set wildmenu
set mouse-=a
filetype off
set tabstop=4
set shiftwidth=4
set encoding=utf-8
set shell=/bin/bash
set clipboard=unnamedplus " using system clipboard
set hlsearch
set incsearch
set linebreak
set foldmethod=indent
set foldlevel=10
set ignorecase
set smartcase
set lazyredraw
set wildmode=longest,full
set pastetoggle=<F2>
set splitright
set splitbelow
set backupcopy=yes
set backspace=2
set ruler

nnoremap <SPACE> <Nop>
let mapleader=" " " mapleader

" set the runtime path to include Vundle and fzf
set rtp+=~/.vim/bundle/Vundle.vim
set rtp+=~/.fzf

" for plugin
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'tpope/vim-fugitive'
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
Plugin 'ascenator/L9', {'name': 'newL9'}
Plugin 'JamshedVesuna/vim-markdown-preview'
Plugin 'nvie/vim-flake8'
Plugin 'Chiel92/vim-autoformat'
Plugin 'ekalinin/dockerfile.vim'
Plugin 'junegunn/fzf.vim'
Plugin 'junegunn/fzf', { 'do': { -> fzf#install() } }
Plugin 'Valloric/YouCompleteMe', { 'commit':'d98f896' }
Plugin 'tpope/vim-surround'
Plugin 'scrooloose/nerdcommenter'
Plugin 'christoomey/vim-tmux-navigator'
Plugin 'Vimjas/vim-python-pep8-indent'
Plugin 'preservim/nerdtree'
Plugin 'jiangmiao/auto-pairs'
Plugin 'wellle/tmux-complete.vim'
Plugin 'mattn/emmet-vim'
call vundle#end()

filetype plugin indent on
filetype plugin on

nmap <leader>` :Black<CR>

" set fold
nnoremap <leader>1 :set foldlevel=0<CR>
nnoremap <leader>2 :set foldlevel=1<CR>
nnoremap <leader>3 :set foldlevel=2<CR>
nnoremap <leader>4 :set foldlevel=11<CR>

nnoremap <C-f> :Rg<CR>

" for splits
nnoremap <leader>\ :vsplit<CR>
nnoremap <leader>- :split<CR>

" for buffer
nnoremap <leader>h :bp<CR>
nnoremap <leader>l :bn<CR>
nnoremap <leader>bd :bp\|bd#<CR>

" for fzf
nnoremap <leader>f :FZF<CR>
let g:fzf_preview_window = ['right:50%']
let $FZF_DEFAULT_COMMAND = "rg --files --hidden"

" for NERDTree
let NERDTreeIgnore = ["__pycache__"]
nmap <C-n> :NERDTreeToggle<CR>
let g:NERDSpaceDelims = 1
nmap <leader>r :NERDTreeFind<cr>

" for copilot
nnoremap <leader>s :Copilot panel<CR>
imap <silent><script><expr> <C-k> copilot#Next()<CR>

let g:copilot_filetypes = {
  \ '*': v:false,
  \ 'Dockerfile': v:true,
  \ 'python': v:true,
  \ 'json': v:true,
  \ 'yaml': v:true,
  \ 'yml': v:true,
  \ 'text': v:true,
  \ 'txt': v:true,
  \ 'sh': v:true,
  \ 'md': v:true,
  \ 'gitignore': v:true,
  \ }



" for YCM, Youcompleteme
let g:ycm_global_ycm_extra_conf = "~/.ycm_extra_conf.py"
let g:ycm_show_diagnostics_ui = 0
let g:ycm_enable_diagnostic_signs = 0
let g:ycm_enable_diagnostic_highlighting = 0
let g:ycm_auto_hover=""  " this guys is being default at April :))
let g:ycm_complete_in_comments = 1
let g:ycm_semantic_triggers =  {
  \   "c" : ["->", "."],
  \   "cpp,cuda,objcpp" : ["->", ".", "::"],
  \   "cs,java,javascript,typescript,d,python,perl6,scala,vb,elixir,go" : [".", "re!\w{2}"],
  \ }
set completeopt-=preview
let g:ycm_python_binary_path = "python3"
let g:ycm_disable_for_files_larger_than_kb = 2000
let g:ycm_key_list_stop_completion = ["<C-y>", "<CR>"]
let g:ycm_key_invoke_completion = "<C-j>"

nnoremap ? :YcmCompleter GetDoc<CR>
nnoremap gt :YcmCompleter GetType<CR>
nnoremap gd :YcmCompleter GoToDefinitionElseDeclaration<CR>
nnoremap rn :YcmCompleter RefactorRename 

" for markdown
let vim_markdown_preview_github=1
let vim_markdown_preview_toggle=1

" for seamlessly navigate vim splits and tmux panes
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

nnoremap <silent> <C-h> :TmuxNavigateLeft<cr>
nnoremap <silent> <C-j> :TmuxNavigateDown<cr>
nnoremap <silent> <C-k> :TmuxNavigateUp<cr>
nnoremap <silent> <C-l> :TmuxNavigateRight<cr>

" keep it always centered
noremap j jzz
noremap k kzz
noremap # #zz
noremap * *zz
noremap `` ``zz
noremap n nzz

xnoremap y y`]
xnoremap <C-y> "+y`]
xnoremap <C-p> "+P`]
nnoremap <C-p> "+P
nnoremap <C-c> gg"+yG``
inoremap <C-c> <esc>

if $TERM =~ "xterm"
  set noek
endif

nnoremap <esc> :noh<Cr><esc>
nnoremap <esc>^[ <esc>^[

" for highlight
hi Folded ctermbg=Black
hi DiffText   cterm=none ctermfg=Black ctermbg=Red gui=none guifg=Black guibg=Red
hi DiffChange cterm=none ctermfg=Black ctermbg=LightMagenta gui=none guifg=Black guibg=LightMagenta

if &diff
	colorscheme desert
endif

autocmd FileType python setlocal indentkeys-=<:>
autocmd FileType python setlocal indentkeys-=:"
autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab indentkeys-=0#
" autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab indentkeys-=0# indentkeys-=<:>
autocmd BufNewFile,BufRead Jenkinsfile setfiletype groovy
autocmd VimResized * wincmd =

" ref: https://stackoverflow.com/questions/62148994/strange-character-since-last-update-42m-in-vim
let &t_TI = ""
let &t_TE = ""

" for Zoom / Restore window.
function! s:ZoomToggle() abort
    if exists('t:zoomed') && t:zoomed
        execute t:zoom_winrestcmd
        let t:zoomed = 0
    else
        let t:zoom_winrestcmd = winrestcmd()
        resize
        vertical resize
        let t:zoomed = 1
    endif
endfunction
command! ZoomToggle call s:ZoomToggle()
nnoremap <silent> <Leader><Leader> :ZoomToggle<CR>

command! W w
command! FormatCpp %!astyle


pyx << EOF
import os.path
import sys
import vim
if "VIRTUAL_ENV" in os.environ:
	project_base_dir = os.environ["VIRTUAL_ENV"]
	sys.path.insert(0, project_base_dir)
	activate_this = os.path.join(project_base_dir, "bin/activate_this.py")
	if os.path.exists(activate_this):
		exec(compile(open(activate_this, "rb").read(), activate_this, "exec"), dict(__file__=activate_this))
EOF
