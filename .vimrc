" general config
syntax on
set nocompatible 
set number
set wildmenu
set mouse-=a
filetype off
set tabstop=4
set shiftwidth=4
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
Plugin 'tibabit/vim-templates'
Plugin 'Valloric/YouCompleteMe', { 'commit':'d98f896' }
Plugin 'jremmen/vim-ripgrep'
Plugin 'scrooloose/nerdcommenter'
Plugin 'christoomey/vim-tmux-navigator'
Plugin 'Vimjas/vim-python-pep8-indent'
Plugin 'preservim/nerdtree'
" Plugin 'psf/black'
call vundle#end()

filetype plugin indent on
filetype plugin on

" plugin vim-fugitive
" nnoremap <leader>gs :Gstatus<CR>
" nnoremap <leader>gc :Gcommit<CR>
" nnoremap <leader>gp :Gpush<CR>
" nnoremap <leader>gd :Git diff HEAD<CR>
" nnoremap <leader>gb :Git branch -a<CR>
" nnoremap <leader>gw :Gwrite<CR>
" nnoremap <leader>gj :diffget //3<CR>
" nnoremap <leader>gh :diffget //2<CR>
" nnoremap <leader>gl :Git log --decorate --graph --oneline --all<CR>


nmap <leader>` :Black<CR>

" set fold
nnoremap <leader>1 :set foldlevel=0<CR>
nnoremap <leader>2 :set foldlevel=1<CR>
nnoremap <leader>3 :set foldlevel=2<CR>
nnoremap <leader>4 :set foldlevel=11<CR>

nnoremap <C-f> :Rg

" for splits
nnoremap <leader>\ :vsplit<CR>
nnoremap <leader>- :split<CR>

" for buffer
nnoremap <leader>h :bp<CR>
nnoremap <leader>l :bn<CR>
nnoremap <leader>bd :bp\|bd#<CR>

" for fzf
nnoremap <leader>f :FZF<CR>
let g:fzf_preview_window = ""
let g:fzf_preview_window = "right:60%"
let $FZF_DEFAULT_COMMAND = "rg --files --hidden"


" for NERDTree
let NERDTreeIgnore = ["__pycache__"]
nmap <C-n> :NERDTreeToggle<CR>
let g:NERDSpaceDelims = 1


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
  \   "python" : [".", "re!\w{2}"],
  \ }
set completeopt-=preview
" let g:EclimFileTypeValidate = 0
" let g:EclimCompletionMethod = "omnifunc"
let g:ycm_python_binary_path = "python3"
let g:ycm_disable_for_files_larger_than_kb = 2000
let g:ycm_key_list_stop_completion = ["<C-y>", "<CR>"]
let g:ycm_key_invoke_completion = "<C-j>"

nnoremap ? :YcmCompleter GetDoc<CR>
nnoremap gt :YcmCompleter GetType<CR>
nnoremap gd :YcmCompleter GoToDefinitionElseDeclaration<CR>

" for netrw sidebar
let g:netrw_banner = 0
let g:netrw_liststyle = 0
let g:netrw_altv = 1
let g:netrw_winsize = 80
let g:netrw_browse_split = 2

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

autocmd FileType python setlocal indentkeys-=<:>
autocmd FileType python setlocal indentkeys-=:"
autocmd BufNewFile,BufRead Jenkinsfile setfiletype groovy

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


pyx << EOF
import os.path
import sys
import vim
if "VIRTUAL_ENV" in os.environ:
    project_base_dir = os.environ["VIRTUAL_ENV"]
    sys.path.insert(0, project_base_dir)
    activate_this = os.path.join(project_base_dir, "bin/activate_this.py")
	# execfile(activate_this, dict(__file__=activate_this))
    exec(compile(open(activate_this, "rb").read(), activate_this, "exec"), dict(__file__=activate_this))
EOF
