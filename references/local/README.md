# 独自の規則の置き場所

このフォルダは、フォーク ShortArrow/yomiyasu の `shortarrow` ブランチだけにあります。
上流 nanaism/yomiyasu にはありません。

`SKILL.md` の Step 1 の後にある段落が、このフォルダの `.md` をすべて読ませます。
この README.md もそのとき読まれるので、規則は書かず、置き方だけを書きます。

## 置き方

- 規則は 1 つの話題につき 1 つの `.md` にします。
  上流のファイルを書き換えずに済むので、上流を取り込んでもぶつかりません。
- 本体の規則と食い違う規則は、どの規則を上書きするかを本文に書きます。
  食い違ったときは、このフォルダの規則が優先されます。
- lint の語のリスト（`references/lists/*.txt`）は、ここに置いても読まれません。

## 上流を取り込む

1. `gh repo sync ShortArrow/yomiyasu -b main` で、フォークの `main` を上流に追いつかせます。
2. `git fetch origin` の後、`shortarrow` を `origin/main` の上に rebase します。
3. `SKILL.md` の段落がぶつかったら、Step 2 の見出しの直前に置き直します。
4. `git push --force-with-lease origin shortarrow` で上げます。
