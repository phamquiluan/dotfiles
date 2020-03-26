syntax on
set nocompatible 
set number
set wildmenu
filetype off
filetype plugin indent on
set tabstop=4
set shiftwidth=4
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
Plugin 'tpope/vim-fugitive'
Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
Plugin 'ascenator/L9', {'name': 'newL9'}
Plugin 'JamshedVesuna/vim-markdown-preview'
Plugin 'nvie/vim-flake8'
Plugin 'Chiel92/vim-autoformat'


call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
set shell=/bin/bash
" plugin YCM
Plugin 'Valloric/YouCompleteMe'
let g:ycm_global_ycm_extra_conf = '~/.ycm_extra_conf.py'
let g:ycm_show_diagnostics_ui = 0
let g:ycm_enable_diagnostic_signs = 0 
let g:ycm_enable_diagnostic_highlighting = 0
let g:ycm_complete_in_comments = 1
let g:ycm_semantic_triggers =  {
  \   'c' : ['->', '.'],
  \   'objc' : ['->', '.', 're!\[[_a-zA-Z]+\w*\s', 're!^\s*[^\W\d]\w*\s',
  \             're!\[.*\]\s'],
  \   'ocaml' : ['.', '#'],
  \   'cpp,cuda,objcpp' : ['->', '.', '::'],
  \   'perl' : ['->'],
  \   'php' : ['->', '::'],
  \   'cs,java,javascript,typescript,d,python,perl6,scala,vb,elixir,go' : ['.'],
  \   'ruby' : ['.', '::'],
  \   'lua' : ['.', ':'],
  \   'erlang' : [':'],
  \ }
set completeopt-=preview
let g:EclimFileTypeValidate = 0
let g:EclimCompletionMethod = 'omnifunc'
let g:ycm_python_binary_path = 'python3'
" for sidebar
let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_browse_split = 4
let g:netrw_altv = 1
let g:netrw_winsize = 20

let vim_markdown_preview_github=1
let vim_markdown_preview_toggle=1

augroup ProjectDrawer
  autocmd!
"  autocmd VimEnter * :Vexplore
augroup END


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
inoremap <C-c> <Esc>

Plugin 'scrooloose/nerdcommenter'
let g:NERDSpaceDelims = 1
set hlsearch
set incsearch
set linebreak

" for folded highlight
hi Folded ctermbg=Black
set foldmethod=indent
set foldlevel=10

"if has("autocmd")
"  au VimEnter,InsertLeave * silent execute '!echo -ne "\e[1 q"' | redraw!
"  au InsertEnter,InsertChange *
"    \ if v:insertmode == 'i' | 
"    \   silent execute '!echo -ne "\e[5 q"' | redraw! |
"    \ elseif v:insertmode == 'r' |
"    \   silent execute '!echo -ne "\e[3 q"' | redraw! |
"    \ else |
"    \   silent execute '!echo -ne "\e[1 q"' | redraw! |
"    \ endif
"  au VimLeave * silent execute '!echo -ne "\e[ q"' | redraw!
"endif
"
autocmd FileType python setlocal indentkeys-=<:>
autocmd FileType python setlocal indentkeys-=:"
