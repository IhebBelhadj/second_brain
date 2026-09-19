" ============================================================
"  Obsidian vimrc  —  requires the "Vimrc Support" plugin
"  Leader is <Space>.  Reload after editing: restart Obsidian
"  or run the "Vimrc Support: Reload vimrc" command.
" ============================================================

" ---------- options ----------
set clipboard=unnamed       " yank/paste through the system clipboard
set ignorecase
set smartcase
set incsearch
set hlsearch
set tabstop=2

" ---------- basics ----------
" move by visual line (essential in a wrapped prose editor)
nmap j gj
nmap k gk
vmap j gj
vmap k gk

" fast escape
imap jj <Esc>
imap jk <Esc>

" clear search highlight
exmap nohl obcommand editor:focus
nmap <Space>/ :nohl

" keep the cursor centred when jumping
nmap G Gzz
nmap n nzz
nmap N Nzz

" ---------- file & save ----------
exmap save obcommand editor:save-file
nmap <Space>w :save

exmap closeTab obcommand workspace:close
nmap <Space>q :closeTab

" ---------- navigation ----------
exmap back obcommand app:go-back
exmap forward obcommand app:go-forward
nmap <C-o> :back
nmap <C-i> :forward
nmap <Space>[ :back
nmap <Space>] :forward

exmap followLink obcommand editor:follow-link
exmap followLinkNewTab obcommand editor:open-link-in-new-leaf
nmap gd :followLink
nmap gD :followLinkNewTab

exmap quickSwitcher obcommand switcher:open
nmap <Space>o :quickSwitcher

exmap search obcommand global-search:open
nmap <Space>f :search

exmap commandPalette obcommand command-palette:open
nmap <Space><Space> :commandPalette

exmap backlinks obcommand backlink:open
nmap <Space>b :backlinks

exmap graph obcommand graph:open
nmap <Space>g :graph

exmap outline obcommand outline:open
nmap <Space>u :outline

exmap randomNote obcommand random-note
nmap <Space>z :randomNote

" ---------- panes & splits ----------
exmap splitVertical obcommand workspace:split-vertical
exmap splitHorizontal obcommand workspace:split-horizontal
nmap <Space>v :splitVertical
nmap <Space>s :splitHorizontal

exmap focusLeft obcommand editor:focus-left
exmap focusRight obcommand editor:focus-right
exmap focusTop obcommand editor:focus-top
exmap focusBottom obcommand editor:focus-bottom
nmap <C-h> :focusLeft
nmap <C-l> :focusRight
nmap <C-k> :focusTop
nmap <C-j> :focusBottom

" ---------- editing ----------
exmap togglePreview obcommand markdown:toggle-preview
nmap <Space>p :togglePreview

exmap toggleCheckbox obcommand editor:toggle-checklist-status
nmap <Space>x :toggleCheckbox

exmap toggleBold obcommand editor:toggle-bold
exmap toggleItalic obcommand editor:toggle-italics
exmap toggleHighlight obcommand editor:toggle-highlight
vmap <Space>mb :toggleBold
vmap <Space>mi :toggleItalic
vmap <Space>mh :toggleHighlight

exmap insertLink obcommand editor:insert-link
vmap <Space>k :insertLink

exmap foldAll obcommand editor:fold-all
exmap unfoldAll obcommand editor:unfold-all
exmap toggleFold obcommand editor:toggle-fold
nmap zM :foldAll
nmap zR :unfoldAll
nmap za :toggleFold

" ---------- surround (vimrc-support built-in) ----------
exmap surroundWiki surround [[ ]]
exmap surroundDouble surround " "
exmap surroundSingle surround ' '
exmap surroundBacktick surround ` `
exmap surroundBold surround ** **
exmap surroundItalic surround * *
exmap surroundHighlight surround == ==
exmap surroundParen surround ( )
exmap surroundBracket surround [ ]
exmap surroundBrace surround { }

map <Space>cw :surroundWiki
map <Space>c" :surroundDouble
map <Space>c' :surroundSingle
map <Space>c` :surroundBacktick
map <Space>cb :surroundBold
map <Space>ci :surroundItalic
map <Space>ch :surroundHighlight
map <Space>c( :surroundParen
map <Space>c[ :surroundBracket
map <Space>c{ :surroundBrace

" ---------- vault actions ----------
exmap insertTemplate obcommand templater-obsidian:insert-templater
nmap <Space>t :insertTemplate

exmap reviewFlashcards obcommand obsidian-spaced-repetition:srs-review-flashcards
nmap <Space>r :reviewFlashcards

exmap todayNote obcommand daily-notes
nmap <Space>d :todayNote

exmap newDrawing obcommand obsidian-excalidraw-plugin:excalidraw-autocreate
nmap <Space>e :newDrawing

exmap gitCommitPush obcommand obsidian-git:push
nmap <Space>G :gitCommitPush
