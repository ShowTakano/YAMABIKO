# Hot to setup the environment on Macbook pro macOS
## Install VScode
Mac(vscode)

## Install home-brew
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Install git
```sh
brew install git
```

## install Python
Macのpythonはデフォルトが2.7である。
pyenvを使用してバージョンを切り替える。

### メモ
```sh
 * ここで本来であればすぐにpyenvの手順に移行すれば良かったが、ターミナルのpythonをaliasで一時的に切り替えてしまった。
 * おそらくは以下の手順に影響はない。もし次回実施時にはaliasなどの設定をしない方が良い。
 * もし以下の手順でうまくいなかい場合は、aliasを入れてもいい。
witch python3
alias python='/usr/bin/python3'
参考
https://it-syoya-engineer.com/mac-python-default-change/
https://ja.stackoverflow.com/questions/53587/pythonのデフォルトバージョンを3-7にしたい
```

git graphのエクステンションの画面から、git graphの bash が実行可能。こちらからコマンド実行していく。
```sh
brew install pyenv
echo $SHELL  # このやり方ではbashのはず
```

~/.bash_profileが初期状態では存在しなかった。以下のコマンドだけterminalで実施した。
```sh
cd ~/
touch .bash_profile
open -e .bash_profile  # テキストエディタで編集できる
```

## 下記を記入
```sh
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```
```sh
source ~/.bash_profile
```

とこのままいくと、pyenv install 3.x.xと進みたいが、下記２箇所でエラーになる
1. pyinstaller
pyinstaller成功しない。
--onefileで実行したいが、OSError: Python library not found: python3-devのようなエラーが出る。
そのためにはpyenv installの時点で
PYTHON_CONFIGURE_OPTS="--enable-shared"
オプションが必要。

2. _tkinter
さらにこのままでは最後まで行ってpyinstallerで作成して実行した後に
ModuleNotFoundError: No module named '_tkinter'
となり実行できない。

```sh
brew install tcl-tk
```
```sh
open -e .bash_profile  # テキストエディタで編集できる
```
## 以下の内容を追記
```sh
export PATH="/usr/local/opt/tcl-tk/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
export PKG_CONFIG_PATH="/usr/local/opt/tcl-tk/lib/pkgconfig"
```

## ついにインストール
```sh
PYTHON_CONFIGURE_OPTS="--with-tcltk-includes='-I/usr/local/opt/tcl-tk/include' --with-tcltk-libs='-L/usr/local/opt/tcl-tk/lib -ltcl8.6 -ltk8.6' --enable-shared" pyenv install 3.8.2
```
```sh
pyenv global 3.8.2
pyenv versions
  system
* 3.8.2 (set by /Users/myname/.pyenv/version)
```

tkが使えるか簡易チェック
```sh
python -m tkinter
```

環境は整った。コード依存を入れる
```sh
pip list  # 何もない
pip install pyserial
```
アプリ内のアイコン画像はコメントアウトすること。windowsで作成したエンコード文字列だからだろう。

```sh
pip install pyinstaller
```

## macOS実行ファイル.appを生成
```sh
pyinstaller HHKM_Programmer.py --onefile --noconsole --icon=icons/ico.ico
```
参考
https://qiita.com/saki-engineering/items/92b7ec12ed07338929a3
https://shinshin86.hateblo.jp/entry/2022/01/08/070847
https://zenn.dev/kenghaya/articles/9f07914156fab5
https://qiita.com/Yiwen/items/715e4319bb14d52e3b8e

## macOSバージョン注意
* macOS Catalina バージョン 10.15.7
  * pyinstallerが成功する。
  * しかしアイコンが表示されない。
* macOS Monterey バージョン 12.2.1
  * Catalinaでビルドした.appが起動成功する。
  * Catalinaではアイコンが表示されなかったが、Montereyではアイコンが表示される。
  * 【注意】pyinstallerが実行できない。どうやらOSが新しすぎて、pyinstallerが対応していないようだ。

## リリース
* 右クリックからzip圧縮
* githubのリリースページに添付
## ユーザーダウンロード
* githubのリリースページからダウンロード
* ダウンロードディレクトリをFinderで開く